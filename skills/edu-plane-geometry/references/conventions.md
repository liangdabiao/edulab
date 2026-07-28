# 平面几何交互教学 — 几何构造约定与标注模式

## 核心理念

**纯平面几何（Euclidean geometry）不应显示坐标轴和网格**。画板为浅色背景，还原课本纯几何风格。与 edu-analytic-geometry 区分：无圆锥曲线、无解析坐标轴。

## 坐标方案（内部坐标，不显示）

虽然画板不显示坐标轴和网格，但内部仍然使用数学坐标系进行定位。选取方便的坐标系：

- 直角顶点放在原点 (0,0)，两直角边沿坐标轴
- 对称图形利用对称性减少变量数
- 固定 `a+b` 为常量使图形高度不变
- 确保滑块在全部范围内几何结构有效（不退化）

## 几何构造语法

点支持几何构造语法（对象语法）替代直接坐标：

```jsonc
"points": {
  // 传统坐标语法（仍然支持）
  "A": [0, 0],
  "B": ["a", 0],
  // 对象语法（带 xy 的静态点）
  "C": { "xy": [0, "b"], "color": "given", "label": "C", "emphasis": true },
  // 几何构造语法（推荐用于动态点）
  "D": { "type": "midpoint", "a": "A", "b": "B" },
  "E": { "type": "foot", "from": "C", "to": ["A", "B"] },
  "F": { "type": "intersection", "l1": ["A", "B"], "l2": ["C", "D"] },
  "G": { "type": "on_ray", "from": "A", "dir": "B", "distance": "t" },
  "H": { "type": "on_circle", "center": "A", "radius": "c", "angle": 45 },
  "I": { "type": "rotate", "point": "C", "center": "A", "angle": 90 },
  "J": { "type": "reflect", "point": "C", "line": ["A", "B"] }
}
```

### 构造类型参考

| type | 字段 | 说明 |
|------|------|------|
| `midpoint` | `a, b` | AB 的中点 |
| `foot` | `from, to: [p1,p2]` | 从点 to 线的垂足 |
| `intersection` | `l1: [p1,p2], l2: [p1,p2]` | 两线交点 |
| `on_ray` | `from, dir, distance` | 射线上一点（from→dir方向，给定距离） |
| `on_circle` | `center, radius, angle` | 圆上一点（角度°） |
| `rotate` | `point, center, angle` | 绕中心旋转（°） |
| `reflect` | `point, line: [p1,p2]` | 关于直线反射 |

## 标注系统

独立于 derived 的 `annotations` 数组，用于纯几何标注：

```jsonc
"annotations": [
  { "type": "right_angle", "vertex": "C", "arms": ["A", "B"] },
  { "type": "tick", "segment": ["A", "B"], "count": 1 },
  { "type": "tick", "segment": ["B", "C"], "count": 2 },
  { "type": "parallel_mark", "segment": ["A", "B"], "count": 1 },
  { "type": "angle_arc", "vertex": "A", "arms": ["B", "C"], "label": "$\\theta$" }
]
```

### 标注类型参考

| type | 字段 | 说明 |
|------|------|------|
| `right_angle` | `vertex, arms: [p1,p2]` | 直角记号 ∟ |
| `tick` | `segment: [p1,p2], count` | 等长标记 \|\|（count 条数） |
| `parallel_mark` | `segment: [p1,p2], count` | 平行标记 ►（count 条数） |
| `angle_arc` | `vertex, arms: [p1,p2], label?, radius?` | 角弧标注（可选标签和半径） |

## board 关键字段

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

## derived 常用 type

| type | 字段 | 效果 |
|------|------|------|
| `polygon` | `pts, color, stroke` | 半透明填充多边形 |
| `segment` | `a, b, color, dashed` | 线段 |
| `midpoint` | `name, a, b` | 构造中点 |
| `foot_perp` | `name, point, line` | 构造垂足 |
| `line_through_points` | `name, a, b` | 过两点的直线 |
| `vector` | `from, to, color, label` | 矢量箭头 |

## readouts 几何类型

| type | 字段 | 显示内容 |
|------|------|---------|
| `expr` | `expr, digits` | 任意表达式求值 |
| `angle` | `vertex, arms: [p,q]` | 角度值（度） |
| `ratio` | `a,b, c,d` | 线段 AB 与 CD 长度之比 |
| `area` | `pts: [p,q,r,...]` | 多边形面积 |
| `area_triangle` | `pts:[p,q,r]` | 三角形面积（旧格式，仍支持） |
| `distance` | `a,b` (点) | 两点距离 |
| `coord` | `of` (点) | 坐标 |

## 颜色方案

建议使用半透明填充区分几何区域：

```python
# 三色方案
color_a = "rgba(248,113,113,0.25)"   # 红色半透明
color_b = "rgba(96,165,250,0.25)"    # 蓝色半透明
color_c = "rgba(52,211,153,0.25)"    # 绿色半透明
```

语义色板名（也可直接写 hex）：
`curve`(金黄) · `line`(青) · `aux`(灰) · `ptA`(红) · `ptB`(蓝) · `point`(浅灰) ·
`given`(紫) · `fixed`(翠绿) · `vecA`(红) · `vecB`(蓝) · `locus`(轨迹蓝) ·
`area`(青半透明)

## 表达式引擎

坐标值/`scalars` 中的 `expr` 支持：`+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2
exp log pow min max sign floor ceil hypot PI`

三角函数使用**弧度**（角度需先转换：`theta*PI/180`）。
参数名须是合法 JS 标识符（如 `t`/`k`/`a`/`ratio`，不能用 `θ` 等非标识符）。

## param 使用技巧

| 要点 | 说明 |
|------|------|
| **参数命名** | 用合法 JS 标识符：`t` / `k` / `a` / `ratio` |
| **派生量** | 用 `scalars` 数组按序定义，后者可引用前者 |
| **固定和** | `a+b=S` 固定时，`a` 为 param，`b=S-a` 在 scalars 计算 |
| **角度单位** | 三角函数用弧度，角度需转换：`theta*PI/180` |

## 渲染管线（影响构造选择）

| 顺序 | 层级 | 说明 |
|------|------|------|
| 1 | Grid | 网格（默认关闭） |
| 2 | Axes | 坐标轴（默认关闭） |
| 3 | Conics | 圆锥曲线 |
| 4 | Trace | 轨迹曲线 |
| 5 | **Polygons** | 多边形填充 → `fill()`，然后 `stroke` 可选 |
| 6 | **Annotations** | 直角记号/等长标记/角弧 |
| 7 | **Segments** | 独立线段（画在 annotations 之上） |
| 8 | Lines | 无限延伸的直线 |
| 9 | Vectors | 箭头 |
| 10 | Points | 点 + 标签（最上层） |

**关键规则**：Segments 画在 Polygons 和 Annotations 之上。因此：
- 多边形共享边时，用 `stroke` 而非独立 `segment`，避免双层线条
- 独立 `segment` 只用于不与任何多边形边重合的辅助线
- 等长标记（tick）画在 segment 之下，segment 会覆盖它——如需 tick 可见，不要在有 tick 的边上额外画 segment

## 绘制原则

### 多边形共享边的处理（常见错误）

当多个三角形共享边时（如加菲尔德证明中 RS 和 RT），有两种方式勾勒边界：

| 方式 | 实现 | 效果 |
|------|------|------|
| ❌ 多边形 fill + 独立 segment | `polygon` (无stroke) + `segment` | segment 覆盖在 fill 之上，共享边线条重叠，视觉杂乱 |
| ✅ 多边形 fill + stroke | `polygon` (带stroke) | 每个多边形自行描边，共享边自然重合，干净整洁 |

**结论**：多个多边形共享边时，**只使用 `polygon` 的 `stroke` 属性**，不要添加独立的 `segment`。独立线段只用于辅助线（如延长线、虚线高线）。

### 标注最小化

标注（等长标记/平行标记/直角记号）会增加视觉噪音。原则：
- **直角记号**：证明中关键的直角才标注，通常不超过 3 个
- **等长标记**：只在需要强调等量关系时使用，且优先选最少的 count
- **角弧**：只标注与证明直接相关的角

## 自检清单

- [ ] 画板为浅色底、无坐标轴网格（纯几何风格）
- [ ] 各点坐标/构造正确（边长、角度、面积与预期一致）
- [ ] 滑块在全部范围内几何图形有效（无翻折、无 NaN）
- [ ] **多边形共享边时使用 `stroke` 而非独立 `segment`（无双层线条）**
- [ ] 直角记号、等长标记、角弧标注位置正确，不过度标注
- [ ] 定值指示器显示的恒等式正确
- [ ] 读数的数值精度合理
- [ ] 浏览器无控制台报错
- [ ] KaTeX 公式全部正常渲染
- [ ] 图例颜色与实际着色一致
