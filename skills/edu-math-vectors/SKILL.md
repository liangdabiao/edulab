# 二维向量 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块（如角度 θ / 长度比）驱动实时
  重算的向量量（模长、点积、夹角、分量…），以及"恒等式指示"。
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板。
- **右栏**：2D Canvas 动态向量画板（矢量箭头 + 平行四边形 + 分量投影 + 向量链 + 网格坐标轴），
  叠加画笔涂鸦工具栏。

## 依赖
**无外部依赖**。模板引擎 `template/board-vector.html` 是自包含的单页 HTML。
只要能用 Python 3（标准库即可）做字符串替换就行，或者直接用 JSON 手动注入。

## 工作流程

### 第 1 步：确定题目规约
明确：
- **向量场景**：向量加法/减法、平行四边形法则、点积与夹角、向量分解、向量链
- **可变参数**：角度 θ、向量长度、分量值，确定范围与步长
- **要展示的向量量**：模长、点积、夹角、分量坐标、和向量等
- **语言**：输出语言跟随提示词语言（中文/英文）

### 第 2 步：设计向量系统
选取方便的坐标系，写出各向量分量的参数化表达式。

**坐标放置技巧**：
- 向量起点通常放在原点 O(0,0)
- 固定一个向量，让另一个向量随滑块变化（角度或长度）
- 分量投影线绘制到坐标轴

**常见构造模式**：

| 场景 | 坐标方案 | scalars 序列 |
|------|---------|-------------|
| 向量加法（a 固定，b 旋转） | a=(ax,ay) 固定，b 由角度驱动 | bx=b_len·cosθ, by=b_len·sinθ, sx=ax+bx, sy=ay+by |
| 向量链求和 | 各向量依次首尾相接 | 多个向量分量 scalars |
| 点积探究 | a 固定，b 角度变化 | dot=ax·bx+ay·by, angle=acos(dot/(|a|·|b|)) |

**验证向量正确性**（心算检查）：
- 特殊角度：θ=0°、90°、180° 时分量的正负
- 点积：0° 时 = |a||b|，90° 时 = 0，180° 时 = -|a||b|
- 平行四边形：对边平行且相等
- 向量链：最后一链的终点应等于各分量之和

**viewport 范围**：留 10-15% 边距，确保完整向量图形在画板可见。

### 第 3 步：组装数据并注入模板

> 📍 **输出位置 & 唯一产物**：交付给用户的**只有一个 `.html`**，写到**当前工作目录
> （`Path.cwd()`）**。cwd 里不要留任何别的文件——构建脚本（`.py`）、`__pycache__`、截图等
> 临时文件一律放 `/tmp` 或用完即删。也绝不要写进技能自身目录。

**数据格式**（三段式 JSON，schema 见 `template/board-vector.html` 数据岛 `__LESSON_DATA__`）：

```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "页面标题",
    "problem": "<p>题面 HTML，公式用 $…$ / $$…$$</p>",
    "answer": "$|\\mathbf{a}| = \\sqrt{5} \\approx 2.236$"
  },
  "steps": [
    { "title": "步骤一", "content": "<p>解析内容...</p>" }
  ],
  "board": {
    "view": { "xRange": [-2, 7], "yRange": [-2, 6] },
    "param": {
      "name": "theta",
      "label": "$\\theta$",
      "min": 0, "max": 360, "step": 5, "value": 45,
      "ticks": ["0", "90", "180", "270", "360"]
    },
    "scalars": [
      { "name": "bx", "expr": "3*cos(theta*PI/180)" },
      { "name": "by", "expr": "3*sin(theta*PI/180)" }
    ],
    "points": {
      "O": [0, 0],
      "B_end": ["bx", "by"]
    },
    "derived": [
      { "type": "vector", "name": "vb", "from": "O", "to": "B_end", "color": "vecB", "label": "$\\mathbf{b}$" },
      { "type": "parallelogram", "vectors": ["va", "vb"], "color": "area", "stroke": "#94a3b8" },
      { "type": "vector_components", "of": "B_end", "colorX": "vecCompX", "colorY": "vecCompY" },
      { "type": "vector_chain", "vectors": ["va", "vb"], "color": "vec", "label": "$\\mathbf{a}+\\mathbf{b}$" }
    ],
    "readouts": [
      { "id": "dotv", "label": "$\\mathbf{a}\\cdot\\mathbf{b}$", "type": "dot", "a": "va", "b": "vb", "highlight": true },
      { "id": "ang", "label": "$\\angle(\\mathbf{a},\\mathbf{b})$", "type": "angle_between", "a": "va", "b": "vb" }
    ],
    "constant": { "of": "ma", "label": "$|\\mathbf{a}| \\equiv \\text{定值}$" },
    "legend": [
      { "color": "vecA", "text": "$\\mathbf{a}$" },
      { "color": "vecB", "text": "$\\mathbf{b}$" }
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

SKILL_DIR = Path(".claude/skills/edu-math-vectors")
TEMPLATE = SKILL_DIR / "template" / "board-vector.html"
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

> 注：如果运行时提示路径不对，请使用绝对路径或从 `Path(__file__)` 推导。

### 第 4 步：自检与交付
- **向量正确性**：验证特殊角度下的分量正负、点积正负、夹角正确
- **浏览器预览**：起本地静态服务，检查无控制台报错、KaTeX 正常、滑块交互流畅
  - 滑块拖动时向量方向正确旋转
  - 平行四边形随向量变化重绘（填充区域正确）
  - 分量投影线随向量端点移动
  - 向量链首尾相接
  - constant 指示器全程恒定显示
- **关闭端口**：预览结束立即停掉本地服务
- **清理**：删除 `/tmp` 中的临时脚本，确认 cwd 只有 `.html`

## 数据格式参考（核心字段）

### board 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `view` | `{xRange, yRange}` | 数学坐标视窗（含网格坐标轴） |
| `param` | `{name, min, max, step, value, label, ticks}` | 滑块定义 |
| `scalars` | `[{name, expr}]` | 由 param 派生的命名常量 |
| `points` | `{name: [x,y] 或 {xy,color,label}}` | 定点坐标或构造点 |
| `derived` | 构造序列 | 15 种类型（11 保留 + 4 向量新增） |
| `readouts` | `[{id, label, type, ...}]` | 实时数值（5 保留 + 1 新增） |
| `constant` | `{of, label}` | 定值指示器 |
| `legend` | `[{color, text}]` | 图例 |

### derived 构造类型（15 种）

**4 种向量新增**：

| type | 字段 | 说明 |
|------|------|------|
| `vector_sum` | `name, to, from(可选), color, label` | 从起点到分量和终点画向量（创建点 + 箭头） |
| `parallelogram` | `vectors: [名称1, 名称2], color, stroke` | 两向量构成平行四边形填充 |
| `vector_components` | `of(点), colorX, colorY` | 从点到 x/y 轴的虚线投影 |
| `vector_chain` | `vectors: [名称1, 名称2, ...], color, label, from(可选)` | 向量首尾相接链 |

**11 种保留**：

| type | 字段 | 说明 |
|------|------|------|
| `vector` | `from, to, color, label` | 矢量箭头 |
| `segment` | `a, b, color, dashed, label` | 线段 |
| `polygon` | `pts, color, stroke` | 多边形 |
| `line_through_angle` | `name, point, angle, color, dashed` | 过一点给定角度直线 |
| `line_through_slope` | `name, point, slope, color, dashed` | 过一点给定斜率直线 |
| `line_through_points` | `name, a, b, color, dashed` | 过两点直线 |
| `intersect_line_line` | `name, a, b, color, label` | 两直线交点 |
| `midpoint` | `name, a, b, color, label, emphasis` | 中点 |
| `foot_perp` | `name, point, line, color, label` | 垂足 |
| `reflect` | `name, point, line, color, label` | 关于直线对称点 |
| `point_reflect` | `name, of, center, color, emphasis` | 关于中心对称点 |

### readouts 类型（6 种）

**1 种向量新增**：

| type | 字段 | 说明 |
|------|------|------|
| `angle_between` | `a, b` (向量名) | 两向量夹角（度） |

**5 种保留**：

| type | 字段 | 说明 |
|------|------|------|
| `expr` | `expr, digits` | 表达式求值 |
| `coord` | `of` (点) | 坐标 |
| `distance` | `a,b` (点) | 两点距离 |
| `length` | `of` (向量名) 或 `a,b` (点) | 向量模长或线段长度 |
| `dot` | `a, b` (向量名) | 两向量点积 |

### 颜色语义名
`curve`(金黄) · `line`(青) · `aux`(灰) ·
`ptA`(红) · `ptB`(蓝) · `point`(深灰) · `given`(紫) · `fixed`(翠绿) ·
`vecA`(红) · `vecB`(蓝) · `vec`(金黄) · `vecSum`(翠绿) ·
`vecCompX`(红) · `vecCompY`(蓝) · `locus`(青) ·
`area`(青半透明)。
也可直接写 hex：`#f87171` 或 `rgba(45,212,191,0.15)`。

### 表达式引擎
坐标值/`scalars` 中的 `expr` 支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2 exp log pow min max sign floor ceil hypot PI`
三角函数使用**弧度**（角度需先转换：`theta*PI/180`）。
参数名须是合法 JS 标识符（如 `theta`/`len`/`ax`，不能用 `θ` 等非标识符）。

### 向量渲染机制
- 向量用箭头绘制（带三角形箭头的线段）
- 箭头大小固定（10px），不随缩放变化
- 平行四边形通过两向量的起点和终点计算第四个顶点后填充多边形
- 分量投影用虚线从向量终点画到坐标轴

## 目录
- `template/board-vector.html` — 数据驱动模板（向量渲染器 + 参数引擎 + 数据岛）
- `references/problem-schema.md` — 数据格式文档
- `references/conventions.md` — 向量绘图约定
- `examples/` — 范例参考
