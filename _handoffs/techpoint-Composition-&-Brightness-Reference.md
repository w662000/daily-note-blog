---
layout: default
title: 技术点 · Composition & Brightness Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Composition & Brightness Reference

> 来源：261010_Composition & Brightness Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
def blend_canvas(base, top, mode="normal", opacity=1.0):
    af = base.astype(np.float32) / 255.0
    bf = top.astype(np.float32) / 255.0
    fn = BLEND_MODES.get(mode, BLEND_MODES["normal"])
    result = fn(af, bf)
    if opacity < 1.0:
        result = af * (1 - opacity) + result * opacity
    return np.clip(result * 255, 0, 255).astype(np.uint8)
```
- ```
BLEND_MODES = {
    # Basic arithmetic
    "normal":       lambda a, b: b,
    "add":          lambda a, b: np.clip(a + b, 0, 1),
    "subtract":     lambda a, b: np.clip(a - b, 0, 1),
    "multiply":     lambda a, b: a * b,
    "screen":       lambda a, b: 1 - (1 - a) * (1 - b),

    # Contrast
    "overlay":      lambda a, b: np.where(a < 0.5, 2*a*b, 1 - 2*(1-a)*(1-b)),
    "softlight":    lambda a, b: (1 - 2*b)*a*a + 2*b*a,
    "hardlight":    lambda a, b: np.where(b < 0.5, 2*a*b, 1 - 2*(1-a)*(1-b)),

    # Difference
    "difference":   lambda a, b: np.abs(a - b),
    "exclusion":    lambda a, b: a + b - 2*a*b,

    # Dodge / burn
    "colordodge":   lambda a, b: np.clip(a / (1 - b + 1e-6), 0, 1),
    "colorburn":    lambda a, b: np.clip(1 - (1 - a) / (b + 1e-6), 0, 1),

    # Light
    "linearlight":  lambda a, b: np.clip(a + 2*b - 1, 0, 1),
    "vividlight":   lambda a, b: np.where(b < 0.5,
                        np.clip(1 - (1-a)/(2*b + 1e-6), 0, 1),
                        np.clip(a / (2*(1-b) + 1e-6), 0, 1)),
    "pin_light":    lambda a, b: np.where(b < 0.5,
                        np.minimum(a, 2*b), np.maximum(a, 2*b - 1)),
    "hard_mix":     lambda a, b: np.where(a + b >= 1.0, 1.0, 0.0),

    # Compare
    "lighten":      lambda a, b: np.maximum(a, b),
    "darken":       lambda a, b: np.minimum(a, b),

    # Grain
    "grain_extract": lambda a, b: np.clip(a - b + 0.5, 0, 1),
    "grain_merge":  lambda a, b: np.clip(a + b - 0.5, 0, 1),
}
```
- `hardlight` — strong contrast. Like overlay but keyed on the top layer.
- ```
# Pattern: render layers -> blend sequentially
canvas_a = _render_vf(r, "md", vf_plasma, hf_angle(0.0), PAL_DENSE, f, t, S)
canvas_b = _render_vf(r, "sm", vf_vortex, hf_time_cycle(0.1), PAL_RUNE, f, t, S)
canvas_c = _render_vf(r, "lg", vf_rings, hf_distance(), PAL_BLOCKS, f, t, S)

result = blend_canvas(canvas_a, canvas_b, "screen", 0.8)
result = blend_canvas(result, canvas_c, "difference", 0.6)
```
- ```
def blend_canvas_linear(base, top, mode="normal", opacity=1.0):
    """Blend in linear light space for physically accurate results.
    
    Identical API to blend_canvas(), but converts sRGB → linear before
    blending and linear → sRGB after. More expensive (~2x) due to the
    gamma conversions, but produces correct results for additive blending,
    screen, and any mode where brightness matters.
    """
    af = srgb_to_linear(base.astype(np.float32) / 255.0)
    bf = srgb_to_linear(top.astype(np.float32) / 255.0)
    fn = BLEND_MODES.get(mode, BLEND_MODES["normal"])
    result = fn(af, bf)
    if opacity < 1.0:
        result = af * (1 - opacity) + result * opacity
    result = linear_to_srgb(np.clip(result, 0, 1))
    return np.clip(result * 255, 0, 255).astype(np.uint8)
```
- ```
def blend_many_linear(layers, modes, opacities):
    """Blend a stack of layers in linear light space.
    
    Args:
        layers: list of uint8 (H,W,3) canvases
        modes: list of blend mode strings (len = len(layers) - 1)
        opacities: list of floats (len = len(layers) - 1)
    Returns:
        uint8 (H,W,3) canvas
    """
    # Convert all to linear at once
    linear = [srgb_to_linear(l.astype(np.float32) / 255.0) for l in layers]
    result = linear[0]
    for i in range(1, len(linear)):
        fn = BLEND_MODES.get(modes[i-1], BLEND_MODES["normal"])
        blended = fn(result, linear[i])
        op = opacities[i-1]
        if op < 1.0:
            blended = result * (1 - op) + blended * op
        result = np.clip(blended, 0, 1)
    result = linear_to_srgb(result)
    return np.clip(result * 255, 0, 255).astype(np.uint8)
```
- ```
def _render_vf(r, grid_key, val_fn, hue_fn, pal, f, t, S, sat=0.8, threshold=0.03):
    """Render a value field + hue field to a pixel canvas via a named grid.

    Args:
        r: Renderer instance (has .get_grid())
        grid_key: "xs", "sm", "md", "lg", "xl", "xxl"
        val_fn: (g, f, t, S) -> float32 [0,1] array (rows, cols)
        hue_fn: callable (g, f, t, S) -> float32 hue array, OR float scalar
        pal: character palette string
        f: feature dict
        t: time in seconds
        S: persistent state dict
        sat: HSV saturation (0-1)
        threshold: minimum value to render (below = space)

    Returns:
        uint8 array (VH, VW, 3) — full pixel canvas
    """
    g = r.get_grid(grid_key)
    val = np.clip(val_fn(g, f, t, S), 0, 1)
    mask = val > threshold
    ch = val2char(val, mask, pal)

    # Hue: either a callable or a fixed float
    if callable(hue_fn):
        h = hue_fn(g, f, t, S) % 1.0
    else:
        h = np.full((g.rows, g.cols), float(hue_fn), dtype=np.float32)

    # CRITICAL: broadcast to full shape and copy (see Troubleshooting)
    h = np.broadcast_to(h, (g.rows, g.cols)).copy()

    R, G, B = hsv2rgb(h, np.full_like(val, sat), val)
    co = mkc(R, G, B, g.rows, g.cols)
    return g.render(ch, co)
```
- ```
def fx_psychedelic(r, f, t, S):
    """Three-layer multi-grid scene with beat-reactive kaleidoscope."""
    # Layer A: plasma on medium grid with rainbow hue
    canvas_a = _render_vf(r, "md",
        lambda g, f, t, S: vf_plasma(g, f, t, S) * 1.3,
        hf_angle(0.0), PAL_DENSE, f, t, S, sat=0.8)

    # Layer B: vortex on small grid with cycling hue
    canvas_b = _render_vf(r, "sm",
        lambda g, f, t, S: vf_vortex(g, f, t, S, twist=5.0) * 1.2,
        hf_time_cycle(0.1), PAL_RUNE, f, t, S, sat=0.7)

    # Layer C: rings on large grid with distance hue
    canvas_c = _render_vf(r, "lg",
        lambda g, f, t, S: vf_rings(g, f, t, S, n_base=8, spacing_base=3) * 1.4,
        hf_distance(0.3, 0.02), PAL_BLOCKS, f, t, S, sat=0.9)

    # Blend: A screened with B, then difference with C
    result = blend_canvas(canvas_a, canvas_b, "screen", 0.8)
    result = blend_canvas(result, canvas_c, "difference", 0.6)

    # Beat-triggered kaleidoscope
    if f.get("bdecay", 0) > 0.3:
        result = sh_kaleidoscope(result.copy(), folds=6)

    return result
```
- ```
def tonemap(canvas, target_mean=90, gamma=0.75, black_point=2, white_point=253):
    """Adaptive tone-mapping: normalizes + gamma-corrects so no frame is
    fully dark or washed out.

    1. Compute 1st and 99.5th percentile on 4x subsample (16x fewer values,
       negligible accuracy loss, major speedup at 1080p+)
    2. Stretch that range to [0, 1]
    3. Apply gamma curve (< 1 lifts shadows, > 1 darkens)
    4. Rescale to [black_point, white_point]
    """
    f = canvas.astype(np.float32)
    sub = f[::4, ::4]  # 4x subsample: ~390K values vs ~6.2M at 1080p
    lo = np.percentile(sub, 1)
    hi = np.percentile(sub, 99.5)
    if hi - lo < 10:
        hi = max(hi, lo + 10)  # near-uniform frame fallback
    f = np.clip((f - lo) / (hi - lo), 0.0, 1.0)
    np.power(f, gamma, out=f)          # in-place: avoids allocation
    np.multiply(f, (white_point - black_point), out=f)
    np.add(f, black_point, out=f)
    return np.clip(f, 0, 255).astype(np.uint8)
```
- ```
input 10  -> output 20   (still dark)
input 100 -> output 200  (ok)
input 200 -> output 255  (clipped, lost detail)
```
- ```
input 0.04 -> output 0.08 (lifted from invisible to visible)
input 0.39 -> output 0.50 (moderate lift)
input 0.78 -> output 0.84 (gentle lift, no clipping)
```
- ```
scene_fn(r, f, t, S)  ->  canvas
         |
    tonemap(canvas, gamma=scene_gamma)
         |
    FeedbackBuffer.apply(canvas, ...)
         |
    ShaderChain.apply(canvas, f=f, t=t)
         |
    ffmpeg pipe
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
