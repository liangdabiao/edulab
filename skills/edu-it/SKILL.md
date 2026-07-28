---
name: edu-it
description: >-
  把信息技术 / 通用技术课程做成交互教学网页：步进式知识点讲解 + Canvas 2D 场景动画（算法可视化、
  流程图、神经网络、代码执行、硬件框图等）+ 侧栏面板 + 可交互参数滑块。覆盖编程基础、
  数据处理、算法与思维、人工智能初步、硬件基础、通用技术六大模块。
---

# 信息技术 / 通用技术 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：步进式课程（8-15 步）逐步展示知识点，每步配有
**Canvas 2D 动画场景**（排序动画、查找动画、流程图、神经网络图、代码高亮、框图等）
+ **侧栏面板**（富文本讲解 + 要点列表）+ **顶部信息卡片**（概览）+ **步进器/播放器控制**。
特定步骤支持**交互滑块**，用户可拖动控制算法进度（如排序的交换步骤）。

## 依赖
无外部依赖。模板 `template/board-it.html` 是自包含的单页 HTML（纯 CSS + Canvas 2D + JS）。

## 核心架构
- **单页 HTML**，无外部依赖
- **数据注入**：`__LESSON_DATA__` 占位符模式
- **步骤数据**：`STEPS` 数组 + 场景绘制函数 + 配置
- **场景绘制器**：`SCENES` 字典，key 为场景类型名
- **交互模式**：`sceneArgs.param` 存在时侧栏渲染滑块，驱动实时重绘

## 工作流程

### 第 1 步：设计课程 spec
确定课程主题、分步内容、各步对应的视觉场景类型、配色。

### 第 2 步：写 build_* 构建 spec
参照 `scripts/generate.py` 的范例，编辑教程 spec（步骤列表 + 场景配置 + 元数据）：
```python
spec = {
    "meta": {"title": "...", "subtitle": "...", "module": "algorithm", "accent": "indigo"},
    "cards": [...],          # 顶部概览卡片（1-4 张）
    "steps": [...],          # 步骤数组（tag, name, body, points, scene, sceneArgs）
}
```

### 第 3 步：注入模板
```python
from pathlib import Path
out = Path.cwd() / "tutorial-<主题>.html"
render_html(spec, out)
```

### 第 4 步：自检
- 打开 HTML 确认无控制台报错
- 步骤切换正常、场景渲染正确
- 交互步骤滑块拖动时动画同步更新
- 自动播放/暂停/步进/重置工作正常

### 第 5 步：交付
成品写在用户 cwd，命名形如 `tutorial-<主题>.html`。

## 数据格式

### meta（必填）
```jsonc
{
  "title": "冒泡排序",
  "subtitle": "相邻比较 · 依次冒泡 · O(n²)",
  "module": "algorithm",   // 模块标识：programming / data / algorithm / ai / hardware / tech
  "accent": "indigo"       // 强调色
}
```

支持强调色：amber, violet, emerald, cyan, indigo, sky, red, green, orange, slate, pink

### cards（顶部概览卡片，1-4 张）
```jsonc
[
  {"num": 1, "title": "核心思想", "body": "相邻比较<br>大数冒泡"},
  {"num": 2, "title": "时间复杂度", "body": "最坏 O(n²)"}
]
```

### steps（步骤数组，8-15 步）
```jsonc
[
  {
    "tag": "概念",           // 分类标签
    "name": "算法思想",      // 步骤标题
    "body": "<p>富文本讲解 HTML</p>",
    "points": {
      "title": "要点",
      "items": ["<strong>核心</strong>：相邻比较", "..."]
    },
    "scene": "flowchart",    // 场景类型名
    "sceneArgs": {...}       // 传给场景绘制函数的参数
  }
]
```

### 场景类型与参数

| scene | 用途 | sceneArgs 关键字段 |
|-------|------|-------------------|
| `sort_bars` | 排序动画 | data(数组), progress(0-1), param(滑块定义) |
| `search_visual` | 查找动画 | data, target, progress, param |
| `flowchart` | 流程图 | nodes, edges, active |
| `code_display` | 代码高亮 | lines, highlightLine, lang |
| `array_bars` | 静态柱状图 | data, titles |
| `concept_cards` | 概念卡片 | items[{icon,title,desc,color}] |
| `complexity_chart` | 复杂度表 | items[{name,best,worst,stable}] |
| `block_diagram` | 框图 | blocks[{x,y,w,h,label}], arrows |
| `data_table` | 数据表 | headers, rows, highlight |
| `chart` | 统计图 | type(bar/line/pie), data, labels |
| `neural_net` | 神经网络 | layers, connections, highlight |
| `comparison` | 对比展示 | left{title,items}, right{title,items} |

### 交互滑块（可选）
`sceneArgs` 中包含 `param` 时，侧栏渲染滑块：
```jsonc
"sceneArgs": {
  "data": [5, 3, 8, 4, 2],
  "param": {
    "name": "进度",
    "min": 0,
    "max": 1,
    "step": 0.01,
    "value": 0
  },
  "readouts": [
    {"label": "比较次数", "value": "6"}
  ]
}
```

## 目录结构
- `template/board-it.html` — 数据驱动模板（深色主题）
- `scripts/generate.py` — spec 构建 + 注入 + CLI
- `references/scene-conventions.md` — 场景绘制约定
