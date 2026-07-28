# 函数交互教学 — 绘图约定与构造模式

## 核心理念

**函数绘图应始终显示网格和坐标轴**（与纯平面几何不同）。保留解析风格，让学生直观看到
函数曲线在坐标系中的位置和变化。

## 坐标方案

- 始终显示网格（浅灰色）和坐标轴（深灰色带箭头）
- viewport 留 10-15% 边距
- x 轴和 y 轴刻度标签在后续版本中按需添加

## 函数定义

```jsonc
"functions": [
  { "name": "f", "expr": "a*x^2 + b*x + c", "color": "curve", "label": "$y=ax^2+bx+c$" }
]
```

- `expr` 中使用 `x` 作为自变量
- 支持多函数叠加显示（最多 4 条曲线用 curve-curve4）
- 函数标签自动追加到图例

## 函数采样

- 默认 400 个采样点（可通过 `samples` 覆盖）
- 断点检测：相邻点 y 差 > 10·dx 时断开（处理 tan/1/x 等间断点）
- 超出 viewport 范围的点自动跳过（保持连线整洁）

## 切线

切线通过 `tangent_at_function` derived 类型实现，用户需提供导数表达式：

```jsonc
{ "type": "tangent_at_function", "name": "T", "function": "f",
  "point": "P", "derivative": "2*a*x + b", "color": "tangent" }
```

- 引擎在 x₀ 处计算 f(x₀) 和 f'(x₀)，构造点斜式直线
- 直线自动裁剪到 viewport 范围
- 导数表达式必须与函数表达式一致

## 面积着色

面积区域在函数曲线**之前**绘制，所以曲线在最上层不被遮挡。

### area_under_curve：曲线与基线间的区域

```jsonc
{ "type": "area_under_curve", "function": "f",
  "xRange": [0, "@param"], "baseline": 0, "color": "area" }
```

- `baseline` 默认为 0（x 轴）
- 使用 `"@param"` 让区间端点跟随滑块

### area_between_curves：两曲线间的区域

```jsonc
{ "type": "area_between_curves", "function": "f", "function2": "g",
  "xRange": [0, 3.14], "color": "area" }
```

## @param 占位符

在以下场景支持 `"@param"` 自动替换为当前滑块值：
- `point_on_function.x`
- `area_under_curve.xRange`
- `area_between_curves.xRange`
- `area_value.xRange`（readouts 中）

## 渲染管线

| 顺序 | 层级 | 说明 |
|------|------|------|
| 1 | Grid | 网格线（浅灰） |
| 2 | Axes | 坐标轴 + 箭头 + O/x/y 标签 |
| 3 | **Areas** | 面积着色（半透明多边形，曲线之下） |
| 4 | **Curves** | 函数曲线（最上层，不被遮挡） |
| 5 | Trace | 轨迹（虚线） |
| 6 | Segments | 线段 |
| 7 | Lines | 直线 |
| 8 | Vectors | 箭头 |
| 9 | Points | 点 + 标签（最上层） |

## 通用构造模式

### 二次函数顶点探究

```jsonc
{
  "view": { "xRange": [-4, 4], "yRange": [-2, 10] },
  "param": { "name": "a", "min": 0.5, "max": 3, "step": 0.1, "value": 1.5 },
  "scalars": [
    { "name": "b", "expr": "2" },
    { "name": "c", "expr": "1" },
    { "name": "vx", "expr": "-b/(2*a)" },
    { "name": "vy", "expr": "(4*a*c - b*b)/(4*a)" }
  ],
  "functions": [
    { "name": "f", "expr": "a*x^2 + b*x + c", "color": "curve" }
  ],
  "points": {
    "V": { "xy": ["vx", "vy"], "color": "ptA", "emphasis": true }
  },
  "derived": [
    { "type": "point_on_function", "name": "P", "function": "f", "x": 1.5, "color": "ptB" },
    { "type": "tangent_at_function", "name": "T", "function": "f", "point": "P",
      "derivative": "2*a*x + b", "dashed": true }
  ],
  "readouts": [
    { "id": "fv", "label": "$f(1.5)$", "type": "function_at", "function": "f", "x": 1.5 },
    { "id": "disc", "label": "$\\Delta$", "type": "expr", "expr": "b*b-4*a*c", "highlight": true }
  ]
}
```

### 三角函数探究

```jsonc
{
  "view": { "xRange": [0, 6.28], "yRange": [-1.5, 1.5] },
  "param": { "name": "A", "min": 0.5, "max": 2, "step": 0.1, "value": 1 },
  "functions": [
    { "name": "f", "expr": "A*sin(x)", "color": "curve", "label": "$y=A\\sin x$" }
  ],
  "derived": [
    { "type": "point_on_function", "name": "P", "function": "f", "x": "@param", "color": "ptA" }
  ]
}
```

## 常见问题

### 函数不显示
- 确认 `functions` 数组中的 `expr` 包含 `x` 作为自变量
- 检查 viewport 范围是否覆盖函数的有意义区域
- 检查函数在 viewport 内是否有定义（如 log(x) 要求 x>0）

### 切线方向错误
- 确认导数表达式与函数表达式一致
- 例：f(x) = a*x²+b*x+c → 导数应为 2*a*x+b

### 面积显示 NaN
- 检查 xRange 端点是否有效（xMin < xMax）
- 检查函数在区间内是否处处有定义

## 自检清单

- [ ] 函数表达式语法正确，所有采样点值正常
- [ ] 切线导数表达式与函数匹配，方向正确
- [ ] 面积着色范围有效，数值积分值与理论值一致
- [ ] 滑块全程函数不退化（无 NaN、无无效区间）
- [ ] 画板 viewport 完整显示函数曲线
- [ ] 图例颜色与曲线颜色一致
- [ ] 浏览器无控制台报错
- [ ] KaTeX 公式全部正常渲染
