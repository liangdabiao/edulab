---
name: edu-physics-3d
description: >-
  把需要三维展示的物理场景（洛伦兹力/叉积、原子轨道、晶体结构、刚体旋转、3D 磁场/电磁波
  等）做成交互教学网页：左栏题面 + 动态控制台（滑块驱动的实时物理量读数 + 守恒定律指示），
  中栏 KaTeX 分步解析，右栏 Three.js 3D 交互画板（球体/箭头/轨迹曲线，可旋转缩放）。
  依赖 Three.js（CDN 加载），无需 sympy。形态与 edu-chem-reaction 平行，但面向 3D 物理
  教学而非化学分子。2D 物理场景（抛体、振动、波、光学等）请使用 edu-physics。
  触发词：3D 物理, 洛伦兹力, 叉积, 右手定则, 原子轨道, 晶体结构, 三维旋转, 磁场三维,
  电磁波三维; 3D physics, Lorentz force, cross product, right-hand rule, atomic orbital,
  crystal structure, rigid body rotation, magnetic field 3D, EM wave 3D.
---

# 3D 物理 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块（如角度 θ / 时间 t / 速度 v）驱动实时
  重算的物理量，以及"定值指示"（守恒定律）。
- **中栏**：KaTeX 分步解析，可一键收起。
- **右栏**：Three.js 3D 交互画板（球体/矢量箭头/轨迹曲线 + 网格坐标轴 + 可旋转/缩放/平移
  OrbitControls），叠加视角控制按钮。

## 依赖
- **Three.js r128**（通过 CDN 加载，无本地依赖）
- **OrbitControls**（通过 CDN 加载）
- **KaTeX**（通过 CDN 加载）
- **无 sympy 依赖**（物理量用 scalars 表达式在前端计算）

## 工作流程

### 第 1 步：确定题目规约
明确：
- **物理场景**：洛伦兹力、叉积/右手定则、原子轨道、晶体结构等需要 3D 展示的内容
- **可变参数**：角度 θ、时间 t、速度 v 等
- **物理规律**：F=qv×B、右手定则、轨道形状参数等
- **交互范式**：滑块控制参数变化，3D 箭头/球体/轨迹实时响应
- **语言**：输出语言跟随提示词语言（中文/英文）

### 第 2 步：设计 3D 物理系统
这是最关键的一步。选取合适的坐标系和相机视角。

**坐标放置技巧**：
- 原点放在物理系统中心（如电荷位置、晶格原点）
- 相机初始位置选在能清晰展示三维关系的方向
- 网格地面辅助观察空间方位
- 坐标轴用红/绿/蓝标注 x/y/z 方向

**3D 对象构造模式**：

| 场景 | 对象类型 | 说明 |
|------|---------|------|
| 洛伦兹力 | 3 个箭头（v/B/F 矢量） | 从同一点出发，展示右手定则 |
| 原子轨道 | 球体（原子核）+ 曲线（轨道形状） | 用参数曲线绘制轨道轮廓 |
| 晶体结构 | 球体（原子）+ 圆柱（键） | 排列在晶格位置上 |
| 刚体旋转 | 球体/长方体 + 旋转轴箭头 | 显示角动量方向 |

**验证物理正确性**（心算检查）：
- 叉积方向：θ=0° 时 F=0，θ=90° 时 F=qvB，方向用右手定则验证
- 轨道形状：参数方程是否正确
- 守恒量：是否恒为定值（如能量守恒）

### 第 3 步：组装数据并注入模板

> 📍 **输出位置 & 唯一产物**：交付给用户的**只有一个 `.html`**，写到**当前工作目录
> （`Path.cwd()`）**。cwd 里不要留任何别的文件——构建脚本（`.py`）、`__pycache__`、截图等
> 临时文件一律放 `/tmp` 或用完即删。也绝不要写进技能自身目录。

**数据格式**（三段式 JSON，schema 见 `template/board3d.html` 数据岛 `__LESSON_DATA__`）：

```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "页面标题",
    "problem": "<p>题面 HTML，公式用 $…$ / $$…$$</p>",
    "answer": "$F = q(v\\times B)$"
  },
  "steps": [
    { "title": "步骤一", "content": "<p>解析内容...</p>" },
  ],
  "board3d": {
    "view": {
      "cameraPos": [5, 4, 8],         // 相机初始位置
      "target": [0, 0, 0],            // 注视点
      "showGrid": true,
      "showAxes": true
    },
    "param": {
      "name": "theta",
      "label": "轨道角 $\\theta$ (°)",
      "min": 0, "max": 360,
      "step": 1, "value": 0, "unit": "°"
    },
    "scalars": [
      { "name": "r", "expr": "2" },                         // 轨道半径
      { "name": "rad", "expr": "theta*PI/180" },            // 角度转弧度
      { "name": "px", "expr": "r*cos(rad)" },               // 粒子位置 x
      { "name": "py", "expr": "0" },                        // 粒子位置 y（在 xz 平面圆周运动）
      { "name": "pz", "expr": "r*sin(rad)" },               // 粒子位置 z
      { "name": "vx", "expr": "-r*sin(rad)" },              // 速度 x（切向）
      { "name": "vy", "expr": "0" },
      { "name": "vz", "expr": "r*cos(rad)" },               // 速度 z
      { "name": "vmag", "expr": "sqrt(vx*vx+vy*vy+vz*vz)" },// 速率（恒定）
      { "name": "B", "expr": "3" },                         // 磁场强度（沿 y 轴）
      { "name": "q", "expr": "1" },                         // 电荷
      { "name": "F", "expr": "q*vmag*B" }                   // 洛伦兹力大小（恒定）
    ],
    "objects": [
      {
        "id": "charge",
        "type": "sphere",
        "position": ["px", "py", "pz"],   // 表达式坐标：随滑块移动
        "radius": 0.3,
        "color": "#f87171",
        "label": "电荷 q"
      },
      {
        "id": "v_arrow",
        "type": "arrow",
        "from": ["px", "py", "pz"],
        "to": ["px+vx*0.4", "py+vy*0.4", "pz+vz*0.4"],   // 速度方向箭头
        "color": "#60a5fa",
        "headLength": 0.3,
        "headWidth": 0.15
      },
      {
        "id": "B_arrow",
        "type": "arrow",
        "from": [0, -2.5, 0],
        "to": [0, 2.5, 0],                // 磁场方向（沿 y 轴，固定）
        "color": "#34d399",
        "headLength": 0.3,
        "headWidth": 0.15
      },
      {
        "id": "orbit",
        "type": "curve",
        // 圆轨道：用 theta 作曲线参数（注意 curve 的 expr 用的是同一套 scalars 环境，
        // 这里直接用 cos/sin 画半径 r 的圆）
        "expr": { "x": "r*cos(theta*PI/180)", "y": "0", "z": "r*sin(theta*PI/180)" },
        "tMin": 0, "tMax": 360,
        "segments": 120,
        "color": "#c084fc"
      }
    ],
    "readouts": [
      { "id": "v", "label": "速率 $|v|$", "type": "expr", "expr": "vmag", "digits": 2 },
      { "id": "B", "label": "磁场 $B$", "type": "expr", "expr": "B", "digits": 1 },
      { "id": "F", "label": "洛伦兹力 $F=qvB$", "type": "expr", "expr": "F", "digits": 2, "highlight": true }
    ],
    "constant": { "of": "F", "label": "$F = qvB \\equiv \\text{常数}$" },
    "legend": [
      { "color": "#f87171", "text": "电荷" },
      { "color": "#60a5fa", "text": "$\\vec{v}$" },
      { "color": "#34d399", "text": "$\\vec{B}$" },
      { "color": "#c084fc", "text": "轨道" }
    ]
  }
}
```

> 注：上面示例**所有表达式变量（r/rad/px/vx/vmag/B/q/F 等）都在 `scalars` 里定义**，
> `constant.of:"F"` 也指向 readouts 里真实存在的 id `F`。这样照抄即可跑通，
> 不会出现曲线消失、箭头消失、守恒横幅不显示的问题。

**构建脚本方法**（Python，推荐）：

```python
#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True

SKILL_DIR = Path(".claude/skills/edu-physics-3d")
TEMPLATE = SKILL_DIR / "template" / "board3d.html"
PLACEHOLDER = "__LESSON_DATA__"

data = {
    "lesson": { ... },
    "steps": [ ... ],
    "board3d": { ... }
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

### 第 4 步：自检与交付
- **物理正确性**：验证箭头方向正确（叉积方向、右手定则）、数值正确
- **浏览器预览**：起本地静态服务，检查：
  - Three.js 场景正常加载（无 WebGL 报错）
  - OrbitControls 可旋转/缩放/平移
  - 滑块拖动时 3D 对象实时更新
  - Trace 轨迹线正确
  - readouts 和 constant 正确显示
- **关闭端口**：预览结束立即停掉本地服务
- **清理**：删除 `/tmp` 中的临时脚本，确认 cwd 只有 `.html`

## 数据格式参考（核心字段）

### board3d 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `view` | `{cameraPos, target, showGrid, showAxes}` | 3D 视角配置 |
| `param` | `{name, min, max, step, value, label, unit, ticks}` | 滑块定义 |
| `scalars` | `[{name, expr}]` | 由 param 派生的物理量 |
| `objects` | 对象数组 | sphere / arrow / curve |
| `trace` | `{of, samples, color}` | 轨迹采样 |
| `readouts` | `[{id, label, type, expr, ...}]` | 实时物理量数值 |
| `constant` | `{of, label}` | 守恒定律指示器 |
| `legend` | `[{color, text}]` | 图例 |

### 3D 对象类型

| type | 字段 | 说明 |
|------|------|------|
| `sphere` | `position:[x,y,z], radius, color` | 球体（质点/原子核） |
| `arrow` | `from:[x,y,z], to:[x,y,z], color, headLength, headWidth` | 矢量箭头 |
| `curve` | `expr:{x,y,z}, tMin, tMax, segments, color` | 参数曲线（轨迹/轨道） |

位置/半径等坐标值支持表达式字符串，引擎每帧用当前 scalars 环境求值。

### 表达式引擎
支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2 exp log pow min max sign floor ceil hypot PI`
三角函数使用弧度（角度需转换：`theta*PI/180`）。
参数名须是合法 JS 标识符（如 `t`/`theta`/`v0`，不用 `θ`）。

### trace 轨迹系统
在 `board3d` 中配置 `trace: { of: [x_expr, y_expr, z_expr], color: "locus" }` 后，
引擎在 param 的 `[min, max]` 区间均匀采样 160 步，绘制三维轨迹曲线。
适用于带电粒子在磁场中的螺旋轨迹、空间运动路径等。

## 什么时候用 edu-physics-3d（而不是 edu-physics）

edu-physics（2D）和 edu-physics-3d 的分工：

| 场景 | 使用 skill | 原因 |
|------|-----------|------|
| 抛体运动、简谐振动、波 | edu-physics | 2D 完全够用 |
| 洛伦兹力 `F=qv×B` | **edu-physics-3d** | 叉积方向垂直于平面，必须 3D |
| 右手定则可视化 | **edu-physics-3d** | 力的方向垂直于 v 和 B 平面 |
| 原子轨道形状 | **edu-physics-3d** | s/p/d 轨道是三维空间分布 |
| 晶体结构/晶格 | **edu-physics-3d** | 三维空间排列 |
| 刚体旋转/角动量 | **edu-physics-3d** | 旋转轴在三维空间 |
| 电磁波 E/B 正交 | **edu-physics-3d** | 两场在三维空间正交传播 |
| 磁场（螺线管） | **edu-physics-3d** | 场线在三维空间分布 |

## 目录
- `template/board3d.html` — Three.js 渲染模板（自包含单页 HTML）
- `references/conventions.md` — 3D 物理构造模式、坐标约定
- `examples/` — 范例参考
