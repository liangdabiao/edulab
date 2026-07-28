#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把生物课程 spec 注入 template/board-bio.html，产出单页交互课程。
    5 个 PoC 教程覆盖 5 个教学模块。
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board-bio.html"
PLACEHOLDER = "__TUTORIAL_DATA__"


def render_html(spec: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(spec, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


# =====================================================================
# 1) 分子与细胞 — 细胞结构
# =====================================================================
def build_cell_structure():
    return {
        "meta": {"title": "细胞结构", "subtitle": "动物细胞 · 植物细胞 · 细胞器 · 功能", "module": "molecules_cells", "accent": "emerald"},
        "cards": [
            {"num": 1, "title": "细胞学说", "body": "细胞是生命基本单位<br>一切细胞来自已有细胞"},
            {"num": 2, "title": "动物细胞", "body": "无细胞壁<br>无叶绿体"},
            {"num": 3, "title": "植物细胞", "body": "有细胞壁<br>有叶绿体、大液泡"},
            {"num": 4, "title": "细胞器", "body": "各司其职<br>协同工作"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "细胞学说",
             "body": "<p><strong>细胞学说</strong>是生物学的三大基石之一：<br>1. 所有生物由细胞构成<br>2. 细胞是生命活动的基本单位<br>3. 新细胞来自已有细胞的增殖</p>",
             "points": {"title": "核心要点", "items": ["施莱登和施旺创立细胞学说", "细胞是结构和功能的基本单位", "细胞通过分裂产生新细胞"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "细胞学说",
                 "items": [
                     {"icon": "🔬", "label": "基本单位", "desc": "细胞是生命\n基本单位", "color": "#34d399"},
                     {"icon": "🧬", "label": "细胞起源", "desc": "细胞来自\n已有细胞", "color": "#6366f1"},
                     {"icon": "🔄", "label": "细胞分裂", "desc": "增殖方式\n有丝分裂", "color": "#a78bfa"},
                     {"icon": "📐", "label": "分类", "desc": "原核/真核\n动物/植物", "color": "#fbbf24"},
                 ]
             }},
            # Step 2
            {"tag": "结构", "name": "动物细胞",
             "body": "<p><strong>动物细胞</strong>由细胞膜包裹，内含多种细胞器。主要细胞器包括：细胞核（控制中心）、线粒体（能量工厂）、内质网（蛋白质加工）、高尔基体（分拣包装）、溶酶体（消化）等。</p>",
             "points": {"title": "动物细胞特点", "items": ["无细胞壁", "无叶绿体", "有小液泡（小泡）", "有中心体"]},
             "scene": "cell_diagram", "sceneArgs": {
                 "type": "animal", "title": "动物细胞结构", "labels": True
             }},
            # Step 3
            {"tag": "结构", "name": "细胞膜",
             "body": "<p><strong>细胞膜</strong>由磷脂双分子层和蛋白质构成，具有选择透过性。物质跨膜运输方式：<br>• 自由扩散 — 不耗能，顺浓度梯度<br>• 协助扩散 — 借助通道蛋白<br>• 主动运输 — 消耗ATP，逆浓度梯度</p>",
             "points": {"title": "膜运输方式", "items": ["自由扩散：O₂、CO₂", "协助扩散：葡萄糖", "主动运输：离子、氨基酸"]},
             "scene": "membrane_transport", "sceneArgs": {
                 "type": "diffusion", "title": "自由扩散"
             }},
            # Step 4
            {"tag": "功能", "name": "线粒体与ATP",
             "body": "<p><strong>线粒体</strong>是细胞的能量工厂，通过有氧呼吸将有机物中的化学能释放出来，一部分转移到ATP中。线粒体具有双层膜，内膜向内折叠形成嵴，增大了反应面积。</p>",
             "points": {"title": "线粒体", "items": ["双层膜结构", "内膜折叠形成嵴", "有氧呼吸的主要场所", "被称为细胞的动力车间"]},
             "scene": "cell_diagram", "sceneArgs": {
                 "type": "animal", "highlight": ["mitochondria"], "title": "线粒体 — 能量工厂"
             }},
            # Step 5
            {"tag": "结构", "name": "植物细胞",
             "body": "<p><strong>植物细胞</strong>除了具有动物细胞的基本结构外，还有：<br>• <strong>细胞壁</strong> — 纤维素构成，支持和保护<br>• <strong>叶绿体</strong> — 光合作用的场所<br>• <strong>大液泡</strong> — 储存水分和营养物质</p>",
             "points": {"title": "植物细胞特有结构", "items": ["细胞壁：纤维素和果胶", "叶绿体：光合作用", "大液泡：维持渗透压"]},
             "scene": "cell_diagram", "sceneArgs": {
                 "type": "plant", "title": "植物细胞结构", "labels": True
             }},
            # Step 6
            {"tag": "功能", "name": "叶绿体与光合作用",
             "body": "<p><strong>叶绿体</strong>是光合作用的场所，含有叶绿素。光合作用将CO₂和H₂O转化为有机物并释放O₂，是植物能量转换的核心过程。</p>",
             "points": {"title": "光合作用", "items": ["场所：叶绿体", "原料：CO₂ + H₂O", "产物：有机物 + O₂", "能量转换：光能→化学能"]},
             "scene": "cell_diagram", "sceneArgs": {
                 "type": "plant", "highlight": ["chloroplast"], "title": "叶绿体 — 光合作用"
             }},
            # Step 7
            {"tag": "对比", "name": "动物细胞 vs 植物细胞",
             "body": "<p>动物细胞和植物细胞既有共同点又有区别。理解它们的异同是学习生物学的基础。</p>",
             "points": {"title": "对比要点", "items": ["相同：都有细胞膜、细胞核、线粒体等", "不同：植物有细胞壁、叶绿体、大液泡"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "动物细胞 vs 植物细胞",
                 "left": {"title": "动物细胞", "color": "#f87171", "items": ["无细胞壁", "无叶绿体", "小液泡", "有中心体"]},
                 "right": {"title": "植物细胞", "color": "#34d399", "items": ["有细胞壁 (纤维素)", "有叶绿体", "有大液泡", "细胞排列规则"]},
             }},
            # Step 8
            {"tag": "过程", "name": "有丝分裂",
             "body": "<p><strong>有丝分裂</strong>是体细胞分裂的方式，分为前期、中期、后期、末期四个阶段。分裂前染色体复制，分裂后两个子细胞遗传物质完全相同。</p>",
             "points": {"title": "分裂过程", "items": ["前期：染色体凝缩", "中期：排列在赤道板", "后期：着丝粒分裂", "末期：核膜重建"]},
             "scene": "mitosis_meiosis", "sceneArgs": {
                 "type": "mitosis", "title": "有丝分裂过程"
             }},
            # Step 9
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>本课学习了细胞的基本结构和功能，从细胞学说到细胞器、跨膜运输和细胞分裂。理解细胞是理解生命的基础。</p>",
             "points": {"title": "本课要点", "items": ["细胞是生命活动的基本单位", "动植物细胞的异同", "细胞器分工协作", "物质跨膜运输方式", "有丝分裂的四个阶段"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "🧬", "label": "细胞学说", "desc": "基本单位\n来自已有细胞", "color": "#34d399"},
                     {"icon": "🔬", "label": "细胞结构", "desc": "动物 vs 植物\n细胞器功能", "color": "#6366f1"},
                     {"icon": "🚰", "label": "膜运输", "desc": "扩散/主动\n运输方式", "color": "#06b6d4"},
                     {"icon": "🔄", "label": "细胞分裂", "desc": "有丝分裂\n四个阶段", "color": "#a78bfa"},
                 ]
             }},
        ]
    }


# =====================================================================
# 2) 遗传与进化 — 孟德尔遗传学
# =====================================================================
def build_mendel_genetics():
    return {
        "meta": {"title": "孟德尔遗传学", "subtitle": "分离定律 · 自由组合 · DNA · 进化", "module": "genetics", "accent": "violet"},
        "cards": [
            {"num": 1, "title": "孟德尔定律", "body": "分离定律<br>自由组合定律"},
            {"num": 2, "title": "基因", "body": "显性/隐性<br>等位基因"},
            {"num": 3, "title": "DNA", "body": "双螺旋结构<br>碱基互补配对"},
            {"num": 4, "title": "进化", "body": "自然选择<br>适者生存"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "遗传的基本定律",
             "body": "<p><strong>孟德尔</strong>通过豌豆杂交实验发现了遗传的两大定律：<br>• <strong>分离定律</strong>：等位基因在减数分裂时分离，分别进入不同配子<br>• <strong>自由组合定律</strong>：非同源染色体上的非等位基因自由组合</p>",
             "points": {"title": "孟德尔定律", "items": ["分离定律：配子中只含一个等位基因", "自由组合：多对基因独立遗传", "3:1 和 9:3:3:1 表型比"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "孟德尔遗传定律",
                 "items": [
                     {"icon": "🧪", "label": "分离定律", "desc": "等位基因分离\n进入不同配子", "color": "#a78bfa"},
                     {"icon": "🔄", "label": "自由组合", "desc": "非等位基因\n自由组合", "color": "#6366f1"},
                     {"icon": "📊", "label": "表型比", "desc": "单因子3:1\n双因子9:3:3:1", "color": "#fbbf24"},
                     {"icon": "🧬", "label": "显隐关系", "desc": "显性掩盖隐性\n的遗传现象", "color": "#34d399"},
                 ]
             }},
            # Step 2
            {"tag": "概念", "name": "基本术语",
             "body": "<p>理解以下基本术语：<br>• <strong>基因</strong> — 遗传的基本单位<br>• <strong>等位基因</strong> — 同源染色体同一位置的基因<br>• <strong>纯合子</strong> — 等位基因相同 (AA, aa)<br>• <strong>杂合子</strong> — 等位基因不同 (Aa)<br>• <strong>表型</strong> — 表现出的性状<br>• <strong>基因型</strong> — 基因组成</p>",
             "points": {"title": "术语速查", "items": ["基因：遗传物质的功能单位", "等位基因：控制相对性状", "纯合子：AA 或 aa", "杂合子：Aa"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "遗传学术语",
                 "items": [
                     {"icon": "🧬", "label": "基因", "desc": "遗传单位\nDNA 片段", "color": "#6366f1"},
                     {"icon": "⚡", "label": "显性基因", "desc": "大写字母表示\nA、B、D...", "color": "#34d399"},
                     {"icon": "⬇️", "label": "隐性基因", "desc": "小写字母表示\na、b、d...", "color": "#6b7280"},
                     {"icon": "📋", "label": "表型", "desc": "观察到的\n性状表现", "color": "#fbbf24"},
                 ]
             }},
            # Step 3
            {"tag": "演示", "name": "单因子杂交",
             "body": "<p>以豌豆花色为例：<br>P：紫花(AA) × 白花(aa)<br>F₁：全部紫花(Aa)<br>F₂：紫花:白花 = 3:1</p><p>这是孟德尔<strong>分离定律</strong>的经典实验，证明等位基因在形成配子时分离。</p>",
             "points": {"title": "分离定律验证", "items": ["P: AA × aa", "F₁: 全部 Aa (紫花)", "F₂: 1AA : 2Aa : 1aa", "F₂ 表型比: 3:1"]},
             "scene": "punnett_square", "sceneArgs": {
                 "title": "单因子杂交 F₂ 代", "parent1": ["A", "a"], "parent2": ["A", "a"], "showPhenotype": True
             }},
            # Step 4
            {"tag": "演示", "name": "显性与隐性",
             "body": "<p>在F₂代中，共有三种基因型：<br>• <strong>AA</strong> — 纯合显性（紫花）<br>• <strong>Aa</strong> — 杂合（紫花，显性掩盖隐性）<br>• <strong>aa</strong> — 纯合隐性（白花）</p><p>表型比为 <strong>紫花:白花 = 3:1</strong>，但基因型比为 <strong>AA:Aa:aa = 1:2:1</strong></p>",
             "points": {"title": "显性规律", "items": ["AA 纯合显性 → 紫花", "Aa 杂合 → 紫花（显性表现）", "aa 纯合隐性 → 白花", "表型比 3:1 ≠ 基因型比 1:2:1"]},
             "scene": "punnett_square", "sceneArgs": {
                 "title": "基因型 vs 表型", "parent1": ["A", "a"], "parent2": ["A", "a"], "showPhenotype": True
             }},
            # Step 5
            {"tag": "概念", "name": "基因表达",
             "body": "<p><strong>中心法则</strong>描述了遗传信息传递的方向：</p><p>DNA → <strong>转录</strong> → mRNA → <strong>翻译</strong> → 蛋白质</p><p>• <strong>转录</strong>：DNA解旋，以一条链为模板合成mRNA<br>• <strong>翻译</strong>：mRNA上的密码子决定氨基酸序列</p>",
             "points": {"title": "中心法则", "items": ["DNA 携带遗传信息", "转录在细胞核中进行", "翻译在核糖体上进行", "蛋白质最终执行功能"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "中心法则 · 基因表达流程",
                 "nodes": [
                     {"id": 0, "x": 30, "y": 70, "w": 120, "h": 44, "label": "DNA", "type": "process", "color": "#a78bfa"},
                     {"id": 1, "x": 190, "y": 70, "w": 120, "h": 44, "label": "转录", "type": "process", "color": "#6366f1"},
                     {"id": 2, "x": 350, "y": 70, "w": 120, "h": 44, "label": "mRNA", "type": "process", "color": "#06b6d4"},
                     {"id": 3, "x": 510, "y": 70, "w": 120, "h": 44, "label": "翻译", "type": "process", "color": "#6366f1"},
                     {"id": 4, "x": 670, "y": 70, "w": 120, "h": 44, "label": "蛋白质", "type": "process", "color": "#34d399"},
                     {"id": 5, "x": 350, "y": 150, "w": 180, "h": 44, "label": "tRNA携带氨基酸", "type": "io", "color": "#fbbf24"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [5, 3]]
             }},
            # Step 6
            {"tag": "结构", "name": "DNA双螺旋",
             "body": "<p><strong>DNA</strong>由两条反向平行的脱氧核苷酸链组成，形成双螺旋结构。<br>• <strong>外侧</strong>：磷酸和脱氧核糖交替连接构成骨架<br>• <strong>内侧</strong>：碱基通过氢键配对（A-T，G-C）<br>• 碱基互补配对原则保证了DNA复制的精确性</p>",
             "points": {"title": "DNA结构要点", "items": ["双螺旋由Watson和Crick发现", "A配T（两个氢键）", "G配C（三个氢键）", "两条链反向平行"]},
             "scene": "dna_helix", "sceneArgs": {
                 "title": "DNA双螺旋结构", "showBases": True, "sequence": "ATGCGTACG", "highlightRegion": [2, 5]
             }},
            # Step 7
            {"tag": "概念", "name": "进化理论",
             "body": "<p><strong>自然选择</strong>是达尔文进化论的核心：<br>• 生物个体之间存在差异（变异）<br>• 适者生存，不适者被淘汰<br>• 有利变异逐代积累</p><p>现代进化理论补充了<strong>基因频率</strong>变化的观点：进化是种群基因频率的改变。</p>",
             "points": {"title": "进化理论", "items": ["自然选择是进化的动力", "变异为进化提供原材料", "隔离导致新物种形成", "种群基因频率改变 = 进化"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "现代生物进化理论",
                 "items": [
                     {"icon": "🌿", "label": "自然选择", "desc": "适者生存\n不适者淘汰", "color": "#34d399"},
                     {"icon": "🧬", "label": "变异", "desc": "突变和基因\n重组提供原料", "color": "#a78bfa"},
                     {"icon": "📈", "label": "基因频率", "desc": "种群进化\n的本质变化", "color": "#fbbf24"},
                     {"icon": "🏝️", "label": "隔离", "desc": "地理隔离\n生殖隔离", "color": "#6366f1"},
                 ]
             }},
            # Step 8
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>本课学习了孟德尔遗传定律、基因表达、DNA结构和进化理论。遗传与进化是贯穿生物学的核心主线。</p>",
             "points": {"title": "本课要点", "items": ["分离定律 vs 自由组合定律", "中心法则：DNA→RNA→蛋白质", "DNA双螺旋与碱基配对", "自然选择驱动进化"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "📐", "label": "孟德尔定律", "desc": "分离与自由\n组合定律", "color": "#a78bfa"},
                     {"icon": "🧬", "label": "DNA", "desc": "双螺旋结构\n碱基互补配对", "color": "#06b6d4"},
                     {"icon": "📋", "label": "中心法则", "desc": "DNA→RNA\n→蛋白质", "color": "#6366f1"},
                     {"icon": "🌿", "label": "进化", "desc": "自然选择\n基因频率变化", "color": "#34d399"},
                 ]
             }},
        ]
    }


# =====================================================================
# 3) 稳态与环境 — 免疫系统
# =====================================================================
def build_immune_system():
    return {
        "meta": {"title": "免疫调节", "subtitle": "神经 · 体液 · 免疫 · 生态系统", "module": "homeostasis", "accent": "cyan"},
        "cards": [
            {"num": 1, "title": "稳态", "body": "内环境<br>反馈调节"},
            {"num": 2, "title": "神经调节", "body": "反射弧<br>传导信号"},
            {"num": 3, "title": "免疫调节", "body": "特异性/非特异性<br>T细胞/B细胞"},
            {"num": 4, "title": "生态系统", "body": "食物网<br>能量金字塔"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "稳态调节",
             "body": "<p><strong>稳态</strong>是指内环境的理化性质（温度、pH、渗透压等）保持相对稳定的状态。机体通过<strong>神经-体液-免疫</strong>三大调节网络维持稳态。</p>",
             "points": {"title": "调节网络", "items": ["神经调节：快速、精确", "体液调节：广泛、持久", "免疫调节：防御、监控", "反馈调节维持平衡"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "稳态调节三大系统",
                 "items": [
                     {"icon": "⚡", "label": "神经调节", "desc": "快速精确\n反射弧完成", "color": "#6366f1"},
                     {"icon": "💧", "label": "体液调节", "desc": "激素运输\n广泛持久", "color": "#06b6d4"},
                     {"icon": "🛡️", "label": "免疫调节", "desc": "防御病原体\n免疫监控", "color": "#34d399"},
                     {"icon": "🔄", "label": "反馈调节", "desc": "负反馈为主\n维持稳态", "color": "#fbbf24"},
                 ]
             }},
            # Step 2
            {"tag": "结构", "name": "神经系统",
             "body": "<p>人体<strong>神经系统</strong>分为中枢神经系统（脑和脊髓）和外周神经系统。<br>• <strong>大脑</strong>：最高级中枢，负责感觉、运动、语言、思维<br>• <strong>小脑</strong>：维持身体平衡，协调运动<br>• <strong>脑干</strong>：维持基本生命活动（呼吸、心跳）</p>",
             "points": {"title": "脑结构功能", "items": ["大脑：高级神经活动", "小脑：平衡和协调", "脑干：生命中枢", "脊髓：反射和传导"]},
             "scene": "physiology", "sceneArgs": {
                 "system": "brain", "title": "脑结构"
             }},
            # Step 3
            {"tag": "过程", "name": "反射弧",
             "body": "<p><strong>反射</strong>是神经调节的基本方式。反射弧包括五个环节：</p><p><strong>感受器 → 传入神经 → 神经中枢 → 传出神经 → 效应器</strong></p><p>反射分为条件反射（如望梅止渴）和非条件反射（如膝跳反射）。</p>",
             "points": {"title": "反射弧组成", "items": ["感受器：接受刺激", "传入神经：传导信号给中枢", "神经中枢：分析和处理", "传出神经：传导指令", "效应器：执行反应"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "反射弧结构",
                 "nodes": [
                     {"id": 0, "x": 30, "y": 80, "w": 110, "h": 44, "label": "感受器", "color": "#f87171"},
                     {"id": 1, "x": 180, "y": 80, "w": 110, "h": 44, "label": "传入神经", "color": "#fbbf24"},
                     {"id": 2, "x": 330, "y": 80, "w": 110, "h": 44, "label": "神经中枢", "color": "#6366f1"},
                     {"id": 3, "x": 480, "y": 80, "w": 110, "h": 44, "label": "传出神经", "color": "#fbbf24"},
                     {"id": 4, "x": 630, "y": 80, "w": 110, "h": 44, "label": "效应器", "color": "#34d399"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]
             }},
            # Step 4
            {"tag": "概念", "name": "免疫调节",
             "body": "<p><strong>免疫系统</strong>是人体的防御系统，分为：<br>• <strong>非特异性免疫</strong>：天生具有，包括皮肤屏障、吞噬细胞<br>• <strong>特异性免疫</strong>：后天获得，分体液免疫和细胞免疫</p>",
             "points": {"title": "免疫防线", "items": ["第一道防线：皮肤、黏膜", "第二道防线：吞噬细胞、杀菌物质", "第三道防线：B细胞/T细胞", "特异性免疫有记忆性"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "免疫系统组成",
                 "items": [
                     {"icon": "🛡️", "label": "第一道防线", "desc": "皮肤黏膜\n物理屏障", "color": "#6366f1"},
                     {"icon": "⚔️", "label": "第二道防线", "desc": "吞噬细胞\n炎症反应", "color": "#fbbf24"},
                     {"icon": "🎯", "label": "第三道防线", "desc": "B细胞/T细胞\n特异性免疫", "color": "#34d399"},
                     {"icon": "💉", "label": "免疫记忆", "desc": "记忆细胞\n疫苗原理", "color": "#06b6d4"},
                 ]
             }},
            # Step 5
            {"tag": "对比", "name": "特异性 vs 非特异性",
             "body": "<p>两种免疫方式相辅相成：<br>• 非特异性免疫是基础，对所有病原体都有效<br>• 特异性免疫针对特定病原体，有记忆性</p>",
             "points": {"title": "对比", "items": ["非特异性：先天、广谱、无记忆", "特异性：后天、专一、有记忆", "两者协同工作"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "非特异性 vs 特异性免疫",
                 "left": {"title": "非特异性免疫", "color": "#6366f1", "items": ["天生就有", "无针对性", "无记忆性", "第一、二道防线"]},
                 "right": {"title": "特异性免疫", "color": "#34d399", "items": ["后天获得", "针对特定病原体", "有记忆性", "第三道防线"]},
             }},
            # Step 6
            {"tag": "过程", "name": "体液免疫",
             "body": "<p><strong>体液免疫</strong>主要由B细胞介导，产生抗体中和病原体。</p><p>抗原 → B细胞（受刺激）→ 浆细胞 → 抗体<br>↳ 记忆细胞（长期留存）</p>",
             "points": {"title": "体液免疫过程", "items": ["B细胞识别抗原", "增殖分化为浆细胞和记忆细胞", "浆细胞分泌抗体", "抗体中和抗原"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "体液免疫流程",
                 "nodes": [
                     {"id": 0, "x": 40, "y": 60, "w": 120, "h": 40, "label": "抗原入侵", "color": "#f87171"},
                     {"id": 1, "x": 200, "y": 60, "w": 120, "h": 40, "label": "B细胞识别", "color": "#6366f1"},
                     {"id": 2, "x": 200, "y": 140, "w": 120, "h": 40, "label": "记忆细胞", "color": "#34d399"},
                     {"id": 3, "x": 200, "y": 220, "w": 120, "h": 40, "label": "浆细胞", "color": "#06b6d4"},
                     {"id": 4, "x": 400, "y": 220, "w": 120, "h": 40, "label": "抗体分泌", "color": "#fbbf24"},
                     {"id": 5, "x": 560, "y": 220, "w": 130, "h": 40, "label": "抗原-抗体结合", "color": "#34d399"},
                 ],
                 "edges": [[0, 1], [1, 2], [1, 3], [3, 4], [4, 5]]
             }},
            # Step 7
            {"tag": "演示", "name": "生态系统与食物网",
             "body": "<p><strong>生态系统</strong>由生物群落和非生物环境组成。各营养级之间存在<strong>捕食关系</strong>，形成食物网。<br>• 能量沿食物链单向流动<br>• 传递效率约为10%<br>• 营养级越高，生物量越少</p>",
             "points": {"title": "生态概念", "items": ["生产者：将无机物转化为有机物", "消费者：直接或间接以生产者为食", "分解者：分解有机物为无机物", "能量金字塔体现传递效率"]},
             "scene": "food_web", "sceneArgs": {
                 "mode": "pyramid", "title": "能量金字塔",
                 "species": [
                     {"n": "生产者（草）", "col": "#34d399", "w": 0.9, "energy": "10000"},
                     {"n": "初级消费者（昆虫）", "col": "#60a5fa", "w": 0.7, "energy": "1000"},
                     {"n": "次级消费者（青蛙）", "col": "#fb923c", "w": 0.5, "energy": "100"},
                     {"n": "三级消费者（蛇）", "col": "#ef4444", "w": 0.3, "energy": "10"},
                 ]
             }},
            # Step 8
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>本课学习了人体稳态的三大调节方式，以及生态系统的物质循环和能量流动。</p>",
             "points": {"title": "本课要点", "items": ["神经-体液-免疫调节网络", "反射弧五环节", "特异性免疫与非特异性免疫", "能量金字塔与10%传递效率"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "⚡", "label": "神经调节", "desc": "反射弧\n快速精确", "color": "#6366f1"},
                     {"icon": "🛡️", "label": "免疫调节", "desc": "三道防线\n特异性免疫", "color": "#34d399"},
                     {"icon": "🌿", "label": "生态系统", "desc": "能量流动\n物质循环", "color": "#06b6d4"},
                     {"icon": "🔄", "label": "稳态平衡", "desc": "反馈调节\n维持内环境", "color": "#fbbf24"},
                 ]
             }},
        ]
    }


# =====================================================================
# 4) 生物技术 — PCR技术
# =====================================================================
def build_pcr_technique():
    return {
        "meta": {"title": "PCR技术", "subtitle": "聚合酶链式反应 · 引物 · Taq酶 · 指数扩增", "module": "biotech", "accent": "red"},
        "cards": [
            {"num": 1, "title": "PCR定义", "body": "体外扩增<br>特定DNA片段"},
            {"num": 2, "title": "三步骤", "body": "变性·退火·延伸<br>循环重复"},
            {"num": 3, "title": "指数扩增", "body": "2ⁿ倍增长<br>快速高效"},
            {"num": 4, "title": "应用", "body": "诊断·法医<br>基因工程"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "PCR技术概述",
             "body": "<p><strong>PCR</strong>（聚合酶链式反应）是一种在体外快速扩增特定DNA片段的技术。由Kary Mullis于1983年发明，获诺贝尔化学奖。</p><p>核心要素：<br>• <strong>模板DNA</strong> — 待扩增的DNA<br>• <strong>引物</strong> — 确定扩增起始位置<br>• <strong>Taq DNA聚合酶</strong> — 耐高温的DNA合成酶<br>• <strong>dNTP</strong> — 四种脱氧核苷酸原料</p>",
             "points": {"title": "PCR三要素", "items": ["模板DNA：待扩增的目标序列", "引物：人工合成的短DNA片段", "Taq酶：耐高温DNA聚合酶", "dNTP：A、T、G、C原料"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "PCR核心要素",
                 "items": [
                     {"icon": "🧬", "label": "模板DNA", "desc": "待扩增的\n目标片段", "color": "#6366f1"},
                     {"icon": "📍", "label": "引物", "desc": "确定扩增\n起始位置", "color": "#fbbf24"},
                     {"icon": "🔥", "label": "Taq聚合酶", "desc": "耐高温\n94°C不变性", "color": "#f87171"},
                     {"icon": "🧪", "label": "dNTP", "desc": "四种原料\nA/T/G/C", "color": "#34d399"},
                 ]
             }},
            # Step 2
            {"tag": "过程", "name": "变性 — 双链分离",
             "body": "<p><strong>变性</strong>（94-98°C）：加热使DNA双链间的氢键断裂，双螺旋解旋成为两条单链，作为后续复制的模板。</p>",
             "points": {"title": "变性要点", "items": ["温度：94-98°C", "氢键断裂", "双链→两条单链", "DNA骨架不断裂"]},
             "scene": "pcr_process", "sceneArgs": {
                 "active": "denaturation", "progress": 0.5, "cycles": 1
             }},
            # Step 3
            {"tag": "过程", "name": "退火 — 引物结合",
             "body": "<p><strong>退火</strong>（50-65°C）：降温后，引物与模板DNA的互补序列结合。引物决定了扩增的起始点和长度。</p>",
             "points": {"title": "退火要点", "items": ["温度：50-65°C", "引物与模板互补结合", "引物决定扩增特异性", "退火温度影响特异性"]},
             "scene": "pcr_process", "sceneArgs": {
                 "active": "annealing", "progress": 0.5, "cycles": 1
             }},
            # Step 4
            {"tag": "过程", "name": "延伸 — DNA合成",
             "body": "<p><strong>延伸</strong>（72°C）：Taq DNA聚合酶从引物3'端开始，沿模板链方向（5'→3'）合成新的DNA链。延伸速度约每分钟1000个碱基。</p>",
             "points": {"title": "延伸要点", "items": ["温度：72°C（最适温度）", "Taq酶催化DNA合成", "方向：5'→3'延伸", "合成速度约1000 bp/min"]},
             "scene": "pcr_process", "sceneArgs": {
                 "active": "extension", "progress": 0.5, "cycles": 1
             }},
            # Step 5
            {"tag": "演示", "name": "PCR指数扩增",
             "body": "<p>每个PCR循环使DNA数量翻倍：<br>• 循环1：2条→4条<br>• 循环2：4条→8条<br>• 循环3：8条→16条<br>• ...经过30个循环，DNA扩增约10⁹倍！</p><p>这就是PCR技术如此强大的原因——指数级扩增。</p>",
             "points": {"title": "指数扩增", "items": ["每循环DNA量翻倍", "N个循环=2^N倍", "30个循环≈10⁹倍", "快速获得大量DNA"]},
             "scene": "pcr_process", "sceneArgs": {
                 "cycles": 3, "active": "denaturation", "progress": 0
             }},
            # Step 6
            {"tag": "概念", "name": "PCR的应用",
             "body": "<p>PCR技术在多个领域有广泛应用：<br><br>• <strong>医学诊断</strong>：检测病原体DNA，如新冠病毒<br>• <strong>法医学</strong>：DNA指纹鉴定，亲子鉴定<br>• <strong>基因工程</strong>：扩增目的基因用于克隆<br>• <strong>研究</strong>：测序、突变分析、基因表达分析</p>",
             "points": {"title": "PCR应用", "items": ["临床诊断：快速检测病原体", "法医鉴定：DNA指纹分析", "基因克隆：扩增目的基因", "科学研究：测序与分析"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "PCR应用领域",
                 "items": [
                     {"icon": "🏥", "label": "医学诊断", "desc": "病毒检测\n疾病筛查", "color": "#f87171"},
                     {"icon": "🔍", "label": "法医鉴定", "desc": "DNA指纹\n亲子鉴定", "color": "#6366f1"},
                     {"icon": "🧬", "label": "基因工程", "desc": "目的基因\n克隆扩增", "color": "#34d399"},
                     {"icon": "🔬", "label": "科学研究", "desc": "基因测序\n突变分析", "color": "#06b6d4"},
                 ]
             }},
            # Step 7
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>PCR是分子生物学最基础也最重要的技术之一。理解变性→退火→延伸三步骤循环和指数扩增原理是关键。</p>",
             "points": {"title": "本课要点", "items": ["PCR三步骤：变性、退火、延伸", "Taq酶耐高温是关键", "指数扩增实现DNA大量复制", "广泛应用：诊断、法医、研究"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "🔥", "label": "变性 94°C", "desc": "双链解旋\n成单链模板", "color": "#f87171"},
                     {"icon": "❄️", "label": "退火 55°C", "desc": "引物结合\n确定起点", "color": "#fb923c"},
                     {"icon": "🌡️", "label": "延伸 72°C", "desc": "Taq酶\n合成DNA", "color": "#34d399"},
                     {"icon": "📈", "label": "指数增长", "desc": "2^N扩增\n快速高效", "color": "#6366f1"},
                 ]
             }},
        ]
    }


# =====================================================================
# 5) 人体生理 — 循环系统
# =====================================================================
def build_circulatory_system():
    return {
        "meta": {"title": "人体生理 — 循环与呼吸", "subtitle": "心脏 · 血液循环 · 呼吸 · 气体交换", "module": "physiology", "accent": "red"},
        "cards": [
            {"num": 1, "title": "循环系统", "body": "体循环<br>肺循环"},
            {"num": 2, "title": "心脏", "body": "四腔室<br>泵血功能"},
            {"num": 3, "title": "呼吸系统", "body": "气体交换<br>肺泡结构"},
            {"num": 4, "title": "泌尿系统", "body": "肾单位<br>过滤重吸收"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "循环系统概述",
             "body": "<p><strong>循环系统</strong>由心脏、血管和血液构成，负责运输氧气、营养物质、代谢废物和激素。包括：<br>• <strong>体循环</strong>：左心室→全身→右心房（含氧血→缺氧血）<br>• <strong>肺循环</strong>：右心室→肺→左心房（缺氧血→富氧血）</p>",
             "points": {"title": "循环系统功能", "items": ["运输O₂和CO₂", "输送营养和激素", "带走代谢废物", "维持体温稳定"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "循环系统概览",
                 "items": [
                     {"icon": "❤️", "label": "心脏", "desc": "四腔室\n泵血动力", "color": "#f87171"},
                     {"icon": "🫁", "label": "肺", "desc": "气体交换\n获取O₂", "color": "#06b6d4"},
                     {"icon": "🔄", "label": "血管", "desc": "动脉/静脉\n/毛细血管", "color": "#6366f1"},
                     {"icon": "💧", "label": "血液", "desc": "红细胞/白细胞\n/血小板", "color": "#fbbf24"},
                 ]
             }},
            # Step 2
            {"tag": "结构", "name": "心脏结构",
             "body": "<p><strong>心脏</strong>是循环的动力泵，有四腔室：<br>• <strong>左心房</strong> — 接收肺静脉来的含氧血<br>• <strong>左心室</strong> — 泵血到全身（壁最厚）<br>• <strong>右心房</strong> — 接收体循环回流的缺氧血<br>• <strong>右心室</strong> — 泵血到肺</p><p>心房和心室之间有瓣膜，防止血液倒流。</p>",
             "points": {"title": "心脏结构", "items": ["左心室壁最厚，负责体循环", "右心室泵血到肺（压力小）", "房室瓣防止血液倒流", "心率约75次/分钟"]},
             "scene": "physiology", "sceneArgs": {
                 "system": "heart", "flowArrows": True
             }},
            # Step 3
            {"tag": "过程", "name": "体循环",
             "body": "<p><strong>体循环</strong>（大循环）：<br>左心室 → <strong>主动脉</strong> → 全身各级动脉 → 毛细血管（物质交换）→ 各级静脉 → <strong>上/下腔静脉</strong> → 右心房</p><p>体循环将含氧丰富的动脉血变为含CO₂较多的静脉血。</p>",
             "points": {"title": "体循环路径", "items": ["起点：左心室", "特点：含氧血→组织→缺氧血", "功能：供给O₂和营养", "终点：右心房"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "体循环流程",
                 "nodes": [
                     {"id": 0, "x": 30, "y": 80, "w": 100, "h": 44, "label": "左心室", "color": "#f87171"},
                     {"id": 1, "x": 170, "y": 80, "w": 100, "h": 44, "label": "主动脉", "color": "#ef4444"},
                     {"id": 2, "x": 310, "y": 80, "w": 120, "h": 44, "label": "全身毛细血管", "color": "#fbbf24"},
                     {"id": 3, "x": 470, "y": 80, "w": 100, "h": 44, "label": "腔静脉", "color": "#3b82f6"},
                     {"id": 4, "x": 610, "y": 80, "w": 100, "h": 44, "label": "右心房", "color": "#3b82f6"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]
             }},
            # Step 4
            {"tag": "过程", "name": "肺循环",
             "body": "<p><strong>肺循环</strong>（小循环）：<br>右心室 → <strong>肺动脉</strong> → 肺部毛细血管（气体交换）→ <strong>肺静脉</strong> → 左心房</p><p>肺循环将CO₂排出体外，补充O₂，使静脉血变为动脉血。</p>",
             "points": {"title": "肺循环路径", "items": ["起点：右心室", "特点：缺氧血→肺→含氧血", "功能：排出CO₂，摄取O₂", "终点：左心房"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "肺循环流程",
                 "nodes": [
                     {"id": 0, "x": 30, "y": 80, "w": 100, "h": 44, "label": "右心室", "color": "#3b82f6"},
                     {"id": 1, "x": 170, "y": 80, "w": 100, "h": 44, "label": "肺动脉", "color": "#6366f1"},
                     {"id": 2, "x": 310, "y": 80, "w": 120, "h": 44, "label": "肺部毛细血管", "color": "#34d399"},
                     {"id": 3, "x": 470, "y": 80, "w": 100, "h": 44, "label": "肺静脉", "color": "#f87171"},
                     {"id": 4, "x": 610, "y": 80, "w": 100, "h": 44, "label": "左心房", "color": "#f87171"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]
             }},
            # Step 5
            {"tag": "结构", "name": "呼吸系统",
             "body": "<p><strong>呼吸系统</strong>由呼吸道和肺组成：<br>• <strong>呼吸道</strong>：鼻→咽→喉→气管→支气管<br>• <strong>肺</strong>：由大量肺泡构成<br>• <strong>肺泡</strong>：气体交换的场所，壁极薄，表面有丰富的毛细血管</p>",
             "points": {"title": "呼吸系统", "items": ["气管有C形软骨支撑", "支气管分支成细支气管", "肺泡数量可达3亿个", "肺泡壁只有一层细胞"]},
             "scene": "physiology", "sceneArgs": {
                 "system": "lungs"
             }},
            # Step 6
            {"tag": "过程", "name": "气体交换",
             "body": "<p><strong>气体交换</strong>在肺泡和毛细血管之间进行：<br>• <strong>O₂</strong> 从肺泡扩散到血液（O₂与血红蛋白结合）<br>• <strong>CO₂</strong> 从血液扩散到肺泡</p><p>方向由浓度梯度决定，属于<strong>自由扩散</strong>，不耗能。</p>",
             "points": {"title": "气体交换", "items": ["O₂进入血液与血红蛋白结合", "CO₂从血液进入肺泡排出", "扩散方向由浓度决定", "肺泡巨大表面积利于交换"]},
             "scene": "membrane_transport", "sceneArgs": {
                 "type": "diffusion", "title": "肺泡气体交换（自由扩散）"
             }},
            # Step 7
            {"tag": "结构", "name": "泌尿系统",
             "body": "<p><strong>泌尿系统</strong>由肾脏、输尿管、膀胱和尿道组成。<br>• <strong>肾脏</strong>：形成尿液的器官<br>• <strong>肾单位</strong>：肾脏的结构和功能单位，包括肾小球、肾小囊和肾小管<br>• 尿液形成经<strong>滤过→重吸收→分泌</strong>三过程</p>",
             "points": {"title": "泌尿系统", "items": ["肾单位：100万个/肾", "肾小球滤过形成原尿", "肾小管重吸收有用物质", "排出多余水分和废物"]},
             "scene": "physiology", "sceneArgs": {
                 "system": "kidney"
             }},
            # Step 8
            {"tag": "结构", "name": "消化系统",
             "body": "<p><strong>消化系统</strong>负责食物的消化和营养吸收：<br>• <strong>消化管</strong>：口腔→咽→食道→胃→小肠→大肠→肛门<br>• <strong>消化腺</strong>：唾液腺、肝脏、胰腺<br>• <strong>小肠</strong>是消化吸收的主要场所</p>",
             "points": {"title": "消化系统", "items": ["胃：蛋白质初步消化", "小肠：消化吸收主场所", "肝脏：分泌胆汁、解毒", "胰腺：分泌消化酶和胰岛素"]},
             "scene": "physiology", "sceneArgs": {
                 "system": "digestive"
             }},
            # Step 9
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>本课学习了人体循环、呼吸、泌尿和消化四大系统的结构和功能。各系统协调配合，维持人体正常生命活动。</p>",
             "points": {"title": "本课要点", "items": ["心脏四腔室结构与功能", "体循环和肺循环路径", "肺泡气体交换原理", "肾单位滤过与重吸收", "小肠是消化吸收主场所"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "❤️", "label": "循环系统", "desc": "心脏泵血\n体/肺循环", "color": "#f87171"},
                     {"icon": "🫁", "label": "呼吸系统", "desc": "气体交换\n肺泡结构", "color": "#06b6d4"},
                     {"icon": "🧻", "label": "泌尿系统", "desc": "肾单位\n滤过重吸收", "color": "#fbbf24"},
                     {"icon": "🔬", "label": "消化系统", "desc": "小肠吸收\n腺体分泌", "color": "#34d399"},
                 ]
             }},
        ]
    }


# =====================================================================
# Registry & CLI
# =====================================================================
REGISTRY = {
    "cell_structure": build_cell_structure,
    "mendel_genetics": build_mendel_genetics,
    "immune_system": build_immune_system,
    "pcr_technique": build_pcr_technique,
    "circulatory_system": build_circulatory_system,
}


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python generate.py <key> [output.html]")
        print("      python generate.py all [out_dir]")
        print("      python generate.py list")
        return

    cmd = args[0]
    if cmd == "list":
        print("已注册教程 (%d):" % len(REGISTRY))
        for k in sorted(REGISTRY):
            print("  -", k)
    elif cmd == "all":
        out_dir = Path(args[1]) if len(args) > 1 else Path.cwd()
        out_dir = Path(out_dir)
        for k, fn in sorted(REGISTRY.items()):
            spec = fn()
            out = out_dir / ("tutorial-" + k + ".html")
            render_html(spec, out)
            print("written:", out)
    else:
        fn = REGISTRY.get(cmd)
        if not fn:
            print("未知教程:", cmd, "可用:", list(REGISTRY.keys()))
            return
        spec = fn()
        out = Path(args[1]) if len(args) > 1 else Path.cwd() / ("tutorial-" + cmd + ".html")
        render_html(spec, out)
        print("written:", out)


if __name__ == "__main__":
    main()
