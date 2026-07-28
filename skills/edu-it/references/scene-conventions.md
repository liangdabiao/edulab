# edu-it 场景绘制约定

## 通用颜色语义

| 语义名 | 用途 | Hex |
|--------|------|-----|
| `comparing` | 排序/查找中正在比较的元素 | `#fbbf24` (黄) |
| `swapping` | 正在交换的元素 | `#f87171` (红) |
| `sorted` | 已排序就位的元素 | `#34d399` (绿) |
| `unsorted` | 未排序的待处理元素 | `#6366f1` (紫) |
| `excluded` | 已被排除的搜索区间 | `#1e293b` (暗) |
| `found` | 查找命中 | `#34d399` (绿) |
| `target` | 查找目标值标注 | `#fbbf24` (黄) |
| `line` | 普通线条/边框 | `#475569` |
| `text` | 普通文本 | `#94a3b8` |
| `highlight` | 高亮文本 | `#e8eef8` |

## 场景绘制函数签名

所有场景函数签名：`function(t, args)`
- `t`: 全局时间（秒），用于动画循环
- `args`: 从 sceneArgs 传入的配置对象

### Canvas 工具函数（模板内置）
- `drawText(text, x, y, color, fontSize, textAlign, textBaseline)`
- `roundRect(x, y, w, h, r)` (只 path，需 fill/stroke)
- `glow(color, blur, fn)` — 发光效果包装

## 各场景规范

### sort_bars（排序动画）
```jsonc
{
  "scene": "sort_bars",
  "sceneArgs": {
    "data": [5, 3, 8, 4, 2],           // 数组数据
    "title": "排序标题",                 // 可选
    "param": {                          // 出现则启用交互滑块
      "name": "进度", "min": 0, "max": 1, "step": 0.01, "value": 0
    }
  }
}
```
颜色规则：comparing(黄) / swapping(红) / sorted(绿) / unsorted(紫)

### search_visual（查找动画）
```jsonc
{
  "scene": "search_visual",
  "sceneArgs": {
    "data": [2, 5, 8, 12, 16],
    "target": 8,
    "type": "binary",                   // "binary" 或 "linear"
    "title": "查找标题",
    "param": { /* 同 sort_bars */ }
  }
}
```
颜色规则：mid(黄) / checked(红) / excluded(暗) / found(绿)

### flowchart（流程图）
```jsonc
{
  "scene": "flowchart",
  "sceneArgs": {
    "title": "标题",
    "nodes": [
      { "id": 0, "x": 200, "y": 40, "w": 120, "h": 40,
        "label": "开始", "type": "startend" }
    ],
    "edges": [[0, 1], [1, 2]],
    "active": -1    // -1=全部高亮, N=仅高亮第N个节点
  }
}
```
节点 type: `startend`(圆角) / `process`(矩形) / `decision`(菱形)

### concept_cards（概念卡片）
```jsonc
{
  "scene": "concept_cards",
  "sceneArgs": {
    "title": "标题",
    "items": [
      { "icon": "💡", "label": "核心思想", "desc": "描述文字", "color": "#6366f1" }
    ]
  }
}
```

### complexity_chart（复杂度对比表）
```jsonc
{
  "scene": "complexity_chart",
  "sceneArgs": {
    "title": "标题",
    "items": [
      {"name": "冒泡排序", "best": "O(n)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": true}
    ]
  }
}
```

### comparison（对比展示）
```jsonc
{
  "scene": "comparison",
  "sceneArgs": {
    "title": "对比标题",
    "left": { "title": "左侧标题", "color": "#f87171", "items": ["项1", "项2"] },
    "right": { "title": "右侧标题", "color": "#34d399", "items": ["项1", "项2"] }
  }
}
```

### block_diagram（框图/架构图）
```jsonc
{
  "scene": "block_diagram",
  "sceneArgs": {
    "title": "架构图",
    "blocks": [
      { "x": 40, "y": 80, "w": 120, "h": 50, "label": "CPU", "color": "#6366f1" }
    ],
    "arrows": [
      { "x1": 100, "y1": 130, "x2": 100, "y2": 170, "label": "数据总线", "color": "#34d399" }
    ]
  }
}
```

### 代码高亮（与场景配合）
```jsonc
{
  "scene": "sort_bars",
  "sceneArgs": {
    "code": {
      "lines": ["def bubble_sort(arr):", "    n = len(arr)"],
      "highlightLine": 2    // 高亮第2行（1-indexed），-1=不高亮
    }
  }
}
```
代码以大号 `div` 覆盖层显示在 Canvas 右上角，`highlightLine` 控制高亮行。
