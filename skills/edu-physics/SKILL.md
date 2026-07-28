---
name: edu-physics
description: >-
  把二维平面足以展示的物理教学场景（力学、热学、电磁学、光学、原子物理、振动与波、近代物理）
  做成交互教学网页：左栏题面 + 动态控制台（一个滑块驱动的实时物理量读数 + 守恒定律恒等式指示/
  状态判定），中栏 KaTeX 分步解析，右栏 2D Canvas 动态物理画板（轨迹/质点/矢量/波形/能量条/
  光线 + 画笔涂鸦）。无需外部物理引擎，通过坐标构造 + scalars 表达式 + trace/vector/constant
  实现交互。形态与 edu-plane-geometry 平行，但面向物理场景而非纯几何。
  三维物理（洛伦兹力/叉积方向、原子轨道、晶体结构、刚体旋转、电磁波正交等）请使用 edu-physics-3d。
  触发词：物理, 力学, 抛体运动, 动量守恒, 能量守恒, 简谐振动, 机械波, 电场, 磁场, 电磁感应,
  折射, 反射, 干涉, 衍射, 气体状态方程, 热力学, 原子物理, 相对论, 核物理 交互教学;
  physics, projectile motion, conservation of energy, conservation of momentum,
  simple harmonic motion, waves, electric field, magnetic field, refraction,
  reflection, gas laws, thermodynamics, atomic physics, interactive physics page.
---

# 物理 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块（如时间 t / 角度 θ / 速度 v / 温度 T）驱动实时
  重算的物理量（位置、速度、加速度、能量、动量…），以及"恒等式指示"（守恒定律）或"状态判定"。
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板。
- **右栏**：2D Canvas 动态物理画板（轨迹 trace + 质点 + 矢量箭头 + 波形 + 光线 + 电场线 +
  网格坐标轴），叠加画笔涂鸦工具栏。

## edu-physics（2D）与 edu-physics-3d 的分工

本技能（edu-physics）覆盖**二维平面即足以展示**的物理场景。凡是物理量/方向/轨迹涉及**三维空间**、
需要从任意角度观察的，请使用独立的 **edu-physics-3d** 技能（Three.js 三维画板）。

| 场景 | 使用技能 | 原因 |
|------|---------|------|
| 抛体运动、简谐振动、波 | **edu-physics** | 2D 完全够用 |
| 斜面滑块、碰撞、圆周运动 | **edu-physics** | 平面内运动 |
| 电场线、等势面、电路 | **edu-physics** | 平面场分布 |
| 气体状态变化、热力学循环 | **edu-physics** | PV 图平面 |
| 洛伦兹力 `F=qv×B` | **edu-physics-3d** | 叉积方向垂直于平面，必须 3D |
| 右手定则可视化 | **edu-physics-3d** | 力的方向垂直于 v 和 B 平面 |
| 原子轨道形状 | **edu-physics-3d** | s/p/d 轨道是三维空间分布 |
| 晶体结构/晶格 | **edu-physics-3d** | 三维空间排列 |
| 刚体旋转/角动量 | **edu-physics-3d** | 旋转轴在三维空间 |
| 电磁波 E/B 正交 | **edu-physics-3d** | 两场在三维空间正交传播 |
| 磁场（螺线管） | **edu-physics-3d** | 场线在三维空间分布 |

edu-physics 输出 2D Canvas 单页 HTML；edu-physics-3d 输出 Three.js 3D 单页 HTML。
两者数据岛格式不同（`board` vs `board3d`），详见各自 SKILL.md。

## 依赖
**无外部依赖**（不需要物理引擎、不需要 sympy）。模板引擎 `template/board.html` 是自包含的单页
HTML。只要能用 Python 3（标准库即可）做字符串替换就行，或者直接用 JSON 手动注入。

## 工作流程

### 第 1 步：确定题目规约
明确：
- **物理场景**：抛体运动/碰撞/振动/波动/折射/电场/气体变化等
- **可变参数**：时间 t、角度 θ、速度 v、温度 T 等，确定范围与步长
- **物理规律**：运动方程、牛顿定律、能量/动量守恒、气体状态方程等
- **交互范式**：滑块控制时间/角度/参数，观察物理量变化 + 轨迹/矢量/守恒验证
- **语言**：输出语言跟随提示词语言（中文/英文）

### 第 2 步：设计物理系统
这是最关键的一步。选取方便的系统坐标，写出物理量的参数化表达式。

**坐标放置技巧**：
- 抛体运动以抛出点为原点，x 水平向右、y 竖直向上
- 简谐振动以平衡位置为原点
- 光的折射将界面放在 x 轴上
- 斜面沿 x 轴方向

**物理量构造模式**：

| 场景 | 坐标方案 | scalars 序列 |
|------|---------|-------------|
| 抛体运动 | 原点在抛出点 | vx=v₀cosθ, vy=v₀sinθ-gt, x=vx·t, y=vy·t-½gt² |
| 简谐振动 | 平衡位置在原点 | x=A·cos(ωt+φ), v=-Aω·sin(ωt+φ), a=-Aω²·cos(ωt+φ) |
| 斜面滑块 | 斜面沿 x 轴 | a=g(sinθ-μcosθ), v=at, s=½at² |
| 动量守恒 | 同一直线 | v1'=(m1-m2)v1/(m1+m2), v2'=2m1v1/(m1+m2) |

**验证物理正确性**（心算检查）：
- 初始条件：t=0 时位置、速度、能量是否正确
- 守恒检验：机械能 Eₖ+Eₚ 是否为常数
- 边界条件：最高点 vy=0、落地点 y=0 时 x 是否正确

**viewport 范围**：留 10-15% 边距，确保完整运动轨迹在画板可见。

### 第 3 步：组装数据并注入模板

> 📍 **输出位置 & 唯一产物**：交付给用户的**只有一个 `.html`**，写到**当前工作目录
> （`Path.cwd()`）**。cwd 里不要留任何别的文件——构建脚本（`.py`）、`__pycache__`、截图等
> 临时文件一律放 `/tmp` 或用完即删。也绝不要写进技能自身目录。

**数据格式**（三段式 JSON，schema 见 `template/board.html` 数据岛 `__LESSON_DATA__`）：

```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "页面标题",
    "problem": "<p>题面 HTML，公式用 $…$ / $$…$$</p>",
    "answer": "$E_k+E_p = \\text{const}$"
  },
  "steps": [
    { "title": "步骤一", "content": "<p>解析内容...</p>" },
  ],
  "board": {
    "view": { "xRange": [-1, 10], "yRange": [-1, 6] },
    "points": {
      "O": [0, 0],
      "P": ["v0*cos(theta*PI/180)*t", "v0*sin(theta*PI/180)*t-0.5*g*t*t"],
      // 速度矢量箭头末端 = 当前位置 + 速度方向（缩放），用表达式点驱动
      "Vtip": ["x+vx*0.3", "y+vy*0.3"]
    },
    "param": {
      "name": "t",
      "label": "时间 $t$ (s)",
      "min": 0, "max": 5, "step": 0.05,
      "value": 0, "unit": "s",
      "ticks": ["0", "2.5", "5"]
    },
    "scalars": [
      { "name": "v0", "expr": "10" },
      { "name": "theta", "expr": "45" },
      { "name": "g", "expr": "9.8" },
      { "name": "vx", "expr": "v0*cos(theta*PI/180)" },
      { "name": "vy", "expr": "v0*sin(theta*PI/180)-g*t" },
      { "name": "x", "expr": "vx*t" },
      { "name": "y", "expr": "vy*t-0.5*g*t*t" },
      { "name": "Ek", "expr": "0.5*(vx*vx+vy*vy)" },
      { "name": "Ep", "expr": "g*y" },
      { "name": "E", "expr": "Ek+Ep" }
    ],
    "derived": [
      // 质点 P（points 里定义的点默认按浅灰渲染；这里用 vector 叠加箭头更醒目）
      // 位移矢量：从原点指向质点
      { "type": "vector", "name": "r_vec", "from": "O", "to": "P", "color": "vecA", "label": "$\\vec{r}$" },
      // 速度矢量：从质点 P 指向 Vtip（随速度方向变化的箭头）
      { "type": "vector", "name": "v_vec", "from": "P", "to": "Vtip", "color": "vec", "label": "$\\vec{v}$" },
    ],
    "readouts": [
      { "id": "x", "label": "水平位移 $x$", "type": "expr", "expr": "x", "digits": 2, "color": "vecA" },
      { "id": "y", "label": "竖直位移 $y$", "type": "expr", "expr": "y", "digits": 2, "color": "vecB" },
      { "id": "vx", "label": "$v_x$", "type": "expr", "expr": "vx", "digits": 2, "color": "vecA" },
      { "id": "vy", "label": "$v_y$", "type": "expr", "expr": "vy", "digits": 2, "color": "vecB" },
      { "id": "Ek", "label": "$E_k = \\frac{1}{2}mv^2$", "type": "expr", "expr": "Ek", "digits": 2 },
      { "id": "Ep", "label": "$E_p = mgy$", "type": "expr", "expr": "Ep", "digits": 2 },
      { "id": "E", "label": "$E = E_k+E_p$", "type": "expr", "expr": "E", "digits": 4, "highlight": true }
    ],
    // 定值指示（机械能守恒）—— of 指向上面 readouts 里真实存在的 id "E"
    "constant": { "of": "E", "label": "$E_k+E_p \\equiv \\text{常数}$" },
    // trace 轨迹
    "trace": { "of": "P", "color": "locus" },
    // 图例
    "legend": [
      { "color": "locus", "text": "轨迹" },
      { "color": "vec", "text": "速度 $\\vec{v}$" },
    ]
  }
}
```

**构建脚本方法**（Python，推荐）：
将构建脚本放 `/tmp`，直接做字符串替换：

```python
#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True

SKILL_DIR = Path(".claude/skills/edu-physics")
TEMPLATE = SKILL_DIR / "template" / "board.html"
PLACEHOLDER = "__LESSON_DATA__"

data = {
    "lesson": { ... },
    "steps": [ ... ],
    "board": { ... }
}

template = TEMPLATE.read_text(encoding="utf-8")
out_path = Path.cwd() / "solution-xxx.html"
out_path.write_text(
    template.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)),
    encoding="utf-8"
)
print("written:", out_path)
```

```bash
python3 -B /tmp/build.py && rm -f /tmp/build.py
```

> 注：如果运行时提示 `template/board.html` 路径不对，请使用绝对路径或从 `Path(__file__)` 推导。

### 第 4 步：自检与交付
- **物理正确性**：验证 t=0 初始条件、守恒量恒为定值、边界条件正确
- **浏览器预览**：起本地静态服务，检查无控制台报错、KaTeX 正常、滑块交互流畅
  - 滑块拖动时质点沿预期轨迹运动
  - trace 轨迹曲线正确（抛体为抛物线、SHM 为正弦等）
  - 矢量方向/大小随参数正确变化
  - constant 指示器全程恒定显示
- **关闭端口**：预览结束立即停掉本地服务
- **清理**：删除 `/tmp` 中的临时脚本，确认 cwd 只有 `.html`

## 数据格式参考（核心字段）

### board 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `view` | `{xRange, yRange}` | 数学坐标视窗 |
| `points` | `{name: [x,y] 或 {xy,color,label}}` | 关键位置坐标 |
| `param` | `{name, min, max, step, value, label, unit, ticks}` | 滑块定义 |
| `scalars` | `[{name, expr}]` | 由 param 派生的物理量 |
| `derived` | 构造序列 | point / vector / segment / polygon 等 |
| `readouts` | `[{id, label, type, ...}]` | 实时物理量数值 |
| `constant` | `{of, label}` | 守恒定律指示器 |
| `trace` | `{of, color}` | 轨迹采样（160步） |
| `legend` | `[{color, text}]` | 图例 |

### readouts 常用 type

| type | 字段 | 显示内容 |
|------|------|---------|
| `expr` | `expr, digits` | 任意物理量表达式 |
| `distance` | `a,b` (点) | 两点距离 |
| `coord` | `of` (点) | 坐标 |
| `status` | `expr, rhs, okText, badText` | 布尔状态判定（如"超重"/"失重"） |

### derived 常用 type

> 注意：质点位置在 `points` 里定义后会自动渲染（默认浅灰）；如需改变颜色/标签，
> 在 `points` 里用 `{xy, color, label}` 形式声明，而不是用 derived 的 `point`（该 type 未实现）。
> 速度/力矢量随质点变化时，常用做法：在 `points` 里定义一个"箭头末端"点（坐标用表达式），
> 再用 `vector` 从质点指向它（见上面抛体示例的 `Vtip`）。

| type | 字段 | 效果 |
|------|------|------|
| `segment` | `name, a, b, color, dashed` | 线段（光线/电场线/边界） |
| `vector` | `name, from, to, color, label` | 位移/力/场强矢量（`name` 必填） |
| `polygon` | `pts, color, stroke` | 半透明填充（能量条/区域） |
| `midpoint` | `name, a, b` | 中点 |
| `line_through_points` | `name, a, b, color` | 过两点直线 |
| `line_through_slope` | `name, point, slope, color` | 过一点斜率直线 |

### 颜色语义名
`curve`(金黄) · `line`(青) · `aux`(灰辅助) · `ptA`(红) · `ptB`(蓝) · `point`(浅灰) ·
`given`(紫) · `fixed`(翠绿) · `vecA`(红) · `vecB`(蓝) · `locus`(轨迹紫红) ·
`area`(青半透明)。
也可直接写 hex：`#f87171` 或 `rgba(248,113,113,0.25)`。

### 表达式引擎
坐标值/`scalars` 中的 `expr` 支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2
exp log pow min max sign floor ceil hypot PI`
三角函数使用**弧度**（角度需先转换：`theta*PI/180`）。
参数名须是合法 JS 标识符（如 `t`/`v0`/`theta`，不能用 `θ` 等非标识符）。

### trace 轨迹系统
在 `board` 中配置 `trace: { of: "点名称", color: "颜色" }` 后，引擎在 param 的 `[min, max]` 区间
均匀采样 160 步，对指定点绘制轨迹路径。适用于：
- 抛体运动的抛物线轨迹
- 简谐振动的 x-t 曲线（横轴时间，纵轴位移）
- 波的包络线

### constant 定值指示器
配置 `constant: { of: "读数id", label: "标签" }` 后，当读数值随滑块变化恒为定值时，
页面显示绿色横幅提示。适用于：
- 机械能守恒 (`Eₖ+Eₚ` 恒定)
- 动量守恒 (`m₁v₁+m₂v₂` 恒定)
- 勾股定理 (`a²+b²-c²≡0`)
- 其他恒等式

## 目录
- `template/board.html` — 数据驱动模板（通用 2D 渲染器 + 参数引擎 + 数据岛 `__LESSON_DATA__`）
- `references/conventions.md` — 物理交互范式、构造模式、自检清单
- `examples/` — 范例参考
