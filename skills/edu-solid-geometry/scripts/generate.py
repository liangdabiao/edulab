#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把结构化课程数据注入 template/lesson.html，产出单页 HTML。

数据全部由 lib/geometry_kernel.py 的确定性计算驱动（方案 A）：
坐标、向量、最终答案均为 sympy 精确计算结果，3D 坐标与解题数值同源、严格一致。

依赖: sympy。用一个能 import sympy 的 python3 运行（若缺: python3 -m pip install sympy）:
    python3 scripts/generate.py [输出路径.html]
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "lesson.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import geometry_kernel as gk  # noqa: E402
import bodies  # noqa: E402


def _centroid(three_points):
    names = list(three_points)
    n = len(names)
    return [sum(three_points[k][i] for k in names) / n for i in range(3)]


def render_html(data: dict, out_path: Path) -> Path:
    """把数据以 JSON 形式注入模板占位符，写出 html。"""
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    payload = json.dumps(data, ensure_ascii=False)
    html = template.replace(PLACEHOLDER, payload)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def build_cube_data() -> dict:
    """正方体 ABCD-A1B1C1D1（棱长 1），求直线 A1C 与底面 ABCD 所成角的正弦值。

    几何体拓扑取自 bodies.cuboid，顶点坐标与答案取自 geometry_kernel（同源）。
    """
    sol = gk.solve_cube_line_plane_angle(edge=1, scale=2)
    mp = sol["math_points"]
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]

    topo = bodies.cuboid()  # spheres + 12 条棱
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [6, 5, 7],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Line_A1C": {"type": "line", "a": "A1", "b": "C", "color": "emphasis", "depthTest": False},
            "Plane_ABCD": {"type": "plane", "pts": ["A", "B", "C", "D"]},
            "Normal_Vector": {"type": "arrow", "origin": "A", "dir": [0, 1, 0], "length": 1.6, "color": "normal"},
            "Axis": {"type": "axes", "size": 2.6},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 线面角",
        "title": "正方体ABCD-A₁B₁C₁D₁中，棱长为1，求直线A₁C与底面ABCD所成角的正弦值",
        "answerLabel": "直线 A₁C 与底面 ABCD 所成角的正弦值",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>以顶点 $A$ 为原点，$AB$、$AD$、$AA_1$ 分别为 $x$、$y$、$z$ 轴建立坐标系。</p>"
                r"<p>因为棱长为 $1$，关键点坐标为：</p>"
                r"$$A" + mp["A"] + r", C" + mp["C"] + r", A_1" + mp["A1"] + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 6, "y": 5, "z": 7},
        },
        {
            "title": "求直线 A₁C 的方向向量",
            "content": (
                r"<p>直线 $A_1C$ 的方向向量为：</p>"
                r"$$\vec{A_1C} = C - A_1 = " + v["A1C"] + r"$$"
            ),
            "highlight": ["Line_A1C"],
            "cameraPos": {"x": 5, "y": 4, "z": 8},
        },
        {
            "title": "确定底面 ABCD 的法向量",
            "content": (
                r"<p>底面 $ABCD$ 在平面 $z = 0$ 上，其法向量竖直向上：</p>"
                r"$$\vec{n} = " + v["n_simpl"] + r"$$"
            ),
            "highlight": ["Line_A1C", "Plane_ABCD", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 6, "z": 5},
        },
        {
            "title": "利用向量公式求解",
            "content": (
                r"<p>设直线 $A_1C$ 与底面所成角为 $\theta$。</p>"
                r"<p>线面角公式：$\sin\theta = \dfrac{|\vec{A_1C} \cdot \vec{n}|}{|\vec{A_1C}|\,|\vec{n}|}$</p>"
                r"<p>计算数量积与模长：</p>"
                r"$$\vec{A_1C} \cdot \vec{n} = " + v["dot"] + r", \quad |\vec{A_1C}| = " + v["norm_line"] + r"$$"
                r"<p>代入公式：</p>"
                r"$$\sin\theta = " + v["sin"] + r"$$"
                r"<p>所以，直线 $A_1C$ 与底面 $ABCD$ 所成角的正弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_A1C", "Plane_ABCD", "Normal_Vector"],
            "cameraPos": {"x": 5, "y": 5, "z": 6},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_data(base_edge=2, height=1) -> dict:
    """正四棱锥 P-ABCD（E 为 PC 中点）线面角；底边、高可参数化（随机出题用）。

    数值全部来自 geometry_kernel，文字步骤只负责把这些数值组织成讲解。
    """
    sol = gk.solve_pyramid_line_plane_angle(base_edge=base_edge, height=height, scale=1.5)
    mp = sol["math_points"]   # 数学坐标的 LaTeX，例如 "(\\sqrt{2}, 0, 0)"
    v = sol["vals"]           # 各步骤中间量 LaTeX
    ans = sol["answer_latex"]
    diag_tex = gk.tex(gk.sp.sympify(base_edge) * gk.sqrt(2))
    half_tex = gk.tex(gk.sp.sympify(base_edge) * gk.sqrt(2) / 2)

    # ---- 3D 模型：顶点坐标取自 kernel（与解题同源）；拓扑/高亮在此声明 ----
    model = {
        "target": [0, 0.45, 0],
        "initialCamera": [5, 4, 5],
        "points": sol["three_points"],
        "spheres": ["O", "P", "A", "B", "C", "D", "E"],
        "edges": [
            {"a": "A", "b": "B"},
            {"a": "B", "b": "C"},
            {"a": "C", "b": "D"},
            {"a": "D", "b": "A", "dashed": True},
            {"a": "P", "b": "A"},
            {"a": "P", "b": "B"},
            {"a": "P", "b": "C"},
            {"a": "P", "b": "D"},
            {"a": "A", "b": "C", "color": "aux", "dashed": True},
            {"a": "B", "b": "D", "color": "aux", "dashed": True, "name": "Line_BD"},
        ],
        "elements": {
            "Line_BE": {"type": "line", "a": "B", "b": "E", "color": "emphasis", "depthTest": False},
            "Plane_PAC": {"type": "plane", "pts": ["P", "A", "C"]},
            "Normal_Vector": {"type": "arrow", "origin": "O", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Axis": {"type": "axes", "size": 3},
            # 线段长度标注（已知条件：底边、对角线、高）
            "Len_AB": {"type": "measure", "a": "A", "b": "B", "label": str(base_edge)},
            "Len_AC": {"type": "measure", "a": "A", "b": "C", "label": diag_tex},
            "Len_PO": {"type": "measure", "a": "P", "b": "O", "label": str(height)},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 线面角",
        "title": f"正四棱锥P-ABCD中，底面边长为{base_edge}，高为{height}，E为PC中点，求直线BE与平面PAC所成角的正弦值",
        "answerLabel": "直线 BE 与平面 PAC 所成角的正弦值",
        "answerValue": f"${ans}$",
    }

    # ---- 步骤文案：数值占位由 kernel 计算结果填入（不心算）----
    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>首先，我们需要建立一个合适的空间直角坐标系来量化几何元素。</p>"
                r"<p>取底面正方形 $ABCD$ 的中心 $O$ 为原点 $(0,0,0)$。</p>"
                r"<p>让底面对角线 $AC$ 在 $x$ 轴，$BD$ 在 $y$ 轴，顶点 $P$ 在 $z$ 轴上。</p>"
                r"<p>因为底面边长为 $" + str(base_edge) + r"$，所以两条对角线长为 $" + diag_tex + r"$，半对角线长为 $" + half_tex + r"$。于是关键点坐标为：</p>"
                r"$$A" + mp["A"] + r", C" + mp["C"] + r"$$"
                r"$$B" + mp["B"] + r", D" + mp["D"] + r"$$"
                r"$$P" + mp["P"] + r"$$"
                r"<p>这样 $AC \perp BD$ 关系更明显。</p>"
            ),
            "highlight": ["Axis", "Len_AB", "Len_AC", "Len_PO"],
            "cameraPos": {"x": 5, "y": 4, "z": 5},
        },
        {
            "title": "计算中点 E 与向量 BE",
            "content": (
                r"<p>已知 $E$ 是侧棱 $PC$ 的中点。</p>"
                r"<p>利用中点坐标公式：$E = \frac{P + C}{2}$</p>"
                r"$$P" + mp["P"] + r", C" + mp["C"] + r"$$"
                r"$$E = " + v["E"] + r"$$"
                r"<p>接下来计算直线 $BE$ 的方向向量 $\vec{BE}$：</p>"
                r"$$\vec{BE} = E - B = " + v["BE"] + r"$$"
            ),
            "highlight": ["Line_BE"],
            "cameraPos": {"x": 3, "y": 3, "z": 6},
        },
        {
            "title": "确定平面 PAC 的法向量",
            "content": (
                r"<p>我们需要求直线 $BE$ 与平面 $PAC$ 的夹角。</p>"
                r"<p>观察几何体特征：</p>"
                r"<ul>"
                r"<li>底面 $ABCD$ 是正方形，对角线互相垂直，即 $AC \perp BD$。</li>"
                r"<li>顶点 $P$ 在底面的投影是中心 $O$，所以 $PO \perp AC$。</li>"
                r"</ul>"
                r"<p>因为 $AC \perp BD$ 且 $AC \perp PO$，所以直线 $BD \perp$ 平面 $PAC$。</p>"
                r"<p>因此，平面 $PAC$ 的法向量 $\vec{n}$ 就是 $\vec{BD}$ 的方向：</p>"
                r"$$\vec{n} = " + v["n"] + r"$$"
                r"<p>简化取 $\vec{n} = " + v["n_simpl"] + r"$。</p>"
            ),
            "highlight": ["Line_BE", "Plane_PAC", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 5, "z": 2},
        },
        {
            "title": "利用向量公式求解",
            "content": (
                r"<p>设直线 $BE$ 与平面 $PAC$ 所成角为 $\theta$。</p>"
                r"<p>根据线面角公式：$\sin\theta = \dfrac{|\vec{BE} \cdot \vec{n}|}{|\vec{BE}|\,|\vec{n}|}$</p>"
                r"<p>向量数据：</p>"
                r"<ul>"
                r"<li>$\vec{BE} = " + v["BE"] + r"$</li>"
                r"<li>$\vec{n} = " + v["n_simpl"] + r"$</li>"
                r"</ul>"
                r"<p>计算数量积与模长：</p>"
                r"$$\vec{BE} \cdot \vec{n} = " + v["dot"] + r", \quad |\vec{BE}| = " + v["norm_BE"] + r"$$"
                r"<p>代入公式：</p>"
                r"$$\sin\theta = " + v["sin"] + r"$$"
                r"<p>所以，直线 $BE$ 与平面 $PAC$ 所成角的正弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_BE", "Plane_PAC", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 4.5, "z": 4},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_box_volume_data(lx=3, ly=4, lz=5) -> dict:
    """长方体 ABCD-A1B1C1D1，已知长宽高，求体积。演示非角度题型端到端出图。"""
    V = gk.volume_box(lx, ly, lz)
    pts = gk.cuboid(lx, ly, lz)
    scale = 3.0 / max(lx, ly, lz)
    tp = gk.to_three(pts, scale=scale)
    topo = bodies.cuboid()
    center = _centroid(tp)
    ans = gk.tex(V)

    model = {
        "target": center,
        "initialCamera": [center[0] + 5, center[1] + 4, center[2] + 6],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Edge_L": {"type": "line", "a": "A", "b": "B", "color": "emphasis"},
            "Edge_W": {"type": "line", "a": "A", "b": "D", "color": "emphasis"},
            "Edge_H": {"type": "line", "a": "A", "b": "A1", "color": "emphasis"},
            "Axis": {"type": "axes", "size": max(tp_span(tp), 2.5)},
        },
    }
    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 体积",
        "title": f"长方体ABCD-A₁B₁C₁D₁的长、宽、高分别为 {lx}、{ly}、{lz}，求其体积",
        "answerLabel": "长方体的体积",
        "answerValue": f"${ans}$",
    }
    steps = [
        {
            "title": "明确长、宽、高",
            "content": (
                r"<p>以顶点 $A$ 为原点建立坐标系，三条从 $A$ 出发的棱即长、宽、高：</p>"
                r"<ul>"
                r"<li>长 $AB = " + str(lx) + r"$</li>"
                r"<li>宽 $AD = " + str(ly) + r"$</li>"
                r"<li>高 $AA_1 = " + str(lz) + r"$</li>"
                r"</ul>"
            ),
            "highlight": ["Edge_L", "Edge_W", "Edge_H", "Axis"],
            "cameraPos": {"x": center[0] + 5, "y": center[1] + 4, "z": center[2] + 6},
        },
        {
            "title": "应用长方体体积公式",
            "content": (
                r"<p>长方体体积等于长 × 宽 × 高：</p>"
                r"$$V = AB \times AD \times AA_1$$"
            ),
            "highlight": ["Edge_L", "Edge_W", "Edge_H"],
            "cameraPos": {"x": center[0] + 4, "y": center[1] + 5, "z": center[2] + 5},
        },
        {
            "title": "代入求值",
            "content": (
                r"$$V = " + str(lx) + r" \times " + str(ly) + r" \times " + str(lz) + r" = " + ans + r"$$"
                r"<p>所以该长方体的体积为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Edge_L", "Edge_W", "Edge_H"],
            "cameraPos": {"x": center[0] + 5, "y": center[1] + 4, "z": center[2] + 5},
        },
    ]
    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def tp_span(three_points):
    xs = [three_points[k][i] for k in three_points for i in range(3)]
    return max(abs(x) for x in xs) + 0.5


def build_random_data(seed=0) -> dict:
    """随机出题：随机选题型与参数，求解，答案不规整就重抽，返回可渲染数据。

    当前覆盖：长方体体积、正四棱锥线面角。可按同样的 resample 模式扩展更多题型。
    """
    import random
    rng = random.Random(seed)
    kind = rng.choice(["box_volume", "pyramid_lpa"])

    if kind == "box_volume":
        lx, ly, lz = (rng.randint(2, 6) for _ in range(3))
        return build_box_volume_data(lx, ly, lz)

    # pyramid 线面角：重抽直到答案规整
    for _ in range(50):
        a = rng.choice([2, 4, 6])
        h = rng.randint(1, 4)
        sol = gk.solve_pyramid_line_plane_angle(base_edge=a, height=h)
        if gk.is_clean(sol["_exact"]["sin_theta"]):
            return build_data(base_edge=a, height=h)
    # 兜底
    return build_box_volume_data()


def build_cube_angles_data() -> dict:
    """正方体 ABCD-A1B1C1D1（棱长 1）：空间角的正弦和余弦。

    以一道典型高考题为驱动：正方体中，求对角线 A1C 与底面所成角的正弦值、
    以及与棱 AB 所成角的余弦值。通过两个具体问题，引出方向余弦的统一视角。
    """
    sol = gk.solve_cube_direction_cosines(edge=1, scale=2)
    mp = sol["math_points"]
    v = sol["vals"]
    tp = sol["three_points"]
    topo = bodies.cuboid()
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [6, 5, 7],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Line_A1C": {"type": "line", "a": "A1", "b": "C", "color": "emphasis", "depthTest": False},
            "Line_AB":  {"type": "line", "a": "A", "b": "B", "color": "emphasis", "depthTest": False},
            "Plane_ABCD":  {"type": "plane", "pts": ["A", "B", "C", "D"]},
            "Normal_Vector": {"type": "arrow", "origin": "A", "dir": [0, 0, 1], "length": 1.6, "color": "normal"},
            "Axis": {"type": "axes", "size": 2.6},
            "Len_AB": {"type": "measure", "a": "A", "b": "B", "label": "1"},
            "Len_AA1": {"type": "measure", "a": "A", "b": "A1", "label": "1"},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "典型题 \u00b7 空间角",
        "title": "在正方体 ABCD-A\u2081B\u2081C\u2081D\u2081 中，求对角线 A\u2081C 与底面 ABCD 所成角的正弦值，以及与棱 AB 所成角的余弦值",
        "answerLabel": "线面角正弦 = 异面直线余弦 =",
        "answerValue": f"${v['sin_lp']}$",
    }

    steps = [
        {
            "title": "审题：我们要算什么？",
            "content": (
                r"<p>先看清题目要求——这是两个问题，但用同一根对角线：</p>"
                r"<p><strong>问题一</strong>：求 $A_1C$ 与底面 $ABCD$ 所成角 $\theta$ 的<strong>正弦值</strong>。</p>"
                r"<p><strong>问题二</strong>：求 $A_1C$ 与棱 $AB$ 所成角 $\varphi$ 的<strong>余弦值</strong>。</p>"
                r"<p>注意：</p>"
                r"<ul>"
                r"<li>线面角是<strong>直线与它在平面上的投影</strong>之间的夹角</li>"
                r"<li>异面直线夹角是平移后两条直线形成的<strong>锐角</strong></li>"
                r"</ul>"
                r"<p>两类角都用<strong>向量法</strong>统一处理。让我们从建系开始。</p>"
            ),
            "highlight": ["Line_A1C", "Plane_ABCD"],
            "cameraPos": {"x": 6, "y": 5, "z": 7},
        },
        {
            "title": "第 1 步：建立坐标系",
            "content": (
                r"<p>以 $A$ 为原点，$AB$ 为 $x$ 轴、$AD$ 为 $y$ 轴、$AA_1$ 为 $z$ 轴：</p>"
                r"<p>底面四点：</p>"
                r"$$A(0,0,0),\; B(1,0,0),\; C(1,1,0),\; D(0,1,0)$$"
                r"<p>顶面四点：</p>"
                r"$$A_1(0,0,1),\; B_1(1,0,1),\; C_1(1,1,1),\; D_1(0,1,1)$$"
                r"<p>现在所有关键点有了坐标（棱长 $1$，坐标简洁）。</p>"
            ),
            "highlight": ["Axis", "Len_AB", "Len_AA1"],
            "cameraPos": {"x": 6, "y": 5, "z": 7},
        },
        {
            "title": "第 2 步：求方向向量",
            "content": (
                r"<p>线面角需要<strong>直线的方向向量 $\vec v$</strong> 和<strong>平面的法向量 $\vec n$</strong>。</p>"
                r"<p>对角线 $A_1C$ 的方向向量：</p>"
                r"$$\overrightarrow{A_1C} = C - A_1 = " + v["v"] + r"$$"
                r"<p>模长：$|\overrightarrow{A_1C}| = " + v["norm_v"] + r"$</p>"
                r"<p>棱 $AB$ 的方向向量：$\overrightarrow{AB} = (1,0,0)$</p>"
                r"<p>底面 $ABCD$ 在 $z=0$ 平面上，法向量 $\vec n = (0,0,1)$。</p>"
                r"<p>向量已就位，接下来套公式即可。</p>"
            ),
            "highlight": ["Line_A1C", "Line_AB", "Plane_ABCD", "Axis"],
            "cameraPos": {"x": 5, "y": 4, "z": 8},
        },
        {
            "title": "第 3 步：求线面角的正弦",
            "content": (
                r"<p><strong>线面角公式</strong>：若直线方向向量为 $\vec v$，平面法向量为 $\vec n$，</p>"
                r"$$\sin\theta = \frac{|\vec v \cdot \vec n|}{|\vec v|\,|\vec n|}$$"
                r"<p>代入 $\vec v = \overrightarrow{A_1C} = " + v["v"] + r"$，$\vec n = (0,0,1)$：</p>"
                r"<p>点积就是取 $\vec v$ 的 $z$ 分量绝对值：$| -1 | = 1$，所以</p>"
                r"$$\sin\theta = \frac{1}{\sqrt{3} \times 1} = \frac{\sqrt{3}}{3}$$"
                r"<p>答案是 $\sin\theta = \frac{\sqrt{3}}{3}$。</p>"
            ),
            "highlight": ["Line_A1C", "Plane_ABCD", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 6, "z": 5},
        },
        {
            "title": "第 4 步：求异面直线夹角的余弦",
            "content": (
                r"<p><strong>异面直线夹角公式</strong>：若两条直线的方向向量为 $\vec v_1, \vec v_2$，</p>"
                r"$$\cos\varphi = \frac{|\vec v_1 \cdot \vec v_2|}{|\vec v_1|\,|\vec v_2|}$$"
                r"<p>代入 $\vec v_1 = \overrightarrow{A_1C} = " + v["v"] + r"$，$\vec v_2 = \overrightarrow{AB} = (1,0,0)$：</p>"
                r"<p>点积：$1 \cdot 1 + 1 \cdot 0 + (-1) \cdot 0 = 1$</p>"
                r"$$\cos\varphi = \frac{1}{\sqrt{3} \times 1} = \frac{\sqrt{3}}{3}$$"
                r"<p>答案是 $\cos\varphi = \frac{\sqrt{3}}{3}$。</p>"
            ),
            "highlight": ["Line_A1C", "Line_AB"],
            "cameraPos": {"x": 6, "y": 3, "z": 6},
        },
        {
            "title": "发现：线面角正弦 = 异面直线余弦？",
            "content": (
                r"<p>算出来两个结果一样：</p>"
                r"$$\sin\theta = \frac{\sqrt{3}}{3},\qquad \cos\varphi = \frac{\sqrt{3}}{3}$$"
                r"<p>这是巧合吗？</p>"
                r"<p>不是！因为 $AB$ 就是 $x$ 轴，$ABCD$ 的法向量就是 $z$ 轴。</p>"
                r"<p>记 $\overrightarrow{A_1C} = (\,1,\;1,\;-1\,)$，各分量除以模长 $\sqrt{3}$ 就是<strong>方向余弦</strong>：</p>"
                r"$$\cos\alpha = \frac{1}{\sqrt{3}},\quad"
                r"\cos\beta = \frac{1}{\sqrt{3}},\quad"
                r"\cos\gamma = -\frac{1}{\sqrt{3}}$$"
                r"<p>于是 $\sin\theta = |\cos\gamma| = \frac{\sqrt{3}}{3}$，$\cos\varphi = |\cos\alpha| = \frac{\sqrt{3}}{3}$。</p>"
                r"<p>它们根本上是同一个东西——<strong>方向余弦的绝对值</strong>。</p>"
            ),
            "highlight": ["Line_A1C", "Line_AB", "Plane_ABCD", "Normal_Vector", "Axis"],
            "cameraPos": {"x": 5, "y": 5, "z": 6},
        },
        {
            "title": "总结：空间角公式一览",
            "content": (
                r"<p>两道题共用一组向量计算，核心公式就两个：</p>"
                r"<table style='width:100%;border-collapse:collapse;margin:12px 0;font-size:14px'>"
                r"<tr style='background:rgba(14,165,233,0.15);border-bottom:1px solid #2a4a6a'>"
                r"<th style='padding:8px 10px;text-align:left'>角的类型</th>"
                r"<th style='padding:8px 10px;text-align:left'>公式</th>"
                r"<th style='padding:8px 10px;text-align:left'>本题答案</th></tr>"
                r"<tr style='border-bottom:1px solid #1a2a3a'>"
                r"<td style='padding:8px 10px'>线面角</td>"
                r"<td style='padding:8px 10px'>$\sin\theta = \frac{|\vec v \cdot \vec n|}{|\vec v||\vec n|}$</td>"
                r"<td style='padding:8px 10px'>$\frac{\sqrt{3}}{3}$</td></tr>"
                r"<tr>"
                r"<td style='padding:8px 10px'>异面直线夹角</td>"
                r"<td style='padding:8px 10px'>$\cos\varphi = \frac{|\vec v_1 \cdot \vec v_2|}{|\vec v_1||\vec v_2|}$</td>"
                r"<td style='padding:8px 10px'>$\frac{\sqrt{3}}{3}$</td></tr>"
                r"</table>"
                r"<p><strong>方向余弦</strong>：$\cos\alpha = \frac{x}{|\vec v|}$ 等，满足 $\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1$。</p>"
                r"<p>线面角正弦 = 直线与法向量夹角余弦的绝对值；</p>"
                r"<p>异面直线夹角余弦 = 两方向向量夹角余弦的绝对值。</p>"
                r"<p>两个公式都源于<strong>向量的点积</strong>，理解了这一点，空间角问题迎刃而解。</p>"
            ),
            "highlight": ["Line_A1C", "Axis", "Plane_ABCD", "Normal_Vector", "Line_AB"],
            "cameraPos": {"x": 5, "y": 5, "z": 6},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": v["sin_lp"]}



PROBLEMS = {
    "pyramid": build_data,
    "cube": build_cube_data,
    "box": build_box_volume_data,
    "angles": build_cube_angles_data,  # 空间角：正弦和余弦
}


def main():
    args = list(sys.argv[1:])
    problem = "pyramid"
    out = None
    seed = 0
    for a in args:
        if a in PROBLEMS or a == "random":
            problem = a
        elif a.isdigit():
            seed = int(a)
        else:
            out = Path(a)
    if out is None:
        # 默认写到“用户当前工作目录”(cwd)，而不是技能自身目录
        out = Path.cwd() / f"{problem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = build_random_data(seed) if problem == "random" else PROBLEMS[problem]()

    # --- 自检：最终步骤展示的答案必须等于答案卡的答案（同为 kernel 计算结果）---
    final_step = data["steps"][-1]["content"]
    assert data["_answer"] in final_step, "最终步骤未包含计算所得答案"
    data.pop("_answer", None)

    render_html(data, out)
    print(f"已生成: {out}")


if __name__ == "__main__":
    main()
