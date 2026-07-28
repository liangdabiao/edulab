# edulab — AI-Powered Interactive Teaching Skills

[简体中文](README.zh-CN.md) · **English**

A collection of **14 Claude Code skills** for subject education. Each skill auto-generates an interactive teaching web page from a subject topic — with Canvas 2D animations / Three.js 3D scenes, step-by-step walkthroughs, side-panel knowledge cards, and interactive parameter controls — covering Chemistry, IT, Biology, Geography, Mathematics, Physics, and Geometry.

## Install

```bash
npx skills add wy51ai/edulab
```

Or use as a Claude Code plugin:

```
/plugin marketplace add wy51ai/edulab
/plugin install edulab
```

Skills activate automatically on subject keywords in Claude Code, or can be invoked manually.

---

## Skills Overview

### 🧪 Chemistry

#### edu-chem-reaction — 3D Molecular Reaction Demonstrations

Generates a self-contained Three.js 3D demo page for a single chemical reaction. Left side: interactive molecular animation (drag slider to watch bonds break/form, atoms recombine, step highlighting). Right side: KaTeX equation, step-by-step narration, atom conservation counter, optional energy-reaction coordinate curve.

**Dual engine architecture**: `morph` (atoms fly to new partners — demonstrates atom conservation) and `mechanism` (rigid fragment keyframes — demonstrates catalysis/transition states). Sympy-driven: auto-balances equations, validates atom mapping (bijection), derives bond breaking/formation.

#### edu-chem-tutorial — Step-by-Step Chemistry Tutorials

Generates Canvas 2D step-by-step tutorials for non-reaction chemistry topics (redox balancing, metal activity series, electrolytes, etc.). `STEPS` array drives navigation, `SCENES` dictionary maps drawing functions, `__TUTORIAL_DATA__` placeholder injection. Optional interactive parameter sliders.

---

### 💻 Information Technology

#### edu-it — IT & General Technology Interactive Lessons

Generates step-by-step teaching pages with Canvas 2D animations for algorithms (bubble/selection/insertion sort, binary search), programming flowcharts, neural network structures, code execution visualization, hardware block diagrams, data charts, and electronic control systems. 20+ built-in scene types across algorithms, programming, data/AI, hardware/networking, and design.

---

### 🧬 Biology

#### edu-bio — Biology Interactive Lessons

Generates step-by-step teaching pages with 8 biology-specific Canvas 2D scenes: cell structure (organelle labeling), membrane transport, DNA double helix, cell division (mitosis/meiosis), Mendelian genetics, food webs, physiological systems, and PCR process.

---

### 🌍 Geography

#### edu-geo — Geography Interactive Lessons

Generates step-by-step teaching pages with 8 geography-specific Canvas 2D scene drawers: 3D globe (rotation/revolution), atmospheric circulation, water cycle, plate tectonics, population pyramids, urban models (concentric/sector/multiple-nuclei), map charts, and GIS layers.

---

### 📐 Mathematics

#### edu-math-function — Function Graph Interactive Lessons

Three-column page: left has parameter sliders (coefficient, frequency, phase) driving real-time function values, derivatives, and definite integrals; center has KaTeX step-by-step derivation; right has a Canvas 2D function plot (curve + tangent + shaded area + dynamic point + grid), with a drawing toolbar overlay.

#### edu-math-vectors — 2D Vector Interactive Lessons

Three-column page: slider-driven real-time vector quantities (magnitude, dot product, angle, components). Canvas 2D vector board: arrows, parallelogram law, component projection, vector chains, coordinate grid.

#### edu-math-stats — Probability & Statistics Interactive Lessons

Three-column page: slider-driven statistics (mean, stddev, probability, percentiles). Canvas 2D stats board: normal distribution curve, histograms, box plots, scatter plots with regression.

#### edu-math-logic — Set Logic Interactive Lessons

Three-column page with three visualization modes: **Venn diagrams** (2-3 set circles with intersection coloring), **truth tables** (HTML tables, 2^n rows, automatic expression evaluation), **logic gates** (Canvas-drawn AND/OR/NOT/NAND/NOR/XOR).

---

### ⚛ Physics

#### edu-physics — 2D Physics Interactive Lessons

Three-column page for 2D physics scenarios. Slider-driven real-time physical quantities with conservation law indicators. Canvas 2D supports: particle trajectories, vector arrows, waves, energy bars, light rays, drawing toolbar. No external physics engine — built through coordinate construction and scalars expressions.

Covers: mechanics, thermodynamics, electromagnetism, optics, vibration/waves, atomic physics.

#### edu-physics-3d — 3D Physics Interactive Lessons

Three-column page for 3D physics scenarios. Uses Three.js (CDN-loaded) with OrbitControls for rotatable/zoomable 3D scenes. No Python dependency.

Covers: Lorentz force, cross products, atomic orbitals, crystal structures, rigid body rotation, 3D EM waves.

---

### 📐 Geometry

#### edu-plane-geometry — Plane Geometry Interactive Lessons

Three-column page for Euclidean/plane geometry theorems. Canvas 2D board uses a light background with no coordinate grid (textbook style). Points are defined via geometric construction syntax (midpoint, foot of perpendicular, intersection, rotation, reflection). Annotation system for right-angle marks, equal-length marks, and arc labels.

#### edu-solid-geometry — Solid Geometry Interactive Problem Solving

Generates a self-contained interactive lesson page — MathJax step-by-step derivation on the left, Three.js interactive 3D model on the right. Sympy exact-computation core (`lib/geometry_kernel.py`) drives all calculations: coordinates, vectors, and final answer are all computed precisely with automatic radical simplification.

**Coordinate convention**: math coordinates (z-up) → three.js coordinates (y-up) via `kernel.to_three()`. One source drives both solution text and 3D rendering — "diagram, solution, and answer" are strictly consistent.

Problem types: line-plane angle, dihedral angle, skew-line angle, point-to-plane distance, volume, direction cosines on cubes/cuboids, pyramids/prisms, cylinders/cones.

Input modes: text problem, random generation (auto-resample if answer is messy), image upload with vision recognition.

#### edu-analytic-geometry — Analytic Geometry Interactive Problem Solving

Generates a self-contained interactive lesson page for conic sections. Canvas 2D + KaTeX with a data-driven interactive engine. A parameter slider drives derived constructions (line∩conic, point-on-conic, tangent…) with real-time readouts, range bars (open/closed interval endpoints auto-determined), and fixed-value indicators.

Unified solution method: parameterized line `x = my + c` → system → Vieta's formulas → substitution. Sympy-driven exact computation.

Problem types: standard equation, chord length, dot-product range/fixed value, triangle-area extremum, fixed point, fixed value (slope product), locus, tangent, eccentricity — on ellipses/hyperbolas/parabolas/circles.

---

## Architecture Overview

The 14 skills fall into two architectural families:

### Family A: Tutorial/Board Pattern (Canvas 2D, step-based, no sympy)

Skills: edu-chem-tutorial, edu-it, edu-bio, edu-geo, edu-math-function, edu-math-vectors, edu-math-stats, edu-math-logic, edu-physics, edu-plane-geometry

Single-page HTML, `__TUTORIAL_DATA__` / `__LESSON_DATA__` placeholder injection, `STEPS` arrays, `SCENES` drawing dictionaries, optional interactive sliders via `sceneArgs.param`. No external dependencies.

### Family B: Calculation Kernel Pattern (sympy-driven, Three.js or Canvas 2D)

Skills: edu-chem-reaction, edu-solid-geometry, edu-analytic-geometry, edu-physics-3d

Sympy (or physics kernel) for precise calculation driving both answer and visuals. Computation core output and visual coordinates share the same source. Three input modes: text problem, random generation, image upload. Built-in self-check: kernel answer == answer card == final step value.

## How It Works

1. **AI understands input** — Claude Code identifies the subject topic from user input (text/image/keywords)
2. **Skill activates** — matching edu-* skill invokes its generation logic
3. **Structured data assembled** — `{lesson, steps, model/scenes}` structure built from templates
4. **Template injection** — JSON injected as data island (`<script id="lesson-data" type="application/json">`)
5. **Self-check & deliver** — answer correctness verified, standalone HTML written to user working directory

## License

[Apache-2.0](LICENSE)

## Author

WY · [@akokoi1](https://x.com/akokoi1)
