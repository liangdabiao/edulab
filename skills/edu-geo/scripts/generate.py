#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把地理课程 spec 注入 template/board-geo.html，产出单页交互课程。
    4 个 PoC 教程覆盖 4 个教学模块。
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board-geo.html"
PLACEHOLDER = "__TUTORIAL_DATA__"


def render_html(spec: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(spec, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


# =====================================================================
# 1) 自然地理 — 地球运动与大气
# =====================================================================
def build_physical_geo():
    return {
        "meta": {"title": "自然地理基础", "subtitle": "地球运动 · 大气环流 · 水循环 · 板块构造", "module": "physical", "accent": "cyan"},
        "cards": [
            {"num": 1, "title": "地球运动", "body": "自转·昼夜交替<br>公转·四季变化"},
            {"num": 2, "title": "大气环流", "body": "三圈环流<br>气压带风带"},
            {"num": 3, "title": "水循环", "body": "蒸发·降水<br>径流·下渗"},
            {"num": 4, "title": "板块构造", "body": "板块运动<br>地震·火山"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "地球运动",
             "body": "<p><strong>地球运动</strong>包括自转和公转两种基本形式：<br>• <strong>自转</strong>：绕地轴自西向东旋转，周期约24小时，产生昼夜交替<br>• <strong>公转</strong>：绕太阳运行，周期约365.25天，产生四季变化<br>• 地轴与轨道面成66.5°夹角，是四季形成的根本原因</p>",
             "points": {"title": "地球运动", "items": ["自转方向：自西向东", "自转周期：23时56分4秒（恒星日）", "公转轨道：椭圆", "公转周期：365.25天", "四季：春分→夏至→秋分→冬至"]},
             "scene": "globe_3d", "sceneArgs": {
                 "mode": "rotation", "title": "地球自转与昼夜交替"
             }},
            # Step 2
            {"tag": "概念", "name": "地球公转与四季",
             "body": "<p><strong>地球公转</strong>导致太阳直射点的回归运动，形成四季。太阳直射点在南北回归线之间往返运动：<br>• 春分（3.21）→ 夏至（6.22）→ 秋分（9.23）→ 冬至（12.22）→ 春分<br>• 北半球夏季时，太阳直射北回归线</p>",
             "points": {"title": "四季形成", "items": ["太阳直射点回归运动", "南北回归线：23.5°", "昼夜长短随季节变化", "五带划分：热带/温带/寒带"]},
             "scene": "globe_3d", "sceneArgs": {
                 "mode": "revolution", "title": "地球公转与四季变化"
             }},
            # Step 3
            {"tag": "结构", "name": "大气环流",
             "body": "<p><strong>全球大气环流</strong>（三圈环流）是地球上的大气运动基本模式：<br>• <strong>赤道低压带</strong>：空气受热上升，降水丰富<br>• <strong>副热带高压带</strong>（30°）：空气下沉，干燥少雨<br>• <strong>副极地低压带</strong>（60°）：气流辐合上升<br>• <strong>极地高压带</strong>（90°）：冷空气下沉</p>",
             "points": {"title": "气压带风带", "items": ["赤道低压带：高温多雨", "副热带高压带：炎热干燥", "副极地低压带：温和多雨", "极地高压带：寒冷干燥"]},
             "scene": "atmosphere", "sceneArgs": {
                 "type": "global", "title": "全球三圈环流与气压带"
             }},
            # Step 4
            {"tag": "概念", "name": "风带",
             "body": "<p>由于气压差，大气从高压流向低压，受<strong>地转偏向力</strong>影响形成盛行风带：<br>• <strong>信风带</strong>（0°-30°）：东北/东南信风<br>• <strong>西风带</strong>（30°-60°）：盛行西风<br>• <strong>极地东风</strong>（60°-90°）：极地东风</p>",
             "points": {"title": "风带特征", "items": ["信风：低纬度稳定风向", "西风带：中纬度，多气旋", "极地东风：寒冷干燥", "地转偏向力影响风向"]},
             "scene": "atmosphere", "sceneArgs": {
                 "type": "wind", "title": "全球风带分布"
             }},
            # Step 5
            {"tag": "概念", "name": "季风环流",
             "body": "<p><strong>季风</strong>是由于海陆热力性质差异导致的季节性风向变化。<br>• <strong>夏季</strong>：大陆受热快形成低压，风从海洋吹向陆地（温暖湿润）<br>• <strong>冬季</strong>：大陆冷却快形成高压，风从陆地吹向海洋（寒冷干燥）<br>东亚季风是全球最典型的季风区。</p>",
             "points": {"title": "季风成因", "items": ["海陆热力差异是主因", "夏季风：海→陆，暖湿", "冬季风：陆→海，冷干", "东亚季风最典型"]},
             "scene": "atmosphere", "sceneArgs": {
                 "type": "seasonal", "season": "summer", "title": "夏季季风"
             }},
            # Step 6
            {"tag": "过程", "name": "水循环",
             "body": "<p><strong>水循环</strong>是指水在不同圈层之间连续运动的过程，包括：<br>• <strong>蒸发</strong>：海洋/陆地水→水汽<br>• <strong>水汽输送</strong>：风将水汽带到陆地上空<br>• <strong>降水</strong>：水汽凝结降落<br>• <strong>径流</strong>：地表/地下水流回海洋<br>水循环维持了全球水量的动态平衡。</p>",
             "points": {"title": "水循环环节", "items": ["蒸发（蒸腾）", "水汽输送", "降水", "地表径流", "下渗与地下径流"]},
             "scene": "water_cycle", "sceneArgs": {
                 "title": "水循环示意图"
             }},
            # Step 7
            {"tag": "过程", "name": "板块构造",
             "body": "<p><strong>板块构造学说</strong>认为岩石圈被分为六大板块，板块在软流层上运动。<br>• <strong>汇聚边界</strong>：板块碰撞→山脉/海沟/俯冲带<br>• <strong>张裂边界</strong>：板块分离→大洋中脊/裂谷<br>• <strong>转换边界</strong>：板块水平错动→地震<br>板块运动是地震和火山的主要成因。</p>",
             "points": {"title": "板块边界类型", "items": ["汇聚：板块碰撞挤压", "张裂：板块分离", "转换：水平错动", "板块内部相对稳定"]},
             "scene": "plate_tectonics", "sceneArgs": {
                 "type": "convergent", "title": "板块汇聚边界"
             }},
            # Step 8
            {"tag": "过程", "name": "板块类型与地震",
             "body": "<p>三种板块边界各具特征：<br>• <strong>张裂边界</strong>：如大西洋中脊，岩浆上涌形成新洋壳<br>• <strong>转换边界</strong>：如圣安德烈斯断层，地震频发<br>地震波分为纵波（P波）和横波（S波），P波速度快于S波。</p>",
             "points": {"title": "板块与地震", "items": ["张裂：大洋中脊/东非大裂谷", "转换：地震多发", "板块交界=地震带", "环太平洋地震带最活跃"]},
             "scene": "plate_tectonics", "sceneArgs": {
                 "type": "divergent", "title": "板块张裂边界"
             }},
            # Step 9
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>本课学习了自然地理四大核心内容：地球运动、大气环流、水循环和板块构造。这些是理解自然环境的基础。</p>",
             "points": {"title": "本课要点", "items": ["地球自转产生昼夜，公转产生四季", "三圈环流形成全球气压带风带", "水循环维持水资源动态平衡", "板块运动塑造地表形态"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "🌍", "label": "地球运动", "desc": "自转·昼夜\n公转·四季", "color": "#06b6d4"},
                     {"icon": "🌪️", "label": "大气环流", "desc": "三圈环流\n气压带风带", "color": "#6366f1"},
                     {"icon": "💧", "label": "水循环", "desc": "蒸发·降水\n径流·下渗", "color": "#34d399"},
                     {"icon": "🏔️", "label": "板块构造", "desc": "汇聚·张裂\n转换边界", "color": "#fb923c"},
                 ]
             }},
        ]
    }


# =====================================================================
# 2) 人文地理 — 人口与城市
# =====================================================================
def build_population():
    return {
        "meta": {"title": "人口与城市", "subtitle": "人口结构 · 城市化 · 区位分析", "module": "human", "accent": "amber"},
        "cards": [
            {"num": 1, "title": "人口结构", "body": "年龄结构<br>性别结构"},
            {"num": 2, "title": "人口增长", "body": "出生率·死亡率<br>自然增长率"},
            {"num": 3, "title": "城市化", "body": "城市模型<br>功能分区"},
            {"num": 4, "title": "区位分析", "body": "农业·工业<br>交通区位"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "人口结构与金字塔",
             "body": "<p><strong>人口结构</strong>反映一个地区的人口特征，主要包括年龄结构和性别结构。<br>• <strong>人口金字塔</strong>直观显示人口年龄性别构成<br>• 三种类型：<br>  - <strong>扩张型</strong>（年轻型）：高出生率，塔基宽<br>  - <strong>稳定型</strong>：各年龄组较均衡<br>  - <strong>收缩型</strong>（老年型）：低出生率，塔基窄</p>",
             "points": {"title": "人口金字塔类型", "items": ["扩张型：高出生率，发展中国家", "稳定型：出生率适中", "收缩型：老龄化，发达国家"]},
             "scene": "population_pyramid", "sceneArgs": {
                 "title": "人口金字塔（扩张型）",
                 "data": {"male": [15, 13, 11, 9, 7, 5, 3, 2], "female": [14, 12, 10, 9, 8, 6, 4, 2]},
                 "labels": ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]
             }},
            # Step 2
            {"tag": "概念", "name": "人口增长模式",
             "body": "<p>人口增长模式反映出生率、死亡率和自然增长率的关系：<br>• <strong>原始型</strong>：高出生率、高死亡率、低增长率<br>• <strong>传统型</strong>：高出生率、低死亡率、高增长率<br>• <strong>现代型</strong>：低出生率、低死亡率、低增长率</p><p>发达国家多处于现代型，发展中国家多处于传统型向现代型的过渡阶段。</p>",
             "points": {"title": "人口增长阶段", "items": ["原始型：高高低", "传统型：高低高", "现代型：低低低", "我国已进入现代型"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "人口增长模式",
                 "items": [
                     {"icon": "🌿", "label": "原始型", "desc": "高出生率\n高死亡率\n低增长", "color": "#f87171"},
                     {"icon": "📈", "label": "传统型", "desc": "高出生率\n低死亡率\n高增长", "color": "#fb923c"},
                     {"icon": "📊", "label": "现代型", "desc": "低出生率\n低死亡率\n低增长", "color": "#34d399"},
                 ]
             }},
            # Step 3
            {"tag": "概念", "name": "人口迁移",
             "body": "<p><strong>人口迁移</strong>是人口在不同地区之间的空间移动。<br>• <strong>推力因素</strong>：迁出地的不利条件（就业难、资源短缺）<br>• <strong>拉力因素</strong>：迁入地的有利条件（就业机会、教育资源）<br>• 当前趋势：乡村→城市，欠发达地区→发达地区</p>",
             "points": {"title": "人口迁移因素", "items": ["经济因素是主因", "政策、战争等政治因素", "教育、医疗等社会因素", "自然环境影响"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "人口迁移影响因素",
                 "nodes": [
                     {"id": 0, "x": 40, "y": 80, "w": 130, "h": 44, "label": "迁出地\n(推力)", "color": "#f87171"},
                     {"id": 1, "x": 210, "y": 80, "w": 140, "h": 44, "label": "人口迁移决策", "type": "decision", "color": "#fbbf24"},
                     {"id": 2, "x": 400, "y": 80, "w": 130, "h": 44, "label": "迁入地\n(拉力)", "color": "#34d399"},
                     {"id": 3, "x": 210, "y": 160, "w": 140, "h": 44, "label": "迁移人口", "color": "#6366f1"},
                 ],
                 "edges": [[0, 1], [2, 1], [1, 3]]
             }},
            # Step 4
            {"tag": "结构", "name": "城市空间结构",
             "body": "<p>城市内部具有不同的功能分区：<br>• <strong>商业区</strong>：位于市中心，交通便捷<br>• <strong>住宅区</strong>：城市中面积最大的功能区<br>• <strong>工业区</strong>：靠近交通线，位于城市边缘<br><br>三种城市结构模型解释了城市内部的布局规律。</p>",
             "points": {"title": "城市功能区", "items": ["商业区：CBD核心", "住宅区：面积最大", "工业区：城市外围", "各功能区相互联系"]},
             "scene": "urban_model", "sceneArgs": {
                 "type": "concentric", "title": "同心圆城市模型"
             }},
            # Step 5
            {"tag": "对比", "name": "城市结构模型对比",
             "body": "<p>三种经典城市结构模型：<br>• <strong>同心圆模型</strong>（伯吉斯）：从CBD向外扩展<br>• <strong>扇形模型</strong>（霍伊特）：沿交通线呈扇状分布<br>• <strong>多核心模型</strong>：多个功能中心并存<br>实际城市往往融合多种模型特征。</p>",
             "points": {"title": "模型对比", "items": ["同心圆：圈层扩展", "扇形：交通线导向", "多核心：多个中心"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "城市结构模型",
                 "left": {"title": "同心圆", "color": "#f87171", "items": ["CBD核心", "圈层扩展", "伯吉斯提出"]},
                 "right": {"title": "多核心", "color": "#34d399", "items": ["多个中心", "功能分散", "哈里斯提出"]},
             }},
            # Step 6
            {"tag": "概念", "name": "城市化",
             "body": "<p><strong>城市化</strong>是农村人口向城市转移、城市规模扩大的过程。<br>• 发达国家：城市化水平高（>70%），进入成熟期<br>• 发展中国家：城市化速度快，水平中等<br>• <strong>郊区城市化</strong>：人口从市中心迁往郊区<br>• <strong>逆城市化</strong>：人口从城市迁往乡村</p>",
             "points": {"title": "城市化特征", "items": ["城市人口比重上升", "城市用地规模扩大", "产业向城市集中", "城市化水平差异大"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "城市化进程",
                 "items": [
                     {"icon": "🏙️", "label": "初期阶段", "desc": "水平低\n速度慢", "color": "#f87171"},
                     {"icon": "📈", "label": "加速阶段", "desc": "人口快速\n向城市集中", "color": "#fb923c"},
                     {"icon": "🏛️", "label": "成熟阶段", "desc": "水平高\n速度趋缓", "color": "#34d399"},
                     {"icon": "🔄", "label": "郊区/逆城市化", "desc": "向郊区\n乡村扩散", "color": "#6366f1"},
                 ]
             }},
            # Step 7
            {"tag": "概念", "name": "农业区位因素",
             "body": "<p><strong>农业区位</strong>指影响农业布局的自然和社会经济因素。<br>• <strong>自然因素</strong>：气候、地形、土壤、水源<br>• <strong>社会经济因素</strong>：市场、交通、政策、劳动力、科技<br>• 靠近城市的郊区发展都市农业（乳畜、花卉、蔬菜）</p>",
             "points": {"title": "区位因素", "items": ["气候决定作物类型", "市场决定生产规模", "交通影响产品流通", "政策引导产业布局"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "农业区位因素",
                 "items": [
                     {"icon": "☀️", "label": "自然因素", "desc": "气候·地形\n土壤·水源", "color": "#34d399"},
                     {"icon": "🏪", "label": "市场", "desc": "需求决定\n生产类型", "color": "#f87171"},
                     {"icon": "🚛", "label": "交通", "desc": "物流运输\n保鲜能力", "color": "#6366f1"},
                     {"icon": "🔧", "label": "科技", "desc": "良种·化肥\n灌溉技术", "color": "#06b6d4"},
                 ]
             }},
            # Step 8
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>本课学习了人口结构、人口增长模式、城市化过程和区位分析等核心人文地理概念。</p>",
             "points": {"title": "本课要点", "items": ["人口金字塔反映年龄性别结构", "人口增长三阶段模型", "城市化三阶段特征", "城市功能分区与结构模型", "农业区位自然和社会经济因素"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "👥", "label": "人口结构", "desc": "金字塔\n增长模式", "color": "#f87171"},
                     {"icon": "🏙️", "label": "城市化", "desc": "城市模型\n功能区", "color": "#6366f1"},
                     {"icon": "🌾", "label": "农业区位", "desc": "自然因素\n社会经济", "color": "#34d399"},
                     {"icon": "🏭", "label": "工业区位", "desc": "原料·市场\n交通·政策", "color": "#fbbf24"},
                 ]
             }},
        ]
    }


# =====================================================================
# 3) 区域地理 — 中国地理
# =====================================================================
def build_china_geo():
    return {
        "meta": {"title": "中国地理", "subtitle": "自然环境 · 行政区划 · 经济分区", "module": "regional", "accent": "emerald"},
        "cards": [
            {"num": 1, "title": "疆域", "body": "陆域960万km²<br>海域470万km²"},
            {"num": 2, "title": "地形", "body": "三级阶梯<br>多样地形"},
            {"num": 3, "title": "气候", "body": "季风气候<br>东西差异"},
            {"num": 4, "title": "分区", "body": "四大地理分区<br>经济区划"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "中国疆域与行政区划",
             "body": "<p><strong>中国</strong>位于亚洲东部、太平洋西岸。<br>• 陆地面积约960万km²，世界第三<br>• 海域面积约470万km²<br>• 34个省级行政单位（23省、4直辖市、5自治区、2特别行政区）<br>• 北起漠河，南至曾母暗沙，跨约50个纬度</p>",
             "points": {"title": "疆域要点", "items": ["经纬度：4°N-53°N, 73°E-135°E", "陆上邻国14个", "海岸线1.8万km", "东五区至东九区"]},
             "scene": "map_chart", "sceneArgs": {
                 "region": "china", "title": "中国疆域略图",
                 "markers": [
                     {"x": 0.53, "y": 0.18, "label": "北京"},
                     {"x": 0.78, "y": 0.75, "label": "南海"},
                 ]
             }},
            # Step 2
            {"tag": "结构", "name": "中国地形",
             "body": "<p><strong>中国地形</strong>呈三级阶梯分布：<br>• <strong>第一阶梯</strong>：青藏高原（平均4000m以上），世界屋脊<br>• <strong>第二阶梯</strong>：高原盆地（1000-2000m）<br>• <strong>第三阶梯</strong>：平原丘陵（500m以下）<br><br>主要山脉有喜马拉雅山、天山、秦岭、大兴安岭等。</p>",
             "points": {"title": "地形特征", "items": ["西高东低三级阶梯", "地形类型多样", "山区面积占2/3", "主要山脉构成骨架"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "中国三级阶梯",
                 "nodes": [
                    {"id": 0, "x": 100, "y": 60, "w": 150, "h": 44, "label": "第一阶梯\n青藏高原 4000m+", "color": "#f87171"},
                    {"id": 1, "x": 100, "y": 140, "w": 150, "h": 44, "label": "第二阶梯\n高原盆地 1000-2000m", "color": "#fb923c"},
                    {"id": 2, "x": 100, "y": 220, "w": 150, "h": 44, "label": "第三阶梯\n平原丘陵 <500m", "color": "#34d399"},
                    {"id": 3, "x": 320, "y": 100, "w": 160, "h": 44, "label": "昆仑山-祁连山", "type": "io", "color": "#6366f1"},
                    {"id": 4, "x": 320, "y": 170, "w": 160, "h": 44, "label": "大兴安岭-太行山", "type": "io", "color": "#6366f1"},
                 ],
                 "edges": [[0, 3], [3, 1], [1, 4], [4, 2]]
             }},
            # Step 3
            {"tag": "概念", "name": "中国气候",
             "body": "<p>中国气候的主要特征：<br>• <strong>季风气候显著</strong>：东部广大地区受季风影响<br>• <strong>温度带</strong>：热带→亚热带→暖温带→中温带→寒温带<br>• <strong>干湿区</strong>：湿润区→半湿润→半干旱→干旱区<br>• 年降水量从东南沿海（>1600mm）向西北内陆（<200mm）递减</p>",
             "points": {"title": "气候特征", "items": ["季风气候为主", "雨热同期", "降水东多西少", "温度南北差异大"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "中国气候特征",
                 "items": [
                     {"icon": "🌧️", "label": "季风气候", "desc": "夏季高温多雨\n冬季寒冷干燥", "color": "#06b6d4"},
                     {"icon": "🌡️", "label": "温度带", "desc": "热带→亚热带\n→温带→寒温带", "color": "#f87171"},
                     {"icon": "💧", "label": "干湿分区", "desc": "湿润→半湿润\n→半干旱→干旱", "color": "#6366f1"},
                     {"icon": "📊", "label": "降水分布", "desc": "东南沿海多\n西北内陆少", "color": "#34d399"},
                 ]
             }},
            # Step 4
            {"tag": "结构", "name": "中国主要河流",
             "body": "<p>中国河湖众多，主要水系：<br>• <strong>长江</strong>：全长6300km，世界第三，自西向东注入东海<br>• <strong>黄河</strong>：全长5464km，含沙量大，\"地上河\"<br>• 其他重要河流：珠江、淮河、松花江、塔里木河（内流河）<br>• 外流区约占全国面积的2/3。</p>",
             "points": {"title": "主要河流", "items": ["长江：中国第一大河", "黄河：含沙量最大的河", "珠江：南方重要水系", "塔里木河：最大内流河"]},
             "scene": "map_chart", "sceneArgs": {
                 "region": "china", "title": "中国主要河流",
                 "markers": [
                     {"x": 0.47, "y": 0.5, "label": "长江"},
                     {"x": 0.48, "y": 0.28, "label": "黄河"},
                 ]
             }},
            # Step 5
            {"tag": "概念", "name": "四大地理分区",
             "body": "<p>根据自然和人文特征，中国分为四大地理分区：<br>• <strong>北方地区</strong>：秦岭-淮河以北，温带季风气候，小麦为主<br>• <strong>南方地区</strong>：秦岭-淮河以南，亚热带/热带季风，水稻为主<br>• <strong>西北地区</strong>：干旱半干旱，畜牧业为主<br>• <strong>青藏地区</strong>：高寒，独特的高原文化</p>",
             "points": {"title": "四大分区", "items": ["北方：华北平原、东北平原", "南方：长江中下游、珠三角", "西北：草原荒漠、绿洲农业", "青藏：高寒牧区、河谷农业"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "四大地理分区",
                 "items": [
                     {"icon": "🌾", "label": "北方地区", "desc": "温带季风\n小麦·旱作", "color": "#fbbf24"},
                     {"icon": "🌾", "label": "南方地区", "desc": "亚热带季风\n水稻·水田", "color": "#34d399"},
                     {"icon": "🏜️", "label": "西北地区", "desc": "干旱半干旱\n草原·绿洲", "color": "#fb923c"},
                     {"icon": "🏔️", "label": "青藏地区", "desc": "高寒气候\n牧区·河谷", "color": "#6366f1"},
                 ]
             }},
            # Step 6
            {"tag": "概念", "name": "交通与城市",
             "body": "<p>中国交通网络和城市体系：<br>• <strong>铁路</strong>：京沪线、京广线、陇海-兰新线等主要干线<br>• <strong>公路</strong>：高速公路里程世界第一<br>• <strong>港口</strong>：上海港、宁波舟山港等世界级港口<br>• <strong>城市群</strong>：长三角、珠三角、京津冀、成渝等</p>",
             "points": {"title": "交通与城市", "items": ["铁路网以北京为中心", "高速公路网络密集", "沿海港口群发达", "城市群带动区域发展"]},
             "scene": "map_chart", "sceneArgs": {
                 "region": "china", "title": "中国主要城市",
                 "markers": [
                     {"x": 0.53, "y": 0.18, "label": "北京"},
                     {"x": 0.68, "y": 0.62, "label": "上海"},
                     {"x": 0.57, "y": 0.72, "label": "广州"},
                     {"x": 0.42, "y": 0.60, "label": "武汉"},
                     {"x": 0.40, "y": 0.55, "label": "重庆"},
                 ]
             }},
            # Step 7
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>中国地理是区域地理的核心内容，理解我国的自然环境、资源分布和经济格局对把握国情至关重要。</p>",
             "points": {"title": "本课要点", "items": ["三级阶梯地形特征", "季风气候与降水分异", "四大地理分区特点", "主要河流与经济区"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "🗺️", "label": "疆域地形", "desc": "三级阶梯\n多样地形", "color": "#34d399"},
                     {"icon": "🌤️", "label": "气候", "desc": "季风显著\n东湿西干", "color": "#06b6d4"},
                     {"icon": "🏘️", "label": "四大分区", "desc": "南北差异\n东西差异", "color": "#6366f1"},
                     {"icon": "🏙️", "label": "经济", "desc": "城市群\n交通网", "color": "#fbbf24"},
                 ]
             }},
        ]
    }


# =====================================================================
# 4) 地理信息技术 — RS/GPS/GIS
# =====================================================================
def build_gis_tech():
    return {
        "meta": {"title": "地理信息技术", "subtitle": "RS · GPS · GIS · 数字地球", "module": "geo_it", "accent": "sky"},
        "cards": [
            {"num": 1, "title": "RS 遥感", "body": "获取地表信息<br>远距离感知"},
            {"num": 2, "title": "GPS 定位", "body": "全球定位<br>精准导航"},
            {"num": 3, "title": "GIS 分析", "body": "空间分析<br>图层叠加"},
            {"num": 4, "title": "综合应用", "body": "数字地球<br>智慧城市"},
        ],
        "steps": [
            # Step 1
            {"tag": "概念", "name": "地理信息技术概述",
             "body": "<p><strong>地理信息技术</strong>是获取、管理、分析和应用地理信息的现代技术，包括三大核心：<br>• <strong>RS</strong>（遥感）—— 远距离获取地表信息<br>• <strong>GPS</strong>（全球定位系统）—— 确定地面点的精确位置<br>• <strong>GIS</strong>（地理信息系统）—— 分析处理空间数据</p><p>三者的结合称为3S技术。</p>",
             "points": {"title": "3S技术", "items": ["RS：快速获取大面积信息", "GPS：全球覆盖定位导航", "GIS：空间数据管理与分析", "3S技术相互融合"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "3S技术",
                 "items": [
                     {"icon": "🛰️", "label": "RS 遥感", "desc": "远距离感知\n地表信息", "color": "#34d399"},
                     {"icon": "📡", "label": "GPS 定位", "desc": "全球定位\n24颗卫星", "color": "#6366f1"},
                     {"icon": "💻", "label": "GIS 分析", "desc": "空间数据\n处理分析", "color": "#fbbf24"},
                     {"icon": "🌐", "label": "数字地球", "desc": "3S融合\n智慧应用", "color": "#06b6d4"},
                 ]
             }},
            # Step 2
            {"tag": "概念", "name": "RS 遥感技术",
             "body": "<p><strong>遥感（RS）</strong>利用传感器远距离探测地表物体反射或辐射的电磁波。<br>• 搭载平台：卫星、飞机、无人机<br>• 应用领域：气象预报、资源调查、环境监测、农业估产<br>• 不同地物在不同波段有不同反射特征</p>",
             "points": {"title": "RS要点", "items": ["通过电磁波获取信息", "多波段多时相", "大范围快速监测", "不可替代的灾情评估"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "遥感工作原理",
                 "blocks": [
                     {"x": 35, "y": 50, "w": 130, "h": 44, "label": "卫星传感器", "color": "#6366f1"},
                     {"x": 200, "y": 50, "w": 130, "h": 44, "label": "电磁波信号", "color": "#06b6d4"},
                     {"x": 365, "y": 50, "w": 130, "h": 44, "label": "地面接收站", "color": "#34d399"},
                     {"x": 530, "y": 50, "w": 130, "h": 44, "label": "数据分析", "color": "#fbbf24"},
                 ],
                 "arrows": [
                     {"x1": 165, "y1": 72, "x2": 195, "y2": 72, "color": "#94a3b8"},
                     {"x1": 330, "y1": 72, "x2": 360, "y2": 72, "color": "#94a3b8"},
                     {"x1": 495, "y1": 72, "x2": 525, "y2": 72, "color": "#94a3b8"},
                 ]
             }},
            # Step 3
            {"tag": "概念", "name": "GPS 全球定位系统",
             "body": "<p><strong>GPS</strong>由三部分组成：<br>• <strong>空间部分</strong>：24颗卫星分布在6个轨道面上<br>• <strong>地面控制</strong>：监测卫星运行状态<br>• <strong>用户设备</strong>：GPS接收机</p><p>工作原理：通过接收至少4颗卫星的信号，计算三维坐标（经度、纬度、高度）和时间。民用精度可达2-5米。</p>",
             "points": {"title": "GPS要点", "items": ["至少4颗卫星定位", "三维定位+时间", "全球全天候", "免费开放使用"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "GPS系统组成",
                 "items": [
                     {"icon": "🛰️", "label": "空间部分", "desc": "24颗卫星\n6个轨道面", "color": "#6366f1"},
                     {"icon": "🏗️", "label": "地面控制", "desc": "主控站\n监测站", "color": "#fbbf24"},
                     {"icon": "📱", "label": "用户设备", "desc": "GPS接收机\n导航终端", "color": "#34d399"},
                     {"icon": "🌍", "label": "工作原理", "desc": "三角定位\n距离交会", "color": "#06b6d4"},
                 ]
             }},
            # Step 4
            {"tag": "概念", "name": "GIS 地理信息系统",
             "body": "<p><strong>GIS</strong>是采集、存储、管理、分析和显示地理空间数据的计算机系统。<br>• 核心功能：<br>  - 数据采集与输入<br>  - 空间数据管理<br>  - 空间分析与查询<br>  - 可视化表达与输出<br>• GIS区别于普通地图的关键：<strong>空间分析能力</strong></p>",
             "points": {"title": "GIS功能", "items": ["数据管理：海量空间数据", "空间查询：位置/属性", "空间分析：缓冲区/叠加", "可视化：专题地图"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "GIS核心功能",
                 "items": [
                     {"icon": "📋", "label": "数据采集", "desc": "地图数字化\n遥感数据", "color": "#6366f1"},
                     {"icon": "🗄️", "label": "数据管理", "desc": "存储/检索\n空间数据库", "color": "#06b6d4"},
                     {"icon": "🔍", "label": "空间分析", "desc": "叠加分析\n缓冲区分析", "color": "#34d399"},
                     {"icon": "📊", "label": "可视化", "desc": "专题地图\n三维显示", "color": "#fbbf24"},
                 ]
             }},
            # Step 5
            {"tag": "演示", "name": "GIS图层叠加分析",
             "body": "<p><strong>图层叠加</strong>是GIS最核心的分析方法之一。将不同专题的数据层叠加在一起，可以揭示空间要素之间的关系，为决策提供支持。</p><p>应用示例：<br>• 选择建厂地址：叠加交通、人口、地价图层<br>• 灾害评估：叠加地形、降水、人口密度图层<br>• 城市规划：叠加现有设施、用地规划图层</p>",
             "points": {"title": "叠加分析", "items": ["不同专题层空间对齐", "发现要素间关系", "多因素综合分析", "辅助科学决策"]},
             "scene": "gis_layers", "sceneArgs": {
                 "title": "GIS 图层叠加原理",
                 "layers": ["遥感影像", "地形高程", "行政区划", "交通路网", "土地利用"]
             }},
            # Step 6
            {"tag": "概念", "name": "RS与GPS综合应用",
             "body": "<p>RS和GPS在实际应用中常相互配合：<br>• <strong>精准农业</strong>：RS监测作物生长 + GPS精准施肥<br>• <strong>灾害监测</strong>：RS获取灾情影像 + GPS定位受灾点<br>• <strong>导航服务</strong>：GPS定位 + GIS电子地图<br>• <strong>智慧城市</strong>：3S集成应用于交通、环境、安防</p>",
             "points": {"title": "综合应用", "items": ["RS提供实时影像", "GPS提供精确位置", "GIS提供分析平台", "3S融合成数字地球"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "3S技术应用场景",
                 "left": {"title": "传统方法", "color": "#f87171", "items": ["人工实地调查", "纸质地图分析", "经验判断决策", "更新周期长"]},
                 "right": {"title": "3S技术", "color": "#34d399", "items": ["遥感大范围监测", "GPS精准定位", "GIS空间分析", "实时动态更新"]},
             }},
            # Step 7
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>地理信息技术是21世纪的重要技术领域。RS、GPS、GIS三者结合，为资源管理、城市规划、环境监测、灾害评估等提供了强大的工具。</p>",
             "points": {"title": "本课要点", "items": ["RS：远距离获取地表电磁波信息", "GPS：全球定位，至少4颗卫星", "GIS：空间数据管理与分析", "图层叠加是GIS核心分析方法"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "本课总结",
                 "items": [
                     {"icon": "🛰️", "label": "RS遥感", "desc": "多波段成像\n大范围监测", "color": "#34d399"},
                     {"icon": "📡", "label": "GPS定位", "desc": "三角定位\n全球覆盖", "color": "#6366f1"},
                     {"icon": "💻", "label": "GIS分析", "desc": "空间分析\n图层叠加", "color": "#fbbf24"},
                     {"icon": "🌐", "label": "综合应用", "desc": "数字地球\n智慧城市", "color": "#06b6d4"},
                 ]
             }},
        ]
    }


# =====================================================================
# Registry & CLI
# =====================================================================
REGISTRY = {
    "physical_geo": build_physical_geo,
    "population": build_population,
    "china_geo": build_china_geo,
    "gis_tech": build_gis_tech,
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
