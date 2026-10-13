---
layout: default
title: 技术点 · Visual Effects
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Visual Effects

> 来源：261010_Visual Effects_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
noiseSeed(42);
noiseDetail(4, 0.5);  // octaves, falloff

// 1D noise — smooth undulation
let y = noise(x * 0.01);  // returns 0.0 to 1.0

// 2D noise — terrain/texture
let v = noise(x * 0.005, y * 0.005);

// 3D noise — animated 2D field (z = time)
let v = noise(x * 0.005, y * 0.005, frameCount * 0.005);
```
- ```
function fbm(x, y, octaves = 6, lacunarity = 2.0, gain = 0.5) {
  let value = 0;
  let amplitude = 1.0;
  let frequency = 1.0;
  let maxValue = 0;
  for (let i = 0; i < octaves; i++) {
    value += noise(x * frequency, y * frequency) * amplitude;
    maxValue += amplitude;
    amplitude *= gain;
    frequency *= lacunarity;
  }
  return value / maxValue;
}
```
- ```
function domainWarp(x, y, scale, strength, time) {
  // First warp pass
  let qx = fbm(x + 0.0, y + 0.0);
  let qy = fbm(x + 5.2, y + 1.3);

  // Second warp pass (feed back)
  let rx = fbm(x + strength * qx + 1.7, y + strength * qy + 9.2, 4, 2, 0.5);
  let ry = fbm(x + strength * qx + 8.3, y + strength * qy + 2.8, 4, 2, 0.5);

  return fbm(x + strength * rx + time, y + strength * ry + time);
}
```
- ```
function curlNoise(x, y, scale, time) {
  let eps = 0.001;
  // Partial derivatives via finite differences
  let dndx = (noise(x * scale + eps, y * scale, time) -
              noise(x * scale - eps, y * scale, time)) / (2 * eps);
  let dndy = (noise(x * scale, y * scale + eps, time) -
              noise(x * scale, y * scale - eps, time)) / (2 * eps);
  // Curl = perpendicular to gradient
  return createVector(dndy, -dndx);
}
```
- ```
class FlowField {
  constructor(resolution, noiseScale) {
    this.resolution = resolution;
    this.cols = ceil(width / resolution);
    this.rows = ceil(height / resolution);
    this.field = new Array(this.cols * this.rows);
    this.noiseScale = noiseScale;
  }

  update(time) {
    for (let i = 0; i < this.cols; i++) {
      for (let j = 0; j < this.rows; j++) {
        let angle = noise(i * this.noiseScale, j * this.noiseScale, time) * TWO_PI * 2;
        this.field[i + j * this.cols] = p5.Vector.fromAngle(angle);
      }
    }
  }

  lookup(x, y) {
    let col = constrain(floor(x / this.resolution), 0, this.cols - 1);
    let row = constrain(floor(y / this.resolution), 0, this.rows - 1);
    return this.field[col + row * this.cols].copy();
  }
}
```
- ```
class FlowParticle {
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
    this.prev = this.pos.copy();
    this.maxSpeed = 2;
    this.life = 1.0;
  }

  follow(field) {
    let force = field.lookup(this.pos.x, this.pos.y);
    force.mult(0.5);  // force magnitude
    this.acc.add(force);
  }

  update() {
    this.prev = this.pos.copy();
    this.vel.add(this.acc);
    this.vel.limit(this.maxSpeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
    this.life -= 0.001;
  }

  edges() {
    if (this.pos.x > width) this.pos.x = 0;
    if (this.pos.x < 0) this.pos.x = width;
    if (this.pos.y > height) this.pos.y = 0;
    if (this.pos.y < 0) this.pos.y = height;
    this.prev = this.pos.copy();  // prevent wrap line
  }

  display(buffer) {
    buffer.stroke(255, this.life * 30);
    buffer.strokeWeight(0.5);
    buffer.line(this.prev.x, this.prev.y, this.pos.x, this.pos.y);
  }
}
```
- ```
class Particle {
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = p5.Vector.random2D().mult(random(1, 3));
    this.acc = createVector(0, 0);
    this.life = 255;
    this.decay = random(1, 5);
    this.size = random(3, 8);
  }

  applyForce(f) { this.acc.add(f); }

  update() {
    this.vel.add(this.acc);
    this.pos.add(this.vel);
    this.acc.mult(0);
    this.life -= this.decay;
  }

  display() {
    noStroke();
    fill(255, this.life);
    ellipse(this.pos.x, this.pos.y, this.size);
  }

  isDead() { return this.life <= 0; }
}
```
- ```
class Attractor {
  constructor(x, y, strength) {
    this.pos = createVector(x, y);
    this.strength = strength;
  }

  attract(particle) {
    let force = p5.Vector.sub(this.pos, particle.pos);
    let d = constrain(force.mag(), 5, 200);
    force.normalize();
    force.mult(this.strength / (d * d));
    particle.applyForce(force);
  }
}
```
- ```
class Boid {
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = p5.Vector.random2D().mult(random(2, 4));
    this.acc = createVector(0, 0);
    this.maxForce = 0.2;
    this.maxSpeed = 4;
    this.perceptionRadius = 50;
  }

  flock(boids) {
    let alignment = createVector(0, 0);
    let cohesion = createVector(0, 0);
    let separation = createVector(0, 0);
    let total = 0;

    for (let other of boids) {
      let d = this.pos.dist(other.pos);
      if (other !== this && d < this.perceptionRadius) {
        alignment.add(other.vel);
        cohesion.add(other.pos);
        let diff = p5.Vector.sub(this.pos, other.pos);
        diff.div(d * d);
        separation.add(diff);
        total++;
      }
    }
    if (total > 0) {
      alignment.div(total).setMag(this.maxSpeed).sub(this.vel).limit(this.maxForce);
      cohesion.div(total).sub(this.pos).setMag(this.maxSpeed).sub(this.vel).limit(this.maxForce);
      separation.div(total).setMag(this.maxSpeed).sub(this.vel).limit(this.maxForce);
    }

    this.acc.add(alignment.mult(1.0));
    this.acc.add(cohesion.mult(1.0));
    this.acc.add(separation.mult(1.5));
  }

  update() {
    this.vel.add(this.acc);
    this.vel.limit(this.maxSpeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }
}
```
- ```
loadPixels();
for (let y = 0; y < height; y++) {
  for (let x = 0; x < width; x++) {
    let idx = 4 * (y * width + x);
    let r = pixels[idx];
    let g = pixels[idx + 1];
    let b = pixels[idx + 2];
    let a = pixels[idx + 3];

    // Modify
    pixels[idx] = 255 - r;       // invert red
    pixels[idx + 1] = 255 - g;   // invert green
    pixels[idx + 2] = 255 - b;   // invert blue
  }
}
updatePixels();
```
- ```
loadPixels();
for (let i = 0; i < pixels.length; i += 4) {
  let x = (i / 4) % width;
  let y = floor((i / 4) / width);
  let n = noise(x * 0.01, y * 0.01, frameCount * 0.02);
  let c = n * 255;
  pixels[i] = c;
  pixels[i + 1] = c;
  pixels[i + 2] = c;
  pixels[i + 3] = 255;
}
updatePixels();
```
- ```
filter(BLUR, 3);        // Gaussian blur (radius)
filter(THRESHOLD, 0.5); // Black/white threshold
filter(INVERT);          // Color inversion
filter(POSTERIZE, 4);    // Reduce color levels
filter(GRAY);            // Desaturate
filter(ERODE);           // Thin bright areas
filter(DILATE);          // Expand bright areas
filter(OPAQUE);          // Remove transparency
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
