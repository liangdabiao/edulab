# 函数交互教学 — 数据格式

## board 字段总览

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `view` | `{xRange, yRange}` | 是 | 数学坐标视窗 |
| `param` | `{name, min, max, step, value, label, ticks}` | 推荐 | 滑块定义 |
| `scalars` | `[{name, expr}]` | 否 | 派生常量 |
| `functions` | `[{name, expr, color, label, samples, lineWidth, dashed}]` | 否 | 函数定义 |
| `points` | `{name: [x,y] \| {xy,color,label,emphasis,hidden}}` | 否 | 顶点坐标 |
| `derived` | `[{type, ...}]` | 否 | 构造序列 |
| `readouts` | `[{id, label, type, ...}]` | 否 | 读数列表 |
| `constant` | `{of, label}` | 否 | 定值指示器 |
| `trace` | `{of, color}` | 否 | 轨迹 |
| `legend` | `[{color, text}]` | 否 | 图例 |

## view

```jsonc
{ "xRange": [-4, 4], "yRange": [-2, 10] }
```

始终显示网格和坐标轴（函数绘图风格）。

## param

```jsonc
{
  "name": "a",            // 合法 JS 标识符
  "label": "$a$",         // 显示标签（KaTeX）
  "min": 0.5, "max": 3,   // 范围
  "step": 0.1,            // 步长
  "value": 1.5,           // 默认值
  "standard": 1,          // 重置值（可选，默认同 value）
  "ticks": ["0.5","1","1.5","2","2.5","3"]  // 刻度标签
}
```

## scalars

由 param 值派生的常量序列，后者可引用前者：

```jsonc
[
  { "name": "b", "expr": "2" },
  { "name": "c", "expr": "1" },
  { "name": "vx", "expr": "-b/(2*a)" }
]
```

## functions

函数定义（顶层数组）：

```jsonc
[
  {
    "name": "f",                     // 函数名，被 derived/readouts 引用
    "expr": "a*x^2 + b*x + c",       // 表达式（x 为自变量）
    "color": "curve",                // 曲线颜色
    "label": "$y=ax^2+bx+c$",        // 图例标签
    "samples": 400,                  // 采样点数（可选，默认 400）
    "lineWidth": 3,                  // 线条宽度（可选）
    "dashed": false                  // 虚线（可选）
  }
]
```

## points

```jsonc
{
  "A": [1, 0],                       // 简单坐标
  "V": { "xy": ["vx", "vy"],         // 表达式坐标
    "color": "ptA",                  // 颜色
    "label": "V",                    // 标签（false 隐藏）
    "emphasis": true,                // 大点
    "hidden": false                  // 隐藏
  }
}
```

## derived

### 函数类型

**point_on_function**: 在曲线上取点
```jsonc
{ "type": "point_on_function", "name": "P", "function": "f", "x": 1.5,
  "color": "ptB", "label": "P" }
```
- `x` 可以是数字、表达式字符串，或 `"@param"`（当前滑块值）

**tangent_at_function**: 切线
```jsonc
{ "type": "tangent_at_function", "name": "T", "function": "f",
  "point": "P", "derivative": "2*a*x + b", "color": "tangent", "dashed": true }
```
- `point` 引用已有点（如 point_on_function 创建的点）
- `derivative` 是导数表达式（用户需提供）

**area_under_curve**: 曲线下面积
```jsonc
{ "type": "area_under_curve", "name": "S", "function": "f",
  "xRange": [0, "@param"], "baseline": 0, "color": "area" }
```
- `baseline` 默认为 0（x 轴）
- `xRange` 支持 `"@param"` 占位符

**area_between_curves**: 两曲线间面积
```jsonc
{ "type": "area_between_curves", "name": "S2",
  "function": "f", "function2": "g",
  "xRange": [0, 3.14], "color": "area" }
```

### 几何类型（保留自 board.html）

**segment**: 
```jsonc
{ "type": "segment", "a": "A", "b": "P", "color": "aux", "dashed": true }
```

**polygon**:
```jsonc
{ "type": "polygon", "pts": ["A","B","C"], "color": "rgba(...)", "stroke": "#ccc" }
```

**vector**:
```jsonc
{ "type": "vector", "from": "A", "to": "P", "color": "vec", "label": "$\\vec{v}$" }
```

**line_through_points**:
```jsonc
{ "type": "line_through_points", "name": "L", "a": "A", "b": "B", "color": "line" }
```

**line_through_slope**:
```jsonc
{ "type": "line_through_slope", "name": "L", "point": "A", "slope": 2, "color": "line" }
```

**midpoint**:
```jsonc
{ "type": "midpoint", "name": "M", "a": "A", "b": "B", "color": "point", "emphasis": true }
```

**foot_perp**:
```jsonc
{ "type": "foot_perp", "name": "D", "point": "C", "line": "L", "color": "point" }
```

## readouts

### 函数类型

**function_at**: 
```jsonc
{ "id": "fv", "label": "$f(1.5)$", "type": "function_at", "function": "f",
  "x": 1.5, "digits": 2, "color": "#3b82f6" }
```

**derivative_at**:
```jsonc
{ "id": "dv", "label": "$f'(1.5)$", "type": "derivative_at",
  "derivative": "2*a*x + b", "x": 1.5, "digits": 2 }
```

**area_value**:
```jsonc
{ "id": "av", "label": "面积", "type": "area_value", "function": "f",
  "xRange": [0, "@param"], "baseline": 0, "digits": 3 }
```

### 几何类型

**expr**:
```jsonc
{ "id": "ex", "label": "$a+b$", "type": "expr", "expr": "a+b",
  "digits": 2, "highlight": true }
```

**coord**:
```jsonc
{ "id": "cr", "label": "P 坐标", "type": "coord", "of": "P" }
```

**distance**:
```jsonc
{ "id": "dist", "label": "AB", "type": "distance", "a": "A", "b": "B" }
```

## constant

```jsonc
{ "of": "disc", "label": "$\\Delta \\equiv b^2-4ac$" }
```

## 颜色语义名

| 名 | hex | 用途 |
|----|-----|------|
| `curve` | `#f59e0b` | 函数曲线主色 |
| `curve2` | `#ec4899` | 函数曲线第二色 |
| `curve3` | `#06b6d4` | 函数曲线第三色 |
| `curve4` | `#8b5cf6` | 函数曲线第四色 |
| `tangent` | `#10b981` | 切线 |
| `line` | `#2dd4bf` | 直线 |
| `aux` | `#94a3b8` | 辅助线 |
| `ptA` | `#ef4444` | 点 A（红） |
| `ptB` | `#3b82f6` | 点 B（蓝） |
| `point` | `#1e293b` | 普通点 |
| `given` | `#a78bfa` | 已知点 |
| `fixed` | `#34d399` | 定点 |
| `vecA` | `#ef4444` | 矢量 A |
| `vecB` | `#3b82f6` | 矢量 B |
| `vec` | `#f59e0b` | 矢量 |
| `locus` | `#06b6d4` | 轨迹 |
| `area` | `rgba(45,212,191,0.15)` | 面积着色 |

## 自检清单

- [ ] functions 表达式语法正确（用 `^` 表示乘方）
- [ ] 滑块在全部范围内函数定义有效（不出现 NaN）
- [ ] 切线导数表达式与函数一致
- [ ] 面积区间合理，数值积分精度可接受
- [ ] 画板 viewport 完整显示函数关键特征
- [ ] constant 指示器验证的恒等式确实恒定
- [ ] 图例颜色与实际曲线颜色一致
