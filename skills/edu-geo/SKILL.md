---
name: edu-geo
description: >-
  把地理课程做成交互教学网页：步进式知识点讲解 + Canvas 2D 场景动画（3D地球、
  大气环流、水循环、板块构造、人口金字塔、城市模型、地图标注、GIS图层等）
  + 侧栏面板。覆盖自然地理、人文地理、区域地理、地理信息技术四大模块。
---

# 地理交互课程 → 交互教学网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：步进式课程（8-15 步）逐步展示知识点，每步配有
**Canvas 2D 动画场景**（地球运动、大气环流、水循环、板块构造、人口金字塔、城市模型、
地图标记、GIS 图层叠加等）+ **侧栏面板** + **顶部信息卡片** + **步进器/播放器控制**。

## 依赖
无外部依赖。模板 `template/board-geo.html` 是自包含的单页 HTML。

## 核心架构
- **单页 HTML**，无外部依赖
- **数据注入**：`__TUTORIAL_DATA__` 占位符模式
- **步骤数据**：`STEPS` 数组 + 场景绘制函数 + 配置
- **场景绘制器**：`SCENES` 字典，key 为场景类型名

## 工作流程
同 edu-it/edu-bio 技能：设计 spec → 写 build_* 函数 → 注入模板 → 自检 → 交付。

## 场景类型

| scene | 用途 | sceneArgs 关键字段 |
|-------|------|-------------------|
| `globe_3d` | 3D地球（自转/公转/昼夜） | mode(rotation/revolution), angle |
| `atmosphere` | 大气环流、风带、季风 | type(global/wind/seasonal), season |
| `water_cycle` | 水循环示意图 | active(step索引) |
| `plate_tectonics` | 板块构造、地壳运动 | type(convergent/divergent/transform) |
| `population_pyramid` | 人口金字塔图 | data{male[],female[]}, labels[] |
| `urban_model` | 城市结构模型 | type(concentric/sector/multiple) |
| `map_chart` | 中国/世界略图 + 标记 | region(china/world), markers[] |
| `gis_layers` | GIS 图层叠加概念 | layers[] |

复用场景：concept_cards, comparison, flowchart, block_diagram, data_table, chart

## 目录结构
- `template/board-geo.html` — 数据驱动模板
- `scripts/generate.py` — spec 构建 + 注入 + CLI
- `references/scene-conventions.md` — 场景绘制约定
