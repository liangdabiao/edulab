# 函数图像 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 一个可变参数滑块（如系数 a / 频率 ω / 相位 φ）驱动实时
  重算的函数值、导数值、定积分面积等，以及"恒等式指示"。
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板。
- **右栏**：2D Canvas 动态函数图像画板（函数曲线 + 切线 + 区域着色 + 动点 + 网格坐标轴），
  叠加画笔涂鸦工具栏。

## 依赖
**无外部依赖**。模板引擎 `template/board-function.html` 是自包含的单页 HTML。
只要能用 Python 3（标准库即可）做字符串替换就行，或者直接用 JSON 手动注入。

## 工作流程

### 第 1 步：确定题目规约
明确：
- **函数类型**：一次/二次/指数/对数/三角/分段函数等
- **可变参数**：系数 a、频率 ω、相位 φ 等，确定范围与步长
- **要展示的数学量**：函数值、导数值、定积分、顶点、极值点、零点等
- **交互范式**：参数调参 → 曲线变化 → 面积/切线实时更新
- **语言**：输出语言跟随提示词语言（中文/英文）

### 第 2 步：设计函数系统
这是最关键的一步。选取合适的数学表达式，确定参数与坐标范围。

**坐标放置技巧**：
- 二次函数以对称轴居中放置
- 三角函数取一个完整周期
- 指数/对数函数考虑渐近线位置
- 确保 viewport 显示关键特征（顶点、零点、渐近线）

**常见构造模式**：

| 场景 | 函数 | scalars 序列 |
|------|------|-------------|
| 二次函数 y=a·x²+b·x+c | f(x) = a·x²+b·x+c | vx=-b/(2a), disc=b²-4ac |
| 三角函数 y=A·sin(ωx+φ) | f(x) = A·sin(ωx+φ) | period=2π/ω |
| 指数函数 y=a·e^{kx} | f(x) = a·e^{k·x} | y0=a (x=0) |
| 对数函数 y=log_a(x) | f(x) = log(x)/log(a) | x>0 注意定义域 |

**验证数学正确性**（心算检查）：
- 特殊点：x=0 时的函数值
- 对称性：偶函数 f(-x)=f(x)，奇函数 f(-x)=-f(x)
- 定积分：用已知积分公式核对数值结果
- 导数：用基本求导公式验证切线斜率

**viewport 范围**：留 10-15% 边距，确保关键特征在画板内完整可见。

### 第 3 步：组装数据并注入模板

> 📍 **输出位置 & 唯一产物**：交付给用户的**只有一个 `.html`**，写到**当前工作目录
> （`Path.cwd()`）**。cwd 里不要留任何别的文件——构建脚本（`.py`）、`__pycache__`、截图等
> 临时文件一律放 `/tmp` 或用完即删。也绝不要写进技能自身目录。

**数据格式**（三段式 JSON，schema 见 `template/board-function.html` 数据岛 `__LESSON_DATA__`）：

```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "页面标题",
    "problem": "<p>题面 HTML，公式用 $…$ / $$…$$</p>",
    "answer": "$\\Delta = b^2-4ac \\equiv 1$"
  },
  "steps": [ ... ],
  "board": {
    "view": { "xRange": [-4, 4], "yRange": [-2, 10] },
    "param": {
      "name": "a",
      "label": "$a$",
      "min": 0.5, "max": 3, "step": 0.1, "value": 1.5,
      "ticks": ["0.5", "1", "1.5", "2", "2.5", "3"]
    },
    "scalars": [
      { "name": "b", "expr": "2" },
      { "name": "c", "expr": "1" }
    ],
    // 函数定义（顶层数组）
    "functions": [
      { "name": "f", "expr": "a*x^2 + b*x + c", "color": "curve", "label": "$y=ax^2+bx+c$" },
      { "name": "g", "expr": "sin(x)", "color": "curve2", "label": "$y=\\sin x$" }
    ],
    "points": {
      "V": { "xy": ["vx", "vy"], "color": "ptA", "label": "V", "emphasis": true }
    },
    "derived": [
      // 函数相关构造
      { "type": "point_on_function", "name": "P", "function": "f", "x": 1.5, "color": "ptB" },
      { "type": "tangent_at_function", "name": "T", "function": "f", "point": "P",
        "derivative": "2*a*x + b", "color": "tangent", "dashed": true },
      { "type": "area_under_curve", "name": "S", "function": "f",
        "xRange": [0, "@param"], "baseline": 0, "color": "area" },
      { "type": "area_between_curves", "name": "S2", "function": "f", "function2": "g",
        "xRange": [0, 3.14], "color": "area" },
      // 保留的几何类型
      { "type": "segment", "a": "A", "b": "P", "color": "aux" },
      { "type": "line_through_points", "name": "L", "a": "A", "b": "P", "color": "line" }
    ],
    "readouts": [
      // 函数读数
      { "id": "fv", "label": "$f(1.5)$", "type": "function_at", "function": "f", "x": 1.5 },
      { "id": "dv", "label": "$f'(1.5)$", "type": "derivative_at", "function": "f", "derivative": "2*a*x+b" },
      { "id": "av", "label": "面积", "type": "area_value", "function": "f", "xRange": [0, "@param"] },
      // 保留类型
      { "id": "disc", "label": "$\\Delta$", "type": "expr", "expr": "disc", "highlight": true }
    ],
    "constant": { "of": "disc", "label": "$\\Delta \\equiv b^2-4ac$" },
    "legend": [ ... ]
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

SKILL_DIR = Path(".claude/skills/edu-math-function")
TEMPLATE = SKILL_DIR / "template" / "board-function.html"
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

> 注：如果运行时提示 `template/board-function.html` 路径不对，请使用绝对路径或从 `Path(__file__)` 推导。

### 第 4 步：自检与交付
- **数值正确性**：验证特殊点函数值、导数值、定积分值符合解析计算
- **浏览器预览**：起本地静态服务，无控制台报错、KaTeX 正常、滑块交互流畅
  - 滑块拖动时曲线实时重绘
  - 切线方向/斜率随参数正确变化
  - 面积着色随区间调整
  - constant 指示器全程恒定显示
- **清理**：删除 `/tmp` 中的临时脚本，确认 cwd 只有 `.html`

## 数据格式参考（核心字段）

### board 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `view` | `{xRange, yRange}` | 数学坐标视窗（含网格坐标轴） |
| `functions` | `[{name, expr, color, label}]` | **函数定义数组（新增）** |
| `points` | `{name: [x,y] 或 {xy,color,label}}` | 定点坐标或构造点 |
| `param` | `{name, min, max, step, value, label, ticks}` | 滑块定义 |
| `scalars` | `[{name, expr}]` | 由 param 派生的命名常量 |
| `derived` | 构造序列 | 11 种类型（7 保留 + 4 新增） |
| `readouts` | `[{id, label, type, ...}]` | 实时数值（3 新增 + 3 保留） |
| `constant` | `{of, label}` | 定值指示器 |
| `legend` | `[{color, text}]` | 图例（自动追加函数标签） |

### derived 构造类型（11 种）

**4 种函数新增**：

| type | 字段 | 说明 |
|------|------|------|
| `point_on_function` | `name, function, x, color, label` | 在函数曲线上取点（x 可表达式） |
| `tangent_at_function` | `name, function, point, derivative, color, dashed` | 过曲线上某点的切线，需提供导数表达式 |
| `area_under_curve` | `name, function, xRange, baseline, color` | 曲线与基线间的区域着色 |
| `area_between_curves` | `name, function, function2, xRange, color` | 两曲线间的区域着色 |

**7 种保留**：

| type | 字段 | 说明 |
|------|------|------|
| `segment` | `a, b, color, dashed` | 线段 |
| `polygon` | `pts, color, stroke` | 多边形 |
| `vector` | `from, to, color, label` | 矢量 |
| `line_through_points` | `name, a, b, color, dashed` | 过两点直线 |
| `line_through_slope` | `name, point, slope, color, dashed` | 过一点斜率直线 |
| `midpoint` | `name, a, b, color, label, emphasis` | 中点 |
| `foot_perp` | `name, point, line, color, label` | 垂足 |

### readouts 类型（6 种）

**3 种函数新增**：

| type | 字段 | 说明 |
|------|------|------|
| `function_at` | `function, x, digits` | 函数在 x 处的值 |
| `derivative_at` | `derivative, x, digits` | 导数在 x 处的值 |
| `area_value` | `function, xRange, baseline, digits` | 定积分数值 |

**3 种保留**：

| type | 字段 | 说明 |
|------|------|------|
| `expr` | `expr, digits` | 表达式求值 |
| `coord` | `of` (点) | 坐标 |
| `distance` | `a,b` (点) | 两点距离 |

### xRange 中使用 `@param`

在 `area_under_curve`, `area_between_curves`, `area_value` 的 `xRange` 字段中，
可以使用 `"@param"` 作为占位符，自动替换为当前滑块值。

### 颜色语义名
`curve`(金黄) · `curve2`(粉红) · `curve3`(青) · `curve4`(紫) ·
`tangent`(翠绿) · `line`(青) · `aux`(灰) ·
`ptA`(红) · `ptB`(蓝) · `point`(深灰) · `given`(紫) · `fixed`(翠绿) ·
`vecA`(红) · `vecB`(蓝) · `vec`(金黄) · `locus`(青) ·
`area`(青半透明)。
也可直接写 hex：`#f87171` 或 `rgba(45,212,191,0.15)`。

### 表达式引擎
坐标值/`scalars`/`functions.expr` 中的 `expr` 支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2 exp log pow min max sign floor ceil hypot PI`
三角函数使用**弧度**（角度需先转换：`theta*PI/180`）。
表达式中的自变量为 **`x`**（由采样引擎注入）。
参数名须是合法 JS 标识符（如 `a`/`b`/`omega`/`phi`）。

### 函数采样机制
在 `view.xRange` 内均匀采样 N=400 点，对每个点将 `x` 注入 env 后调用 `evalExpr`。
断点检测：相邻采样点 y 差 > 10·dx 则断开折线（处理 tan(x)/1/x 等间断点）。
可通过 `functions[].samples` 覆盖采样数。

### 切线机制
用户需提供导数表达式（如 `2*a*x+b`），引擎在 x₀ 处计算 f(x₀) 和 f'(x₀)，
构造点斜式直线并裁剪到 viewport 范围内绘制。

### 面积着色
在指定区间采样曲线上的点 + 基线点 → 构建多边形 → 半透明填充。
使用梯形法数值积分计算面积值。

## 目录
- `template/board-function.html` — 数据驱动模板（函数绘图器 + 参数引擎 + 数据岛）
- `references/problem-schema.md` — 数据格式文档
- `references/conventions.md` — 函数绘图约定
- `examples/` — 范例参考
