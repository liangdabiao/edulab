---
name: edu-math-stats
description: >-
  把一道概率统计题做成交互教学网页：左栏题面 + 动态控制台（一个可变参数滑块如标准差 σ / 样本量 n /
  区间端点 驱动实时重算的统计量：均值、标准差、概率、百分位…），中栏 KaTeX 分步解析，右栏 2D Canvas
  动态统计画板（函数曲线 + 直方图 + 箱线图 + 散点图 + 网格坐标轴），叠加画笔涂鸦。无外部依赖，
  模板自包含，只需 Python 3 标准库做字符串替换注入数据。覆盖正态分布、指数/均匀分布、直方图、
  箱线图、散点图与回归、组合数（nCr/nPr/阶乘）等。形态与 edu-math-function / edu-math-vectors
  平行，但面向概率统计。其他 agent 也可调用本技能生成此类网页。
  触发词：概率, 统计, 正态分布, 高斯分布, 标准差, 均值, 中位数, 百分位, 直方图, 箱线图,
  散点图, 回归, 组合数, 排列数, 阶乘, 概率密度, 解这道统计题; probability, statistics,
  normal distribution, Gaussian, standard deviation, mean, median, percentile, histogram,
  box plot, scatter plot, regression, combinatorics, permutation, factorial, PDF.
---

# 概率统计 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块驱动实时重算的统计量（均值、标准差、概率、百分位…）
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板。
- **右栏**：2D Canvas 动态统计画板（函数曲线 + 直方图 + 箱线图 + 散点图 + 网格坐标轴），叠加画笔涂鸦工具栏。

## 依赖
**无外部依赖**。模板引擎 `template/board-stats.html` 是自包含的单页 HTML。

## 工作流程

### 第 1 步：确定题目规约
明确：
- **统计场景**：正态分布、直方图、箱线图、散点图与回归、组合数计算
- **可变参数**：标准差 σ、样本量 n、区间端点等
- **可视元素**：PDF 曲线、直方图条形、箱线图箱体+须、散点+回归线
- **语言**：输出语言跟随提示词语言

### 第 2 步：设计数据系统

**数据集定义**：在 `board.datasets` 中声明静态数据数组。

**常用统计分布**（用 functions 表达）：

| 分布 | 表达式 |
|------|--------|
| 正态 PDF | `1/(sigma*sqrt(2*PI))*exp(-(x-mu)^2/(2*sigma^2))` |
| 指数 PDF | `lambda*exp(-lambda*x)` |
| 均匀 PDF | `1/(b-a)`（在 [a,b] 内） |

### 第 3 步：组装数据并注入模板

**数据格式**示例：

```jsonc
{
  "board": {
    "view": { "xRange": [-4, 4], "yRange": [-0.05, 0.85] },
    "param": { "name": "sigma", "label": "$\\sigma$", "min": 0.5, "max": 2.5, "step": 0.1, "value": 1.0 },
    "datasets": [
      { "name": "sample", "values": [0.1, -0.3, 0.5, ...] }
    ],
    "functions": [
      { "name": "norm", "expr": "1/(sigma*sqrt(2*PI))*exp(-(x)^2/(2*sigma^2))", "color": "curve" }
    ],
    "derived": [
      { "type": "area_under_curve", "function": "norm", "xRange": ["-sigma", "sigma"], "color": "area" },
      { "type": "histogram", "dataset": "sample", "bins": 15, "xRange": [-4, 4] },
      { "type": "box_plot", "dataset": "sample", "at": -3.5, "width": 0.5 }
    ],
    "readouts": [
      { "id": "prob", "label": "概率", "type": "probability", "function": "norm", "xRange": ["-sigma", "sigma"], "highlight": true },
      { "id": "mu", "label": "均值", "type": "mean", "dataset": "sample" },
      { "id": "s", "label": "标准差", "type": "stddev", "dataset": "sample" }
    ]
  }
}
```

构建方法与其他 edu-math-* skill 相同：Python 写字符串替换。

### 第 4 步：自检与交付
- 函数曲线与直方图/箱线图在同一坐标系正确叠加
- 滑块拖动时概率值 ≈ 68.27%
- 均值/中位数/标准差计算正确
- 直方图 bin 计数正确，箱线图箱体+须位置正确

## 数据格式参考

### board 新字段：datasets

```jsonc
"datasets": [
  { "name": "data1", "values": [1.2, -0.5, 0.3, ...], "color": "bar", "label": "数据集" }
]
```

### derived 新增类型

| type | 字段 | 说明 |
|------|------|------|
| `histogram` | `dataset, bins, xRange, color, stroke` | 直方图条形 |
| `box_plot` | `dataset, at, width, color, fill` | 箱线图 |
| `scatter` | `datasetX, datasetY, color, regression` | 散点图（可选回归线） |

### readouts 新增类型

| type | 字段 | 说明 |
|------|------|------|
| `mean` | `dataset, digits` | 数据集均值 |
| `median` | `dataset, digits` | 中位数 |
| `stddev` | `dataset, digits` | 标准差 |
| `percentile` | `dataset, p, digits` | p 百分位数 |
| `probability` | `function, xRange, digits` | 概率密度曲线下面积 |
| `combinatorics` | `kind, n, r, digits` | 组合数 nCr / 排列数 nPr / 阶乘 |

### 颜色语义名（新增）

| 名 | hex | 用途 |
|----|-----|------|
| `bar` | `rgba(99,102,241,0.6)` | 直方图填充 |
| `barStroke` | `#6366f1` | 直方图边框 |
| `box` | `#f59e0b` | 箱线图 |
| `boxFill` | `rgba(245,158,11,0.2)` | 箱线图填充 |
| `scatter` | `#6366f1` | 散点 |
| `regression` | `#ef4444` | 回归线 |

## 目录
- `template/board-stats.html` — 数据驱动模板（统计渲染器）
- `references/problem-schema.md` — 数据格式文档
- `references/conventions.md` — 统计绘图约定
