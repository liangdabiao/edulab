# 集合逻辑 — 数据格式

## board 字段总览

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `logicType` | `"venn"\|"truthTable"\|"logicGate"` | 是 | 渲染模式 |
| `venn` | `{sets, highlight}` | 否 | 文氏图配置 |
| `truthTable` | `{inputs, outputs}` | 否 | 真值表配置 |
| `logicGates` | `[{type, x, y, size, label, color}]` | 否 | 逻辑门排列 |
| `param` | `{name, min, max, step, value, label, ticks}` | 否 | 滑块定义 |
| `readouts` | `[{id, label, type, expr}]` | 否 | 读数 |

## venn

```jsonc
{
  "sets": [
    { "label": "A", "elements": ["1", "2", "3"] },   // 集合名与元素
    { "label": "B", "elements": ["3", "4", "5"] }
  ],
  "highlight": "interAB"     // 交集高亮（颜色名或 hex）
}
```

## truthTable

```jsonc
{
  "inputs": [
    { "name": "p", "label": "p" },    // name 用于表达式，label 用于表头
    { "name": "q", "label": "q" }
  ],
  "outputs": [
    { "name": "conj", "label": "p∧q", "expr": "p ∧ q" },
    { "name": "disj", "label": "p∨q", "expr": "p ∨ q" },
    { "name": "xor",  "label": "p⊕q", "expr": "p ⊕ q" },
    { "name": "impl", "label": "p→q", "expr": "p → q" },
    { "name": "bic",  "label": "p↔q", "expr": "p ↔ q" }
  ]
}
```

### 逻辑运算符

| 符号 | 引擎替换 | 含义 |
|------|----------|------|
| `∧` | `&&` | 合取 |
| `∨` | `\|\|` | 析取 |
| `¬` | `!` | 否定 |
| `⊕` | `!==` | 异或 |
| `→` | `<=` | 蕴含 |
| `↔` | `===` | 双条件 |

## logicGates

```jsonc
[
  {
    "type": "AND",      // AND | OR | NOT | NAND | NOR | XOR
    "x": 50,            // Canvas x 坐标
    "y": 60,            // Canvas y 坐标
    "size": 35,         // 门大小
    "label": "AND",     // 显示标签
    "color": "gate"     // 可选颜色（默认 gate）
  }
]
```

## param

```jsonc
{
  "name": "t",          // 参数名，用于 readouts expr
  "label": "参数 t",    // 显示标签
  "min": 0,             // 最小值
  "max": 10,            // 最大值
  "step": 1,            // 步长
  "value": 3,           // 初始值
  "ticks": ["0", "5", "10"]  // 刻度标签
}
```

## readouts

```jsonc
{ "id": "r1", "label": "当前值", "type": "expr", "expr": "t", "digits": 2 }
```

仅支持 `type: "expr"` 类型，使用与 board.html 兼容的表达式引擎。

## 表达式引擎

支持：`+ - * / ^ sqrt abs sin cos tan asin acos atan exp log PI`
参数名须是合法 JS 标识符。

## 颜色语义

| 名 | hex | 用途 |
|----|-----|------|
| `setA` | `#ef4444` | 集合 A 圆圈 |
| `setB` | `#3b82f6` | 集合 B 圆圈 |
| `setC` | `#10b981` | 集合 C 圆圈 |
| `interAB` | `rgba(139,92,246,0.15)` | AB 交集填充 |
| `interABC` | `rgba(236,72,153,0.15)` | ABC 交集填充 |
| `gate` | `#1e293b` | 逻辑门线条 |
| `wire` | `#64748b` | 连线 |
| `highlight` | `#f59e0b` | 高亮 |
