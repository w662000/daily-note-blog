---
layout: default
title: 技术点 · Effect Catalog
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Effect Catalog

> 来源：261010_Effect Catalog_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Key principles:
- ```
def bg_sinefield(g, f, t, hue=0.6, bri=0.5, pal=PAL_DEFAULT,
                 freq=(0.13, 0.17, 0.07, 0.09), speed=(0.5, -0.4, -0.3, 0.2)):
    """Layered sine field. Adjust freq/speed tuples for different textures."""
    v1 = np.sin(g.cc*freq[0] + t*speed[0]) * np.sin(g.rr*freq[1] - t*speed[1]) * 0.5 + 0.5
    v2 = np.sin(g.cc*freq[2] - t*speed[2] + g.rr*freq[3]) * 0.4 + 0.5
    v3 = np.sin(g.dist_n*5 + t*0.2) * 0.3 + 0.4
    v4 = np.cos(g.angle*3 - t*0.6) * 0.15 + 0.5
    val = np.clip((v1*0.3 + v2*0.25 + v3*0.25 + v4*0.2) * bri * (0.6 + f["rms"]*0.6), 0.06, 1)
    mask = val > 0.03
    ch = val2char(val, mask, pal)
    h = np.full_like(val, hue) + f.get("cent", 0.5)*0.1 + val*0.08
    R, G, B = hsv2rgb(h, np.clip(0.35+f.get("flat",0.4)*0.4, 0, 1) * np.ones_like(val), val)
    return ch, mkc(R, G, B, g.rows, g.cols)
```
- ```
def bg_video(g, frame_rgb, pal=PAL_DEFAULT, brightness=0.5):
    small = np.array(Image.fromarray(frame_rgb).resize((g.cols, g.rows)))
    lum = np.mean(small, axis=2) / 255.0 * brightness
    mask = lum > 0.02
    ch = val2char(lum, mask, pal)
    co = np.clip(small * np.clip(lum[:,:,None]*1.5+0.3, 0.3, 1), 0, 255).astype(np.uint8)
    return ch, co
```
- ```
def bg_noise(g, f, t, pal=PAL_BLOCKS, density=0.3, hue_drift=0.02):
    val = np.random.random((g.rows, g.cols)).astype(np.float32) * density * (0.5 + f["rms"]*0.5)
    val = np.clip(val, 0, 1); mask = val > 0.02
    ch = val2char(val, mask, pal)
    R, G, B = hsv2rgb(np.full_like(val, t*hue_drift % 1), np.full_like(val, 0.3), val)
    return ch, mkc(R, G, B, g.rows, g.cols)
```
- ```
def bg_smooth_noise(g, f, t, hue=0.5, bri=0.5, pal=PAL_DOTS, octaves=3):
    """Layered sine approximation of Perlin noise. Cheap, smooth, organic."""
    val = np.zeros((g.rows, g.cols), dtype=np.float32)
    for i in range(octaves):
        freq = 0.05 * (2 ** i)
        amp = 0.5 / (i + 1)
        phase = t * (0.3 + i * 0.2)
        val += np.sin(g.cc * freq + phase) * np.cos(g.rr * freq * 0.7 - phase * 0.5) * amp
    val = np.clip(val * 0.5 + 0.5, 0, 1) * bri
    mask = val > 0.03
    ch = val2char(val, mask, pal)
    h = np.full_like(val, hue) + val * 0.1
    R, G, B = hsv2rgb(h, np.full_like(val, 0.5), val)
    return ch, mkc(R, G, B, g.rows, g.cols)
```
- ```
def bg_cellular(g, f, t, n_centers=12, hue=0.5, bri=0.6, pal=PAL_BLOCKS):
    """Voronoi-like cells using distance to nearest of N moving centers."""
    rng = np.random.RandomState(42)  # deterministic centers
    cx = (rng.rand(n_centers) * g.cols).astype(np.float32)
    cy = (rng.rand(n_centers) * g.rows).astype(np.float32)
    # Animate centers
    cx_t = cx + np.sin(t * 0.5 + np.arange(n_centers) * 0.7) * 5
    cy_t = cy + np.cos(t * 0.4 + np.arange(n_centers) * 0.9) * 3
    # Min distance to any center
    min_d = np.full((g.rows, g.cols), 999.0, dtype=np.float32)
    for i in range(n_centers):
        d = np.sqrt((g.cc - cx_t[i])**2 + (g.rr - cy_t[i])**2)
        min_d = np.minimum(min_d, d)
    val = np.clip(1.0 - min_d / (g.cols * 0.3), 0, 1) * bri
    # Cell edges (where distance is near-equal between two centers)
    # ... second-nearest trick for edge highlighting
    mask = val > 0.03
    ch = val2char(val, mask, pal)
    R, G, B = hsv2rgb(np.full_like(val, hue) + min_d * 0.005, np.full_like(val, 0.5), val)
    return ch, mkc(R, G, B, g.rows, g.cols)
```
- ```
# S is the persistent state dict (same as r.S, passed explicitly)
if "px" not in S:
    S["px"]=[]; S["py"]=[]; S["vx"]=[]; S["vy"]=[]; S["life"]=[]; S["char"]=[]

# Emit new particles (on beat, continuously, or on trigger)
# Update: position += velocity, apply forces, decay life
# Draw: map to grid, set char/color based on life
# Cull: remove dead, cap total count
```
- ```
# Energy / explosive
PART_ENERGY  = list("*+#@\u26a1\u2726\u2605\u2588\u2593")
PART_SPARK   = list("\u00b7\u2022\u25cf\u2605\u2736*+")
# Organic / natural
PART_LEAF    = list("\u2740\u2741\u2742\u2743\u273f\u2618\u2022")
PART_SNOW    = list("\u2744\u2745\u2746\u00b7\u2022*\u25cb")
PART_RAIN    = list("|\u2502\u2503\u2551/\\")
PART_BUBBLE  = list("\u25cb\u25ce\u25c9\u25cf\u2218\u2219\u00b0")
# Data / tech
PART_DATA    = list("01{}[]<>|/\\")
PART_HEX     = list("0123456789ABCDEF")
PART_BINARY  = list("01")
# Mystical
PART_RUNE    = list("\u16a0\u16a2\u16a6\u16b1\u16b7\u16c1\u16c7\u16d2\u16d6\u16da\u16de\u16df\u2726\u2605")
PART_ZODIAC  = list("\u2648\u2649\u264a\u264b\u264c\u264d\u264e\u264f\u2650\u2651\u2652\u2653")
# Minimal
PART_DOT     = list("\u00b7\u2022\u25cf")
PART_DASH    = list("-=~\u2500\u2550")
```
- ```
def emit_explosion(S, f, center_r, center_c, char_set=PART_ENERGY, count_base=80):
    if f.get("beat", 0) > 0:
        for _ in range(int(count_base + f["rms"]*150)):
            ang = random.uniform(0, 2*math.pi)
            sp = random.uniform(1, 9) * (0.5 + f.get("sub_r", 0.3)*2)
            S["px"].append(float(center_c))
            S["py"].append(float(center_r))
            S["vx"].append(math.cos(ang)*sp*2.5)
            S["vy"].append(math.sin(ang)*sp)
            S["life"].append(1.0)
            S["char"].append(random.choice(char_set))
# Update: gravity on vy += 0.03, life -= 0.015
# Color: life * 255 for brightness, hue fade controlled by caller
```
- ```
# Emit: sy = rows-1, vy = -random.uniform(1,5), vx = random.uniform(-1.5,1.5)
# Update: vx += random jitter * 0.3, life -= 0.01
# Cap at ~1500 particles
```
- ```
# Init: N=600 particles spread across screen
# Update: slow upward drift, fade life progressively
# life -= 0.002 * (1 + elapsed * 0.05)  # accelerating fade
```
- ```
# N stars with (sx, sy, sz) in normalized coords
# Move: sz -= speed (stars approach camera)
# Project: px = cx + sx/sz * cx, py = cy + sy/sz * cy
# Reset stars that pass camera (sz <= 0.01)
# Brightness = (1 - sz), draw streaks behind bright stars
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
