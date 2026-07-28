# edu-geo 场景绘制约定

## 通用颜色语义

| 语义名 | 用途 | Hex |
|--------|------|-----|
| `ocean` | 海洋、水 | `#06b6d4` (cyan) |
| `land` | 陆地、植被 | `#34d399` (emerald) |
| `mountain` | 山地、地形 | `#fb923c` (orange) |
| `city_core` | 中心城区 | `#f87171` (red) |
| `suburb` | 郊区、过渡带 | `#fbbf24` (amber) |
| `industry` | 工业区 | `#6366f1` (indigo) |
| `plate` | 板块 | `#fb923c` / `#6366f1` |

## 各场景规范

### globe_3d（3D地球）
```jsonc
{
  "scene": "globe_3d",
  "sceneArgs": {
    "mode": "rotation",       // rotation(自转) 或 revolution(公转)
    "angle": 1.5,             // 旋转角度（弧度）
    "title": "地球自转"
  }
}
```
自转模式：经纬网格地球 + 昼夜分界线
公转模式：太阳居中 + 地球沿椭圆轨道 + 四季标注

### atmosphere（大气环流）
```jsonc
{
  "scene": "atmosphere",
  "sceneArgs": {
    "type": "global",         // global(三圈环流) / wind(风带) / seasonal(季风)
    "season": "summer",       // summer 或 winter（仅 seasonal 模式）
    "title": "全球气压带风带"
  }
}
```

### water_cycle（水循环）
```jsonc
{
  "scene": "water_cycle",
  "sceneArgs": {
    "active": -1,             // -1=全部显示, 0=降水, 1=蒸发, 2=径流, 3=下渗
    "title": "水循环示意图"
  }
}
```

### plate_tectonics（板块构造）
```jsonc
{
  "scene": "plate_tectonics",
  "sceneArgs": {
    "type": "convergent",     // convergent(汇聚) / divergent(张裂) / transform(转换)
    "title": "板块边界类型"
  }
}
```
汇聚边界：俯冲带 + 火山/山脉
张裂边界：岩浆上涌 + 大洋中脊
转换边界：断层 + 地震

### population_pyramid（人口金字塔）
```jsonc
{
  "scene": "population_pyramid",
  "sceneArgs": {
    "data": {"male": [10, 15, ...], "female": [8, 12, ...]},
    "labels": ["0-14", "15-64", "65+"],
    "title": "人口年龄结构"
  }
}
```
左男右女，蓝色(男)橙色(女)

### urban_model（城市结构模型）
```jsonc
{
  "scene": "urban_model",
  "sceneArgs": {
    "type": "concentric",    // concentric(同心圆) / sector(扇形) / multiple(多核心)
    "title": "城市空间结构"
  }
}
```

### map_chart（地图标记）
```jsonc
{
  "scene": "map_chart",
  "sceneArgs": {
    "region": "china",       // china 或 world
    "markers": [{"x": 0.5, "y": 0.4, "label": "北京"}],
    "title": "中国地理略图"
  }
}
```
坐标 x,y 为 canvas 比例值（0-1）

### gis_layers（GIS图层）
```jsonc
{
  "scene": "gis_layers",
  "sceneArgs": {
    "layers": ["遥感影像", "地形图", "行政区划"],
    "title": "GIS 图层叠加"
  }
}
```
每层带偏移的堆叠卡片效果
