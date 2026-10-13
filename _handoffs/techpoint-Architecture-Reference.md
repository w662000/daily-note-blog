---
layout: default
title: 技术点 · Architecture Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Architecture Reference

> 来源：261010_Architecture Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
RESOLUTION_PRESETS = {
    "landscape":  (1920, 1080),  # 16:9 — YouTube, default
    "portrait":   (1080, 1920),  # 9:16 — TikTok, Reels, Stories
    "square":     (1080, 1080),  # 1:1  — Instagram feed
    "ultrawide":  (2560, 1080),  # 21:9 — cinematic
    "landscape4k":(3840, 2160),  # 16:9 — 4K
    "portrait4k": (2160, 3840),  # 9:16 — 4K portrait
}

def get_resolution(preset="landscape", custom=None):
    """Returns (VW, VH) tuple."""
    if custom:
        return custom
    return RESOLUTION_PRESETS.get(preset, RESOLUTION_PRESETS["landscape"])
```
- | Key | Font Size | Grid (cols x rows) | Use |
- **Key differences in portrait mode:**
- ```
import platform

def find_font(preferences):
    """Try fonts in order, return first that exists."""
    for name, path in preferences:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"No monospace font found. Tried: {[p for _,p in preferences]}")

FONT_PREFS_MACOS = [
    ("Menlo", "/System/Library/Fonts/Menlo.ttc"),
    ("Monaco", "/System/Library/Fonts/Monaco.ttf"),
    ("SF Mono", "/System/Library/Fonts/SFNSMono.ttf"),
    ("Courier", "/System/Library/Fonts/Courier.ttc"),
]
FONT_PREFS_LINUX = [
    ("DejaVu Sans Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ("Liberation Mono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    ("Noto Sans Mono", "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"),
    ("Ubuntu Mono", "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"),
]
FONT_PREFS_WINDOWS = [
    ("Consolas", r"C:\Windows\Fonts\consola.ttf"),
    ("Courier New", r"C:\Windows\Fonts\cour.ttf"),
    ("Lucida Console", r"C:\Windows\Fonts\lucon.ttf"),
    ("Cascadia Code", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts\CascadiaCode.ttf")),
    ("Cascadia Mono", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts\CascadiaMono.ttf")),
]

def _get_font_prefs():
    s = platform.system()
    if s == "Darwin":
        return FONT_PREFS_MACOS
    elif s == "Windows":
        return FONT_PREFS_WINDOWS
    return FONT_PREFS_LINUX

FONT_PREFS = _get_font_prefs()
```
- ```
grid_bg = GridLayer(find_font(FONT_PREFS), 16)       # background
grid_text = GridLayer(find_font(BOLD_PREFS), 20)      # readable text
```
- ```
all_chars = set()
for pal in [PAL_DEFAULT, PAL_DENSE, PAL_BLOCKS, PAL_RUNE, PAL_KATA,
            PAL_GREEK, PAL_MATH, PAL_DOTS, PAL_BRAILLE, PAL_STARS,
            PAL_HALFFILL, PAL_HATCH, PAL_BINARY, PAL_MUSIC, PAL_BOX,
            PAL_CIRCUIT, PAL_ARROWS, PAL_HERMES]:  # ... all palettes used in project
    all_chars.update(pal)
# Add any overlay text characters
all_chars.update("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,-:;!?/|")
all_chars.discard(" ")  # space is never rendered
```
- ```
class GridLayer:
    def __init__(self, font_path, font_size, vw=None, vh=None):
        """Initialize grid for any resolution.
        vw, vh: video width/height in pixels. Defaults to global VW, VH."""
        vw = vw or VW; vh = vh or VH
        self.vw = vw; self.vh = vh

        self.font = ImageFont.truetype(font_path, font_size)
        asc, desc = self.font.getmetrics()
        bbox = self.font.getbbox("M")
        self.cw = bbox[2] - bbox[0]  # character cell width
        self.ch = asc + desc  # CRITICAL: not textbbox height

        self.cols = vw // self.cw
        self.rows = vh // self.ch
        self.ox = (vw - self.cols * self.cw) // 2  # centering
        self.oy = (vh - self.rows * self.ch) // 2

        # Aspect ratio metadata
        self.aspect = vw / vh  # >1 = landscape, <1 = portrait, 1 = square
        self.is_portrait = vw < vh
        self.is_landscape = vw > vh

        # Index arrays
        self.rr = np.arange(self.rows, dtype=np.float32)[:, None]
        self.cc = np.arange(self.cols, dtype=np.float32)[None, :]

        # Polar coordinates (aspect-corrected)
        cx, cy = self.cols / 2.0, self.rows / 2.0
        asp = self.cw / self.ch
        self.dx = self.cc - cx
        self.dy = (self.rr - cy) * asp
        self.dist = np.sqrt(self.dx**2 + self.dy**2)
        self.angle = np.arctan2(self.dy, self.dx)

        # Normalized (0-1 range) -- for distance falloff
        self.dx_n = (self.cc - cx) / max(self.cols, 1)
        self.dy_n = (self.rr - cy) / max(self.rows, 1) * asp
        self.dist_n = np.sqrt(self.dx_n**2 + self.dy_n**2)

        # Pre-rasterize all characters to float32 bitmaps
        self.bm = {}
        for c in all_chars:
            img = Image.new("L", (self.cw, self.ch), 0)
            ImageDraw.Draw(img).text((0, 0), c, fill=255, font=self.font)
            self.bm[c] = np.array(img, dtype=np.float32) / 255.0
```
- ```
def render(self, chars, colors, canvas=None):
    if canvas is None:
        canvas = np.zeros((VH, VW, 3), dtype=np.uint8)
    for row in range(self.rows):
        y = self.oy + row * self.ch
        if y + self.ch > VH: break
        for col in range(self.cols):
            c = chars[row, col]
            if c == " ": continue
            x = self.ox + col * self.cw
            if x + self.cw > VW: break
            a = self.bm[c]  # float32 bitmap
            canvas[y:y+self.ch, x:x+self.cw] = np.maximum(
                canvas[y:y+self.ch, x:x+self.cw],
                (a[:, :, None] * colors[row, col]).astype(np.uint8))
    return canvas
```
- ```
canvas = np.zeros((VH, VW, 3), dtype=np.uint8)
canvas = grid_lg.render(bg_chars, bg_colors, canvas)   # background layer
canvas = grid_md.render(main_chars, main_colors, canvas)  # main layer
canvas = grid_sm.render(detail_chars, detail_colors, canvas)  # detail overlay
```
- ```
PAL_DEFAULT  = " .`'-:;!><=+*^~?/|(){}[]#&$@%"       # classic ASCII art
PAL_DENSE    = " .:;+=xX$#@\u2588"                          # simple 11-level ramp
PAL_MINIMAL  = " .:-=+#@"                               # 8-level, graphic
PAL_BINARY   = " \u2588"                                      # 2-level, extreme contrast
PAL_GRADIENT = " \u2591\u2592\u2593\u2588"                              # 4-level block gradient
```
- ```
PAL_BLOCKS   = " \u2591\u2592\u2593\u2588\u2584\u2580\u2590\u258c"                 # standard blocks
PAL_BLOCKS_EXT = " \u2596\u2597\u2598\u2599\u259a\u259b\u259c\u259d\u259e\u259f\u2591\u2592\u2593\u2588"  # quadrant blocks (more detail)
PAL_SHADE    = " \u2591\u2592\u2593\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581"          # vertical fill progression
```
- ```
PAL_MATH     = " \u00b7\u2218\u2219\u2022\u00b0\u00b1\u2213\u00d7\u00f7\u2248\u2260\u2261\u2264\u2265\u221e\u222b\u2211\u220f\u221a\u2207\u2202\u2206\u03a9"    # math symbols
PAL_BOX      = " \u2500\u2502\u250c\u2510\u2514\u2518\u251c\u2524\u252c\u2534\u253c\u2550\u2551\u2554\u2557\u255a\u255d\u2560\u2563\u2566\u2569\u256c"          # box drawing
PAL_CIRCUIT  = " .\u00b7\u2500\u2502\u250c\u2510\u2514\u2518\u253c\u25cb\u25cf\u25a1\u25a0\u2206\u2207\u2261"                 # circuit board
PAL_RUNE     = " .\u16a0\u16a2\u16a6\u16b1\u16b7\u16c1\u16c7\u16d2\u16d6\u16da\u16de\u16df"                   # elder futhark runes
PAL_ALCHEMIC = " \u2609\u263d\u2640\u2642\u2643\u2644\u2645\u2646\u2647\u2648\u2649\u264a\u264b"            # planetary/alchemical symbols
PAL_ZODIAC   = " \u2648\u2649\u264a\u264b\u264c\u264d\u264e\u264f\u2650\u2651\u2652\u2653"            # zodiac
PAL_ARROWS   = " \u2190\u2191\u2192\u2193\u2194\u2195\u2196\u2197\u2198\u2199\u21a9\u21aa\u21bb\u27a1"             # directional arrows
PAL_MUSIC    = " \u266a\u266b\u266c\u2669\u266d\u266e\u266f\u25cb\u25cf"                       # musical notation
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
