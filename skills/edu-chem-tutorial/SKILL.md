---
name: edu-chem-tutorial
description: >-
  把化学课程（非单一反应）做成交互式教学课程页：步进式知识点讲解 + Canvas 2D 场景动画 +
  侧栏知识点面板 + 信息卡片 + 播放器控制。适合复杂解释型化学课程，如氧化还原配平、
  金属活动性、元素周期律、离子共存、速率平衡等。Canvas 2D 渲染（无 Three.js），
  数据驱动生成（类似 edu-chem-reaction 的 data injection 模式）。
---

# 化学交互课程 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：步进式课程（5-15 步）逐步展示知识点，每步配有
**Canvas 2D 动画场景**（反应图示、微观示意、图表、对比卡等）+ **侧栏知识点面板**
（富文本讲解 + 要点列表）+ **顶部信息卡片**（概览）+ **步进器/播放器控制**。
形态与 `化学教程新例子/index.html` 一致。

## 核心架构
- **单页 HTML**，无外部依赖（纯 CSS + Canvas 2D + JS）
- **数据注入**：`__TUTORIAL_DATA__` 占位符模式（同 edu-chem-reaction 的 template injection）
- **步骤数据**：`STEPS` 数组 + 场景绘制函数 + 配置
- **Canvas 2D 场景库**：内建常用化学绘制原语

## 工作流程

### 第 1 步：设计课程 spec
确定课程主题、分步内容、各步对应的视觉场景类型、配色语言（中/英）。

### 第 2 步：写 build_* 构建 spec
参照 `scripts/generate.py` 的范例，编辑教程 spec（步骤列表 + 场景配置 + 元数据）：
```python
spec = {
    "meta": {"title": "...", "subtitle": "...", "language": "zh-CN", "accent": "..."},
    "cards": [...],          # 顶部概览卡片
    "steps": [...],          # 步骤数组（tag, name, body, points, scene）
    "scenes": {...},         # 场景绘制函数（可选动画参数）
}
```

### 第 3 步：注入模板
```python
from pathlib import Path
out = Path.cwd() / "tutorial-<课程主题>.html"
render_html(spec, out)   # 将 spec 注入 template/tutorial.html
```

### 第 4 步：自检
- 打开 HTML 确认：无控制台报错、步骤切换正常、场景渲染正常
- 核对：所有步骤都能显示、动画循环正常、播放/暂停/步进工作
- 关闭预览端口

### 第 5 步：交付
成品写在用户 cwd，命名形如 `tutorial-<主题>.html`。

## 数据格式

### meta（必填）
```jsonc
{
  "title": "氧化还原方程式配平",
  "subtitle": "化合价升降法 · 电子守恒 · 双线桥",
  "language": "zh-CN",
  "accent": "amber"  // 强调色
}
```

### cards（顶部概览卡片，1-4 张）
```jsonc
[
  {"num": 1, "title": "概念", "body": "化合价升降<br>电子守恒"},
  {"num": 2, "title": "方法", "body": "标价→找升降<br>求最小公倍数"}
]
```

### steps（步骤数组，5-15 步）
```jsonc
[
  {
    "tag": "基础",           // 分类标签
    "name": "化合价概念",    // 步骤标题
    "body": "<p>富文本讲解 HTML</p>",
    "points": {              // 要点列表（侧栏展示）
      "title": "化合价规则",
      "items": ["<strong>单质</strong>：化合价为 0", "..."]
    },
    "scene": "equation",     // 场景类型名，对应 scenes 中的 key
    "sceneArgs": {...}       // 可选，传给场景绘制函数的参数
  }
]
```

### scenes（场景绘制函数映射）
每个场景类型对应一个 JS 绘制函数，函数签名 `(ctx, W, H, time, args)`。
内置场景类型见 `template/tutorial.html` 的 `SCENE_DRAWERS`。

## 目录
- `template/tutorial.html` — 数据驱动模板（__TUTORIAL_DATA__ 注入）
- `scripts/generate.py` — spec 构建 + 注入 + CLI
- `references/` — 参考文档
