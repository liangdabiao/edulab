# 统计交互教学 — 数据格式

## board 字段总览

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `view` | `{xRange, yRange}` | 是 | 数学坐标视窗 |
| `param` | `{name, min, max, step, value, label, ticks}` | 推荐 | 滑块定义 |
| `scalars` | `[{name, expr}]` | 否 | 派生常量 |
| `datasets` | `[{name, values, color, label}]` | 否 | 静态数据数组 |
| `functions` | `[{name, expr, color, label}]` | 否 | 函数定义（PDF 等） |
| `points` | `{name: [x,y]}` | 否 | 顶点坐标 |
| `derived` | `[{type, ...}]` | 否 | 构造序列 |
| `readouts` | `[{id, label, type, ...}]` | 否 | 读数列表 |
| `constant` | `{of, label}` | 否 | 定值指示器 |
| `legend` | `[{color, text}]` | 否 | 图例 |

## datasets

```jsonc
[
  {
    "name": "sample",          // 数据集名，被 derived/readouts 引用
    "values": [0.1, -0.3, 0.5, 1.2, -0.8, 0.0],  // 数值数组
    "color": "bar",            // 颜色（可选）
    "label": "采样数据"         // 标签（可选）
  }
]
```

## derived 新增类型

### histogram

```jsonc
{
  "type": "histogram",
  "dataset": "sample",      // 数据集名
  "bins": 15,               // 分组数
  "xRange": [-4, 4],        // x 轴范围（可选，默认数据集 min~max）
  "color": "bar",           // 填充色
  "stroke": "barStroke"     // 边框色
}
```

### box_plot

```jsonc
{
  "type": "box_plot",
  "dataset": "sample",      // 数据集名
  "at": -3.5,               // x 位置
  "width": 0.5,             // 箱体宽度
  "color": "box",           // 线条色
  "fill": "boxFill"         // 填充色
}
```

### scatter

```jsonc
{
  "type": "scatter",
  "datasetX": "dataX",          // x 数据集
  "datasetY": "dataY",          // y 数据集
  "color": "scatter",           // 点颜色
  "regression": true,           // 显示回归线（默认 true）
  "regressionColor": "regression"  // 回归线颜色
}
```

## readouts 新增类型

### mean / median / stddev

```jsonc
{ "id": "mu", "label": "$\\bar{x}$", "type": "mean", "dataset": "sample", "digits": 3 }
{ "id": "md", "label": "中位数", "type": "median", "dataset": "sample" }
{ "id": "sd", "label": "$\\sigma$", "type": "stddev", "dataset": "sample" }
```

### percentile

```jsonc
{ "id": "p90", "label": "第 90 百分位", "type": "percentile", "dataset": "sample", "p": 90 }
```

### probability

```jsonc
{
  "id": "prob68", "label": "概率",
  "type": "probability", "function": "norm",
  "xRange": ["-sigma", "sigma"], "digits": 4
}
```

### combinatorics

```jsonc
{ "id": "c", "label": "$C_n^r$", "type": "combinatorics", "kind": "nCr", "n": 10, "r": 3 }
{ "id": "p", "label": "$P_n^r$", "type": "combinatorics", "kind": "nPr", "n": 10, "r": 3 }
{ "id": "f", "label": "$n!$", "type": "combinatorics", "kind": "factorial", "n": 5 }
```

## 颜色语义名（stats 新增）

| 名 | hex | 用途 |
|----|-----|------|
| `bar` | `rgba(99,102,241,0.6)` | 直方图填充 |
| `barStroke` | `#6366f1` | 直方图边框 |
| `box` | `#f59e0b` | 箱线图线条 |
| `boxFill` | `rgba(245,158,11,0.2)` | 箱线图填充 |
| `scatter` | `#6366f1` | 散点图 |
| `regression` | `#ef4444` | 回归线 |

## 表达式引擎

同 edu-math-function：支持 `+ - * / ^ sqrt sin cos ...`。三角函数使用弧度。
