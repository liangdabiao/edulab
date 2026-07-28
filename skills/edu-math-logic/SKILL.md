# 集合逻辑 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML（三栏）：
- **左栏**：题面 + 动态控制台 —— 集合与逻辑概念的文字说明，可选参数滑块
- **中栏**：分步解析（公式用 **KaTeX**），可一键收起把空间让给画板
- **右栏**：三种逻辑可视化模式，通过按钮切换：
  - **文氏图** — 2-3 个集合的圆圈图，交集区域着色，元素标签
  - **真值表** — HTML 表格，2^n 行真值组合，表达式自动评估
  - **逻辑门** — Canvas 绘制 AND/OR/NOT/NAND/NOR/XOR 门符号

## 依赖
**无外部依赖**。模板引擎 `template/board-logic.html` 是自包含的单页 HTML。

## 工作流程

### 第 1 步：确定题目规约
明确：
- **逻辑主题**：集合关系（文氏图）/ 命题逻辑（真值表）/ 数字电路（逻辑门），或三者组合
- **可变参数**：可选滑块控制演示参数
- **集合元素**：文氏图中的元素列表
- **命题变元**：真值表的输入变量名
- **逻辑门排列**：门类型和位置
- **语言**：输出语言跟随提示词语言

### 第 2 步：选择逻辑模式

模板通过 `board.logicType` 字段切换三种渲染模式：

| 模式 | logicType | 渲染方式 | 用途 |
|------|-----------|----------|------|
| 文氏图 | `venn` | Canvas + HTML overlay | 集合关系演示 |
| 真值表 | `truthTable` | HTML table | 命题逻辑计算 |
| 逻辑门 | `logicGate` | Canvas | 门电路符号 |

可在页面内添加按钮动态切换 `BOARD.logicType`。

### 第 3 步：组装数据并注入模板

**数据格式**（三段式 JSON，数据岛 `__LESSON_DATA__`）：

```jsonc
{
  "lesson": {
    "language": "zh-CN",
    "title": "集合逻辑 · 交互教学",
    "problem": "<p>题面 HTML，公式用 $…$ / $$…$$</p>",
    "answer": "<p>答案...</p>"
  },
  "steps": [
    { "title": "步骤一", "content": "<p>解析内容...</p>" }
  ],
  "board": {
    "logicType": "venn",        // venn | truthTable | logicGate
    "consoleTitle": "逻辑控制台",
    // 文氏图配置
    "venn": {
      "sets": [
        { "label": "A", "elements": ["1", "2", "3"] },
        { "label": "B", "elements": ["3", "4", "5"] }
      ],
      "highlight": "interAB"    // 交集高亮色
    },
    // 真值表配置
    "truthTable": {
      "inputs": [
        { "name": "p", "label": "p" },
        { "name": "q", "label": "q" }
      ],
      "outputs": [
        { "name": "conj", "label": "p∧q", "expr": "p ∧ q" },
        { "name": "disj", "label": "p∨q", "expr": "p ∨ q" }
      ]
    },
    // 逻辑门配置
    "logicGates": [
      { "type": "AND", "x": 50, "y": 60, "size": 35, "label": "AND" },
      { "type": "OR",  "x": 250, "y": 60, "size": 35, "label": "OR" }
    ],
    // 可选参数
    "param": {
      "name": "t", "label": "参数 t",
      "min": 0, "max": 10, "step": 1, "value": 3,
      "ticks": ["0", "5", "10"]
    },
    "readouts": [
      { "id": "r1", "label": "读数", "type": "expr", "expr": "t" }
    ]
  }
}
```

**构建脚本方法**（Python）：

```python
#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True

SKILL_DIR = Path(".claude/skills/edu-math-logic")
TEMPLATE = SKILL_DIR / "template" / "board-logic.html"
PLACEHOLDER = "__LESSON_DATA__"

data = { "lesson": {...}, "steps": [...], "board": {...} }

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

### 第 4 步：自检与交付
- 三种模式通过 `logicType` 正确切换
- 真值表 2^n 行的 `0`/`1` 组合完备
- 逻辑门 Canvas 绘制无溢出
- 文氏图圆圈不重叠过度
- 拖动滑块时无报错
- **浏览器预览**：检查无控制台报错、KaTeX 正常
- **关闭端口**：预览结束立即停掉本地服务
- **清理**：删除临时脚本，确认 cwd 只有 `.html`

## 数据格式参考（核心字段）

### board 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `logicType` | `"venn"\|"truthTable"\|"logicGate"` | 是 | 渲染模式 |
| `venn` | `{sets, highlight}` | 否 | 文氏图配置 |
| `truthTable` | `{inputs, outputs}` | 否 | 真值表配置 |
| `logicGates` | `[{type, x, y, size, label}]` | 否 | 逻辑门排列 |
| `param` | `{name, min, max, step, value, ticks}` | 否 | 滑块 |
| `readouts` | `[{id, label, type, expr}]` | 否 | 读数 |

### venn 配置

```jsonc
{
  "sets": [
    { "label": "A", "elements": ["元素1", "元素2", ...] }
  ],
  "highlight": "interAB"   // 交集着色
}
```

支持 1-3 个集合。2 集合时左右排列，3 集合时三角形排列。

### truthTable 配置

```jsonc
{
  "inputs": [
    { "name": "p", "label": "p" }
  ],
  "outputs": [
    { "name": "conj", "label": "p∧q", "expr": "p ∧ q" }
  ]
}
```

**支持的逻辑运算符**（expr 中直接使用 Unicode 符号）：

| 符号 | 含义 | 示例 |
|------|------|------|
| `∧` | 合取 (AND) | `p ∧ q` |
| `∨` | 析取 (OR) | `p ∨ q` |
| `¬` | 否定 (NOT) | `¬p` |
| `⊕` | 异或 (XOR) | `p ⊕ q` |
| `→` | 蕴含 | `p → q` |
| `↔` | 双条件 | `p ↔ q` |

命题变元名必须是合法 JS 标识符（如 `p`/`q`/`r`，不能用特殊字符）。

### logicGates 配置

```jsonc
{
  "type": "AND",    // AND | OR | NOT | NAND | NOR | XOR
  "x": 50,          // Canvas x 坐标
  "y": 60,          // Canvas y 坐标
  "size": 35,       // 门大小
  "label": "AND",   // 显示标签
  "color": "gate"   // 可选颜色
}
```

### 颜色定义

| 名 | hex | 用途 |
|----|-----|------|
| `setA` | `#ef4444` | 集合 A |
| `setB` | `#3b82f6` | 集合 B |
| `setC` | `#10b981` | 集合 C |
| `interAB` | `rgba(139,92,246,0.15)` | AB 交集填充 |
| `interABC` | `rgba(236,72,153,0.15)` | ABC 交集填充 |
| `gate` | `#1e293b` | 逻辑门线条 |
| `wire` | `#64748b` | 连线 |
| `highlight` | `#f59e0b` | 高亮 |

也可直接写 hex：`#f87171` 或 `rgba(248,113,113,0.25)`。

## 目录
- `template/board-logic.html` — 三种逻辑模式渲染模板
- `references/problem-schema.md` — 数据格式文档
- `references/conventions.md` — 逻辑可视化约定
- `examples/` — 范例参考
