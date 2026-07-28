# 统计交互教学 — 绘图约定

## 核心理念
统计绘图应始终显示网格和坐标轴。支持函数曲线（PDF）、直方图条形、箱线图和散点图在同一坐标系叠加显示。

## 渲染管线

| 顺序 | 层级 | 说明 |
|------|------|------|
| 1 | Grid | 网格线 |
| 2 | Axes | 坐标轴 |
| 3 | Polygons | 面积着色（PDF 下区域） |
| 4 | Histogram | 直方图条形 |
| 5 | Box plot | 箱线图 |
| 6 | Curve | 函数曲线（PDF） |
| 7 | Scatter | 散点 + 回归线 |
| 8 | Lines | 直线 |
| 9 | Points | 点 + 标签 |

## 构造模式

### 正态分布探究

```jsonc
{
  "view": { "xRange": [-4, 4], "yRange": [-0.05, 0.85] },
  "param": { "name": "sigma", "min": 0.5, "max": 2.5, "step": 0.1, "value": 1 },
  "scalars": [{ "name": "mu", "expr": "0" }],
  "functions": [{
    "name": "norm", "expr": "1/(sigma*sqrt(2*PI))*exp(-(x)^2/(2*sigma^2))", "color": "curve"
  }],
  "derived": [
    { "type": "area_under_curve", "function": "norm", "xRange": ["-sigma", "sigma"], "color": "area" },
    { "type": "histogram", "dataset": "sample", "bins": 15, "xRange": [-4, 4] },
    { "type": "box_plot", "dataset": "sample", "at": -3.5, "width": 0.5 }
  ],
  "readouts": [
    { "id": "p68", "type": "probability", "function": "norm", "xRange": ["-sigma", "sigma"], "digits": 4 },
    { "id": "mn", "type": "mean", "dataset": "sample" }
  ]
}
```

## 数据集生成
数据集是静态数值数组，使用时在 Python 构建脚本中预先生成（如 Box-Muller 采样）。

## 自检清单
- [ ] 直方图 bin 范围覆盖数据集全部值
- [ ] 箱线图 Q1/Q3/中位线位置正确
- [ ] 概率数值积分精度可接受（至少 3 位小数）
- [ ] 组合数计算结果正确
- [ ] 滑块全程函数不退化（无 NaN）
