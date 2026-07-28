# edu-bio 场景绘制约定

## 通用颜色语义

| 语义名 | 用途 | Hex |
|--------|------|-----|
| `cell_membrane` | 磷脂双分子层 | `#6366f1` (indigo) |
| `nucleus` | 细胞核 | `#a78bfa` (violet) |
| `mitochondria` | 线粒体、能量 | `#fb923c` (orange) |
| `chloroplast` | 叶绿体、植物 | `#34d399` (emerald) |
| `dna_backbone` | DNA/RNA 骨架 | `#06b6d4` (cyan) |
| `base_a` | 腺嘌呤 | `#ef4444` (red) |
| `base_t` | 胸腺嘧啶 | `#3b82f6` (blue) |
| `base_g` | 鸟嘌呤 | `#22c55e` (green) |
| `base_c` | 胞嘧啶 | `#f59e0b` (amber) |
| `dominant` | 显性等位基因 | `#34d399` (emerald) |
| `recessive` | 隐性等位基因 | `#6b7280` (gray) |
| `trophic_1` | 生产者（营养级1） | `#34d399` (emerald) |
| `trophic_2` | 初级消费者 | `#60a5fa` (blue) |
| `trophic_3` | 次级消费者 | `#fb923c` (orange) |
| `trophic_4` | 三级消费者 | `#ef4444` (red) |

## 场景绘制函数签名

所有场景函数签名：`function(t, args)`
- `t`: 全局时间（秒），用于动画循环
- `args`: 从 sceneArgs 传入的配置对象

### Canvas 工具函数（模板内置）
- `drawText(text, x, y, color, fontSize, textAlign, textBaseline)`
- `roundRect(x, y, w, h, r)` (只 path，需 fill/stroke)
- `glow(color, blur, fn)` — 发光效果包装

## 各场景规范

### cell_diagram（细胞结构图）
```jsonc
{
  "scene": "cell_diagram",
  "sceneArgs": {
    "type": "animal",           // "animal" 或 "plant"
    "title": "动物细胞结构",     // 可选
    "highlight": ["mitochondria", "nucleus"],  // 高亮细胞器列表
    "labels": true              // 是否显示标签
  }
}
```
动物细胞：椭圆形边界，含细胞核、线粒体、内质网、高尔基体、溶酶体、核糖体、小泡
植物细胞：矩形边界（有细胞壁），另含叶绿体、大液泡

### membrane_transport（膜运输）
```jsonc
{
  "scene": "membrane_transport",
  "sceneArgs": {
    "type": "diffusion",        // diffusion/active/osmosis/facilitated
    "title": "自由扩散",
    "progress": 0.5             // 0-1 控制分子穿越进度
  }
}
```
颜色：磷脂头(indigo)、通道蛋白(emerald)、水通道(cyan)、ATP(amber)

### dna_helix（DNA双螺旋）
```jsonc
{
  "scene": "dna_helix",
  "sceneArgs": {
    "title": "DNA双螺旋",
    "showBases": true,
    "sequence": "ATGCGTACG",
    "highlightRegion": [2, 5]   // [start, end] 碱基索引
  }
}
```
A=红, T=蓝, G=绿, C=黄

### mitosis_meiosis（细胞分裂）
```jsonc
{
  "scene": "mitosis_meiosis",
  "sceneArgs": {
    "type": "mitosis",          // "mitosis" 或 "meiosis"
    "active": -1,               // -1=全部显示, N=高亮第N阶段
    "title": "有丝分裂"
  }
}
```
有丝分裂：4个阶段（前期/中期/后期/末期）2×2网格
减数分裂：8个阶段（I+II）4×2网格

### punnett_square（遗传图解）
```jsonc
{
  "scene": "punnett_square",
  "sceneArgs": {
    "parent1": ["A", "a"],
    "parent2": ["A", "a"],
    "showPhenotype": true,
    "highlight": [[0, 0], [1, 1]]    // 高亮特定子代格子
  }
}
```
颜色：纯合显性(emerald)、杂合(amber)、纯合隐性(gray)

### food_web（食物网/能量金字塔）
```jsonc
{
  "scene": "food_web",
  "sceneArgs": {
    "mode": "pyramid",           // "pyramid" 或 "web"
    "title": "能量金字塔",
    "species": [
      {"n": "生产者", "col": "#34d399", "w": 0.9, "energy": "10000"}
    ]
  }
}
```
金字塔模式：营养级自下而上变窄
食物网模式：node+edge 图结构

### physiology（生理系统）
```jsonc
{
  "scene": "physiology",
  "sceneArgs": {
    "system": "heart",           // heart/lungs/brain/kidney/digestive
    "highlight": [],             // 高亮结构
    "flowArrows": true           // 是否显示流向箭头
  }
}
```

### pcr_process（PCR过程）
```jsonc
{
  "scene": "pcr_process",
  "sceneArgs": {
    "active": "denaturation",    // denaturation/annealing/extension
    "progress": 0.5,              // 0-1 动画进度
    "cycles": 1                   // 显示循环数
  }
}
```
单循环模式：三步骤并排显示（变性=红, 退火=橙, 延伸=绿）
多循环模式：显示指数扩增过程
