# 3D 物理交互教学 — 构造模式参考

## 坐标系约定

- 右手三维坐标系：x 向右、y 向上、z 向屏幕外（Three.js 默认）
- 网格在水平面（xz 平面）
- 坐标轴颜色：x=红 `#f87171`、y=绿 `#34d399`、z=蓝 `#60a5fa`
- 相机初始位置选在能展示三维关系的最佳视角

## 常见 3D 物理场景构造

### 场景 1：洛伦兹力（F = qv×B）

**物理设定**：正电荷 q 以速度 v 在磁场 B 中运动

```
scalars:
  v0 = 5                    # 速度大小
  B0 = 2                    # 磁场强度
  theta = t                 # v 与 B 夹角（滑块驱动）
  vx = v0 * cos(theta * PI / 180)
  vz = v0 * sin(theta * PI / 180)  # v 在 xz 平面旋转
  vy = 0
  Bx = 0, By = 0, Bz = B0   # B 沿 z 轴
  Fx = q * (vy*Bz - vz*By)  # 叉积 x 分量
  Fy = q * (vz*Bx - vx*Bz)  # 叉积 y 分量
  Fz = q * (vx*By - vy*Bx)  # 叉积 z 分量
  F_mag = sqrt(Fx*Fx + Fy*Fy + Fz*Fz)
```

**3D 对象**：
- sphere：电荷（原点）
- arrow v：v 方向（蓝色）
- arrow B：B 方向（绿色）
- arrow F：F 方向（红色，theta=0 时消失）
- curve：带电粒子螺旋轨迹

**验证**：θ=0°→F=0，θ=90°→F=qvB，θ=180°→F=0

### 场景 2：右手定则（叉积方向）

与洛伦兹力类似，但增加右手手型示意（用曲线弧标注角度）：

- v 沿食指方向，B 沿中指方向
- F 沿拇指方向（垂直于掌心）
- 滑块控制 v 和 B 之间的夹角

### 场景 3：螺旋运动（带电粒子在匀强磁场中）

当 v 与 B 不垂直也不平行时，粒子做螺旋运动：

```
v_parallel = v * cos(theta)     # 沿 B 方向的分量
v_perp = v * sin(theta)         # 垂直于 B 的分量
radius = m * v_perp / (q * B)   # 回旋半径
pitch = v_parallel * T          # 螺距
```

使用 curve 类型绘制三维螺旋线。

### 场景 4：原子轨道（s/p 轨道轮廓）

```
# s 轨道（球面）
r = a0 * n^2                    # 半径
x = r * sin(theta) * cos(phi)
y = r * sin(theta) * sin(phi)
z = r * cos(theta)

# p 轨道（哑铃形）
r = a0 * n^2 * abs(cos(theta))  # 角度依赖
```

用 curve 绘制轨道轮廓线，sphere 表示原子核。

## 3D 对象参数详解

### sphere
```json
{
  "type": "sphere",
  "position": [0, 0, 0],           // 球心 [x,y,z]
  "radius": 0.4,                   // 半径
  "color": "#f87171"               // 颜色
}
```

### arrow
```json
{
  "type": "arrow",
  "from": [0, 0, 0],               // 起点 [x,y,z]
  "to": [2, 0, 0],                 // 终点 [x,y,z]
  "color": "#60a5fa",             // 颜色
  "headLength": 0.3,              // 箭头长度
  "headWidth": 0.15               // 箭头宽度
}
```

### curve
```json
{
  "type": "curve",
  "expr": { "x": "...", "y": "...", "z": "..." },  // 参数方程
  "tMin": 0,                       // 参数范围起始
  "tMax": 10,                      // 参数范围结束
  "segments": 200,                 // 分段数（越大越平滑）
  "color": "#c084fc"              // 颜色
}
```

### trace（轨迹采样）
```json
{
  "trace": {
    "of": ["x_expr", "y_expr", "z_expr"],  // 表达式数组
    "samples": 160,               // 采样点数
    "color": "locus"              // 轨迹颜色
  }
}
```

## 颜色语义

| 名称 | 色值 | 用途 |
|------|------|------|
| `ptA` / `vecA` | `#f87171` | 红色：x 分量/第一对象 |
| `ptB` / `vecB` | `#60a5fa` | 蓝色：z 分量/第二对象 |
| `vec` / `curve` | `#fbbf24` | 金色：合矢量/曲线 |
| `fixed` | `#34d399` | 绿色：y 分量/固定对象 |
| `locus` | `#c084fc` | 紫红：轨迹 |
| `point` | `#94a3b8` | 灰色：一般点 |
| `aux` | `#64748b` | 灰色：辅助元素 |

## 自检清单

- [ ] 场景在浏览器打开后 Three.js 正常加载（无控制台报错）
- [ ] OrbitControls 可旋转/缩放/平移
- [ ] 滑块拖动时 3D 对象实时更新
- [ ] 箭头方向正确（叉积方向验证：θ=0°→F=0，θ=90°→F 最大方向正确）
- [ ] Trace 轨迹正确绘制
- [ ] Readouts 数值正确
- [ ] Constant 指示器（若有）显示正确
- [ ] 图例颜色与实际着色一致
- [ ] KaTeX 公式正常渲染
- [ ] 步骤面板可折叠展开
