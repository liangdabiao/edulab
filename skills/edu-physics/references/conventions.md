# 物理交互教学 — 坐标约定与构造模式

## 2D 与 3D 分工

edu-physics 技能使用 **2D Canvas** 渲染，所有物理场景在二维平面展示。对于以下**必须用三维展示**
的场景，请使用 **edu-physics-3d** 技能（基于 Three.js）：

| 场景 | 使用技能 | 说明 |
|------|---------|------|
| 抛体运动、碰撞、振动 | edu-physics | 平面内运动，2D 充分 |
| 电场线、等势面、波形 | edu-physics | 平面场/波分布 |
| 洛伦兹力 `F=qv×B` | edu-physics-3d | 力方向垂直于 v 和 B 平面，需 3D 观察 |
| 右手定则 / 叉积方向 | edu-physics-3d | 方向关系在三维空间 |
| 原子轨道 (s/p/d) | edu-physics-3d | 轨道是三维空间分布 |
| 晶体结构 / 晶格 | edu-physics-3d | 三维空间排列 |
| 刚体旋转 / 角动量 | edu-physics-3d | 旋转轴在三维 |
| 电磁波 E/B 正交 | edu-physics-3d | 两场正交传播 |
| 磁场（螺线管） | edu-physics-3d | 场线三维分布 |

edu-physics 产出 `board` 数据格式（2D Canvas 引擎），edu-physics-3d 产出 `board3d`
数据格式（Three.js 引擎），两者不兼容。请根据物理场景选择正确的技能。

## 坐标系约定

- 标准数学坐标系：x 向右为正，y 向上为正
- 前端自动映射到屏幕坐标：`sx = offX + x*scale`，`sy = offY - y*scale`（y 轴翻转）
- `view.xRange` / `view.yRange` 控制可视区域，引擎自动计算 `scale`
- 物理常用：抛出点为原点、平衡位置为原点、斜面沿 x 轴

## 物理交互范式

### 范式 1：参数作为时间（最常用）
滑块 t 表示时间，所有物理量（位置、速度、能量）通过运动方程的时间函数计算。

```python
param = {"name": "t", "min": 0, "max": 5, "value": 0}
scalars = [
    {"name": "v0", "expr": "10"},              # 初速度（固定值）
    {"name": "theta", "expr": "45"},           # 抛射角（固定值）
    {"name": "g", "expr": "9.8"},              # 重力加速度
    {"name": "vx", "expr": "v0*cos(theta*PI/180)"},  # 恒为常数
    {"name": "vy", "expr": "v0*sin(theta*PI/180)-g*t"},
    {"name": "x", "expr": "vx*t"},
    {"name": "y", "expr": "vy*t-0.5*g*t*t"},
]
# trace 点 P 的轨迹
trace = {"of": "P", "color": "locus"}
```

### 范式 2：参数作为角度
滑块 θ 表示角度（如抛射角、入射角），观察不同角度下物理量的变化。

```python
param = {"name": "theta", "label": "抛射角 $\\theta$", "min": 0, "max": 90}
scalars = [
    {"name": "v0", "expr": "10"},
    {"name": "vx", "expr": "v0*cos(theta*PI/180)"},
    {"name": "vy", "expr": "v0*sin(theta*PI/180)"},
]
```

### 范式 3：系统参数扫描
滑块控制系统固有参数（质量 m、劲度系数 k、电荷量 Q），观察系统行为变化。

```python
param = {"name": "m", "label": "质量 $m$ (kg)", "min": 1, "max": 10}
scalars = [
    {"name": "k", "expr": "100"},               # 劲度系数固定
    {"name": "omega", "expr": "sqrt(k/m)"},     # 角频率随 m 变化
]
```

### 范式 4：守恒定律验证
用 `constant` 指示器验证守恒量是否恒定：
- 机械能守恒：`E = 0.5*(vx^2+vy^2) + g*y` 恒为常数
- 动量守恒：`m1*v1 + m2*v2` 碰撞前后不变

## 常见物理构造 scalars 模板

### 抛体运动（无空气阻力）

```
vx = v0 * cos(theta * PI / 180)
vy0 = v0 * sin(theta * PI / 180)
vy = vy0 - g * t
x  = vx * t
y  = vy0 * t - 0.5 * g * t * t
Ek = 0.5 * (vx*vx + vy*vy)       # 单位质量动能
Ep = g * y                       # 单位质量势能
E  = Ek + Ep                     # 总机械能（守恒量）
```

### 简谐振动（弹簧振子）

```
omega = sqrt(k/m)
x     = A * cos(omega * t + phi)
v     = -A * omega * sin(omega * t + phi)
a     = -A * omega * omega * cos(omega * t + phi)
Ek    = 0.5 * v * v
Ep    = 0.5 * k * x * x          # 弹性势能 / m
E     = Ek + Ep                  # 总机械能（守恒量）
```

### 斜面滑块

```
theta_rad = theta * PI / 180
a         = g * (sin(theta_rad) - mu * cos(theta_rad))
v         = a * t
s         = 0.5 * a * t * t
```

## vector 使用技巧

矢量箭头表示力/速度/加速度，配置在 derived 中：

```json
{ "type": "vector", "from": "O", "to": "P", "color": "vecA", "label": "$\\vec{r}$" }
```

- 速度矢量：起点在质点位置，方向沿运动切线方向
- 加速度矢量：起点在质点位置，方向指向力心
- 力矢量：起点在受力点，方向沿力的方向
- 矢量箭头自动在端点绘制三角形箭头

## trace 使用技巧

- `trace.of` 指向的必须是 `points` 或 `derived` 中定义的点名
- 引擎在 param `[min, max]` 区间均匀采样 160 步绘制轨迹
- 适用于：抛体抛物线、简谐振动的 x-t 曲线、波的包络线
- 轨迹颜色建议用 `locus`（紫红色）以区别于其他几何元素

## param 使用技巧

| 要点 | 说明 |
|------|------|
| **参数命名** | 用合法 JS 标识符：`t` / `theta` / `v0` / `m` / `k`（不要用 `θ`、`α` 等） |
| **派生量** | 用 `scalars` 数组按序定义，后者可引用前者 |
| **角度单位** | 三角函数用弧度，角度需转换：`theta*PI/180` |
| **固定值** | scalars 可以直接写数字常量：`{"name": "g", "expr": "9.8"}` |
| **表达式运算符** | `+ - * / ^ sqrt cbrt abs sin cos tan asin acos atan atan2 exp log pow min max sign floor ceil hypot PI` |

## 颜色方案

```python
# 矢量颜色
color_vecA = "#f87171"   # 红色：水平分量 / x 方向
color_vecB = "#60a5fa"   # 蓝色：竖直分量 / y 方向
color_vec  = "#fbbf24"   # 金色：合矢量

# 轨迹颜色
color_locus = "#c084fc"  # 紫红：轨迹路径

# 能量区域
color_energy = "rgba(45,212,191,0.16)"  # 青色半透明

# 质点
color_point = "#f87171"  # 红色强调
```

## 自检清单

- [ ] 初始条件正确（t=0 时位置、速度、能量与理论一致）
- [ ] 滑块在全部范围内物理量有效（无 NaN、无超出边界）
- [ ] 守恒量恒为定值（constant 指示器全程显示）
- [ ] trace 轨迹形状正确（抛体为抛物线、SHM 为正弦曲线）
- [ ] 矢量方向正确（速度沿切线、加速度指向力心）
- [ ] 矢量大小随参数合理变化
- [ ] 读数的数值精度合理
- [ ] 浏览器无控制台报错
- [ ] KaTeX 公式全部正常渲染（注意：`\\prescript` 不兼容，改用 `{}^{...}_{...}\\text{...}`）
- [ ] 图例颜色与实际着色一致
