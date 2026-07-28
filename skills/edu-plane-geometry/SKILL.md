---
name: edu-plane-geometry
description: >-
  把一道平面几何定理/问题做成交互教学网页：左栏题面 + 动态控制台（滑块驱动的边长/角度/面积
  实时数值 + 定值/等式恒成立指示），中栏 KaTeX 分步解析，右栏 2D Canvas 动态几何画板
  （三角形、四边形、多边形的点/线段/填充区域 + 直角记号/等长标记/角弧标注 + 画笔涂鸦）。
  无需 sympy，画板为浅色背景、无坐标轴网格，还原课本纯几何风格。点支持几何构造语法
  （中点/垂足/交点/旋转/反射），标注系统独立声明。形态与 edu-analytic-geometry 区分，
  处理纯平面几何问题（无圆锥曲线、无解析坐标轴）。
  触发词：平面几何, 三角形, 四边形, 梯形, 勾股定理, 面积, 全等, 相似, 角度, 几何证明,
  交互教学网页; plane geometry, Euclidean geometry, triangle, quadrilateral, trapezoid,
  Pythagorean theorem, area, congruence, similarity, geometric proof, interactive geometry page.
---

# 平面几何 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块（如边长比、角度、位置参数）驱动实时
  重算的几何量（边长、面积、角度…），以及"恒等式指示"或"范围条"。
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板。
- **右栏**：浅色 2D Canvas 动态几何画板（多边形填充 + 线段 + 点标注 + 
  直角记号/等长标记/角弧），叠加画笔涂鸦工具栏。无坐标轴网格，还原课本纯几何风格。

## 依赖
**无外部依赖**。模板引擎 `template/board-geo.html` 是自包含的单页 HTML。
只要能用 Python 3（标准库即可）做字符串替换就行，或者直接用 JSON 手动注入。

## 与 edu-analytic-geometry 的区别
- edu-plane-geometry：纯平面几何，画板**无坐标轴/网格**（浅色背景），点可通过**几何构造语法**定义
- edu-analytic-geometry：解析几何，画板带坐标轴/网格，涉及圆锥曲线

## 工作流程

### 第 1 步：确定题目规约
明确：
- **几何元素**：三角形（直角/等腰/等边/一般）、四边形（梯形/平行四边形/矩形/正方形）、圆等
- **变量参数**：哪条边可变、角度范围、比例系数
- **要展示的定理/关系**：勾股定理 a²+b²=c²、面积等式、全等条件、相似比等
- **语言**：输出语言跟随提示词语言（中文/英文）

### 第 2 步：设计几何系统
选取方便的坐标系（内部仍需坐标，但画板**不显示坐标轴**/网格）。

**坐标放置技巧**：
- 直角顶点放在原点，两直角边沿坐标轴
- 对称图形利用对称性减少变量数
- 固定 `a+b` 为常量使梯形等图形高度不变
- 确保滑块在全部范围内几何结构有效（不退化）

**几何构造语法**（点支持对象语法替代坐标）：
```jsonc
"points": {
  // 传统坐标语法（仍然支持）
  "A": [0, 0],
  "B": ["a", 0],
  // 几何构造语法（推荐）
  "C": { "type": "midpoint", "a": "A", "b": "B" },
  "D": { "type": "foot", "from": "C", "to": ["A", "B"] },
  "E": { "type": "intersection", "l1": ["A", "B"], "l2": ["C", "D"] },
  "F": { "type": "on_ray", "from": "A", "dir": "B", "distance": "t" },
  "G": { "type": "reflect", "point": "C", "line": ["A", "B"] },
  "H": { "type": "rotate", "point": "C", "center": "A", "angle": 90 }
}
```

### 第 3 步：组装数据并注入模板

> 📍 **输出位置 & 唯一产物**：交付给用户的**只有一个 `.html`**，写到**当前工作目录
> （`Path.cwd()`）**。cwd 里不要留任何别的文件——构建脚本（`.py`）、`__pycache__`、截图等
> 临时文件一律放 `/tmp` 或用完即删。也绝不要写进技能自身目录。

**数据格式**（三段式 JSON，schema 见 `template/board-geo.html` 数据岛 `__LESSON_DATA__`）：

```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "页面标题",
    "problem": "<p>题面 HTML，公式用 $…$ / $$…$$</p>",
    "answer": "$a^2+b^2=c^2$"
  },
  "steps": [
    { "title": "步骤一", "content": "<p>解析内容...</p>" },
  ],
  "board": {
    "view": { "xRange": [-1, 7], "yRange": [-1, 7] },
    "points": {
      "P": [0, 0],
      "Q": ["t", 0],
      "R": [0, "S-t"]
    },
    "param": {
      "name": "t",
      "label": "边长 $a$",
      "min": 1, "max": 5, "step": 0.1,
      "value": 3, "standard": 3
    },
    "scalars": [
      { "name": "a", "expr": "t" },
      { "name": "b", "expr": "S-t" },
      { "name": "c", "expr": "sqrt(a*a+b*b)" }
    ],
    "derived": [
      { "type": "polygon", "pts": ["P", "Q", "R"],
        "color": "rgba(248,113,113,0.25)", "stroke": "#f87171" },
      { "type": "segment", "name": "PQ", "a": "P", "b": "Q", "color": "aux" },
    ],
    "annotations": [
      { "type": "right_angle", "vertex": "R", "arms": ["P", "Q"] },
      { "type": "tick", "segment": ["P", "Q"], "count": 1 },
      { "type": "angle_arc", "vertex": "P", "arms": ["Q", "R"], "label": "$\\theta$" },
    ],
    "readouts": [
      { "id": "a", "label": "边长 $a$", "type": "expr", "expr": "a" },
      { "id": "angleP", "label": "$\\angle P$", "type": "angle",
        "vertex": "P", "arms": ["Q", "R"], "digits": 1 },
      { "id": "area", "label": "面积", "type": "area_triangle",
        "pts": ["P", "Q", "R"] },
    ],
    "constant": { "of": "chk", "label": "$a^2+b^2-c^2 \\equiv 0$" },
    "legend": [
      { "color": "#f87171", "text": "△PQR" },
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

SKILL_DIR = Path(".claude/skills/edu-plane-geometry")
TEMPLATE = SKILL_DIR / "template" / "board-geo.html"
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

> 注意：模板路径改为 `board-geo.html`，非原来的 `board.html`。

### 第 4 步：自检与交付
- **数值正确性**：手动验证面积/长度值符号预期
- **几何正确性**：直角记号、等长标记、角弧标注位置正确
- **浏览器预览**：起本地静态服务，检查无控制台报错、KaTeX 正常、滑块交互流畅
- **关闭端口**：预览结束立即停掉本地服务
- **清理**：删除 `/tmp` 中的临时脚本，确认 cwd 只有 `.html`

## 数据格式参考（核心字段）

### board 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `view` | `{xRange, yRange, showGrid?, showAxes?}` | 数学坐标视窗（网格/轴默认 false） |
| `points` | `{name: [x,y] 或 {xy,...} 或 {type,...}}` | 顶点坐标或几何构造对象 |
| `param` | `{name, min, max, step, value, label, ticks}` | 滑块定义 |
| `scalars` | `[{name, expr}]` | 由 param 派生的命名常量 |
| `derived` | 构造序列 | polygon / segment / midpoint / foot_perp 等 |
| `annotations` | `[{type, ...}]` | 几何标注（直角/等长标记/角弧/平行标记） |
| `readouts` | `[{id, label, type, ...}]` | 实时数值 |
| `constant` | `{of, label}` | 定值指示器 |
| `legend` | `[{color, text}]` | 图例 |

### 点几何构造类型

| type | 字段 | 说明 |
|------|------|------|
| `midpoint` | `a, b` | AB 的中点 |
| `foot` | `from, to: [p1,p2]` | 从点 to 线的垂足 |
| `intersection` | `l1: [p1,p2], l2: [p1,p2]` | 两线交点 |
| `on_ray` | `from, dir, distance` | 射线上一点（from→dir方向，给定距离） |
| `on_circle` | `center, radius, angle` | 圆上一点（角度°） |
| `rotate` | `point, center, angle` | 绕中心旋转（°） |
| `reflect` | `point, line: [p1,p2]` | 关于直线反射 |

### 标注类型

| type | 字段 | 说明 |
|------|------|------|
| `right_angle` | `vertex, arms: [p1,p2]` | 直角记号 ∟ |
| `tick` | `segment: [p1,p2], count` | 等长标记 `\|\|`（count 条数） |
| `parallel_mark` | `segment: [p1,p2], count` | 平行标记 `►`（count 条数） |
| `angle_arc` | `vertex, arms: [p1,p2], label?, radius?` | 角弧标注（可选标签） |

### readouts 新增几何类型

| type | 字段 | 显示内容 |
|------|------|---------|
| `angle` | `vertex, arms: [p,q]` | 角度值（度） |
| `ratio` | `a,b, c,d` | 线段 AB 与 CD 长度之比 |
| `area` | `pts: [p,q,r,...]` | 多边形面积 |

其余已有类型：`expr` / `distance` / `coord` / `area_triangle` / `length` / `status`

### derived 常用 type

| type | 字段 | 效果 |
|------|------|------|
| `polygon` | `pts, color, stroke` | 半透明填充多边形 |
| `segment` | `a, b, color, dashed` | 线段 |
| `midpoint` | `name, a, b` | 中点 |
| `foot_perp` | `name, point, line` | 垂足 |
| `vector` | `from, to, color, label` | 矢量箭头 |

### 表达式引擎
坐标值/`scalars` 中的 `expr` 支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2
exp log pow min max sign floor ceil hypot PI`
三角函数使用**弧度**（角度需先转换：`theta*PI/180`）。
参数名须是合法 JS 标识符（如 `t`/`k`/`a`/`ratio`，不能用 `θ` 等非标识符）。

## 目录
- `template/board-geo.html` — 平面几何模板（浅色画板、无坐标轴、几何构造 + 标注系统）
- `template/board.html` — 通用 2D 模板（带坐标轴网格，兼容旧页面）
- `references/conventions.md` — 几何构造模式、自检清单
- `examples/` — 范例参考
