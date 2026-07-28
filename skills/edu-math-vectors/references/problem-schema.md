# 向量交互教学 — 数据格式

## board 字段总览

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `view` | `{xRange, yRange}` | 是 | 数学坐标视窗 |
| `param` | `{name, min, max, step, value, label, ticks}` | 推荐 | 滑块定义 |
| `scalars` | `[{name, expr}]` | 否 | 派生常量 |
| `points` | `{name: [x,y] \| {xy,color,label,emphasis,hidden}}` | 否 | 顶点坐标 |
| `derived` | `[{type, ...}]` | 否 | 构造序列（15 种） |
| `readouts` | `[{id, label, type, ...}]` | 否 | 读数列表（6 种） |
| `constant` | `{of, label}` | 否 | 定值指示器 |
| `legend` | `[{color, text}]` | 否 | 图例 |

## view

```jsonc
{ "xRange": [-2, 7], "yRange": [-2, 6] }
```

始终显示网格和坐标轴。

## param

```jsonc
{
  "name": "theta",          // 合法 JS 标识符
  "label": "$\\theta$",     // 显示标签（KaTeX）
  "min": 0, "max": 360,     // 范围
  "step": 5,                // 步长
  "value": 45,              // 默认值
  "standard": 45,           // 重置值（可选，默认同 value）
  "ticks": ["0","90","180","270","360"]  // 刻度标签
}
```

## scalars

由 param 值派生的常量序列：

```jsonc
[
  { "name": "ax", "expr": "2" },
  { "name": "ay", "expr": "1" },
  { "name": "bx", "expr": "3*cos(theta*PI/180)" },
  { "name": "by", "expr": "3*sin(theta*PI/180)" }
]
```

## points

```jsonc
{
  "O": [0, 0],
  "A_end": ["ax", "ay"],
  "B_end": { "xy": ["bx", "by"], "color": "ptB", "label": "B", "emphasis": true }
}
```

## derived

### 向量类型

**vector**: 矢量箭头
```jsonc
{ "type": "vector", "name": "va", "from": "O", "to": "A_end", "color": "vecA", "label": "$\\mathbf{a}$" }
```

**vector_sum**: 从原点向分量和画箭头
```jsonc
{ "type": "vector_sum", "name": "vsum", "to": ["ax+bx", "ay+by"], "color": "vecSum", "label": "$\\mathbf{a}+\\mathbf{b}$" }
```
- `to` 为 `[dx, dy]` 数组（表达式字符串），起点默认为原点
- 自动创建点并画箭头

**parallelogram**: 平行四边形填充
```jsonc
{ "type": "parallelogram", "vectors": ["va", "vb"], "color": "area", "stroke": "#94a3b8" }
```
- `vectors` 引用已创建的 `vector` 型 derived 名称
- 算法：O=两向量公共起点，A/B=各自终点，C=A+B-O

**vector_components**: 分量投影虚线
```jsonc
{ "type": "vector_components", "of": "B_end", "colorX": "vecCompX", "colorY": "vecCompY" }
```
- `of` 引用已有点名
- 从点 (x,y) 到 (x,0) 画 x 方向虚线，到 (0,y) 画 y 方向虚线

**vector_chain**: 向量链（首尾相接）
```jsonc
{ "type": "vector_chain", "vectors": ["va", "vb", "vc"], "color": "vec", "label": "$\\mathbf{a}+\\mathbf{b}+\\mathbf{c}$" }
```
- 每个向量的终点成为下一个的起点
- 只给最后一个向量加 label

### 几何类型（保留自 board.html）

**segment**: 
```jsonc
{ "type": "segment", "a": "A", "b": "P", "color": "aux", "dashed": true, "label": "边" }
```

**polygon**:
```jsonc
{ "type": "polygon", "pts": ["A","B","C"], "color": "rgba(...)", "stroke": "#ccc" }
```

**line_through_angle**:
```jsonc
{ "type": "line_through_angle", "name": "L", "point": "A", "angle": 45, "color": "line" }
```

**line_through_slope**:
```jsonc
{ "type": "line_through_slope", "name": "L", "point": "A", "slope": 2, "color": "line" }
```

**line_through_points**:
```jsonc
{ "type": "line_through_points", "name": "L", "a": "A", "b": "B", "color": "line" }
```

**intersect_line_line**:
```jsonc
{ "type": "intersect_line_line", "name": "Q", "a": "L1", "b": "L2", "color": "point" }
```

**midpoint**:
```jsonc
{ "type": "midpoint", "name": "M", "a": "A", "b": "B", "color": "point", "emphasis": true }
```

**foot_perp**:
```jsonc
{ "type": "foot_perp", "name": "D", "point": "C", "line": "L", "color": "point" }
```

**reflect**:
```jsonc
{ "type": "reflect", "name": "A1", "point": "A", "line": "L", "color": "point" }
```

**point_reflect**:
```jsonc
{ "type": "point_reflect", "name": "A1", "of": "A", "center": "O", "color": "point" }
```

## readouts

### 向量类型

**angle_between**: 两向量夹角
```jsonc
{ "id": "ang", "label": "$\\angle(\\mathbf{a},\\mathbf{b})$", "type": "angle_between", "a": "va", "b": "vb" }
```
- 返回值单位：度（°）
- 使用 arccos 计算，结果范围 [0°, 180°]

### 几何类型

**expr**:
```jsonc
{ "id": "ex", "label": "$|\\mathbf{a}|$", "type": "expr", "expr": "mag_a", "digits": 2, "highlight": true, "color": "vecA" }
```

**coord**:
```jsonc
{ "id": "cr", "label": "P 坐标", "type": "coord", "of": "P" }
```

**distance**:
```jsonc
{ "id": "dist", "label": "AB", "type": "distance", "a": "A", "b": "B" }
```

**length**:
```jsonc
{ "id": "la", "label": "$|\\mathbf{a}|$", "type": "length", "of": "va" }
```

**dot**:
```jsonc
{ "id": "dotv", "label": "$\\mathbf{a}\\cdot\\mathbf{b}$", "type": "dot", "a": "va", "b": "vb" }
```

## constant

```jsonc
{ "of": "ma", "label": "$|\\mathbf{a}| = \\sqrt{5} \\equiv \\text{定值}$" }
```

## 颜色语义名

| 名 | hex | 用途 |
|----|-----|------|
| `vecA` | `#ef4444` | 向量 A（红） |
| `vecB` | `#3b82f6` | 向量 B（蓝） |
| `vec` | `#f59e0b` | 向量（金黄） |
| `vecSum` | `#10b981` | 和向量（翠绿） |
| `vecCompX` | `#ef4444` | x 分量投影（红） |
| `vecCompY` | `#3b82f6` | y 分量投影（蓝） |
| `ptA` | `#ef4444` | 点 A（红） |
| `ptB` | `#3b82f6` | 点 B（蓝） |
| `point` | `#1e293b` | 普通点 |
| `given` | `#a78bfa` | 已知点 |
| `fixed` | `#34d399` | 定点 |
| `curve` | `#f59e0b` | 曲线 |
| `line` | `#2dd4bf` | 直线 |
| `aux` | `#94a3b8` | 辅助线 |
| `locus` | `#06b6d4` | 轨迹 |
| `area` | `rgba(45,212,191,0.15)` | 面积/平行四边形填充 |

## 表达式引擎

支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2 exp log pow min max sign floor ceil hypot PI`

三角函数使用**弧度**。角度需先转换：`theta*PI/180`。

参数名须是合法 JS 标识符（如 `theta`/`len`/`ax`，不能用 `θ`）。
