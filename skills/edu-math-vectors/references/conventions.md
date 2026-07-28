# 向量交互教学 — 绘图约定与构造模式

## 核心理念
向量绘图应始终显示网格和坐标轴，保留解析风格。向量起点通常在原点，分量投影线帮助理解向量坐标。

## 坐标方案
- 始终显示网格（浅灰色）和坐标轴（深灰色带箭头）
- viewport 留 10-15% 边距
- 原点 O 应位于画板内或边界附近

## 渲染管线

| 顺序 | 层级 | 说明 |
|------|------|------|
| 1 | Grid | 网格线（浅灰） |
| 2 | Axes | 坐标轴 + 箭头 + O/x/y 标签 |
| 3 | Polygons | 平行四边形填充 |
| 4 | Trace | 轨迹（虚线） |
| 5 | Segments | 线段/分量投影 |
| 6 | Lines | 直线 |
| 7 | Vectors | 矢量箭头（最显眼层） |
| 8 | Points | 点 + 标签（最上层） |

## 向量构造模式

### 向量加法（平行四边形法则）

```jsonc
{
  "view": { "xRange": [-2, 7], "yRange": [-2, 6] },
  "param": { "name": "theta", "label": "$\\theta$", "min": 0, "max": 360, "step": 5, "value": 45 },
  "scalars": [
    { "name": "ax", "expr": "2" }, { "name": "ay", "expr": "1" },
    { "name": "bx", "expr": "3*cos(theta*PI/180)" },
    { "name": "by", "expr": "3*sin(theta*PI/180)" },
    { "name": "sx", "expr": "ax+bx" }, { "name": "sy", "expr": "ay+by" }
  ],
  "points": {
    "O": [0, 0], "A_end": ["ax", "ay"],
    "B_end": ["bx", "by"], "Sum": ["sx", "sy"]
  },
  "derived": [
    { "type": "vector", "name": "va", "from": "O", "to": "A_end", "color": "vecA", "label": "$\\mathbf{a}$" },
    { "type": "vector", "name": "vb", "from": "O", "to": "B_end", "color": "vecB", "label": "$\\mathbf{b}$" },
    { "type": "vector", "name": "vsum", "from": "O", "to": "Sum", "color": "vecSum", "label": "$\\mathbf{a}+\\mathbf{b}$" },
    { "type": "parallelogram", "vectors": ["va", "vb"], "color": "area", "stroke": "#94a3b8" },
    { "type": "vector_components", "of": "A_end", "colorX": "vecCompX", "colorY": "vecCompY" },
    { "type": "vector_components", "of": "B_end", "colorX": "vecCompX", "colorY": "vecCompY" },
    { "type": "segment", "a": ["ax","ay"], "b": ["sx","sy"], "color": "aux", "dashed": true },
    { "type": "segment", "a": ["bx","by"], "b": ["sx","sy"], "color": "aux", "dashed": true }
  ],
  "readouts": [
    { "id": "ma", "label": "$|\\mathbf{a}|$", "type": "expr", "expr": "mag_a", "digits": 3, "color": "vecA" },
    { "id": "dotv", "label": "$\\mathbf{a}\\cdot\\mathbf{b}$", "type": "dot", "a": "va", "b": "vb", "highlight": true },
    { "id": "ang", "label": "$\\angle(\\mathbf{a},\\mathbf{b})$", "type": "angle_between", "a": "va", "b": "vb" }
  ]
}
```

### 向量链求和

```jsonc
{
  "derived": [
    { "type": "vector", "name": "v1", "from": "O", "to": "P", "color": "vecA" },
    { "type": "vector", "name": "v2", "from": "P", "to": "Q", "color": "vecB" },
    { "type": "vector", "name": "v3", "from": "Q", "to": "R", "color": "vec" },
    { "type": "vector_chain", "vectors": ["v1", "v2", "v3"], "color": "vecSum", "label": "$\\sum\\mathbf{v}$" }
  ]
}
```

### 向量分量分解

```jsonc
{
  "derived": [
    { "type": "vector", "name": "v", "from": "O", "to": "Pt", "color": "vec" },
    { "type": "vector_components", "of": "Pt", "colorX": "vecCompX", "colorY": "vecCompY" }
  ]
}
```

## 常见问题

### 向量不显示
- 确认起点和终点坐标有定义且有限（isFinite）
- 检查 viewport 范围是否覆盖向量区域

### 平行四边形显示不正确
- 确认两个向量的 `from` 为同一点
- 平行四边形算法：C = A.to + B.to - A.from

### 分量投影线不显示
- 确认引用的点存在且坐标有限
- 投影线从 (x,y) 画到 (x,0) 和 (0,y)

## 自检清单
- [ ] 所有向量坐标有定义、在 viewport 范围内
- [ ] 特殊角度（0°、90°、180°）分量/点积正确
- [ ] 平行四边形填充随向量变化重绘
- [ ] 分量投影线随向量端点移动
- [ ] 滑块全程图形不退化
- [ ] 图例颜色与向量颜色一致
- [ ] 浏览器无控制台报错
- [ ] KaTeX 公式全部正常渲染
