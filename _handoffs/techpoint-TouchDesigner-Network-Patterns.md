---
layout: default
title: 技术点 · TouchDesigner Network Patterns
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · TouchDesigner Network Patterns

> 来源：261010_TouchDesigner Network Patterns_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Complete network recipes for common creative coding tasks. Each pattern shows the operator chain, MCP tool calls to build it, and key parameter settings.
- ```
Audio File In CHOP -> Audio Spectrum CHOP -> Math CHOP (scale)
                                                |
                                                v (export to noise params)
                          Noise TOP -> Level TOP -> Feedback TOP -> Composite TOP -> Null TOP (out)
                                                        ^                |
                                                        |________________|
```
- ```
1. td_create_operator(parent="/project1", type="audiofileinChop", name="audio_in")
2. td_create_operator(parent="/project1", type="audiospectrumChop", name="spectrum")
3. td_create_operator(parent="/project1", type="mathChop", name="spectrum_scale")
4. td_create_operator(parent="/project1", type="noiseTop", name="noise1")
5. td_create_operator(parent="/project1", type="levelTop", name="level1")
6. td_create_operator(parent="/project1", type="feedbackTop", name="feedback1")
7. td_create_operator(parent="/project1", type="compositeTop", name="comp1")
8. td_create_operator(parent="/project1", type="nullTop", name="out")

9. td_set_operator_pars(path="/project1/audio_in",
     properties={"file": "/path/to/music.wav", "play": true})
10. td_set_operator_pars(path="/project1/spectrum",
     properties={"size": 512})
11. td_set_operator_pars(path="/project1/spectrum_scale",
     properties={"gain": 2.0, "postoff": 0.0})
12. td_set_operator_pars(path="/project1/noise1",
     properties={"type": 1, "monochrome": false, "resolutionw": 1280, "resolutionh": 720,
                  "period": 4.0, "harmonics": 3, "amp": 1.0})
13. td_set_operator_pars(path="/project1/level1",
     properties={"opacity": 0.95, "gamma1": 0.75})
14. td_set_operator_pars(path="/project1/feedback1",
     properties={"top": "/project1/comp1"})
15. td_set_operator_pars(path="/project1/comp1",
     properties={"operand": 0})

16. td_execute_python: """
op('/project1/audio_in').outputConnectors[0].connect(op('/project1/spectrum'))
op('/project1/spectrum').outputConnectors[0].connect(op('/project1/spectrum_scale'))
op('/project1/noise1').outputConnectors[0].connect(op('/project1/level1'))
op('/project1/level1').outputConnectors[0].connect(op('/project1/comp1').inputConnectors[0])
op('/project1/feedback1').outputConnectors[0].connect(op('/project1/comp1').inputConnectors[1])
op('/project1/comp1').outputConnectors[0].connect(op('/project1/out'))
"""

17. td_execute_python: """
# Export spectrum values to drive noise parameters
# This makes the noise react to audio frequencies
op('/project1/noise1').par.seed.expr = "op('/project1/spectrum_scale')['chan1']"
op('/project1/noise1').par.period.expr = "tdu.remap(op('/project1/spectrum_scale')['chan1'].eval(), 0, 1, 1, 8)"
"""
```
- ```
Audio Device In CHOP -> Audio Spectrum CHOP -> Math CHOP (isolate bass)
                                                    |
                                              Trigger CHOP (envelope)
                                                    |
                                              [export to visual params]
```
- **Key parameter settings:**
- ```
# Isolate bass frequencies (20-200 Hz)
Math CHOP: chanop=1 (Add channels), range1low=0, range1high=10
           (first 10 FFT bins = bass frequencies with 512 FFT at 44100Hz)

# ADSR envelope on each beat
Trigger CHOP: attack=0.02, peak=1.0, decay=0.3, sustain=0.0, release=0.1

# Export to visual: Scale, brightness, or color intensity
td_execute_python: "op('/project1/level1').par.brightness1.expr = \"1.0 + op('/project1/trigger1')['chan1'] * 0.5\""
```
- ```
Audio In -> Spectrum -> Audio Band EQ (3 bands: bass, mid, treble)
                              |
                    +---------+---------+
                    |         |         |
                 Bass      Mids     Treble
                  |          |         |
           Noise TOP   Circle TOP  Text TOP
           (slow,dark) (mid,warm)  (fast,bright)
                  |          |         |
                  +-----+----+----+----+
                        |         |
                   Composite  Composite
                        |
                       Out
```
- ```
AudioFileIn CHOP → AudioSpectrum CHOP (FFT=512, outlength=256)
    → Math CHOP (gain=10) → CHOP To TOP (256x2 spectrum texture, dataformat=r)
                                                                   ↓
Constant TOP (time, rgba32float) → GLSL TOP (input 0=time, input 1=spectrum) → Null → MovieFileOut
                                                                                        ↓
AudioFileIn CHOP → Audio Device Out CHOP                                          Record to .mov
```
- ```
# Step 1: Audio chain
# td_execute_python script:
td_execute_python(code="""
root = op('/project1')
audio = root.create(audiofileinCHOP, 'audio_in')
audio.par.file = '/path/to/music.mp3'
audio.par.playmode = 0  # Locked to timeline
audio.par.volume = 0.5

spec = root.create(audiospectrumCHOP, 'spectrum')
audio.outputConnectors[0].connect(spec.inputConnectors[0])

math_n = root.create(mathCHOP, 'math_norm')
spec.outputConnectors[0].connect(math_n.inputConnectors[0])
math_n.par.gain = 5  # boost signal

resamp = root.create(resampleCHOP, 'resample_spec')
math_n.outputConnectors[0].connect(resamp.inputConnectors[0])
resamp.par.timeslice = True
resamp.par.rate = 256

chop2top = root.create(choptoTOP, 'spectrum_tex')
chop2top.par.chop = resamp  # CHOP To TOP has NO input connectors — use par.chop reference

# Audio output (hear the music)
aout = root.create(audiodeviceoutCHOP, 'audio_out')
audio.outputConnectors[0].connect(aout.inputConnectors[0])
result = 'audio chain ok'
""")

# Step 2: Time driver (MUST be rgba32float — see pitfalls #6)
# td_execute_python script:
td_execute_python(code="""
root = op('/project1')
td = root.create(constantTOP, 'time_driver')
td.par.format = 'rgba32float'
td.par.outputresolution = 'custom'
td.par.resolutionw = 1
td.par.resolutionh = 1
td.par.colorr.expr = "absTime.seconds % 1000.0"
td.par.colorg.expr = "int(absTime.seconds / 1000.0)"
result = 'time ok'
""")

# Step 3: GLSL shader (write to /tmp, load from file)
# td_execute_python script:
td_execute_python(code="""
root = op('/project1')
glsl = root.create(glslTOP, 'audio_shader')
glsl.par.outputresolution = 'custom'
glsl.par.resolutionw = 1280
glsl.par.resolutionh = 720

sd = root.create(textDAT, 'shader_code')
sd.text = open('/tmp/my_shader.glsl').read()
glsl.par.pixeldat = sd

# Wire: input 0 = time, input 1 = spectrum texture
op('/project1/time_driver').outputConnectors[0].connect(glsl.inputConnectors[0])
op('/project1/spectrum_tex').outputConnectors[0].connect(glsl.inputConnectors[1])
result = 'glsl ok'
""")

# Step 4: Output + recorder
# td_execute_python script:
td_execute_python(code="""
root = op('/project1')
out = root.create(nullTOP, 'output')
op('/project1/audio_shader').outputConnectors[0].connect(out.inputConnectors[0])

rec = root.create(moviefileoutTOP, 'recorder')
out.outputConnectors[0].connect(rec.inputConnectors[0])
rec.par.type = 'movie'
rec.par.file = '/tmp/output.mov'
rec.par.videocodec = 'mjpa'
result = 'output ok'
""")
```
- ```
out vec4 fragColor;

vec3 palette(float t) {
    vec3 a = vec3(0.5); vec3 b = vec3(0.5);
    vec3 c = vec3(1.0); vec3 d = vec3(0.263, 0.416, 0.557);
    return a + b * cos(6.28318 * (c * t + d));
}

void main() {
    // Input 0 = time (1x1 rgba32float constant)
    // Input 1 = audio spectrum (256x2 CHOP To TOP, stereo — sample at y=0.25 for first channel)
    vec4 td = texture(sTD2DInputs[0], vec2(0.5));
    float t = td.r + td.g * 1000.0;

    vec2 res = uTDOutputInfo.res.zw;
    vec2 uv = (gl_FragCoord.xy * 2.0 - res) / min(res.x, res.y);
    vec2 uv0 = uv;
    vec3 finalColor = vec3(0.0);

    float bass = texture(sTD2DInputs[1], vec2(0.05, 0.25)).r;
    float mids = texture(sTD2DInputs[1], vec2(0.25, 0.25)).r;

    for (float i = 0.0; i < 4.0; i++) {
        uv = fract(uv * (1.4 + bass * 0.3)) - 0.5;
        float d = length(uv) * exp(-length(uv0));

        // Sample spectrum at distance: inner=bass, outer=treble
        float freq = texture(sTD2DInputs[1], vec2(clamp(d * 0.5, 0.0, 1.0), 0.25)).r;

        vec3 col = palette(length(uv0) + i * 0.4 + t * 0.35);
        d = sin(d * (7.0 + bass * 4.0) + t * 1.5) / 8.0;
        d = abs(d);
        d = pow(0.012 / d, 1.2 + freq * 0.8 + bass * 0.5);
        finalColor += col * d;
    }

    // Tone mapping
    finalColor = finalColor / (finalColor + vec3(1.0));
    fragColor = TDOutputSwizzle(vec4(finalColor, 1.0));
}
```
- **Key insights from testing:**
- ```
Noise TOP -> Composite TOP -> Level TOP -> Null TOP (out)
                  ^      |
                  |      v
            Transform TOP <- Feedback TOP
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
