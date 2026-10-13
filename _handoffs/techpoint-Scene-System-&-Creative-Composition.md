---
layout: default
title: 技术点 · Scene System & Creative Composition
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Scene System & Creative Composition

> 来源：261010_Scene System & Creative Composition_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
def fx_example(r, f, t, S):
    local = t
    progress = min(local / 5.0, 1.0)

    g_bg = r.get_grid("sm")
    g_main = r.get_grid("md")
    g_accent = r.get_grid("lg")

    # --- Background: dim atmosphere ---
    bg_val = vf_smooth_noise(g_bg, f, t * 0.3, S, octaves=2, bri=0.15)
    # ... render bg to canvas

    # --- Content: the main visual idea ---
    content_val = vf_spiral(g_main, f, t, S, n_arms=n_arms, tightness=tightness)
    # ... render content on top of canvas

    # --- Accent: sparse highlights ---
    accent_val = vf_noise_static(g_accent, f, t, S, density=0.05)
    # ... render accent on top

    return canvas
```
- ```
# Primary spiral (clockwise)
s1_val = vf_spiral(g_main, f, t * 1.5, S, n_arms=n_arms_1, tightness=tightness_1)

# Counter-rotating spiral (counter-clockwise via negative time)
s2_val = vf_spiral(g_accent, f, -t * 1.2, S, n_arms=n_arms_2, tightness=tightness_2)

# Screen blend creates bright interference at crossing points
canvas = blend_canvas(canvas_with_s1, c2, "screen", 0.7)
```
- ```
collision_phase = abs(progress - 0.5) * 2  # 1→0→1 (0 at collision)

# Wave A approaches from left
offset_a = (1 - progress) * g.cols * 0.4
wave_a = np.sin((g.cc + offset_a) * 0.08 + t * 2) * 0.5 + 0.5

# Wave B approaches from right
offset_b = -(1 - progress) * g.cols * 0.4
wave_b = np.sin((g.cc + offset_b) * 0.08 - t * 2) * 0.5 + 0.5

# Interference peaks at collision
combined = wave_a * 0.5 + wave_b * 0.5 + np.abs(wave_a - wave_b) * (1 - collision_phase) * 0.5
```
- ```
n_pts = int(8 + progress * 30)  # 8 cells → 38 cells
# Pre-generate enough points, slice to n_pts
px = base_x[:n_pts] + np.sin(t * 0.3 + np.arange(n_pts) * 0.7) * (3 + progress * 3)
```
- ```
# Geometry fades out
geo_val = clean_pattern * max(0.05, 1.0 - progress * 0.9)

# Organic process grows in
rd_val = vf_reaction_diffusion(g, f, t, S) * min(1.0, progress * 1.5)

# Render geometry first, organic on top — organic consumes geometry
```
- ```
def layer_strength(enter_t, ramp=1.5):
    """0.0 until enter_t, ramps to 1.0 over ramp seconds."""
    return max(0.0, min(1.0, (local - enter_t) / ramp))

# Layer 1: always present
s1 = layer_strength(0.0)
# Layer 2: enters at 2s
s2 = layer_strength(2.0)
# Layer 3: enters at 4s
s3 = layer_strength(4.0)
# ... etc

# Each layer uses a different effect, grid, palette, and blend mode
# Screen blend between layers so they accumulate light
```
- ```
def fx_scene_name(r, f, t, S) -> canvas:
    """
    Args:
        r: Renderer instance — access multiple grids via r.get_grid("sm")
        f: dict of audio/video features, all values normalized to [0, 1]
        t: time in seconds — local to scene (0.0 at scene start)
        S: dict for persistent state (particles, rain columns, etc.)

    Returns:
        canvas: numpy uint8 array, shape (VH, VW, 3) — full pixel frame
    """
```
- ```
# In render_clip:
t_local = fi / FPS - scene_start
canvas = fx_fn(r, feat, t_local, S)
```
- ```
progress = min(t / scene_duration, 1.0)  # 0→1 over the scene
```
- ```
class Renderer:
    def __init__(self):
        self.grids = {}   # lazy-initialized grid cache
        self.g = None      # "active" grid (for backward compat)
        self.S = {}        # persistent state dict

    def get_grid(self, key):
        """Get or create a GridLayer by size key."""
        if key not in self.grids:
            sizes = {"xs": 8, "sm": 10, "md": 16, "lg": 20, "xl": 24, "xxl": 40}
            self.grids[key] = GridLayer(FONT_PATH, sizes[key])
        return self.grids[key]

    def set_grid(self, key):
        """Set active grid (legacy). Prefer get_grid() for multi-grid scenes."""
        self.g = self.get_grid(key)
        return self.g
```
- **Key difference from v1**: scenes call `r.get_grid("sm")`, `r.get_grid("lg")`, etc. to access multiple grids. Each grid is lazy-initialized and cached. The `set_grid()` method still works for single-grid scenes.
- ```
def fx_simple_rings(r, f, t, S):
    """Single-grid scene: rings with distance-mapped hue."""
    canvas = _render_vf(r, "md",
        lambda g, f, t, S: vf_rings(g, f, t, S, n_base=8, spacing_base=3),
        hf_distance(0.3, 0.02), PAL_STARS, f, t, S, sat=0.85)
    return canvas
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
