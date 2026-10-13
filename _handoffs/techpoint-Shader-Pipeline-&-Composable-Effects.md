---
layout: default
title: 技术点 · Shader Pipeline & Composable Effects
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Shader Pipeline & Composable Effects

> 来源：261010_Shader Pipeline & Composable Effects_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
BLEND_MODES = {
    "normal":       lambda a, b: b,
    "add":          lambda a, b: np.clip(a + b, 0, 1),
    "subtract":     lambda a, b: np.clip(a - b, 0, 1),
    "multiply":     lambda a, b: a * b,
    "screen":       lambda a, b: 1 - (1-a)*(1-b),
    "overlay":      # 2*a*b if a<0.5, else 1-2*(1-a)*(1-b)
    "softlight":    lambda a, b: (1-2*b)*a*a + 2*b*a,
    "hardlight":    # like overlay but keyed on b
    "difference":   lambda a, b: abs(a - b),
    "exclusion":    lambda a, b: a + b - 2*a*b,
    "colordodge":   lambda a, b: a / (1-b),
    "colorburn":    lambda a, b: 1 - (1-a)/b,
    "linearlight":  lambda a, b: a + 2*b - 1,
    "vividlight":   # burn if b<0.5, dodge if b>=0.5
    "pin_light":    # min(a,2b) if b<0.5, max(a,2b-1) if b>=0.5
    "hard_mix":     lambda a, b: 1 if a+b>=1 else 0,
    "lighten":      lambda a, b: max(a, b),
    "darken":       lambda a, b: min(a, b),
    "grain_extract": lambda a, b: a - b + 0.5,
    "grain_merge":  lambda a, b: a + b - 0.5,
}
```
- ```
def blend_canvas(base, top, mode="normal", opacity=1.0):
    """Blend two uint8 canvases (H,W,3) using a named blend mode + opacity."""
    af = base.astype(np.float32) / 255.0
    bf = top.astype(np.float32) / 255.0
    result = BLEND_MODES[mode](af, bf)
    if opacity < 1.0:
        result = af * (1-opacity) + result * opacity
    return np.clip(result * 255, 0, 255).astype(np.uint8)

# Multi-layer compositing
result = blend_canvas(base, layer_a, "screen", 0.7)
result = blend_canvas(result, layer_b, "difference", 0.5)
result = blend_canvas(result, layer_c, "multiply", 0.3)
```
- ```
class FeedbackBuffer:
    def __init__(self):
        self.buf = None  # previous frame (float32, 0-1)
    
    def apply(self, canvas, decay=0.85, blend="screen", opacity=0.5,
              transform=None, transform_amt=0.02, hue_shift=0.0):
        """Mix current frame with decayed/transformed previous frame.
        
        Args:
            canvas: current frame (uint8 H,W,3)
            decay: how fast old frame fades (0=instant, 1=permanent)
            blend: blend mode for mixing feedback
            opacity: strength of feedback mix
            transform: None, "zoom", "shrink", "rotate_cw", "rotate_ccw",
                       "shift_up", "shift_down", "mirror_h"
            transform_amt: strength of spatial transform per frame
            hue_shift: rotate hue of feedback buffer each frame (0-1)
        """
```
- ```
# Infinite zoom tunnel
fb_cfg = {"decay": 0.8, "blend": "screen", "opacity": 0.4,
          "transform": "zoom", "transform_amt": 0.015}

# Rainbow trails (psychedelic)
fb_cfg = {"decay": 0.7, "blend": "screen", "opacity": 0.3,
          "transform": "zoom", "transform_amt": 0.01, "hue_shift": 0.02}

# Ghostly echo (horror)
fb_cfg = {"decay": 0.9, "blend": "add", "opacity": 0.15,
          "transform": "shift_up", "transform_amt": 0.01}

# Kaleidoscopic recursion
fb_cfg = {"decay": 0.75, "blend": "screen", "opacity": 0.35,
          "transform": "rotate_cw", "transform_amt": 0.005, "hue_shift": 0.01}

# Color evolution (abstract)
fb_cfg = {"decay": 0.8, "blend": "difference", "opacity": 0.4, "hue_shift": 0.03}

# Multiplied depth
fb_cfg = {"decay": 0.65, "blend": "multiply", "opacity": 0.3, "transform": "mirror_h"}

# Rising heat haze
fb_cfg = {"decay": 0.5, "blend": "add", "opacity": 0.2,
          "transform": "shift_up", "transform_amt": 0.02}
```
- ```
class ShaderChain:
    """Composable shader pipeline.
    
    Usage:
        chain = ShaderChain()
        chain.add("bloom", thr=120)
        chain.add("chromatic", amt=5)
        chain.add("kaleidoscope", folds=6)
        chain.add("vignette", s=0.2)
        chain.add("grain", amt=12)
        canvas = chain.apply(canvas, f=features, t=time)
    """
    def __init__(self):
        self.steps = []

    def add(self, shader_name, **kwargs):
        self.steps.append((shader_name, kwargs))
        return self  # chainable

    def apply(self, canvas, f=None, t=0):
        if f is None: f = {}
        for name, kwargs in self.steps:
            canvas = _apply_shader_step(canvas, name, kwargs, f, t)
        return canvas
```
- ```
def _apply_shader_step(canvas, name, kwargs, f, t):
    """Dispatch a single shader by name with kwargs.
    
    Args:
        canvas: uint8 (H,W,3) pixel array
        name: shader key string (e.g. "bloom", "chromatic")
        kwargs: dict of shader parameters
        f: audio features dict (keys: bdecay, rms, sub, etc.)
        t: current time in seconds (float)
    Returns:
        canvas: uint8 (H,W,3) — processed
    """
    bd = f.get("bdecay", 0)    # beat decay (0-1, high on beat)
    rms = f.get("rms", 0.3)   # audio energy (0-1)

    # --- Geometry ---
    if name == "crt":
        return sh_crt(canvas, kwargs.get("strength", 0.05))
    elif name == "pixelate":
        return sh_pixelate(canvas, kwargs.get("block", 4))
    elif name == "wave_distort":
        return sh_wave_distort(canvas, t,
            kwargs.get("freq", 0.02), kwargs.get("amp", 8), kwargs.get("axis", "x"))
    elif name == "kaleidoscope":
        return sh_kaleidoscope(canvas.copy(), kwargs.get("folds", 6))
    elif name == "mirror_h":
        return sh_mirror_h(canvas.copy())
    elif name == "mirror_v":
        return sh_mirror_v(canvas.copy())
    elif name == "mirror_quad":
        return sh_mirror_quad(canvas.copy())
    elif name == "mirror_diag":
        return sh_mirror_diag(canvas.copy())

    # --- Channel ---
    elif name == "chromatic":
        base = kwargs.get("amt", 3)
        return sh_chromatic(canvas, max(1, int(base * (0.4 + bd * 0.8))))
    elif name == "channel_shift":
        return sh_channel_shift(canvas,
            kwargs.get("r", (0,0)), kwargs.get("g", (0,0)), kwargs.get("b", (0,0)))
    elif name == "channel_swap":
        return sh_channel_swap(canvas, kwargs.get("order", (2,1,0)))
    elif name == "rgb_split_radial":
        return sh_rgb_split_radial(canvas, kwargs.get("strength", 5))

    # --- Color ---
    elif name == "invert":
        return sh_invert(canvas)
    elif name == "posterize":
        return sh_posterize(canvas, kwargs.get("levels", 4))
    elif name == "threshold":
        return sh_threshold(canvas, kwargs.get("thr", 128))
    elif name == "solarize":
        return sh_solarize(canvas, kwargs.get("threshold", 128))
    elif name == "hue_rotate":
        return sh_hue_rotate(canvas, kwargs.get("amount", 0.1))
    elif name == "saturation":
        return sh_saturation(canvas, kwargs.get("factor", 1.5))
    elif name == "color_grade":
        return sh_color_grade(canvas, kwargs.get("tint", (1,1,1)))
    elif name == "color_wobble":
        return sh_color_wobble(canvas, t, kwargs.get("amt", 0.3) * (0.5 + rms * 0.8))
    elif name == "color_ramp":
        return sh_color_ramp(canvas, kwargs.get("ramp", [(0,0,0),(255,255,255)]))

    # --- Glow / Blur ---
    elif name == "bloom":
        return sh_bloom(canvas, kwargs.get("thr", 130))
    elif name == "edge_glow":
        return sh_edge_glow(canvas, kwargs.get("hue", 0.5))
    elif name == "soft_focus":
        return sh_soft_focus(canvas, kwargs.get("strength", 0.3))
    elif name == "radial_blur":
        return sh_radial_blur(canvas, kwargs.get("strength", 0.03))

    # --- Noise ---
    elif name == "grain":
        return sh_grain(canvas, int(kwargs.get("amt", 10) * (0.5 + rms * 0.8)))
    elif name == "static":
        return sh_static_noise(canvas, kwargs.get("density", 0.05), kwargs.get("color", True))

    # --- Lines / Patterns ---
    elif name == "scanlines":
        return sh_scanlines(canvas, kwargs.get("intensity", 0.08), kwargs.get("spacing", 3))
    elif name == "halftone":
        return sh_halftone(canvas, kwargs.get("dot_size", 6))

    # --- Tone ---
    elif name == "vignette":
        return sh_vignette(canvas, kwargs.get("s", 0.22))
    elif name == "contrast":
        return sh_contrast(canvas, kwargs.get("factor", 1.3))
    elif name == "gamma":
        return sh_gamma(canvas, kwargs.get("gamma", 1.5))
    elif name == "levels":
        return sh_levels(canvas,
            kwargs.get("black", 0), kwargs.get("white", 255), kwargs.get("midtone", 1.0))
    elif name == "brightness":
        return sh_brightness(canvas, kwargs.get("factor", 1.5))

    # --- Glitch / Data ---
    elif name == "glitch_bands":
        return sh_glitch_bands(canvas, f)
    elif name == "block_glitch":
        return sh_block_glitch(canvas, kwargs.get("n_blocks", 8), kwargs.get("max_size", 40))
    elif name == "pixel_sort":
        return sh_pixel_sort(canvas, kwargs.get("threshold", 100), kwargs.get("direction", "h"))
    elif name == "data_bend":
        return sh_data_bend(canvas, kwargs.get("offset", 1000), kwargs.get("chunk", 500))

    else:
        return canvas  # unknown shader — passthrough
```
- | Shader | Key Params | Description |
- ```
def rgb2hsv(r, g, b):
    """Vectorized RGB (0-255 uint8) -> HSV (float32 0-1)."""
    rf = r.astype(np.float32) / 255.0
    gf = g.astype(np.float32) / 255.0
    bf = b.astype(np.float32) / 255.0
    cmax = np.maximum(np.maximum(rf, gf), bf)
    cmin = np.minimum(np.minimum(rf, gf), bf)
    delta = cmax - cmin + 1e-10
    h = np.zeros_like(rf)
    m = cmax == rf; h[m] = ((gf[m] - bf[m]) / delta[m]) % 6
    m = cmax == gf; h[m] = (bf[m] - rf[m]) / delta[m] + 2
    m = cmax == bf; h[m] = (rf[m] - gf[m]) / delta[m] + 4
    h = h / 6.0 % 1.0
    s = np.where(cmax > 0, delta / (cmax + 1e-10), 0)
    return h, s, cmax

def hsv2rgb(h, s, v):
    """Vectorized HSV->RGB. h,s,v are numpy float32 arrays."""
    h = h % 1.0
    c = v * s; x = c * (1 - np.abs((h * 6) % 2 - 1)); m = v - c
    r = np.zeros_like(h); g = np.zeros_like(h); b = np.zeros_like(h)
    mask = h < 1/6;            r[mask]=c[mask]; g[mask]=x[mask]
    mask = (h>=1/6)&(h<2/6);   r[mask]=x[mask]; g[mask]=c[mask]
    mask = (h>=2/6)&(h<3/6);   g[mask]=c[mask]; b[mask]=x[mask]
    mask = (h>=3/6)&(h<4/6);   g[mask]=x[mask]; b[mask]=c[mask]
    mask = (h>=4/6)&(h<5/6);   r[mask]=x[mask]; b[mask]=c[mask]
    mask = h >= 5/6;            r[mask]=c[mask]; b[mask]=x[mask]
    R = np.clip((r+m)*255, 0, 255).astype(np.uint8)
    G = np.clip((g+m)*255, 0, 255).astype(np.uint8)
    B = np.clip((b+m)*255, 0, 255).astype(np.uint8)
    return R, G, B

def mkc(R, G, B, rows, cols):
    """Stack R,G,B uint8 arrays into (rows,cols,3) canvas."""
    o = np.zeros((rows, cols, 3), dtype=np.uint8)
    o[:,:,0] = R; o[:,:,1] = G; o[:,:,2] = B
    return o
```
- ```
_crt_cache = {}
def sh_crt(c, strength=0.05):
    k = (c.shape[0], c.shape[1], round(strength, 3))
    if k not in _crt_cache:
        h, w = c.shape[:2]; cy, cx = h/2, w/2
        Y = np.arange(h, dtype=np.float32)[:, None]
        X = np.arange(w, dtype=np.float32)[None, :]
        ny = (Y - cy) / cy; nx = (X - cx) / cx
        r2 = nx**2 + ny**2
        factor = 1 + strength * r2
        sx = np.clip((nx * factor * cx + cx), 0, w-1).astype(np.int32)
        sy = np.clip((ny * factor * cy + cy), 0, h-1).astype(np.int32)
        _crt_cache[k] = (sy, sx)
    sy, sx = _crt_cache[k]
    return c[sy, sx]
```
- ```
def sh_pixelate(c, block=4):
    """Reduce effective resolution."""
    sm = c[::block, ::block]
    return np.repeat(np.repeat(sm, block, axis=0), block, axis=1)[:c.shape[0], :c.shape[1]]
```
- ```
def sh_wave_distort(c, t, freq=0.02, amp=8, axis="x"):
    """Sinusoidal row/column displacement. Uses time t for animation."""
    h, w = c.shape[:2]
    out = c.copy()
    if axis == "x":
        for y in range(h):
            shift = int(amp * math.sin(y * freq + t * 3))
            out[y] = np.roll(c[y], shift, axis=0)
    else:
        for x in range(w):
            shift = int(amp * math.sin(x * freq + t * 3))
            out[:, x] = np.roll(c[:, x], shift, axis=0)
    return out
```
- ```
def sh_displacement_map(c, dx_map, dy_map, strength=10):
    """Displace pixels using float32 displacement maps (same HxW as c).
    dx_map/dy_map: positive = shift right/down."""
    h, w = c.shape[:2]
    Y = np.arange(h)[:, None]; X = np.arange(w)[None, :]
    ny = np.clip((Y + (dy_map * strength).astype(int)), 0, h-1)
    nx = np.clip((X + (dx_map * strength).astype(int)), 0, w-1)
    return c[ny, nx]
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
