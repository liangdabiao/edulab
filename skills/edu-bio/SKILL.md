---
name: edu-bio
description: >-
  把生物学课程做成交互教学网页：步进式知识点讲解 + Canvas 2D 场景动画（细胞结构、
  膜运输、DNA双螺旋、细胞分裂、遗传图解、食物网、生理系统、PCR过程等）+ 侧栏面板
  + 可交互参数滑块。覆盖分子与细胞、遗传与进化、稳态与环境、生物技术、人体生理五大模块。
---

# 生物学交互课程 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：步进式课程（8-15 步）逐步展示知识点，每步配有
**Canvas 2D 动画场景**（细胞结构、双螺旋、遗传图解、食物链金字塔、生理系统图、PCR 流程等）
+ **侧栏面板**（富文本讲解 + 要点列表）+ **顶部信息卡片**（概览）+ **步进器/播放器控制**。

## 依赖
无外部依赖。模板 `template/board-bio.html` 是自包含的单页 HTML（纯 CSS + Canvas 2D + JS）。

## 核心架构
- **单页 HTML**，无外部依赖
- **数据注入**：`__TUTORIAL_DATA__` 占位符模式
- **步骤数据**：`STEPS` 数组 + 场景绘制函数 + 配置
- **场景绘制器**：`SCENES` 字典，key 为场景类型名
- **交互模式**：`sceneArgs.param` 存在时侧栏渲染滑块，驱动实时重绘

## 工作流程

### 第 1 步：设计课程 spec
确定课程主题、分步内容、各步对应的视觉场景类型、配色。

### 第 2 步：写 build_* 构建 spec
参照 `scripts/generate.py` 的范例，编辑教程 spec：

```python
spec = {
    "meta": {"title": "...", "subtitle": "...", "module": "molecules_cells", "accent": "emerald"},
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
- 自动播放/暂停/步进/重置工作正常

### 第 5 步：交付
成品写在用户 cwd，命名形如 `tutorial-<主题>.html`。

## 数据格式

### meta（必填）
```jsonc
{
  "title": "细胞结构",
  "subtitle": "动物细胞 · 植物细胞 · 细胞器 · 功能",
  "module": "molecules_cells",   // 模块标识
  "accent": "emerald"             // 强调色
}
```

模块标识：molecules_cells, genetics, homeostasis, biotech, physiology
强调色：amber, violet, emerald, cyan, indigo, sky, red, green, orange, slate, pink

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
    "tag": "概念",
    "name": "细胞学说",
    "body": "<p>富文本讲解 HTML</p>",
    "points": {
      "title": "要点",
      "items": ["<strong>核心</strong>：相邻比较", "..."]
    },
    "scene": "concept_cards",
    "sceneArgs": {...}
  }
]
```

### 场景类型与参数

| scene | 用途 | sceneArgs 关键字段 |
|-------|------|-------------------|
| `cell_diagram` | 细胞结构图 | type(animal/plant), highlight[], labels |
| `membrane_transport` | 膜运输 | type(diffusion/active/osmosis/facilitated), progress |
| `dna_helix` | DNA双螺旋 | showBases, sequence, highlightRegion |
| `mitosis_meiosis` | 细胞分裂 | type(mitosis/meiosis), active |
| `punnett_square` | 遗传图解 | parent1[], parent2[], showPhenotype |
| `food_web` | 食物网/金字塔 | mode(web/pyramid), species[] |
| `physiology` | 生理系统 | system(heart/lungs/brain/kidney/digestive) |
| `pcr_process` | PCR过程 | active(denaturation/annealing/extension), progress, cycles |
| `concept_cards` | 概念卡片 | items[{icon,label,desc,color}] |
| `comparison` | 对比展示 | left{title,items}, right{title,items} |
| `flowchart` | 流程图 | nodes, edges, active |
| `block_diagram` | 框图 | blocks, arrows |
| `data_table` | 数据表 | headers, rows, highlight |
| `chart` | 统计图 | type(bar/line/pie), data, labels |

## 目录结构
- `template/board-bio.html` — 数据驱动模板（深色主题）
- `scripts/generate.py` — spec 构建 + 注入 + CLI
- `references/scene-conventions.md` — 场景绘制约定
