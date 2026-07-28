#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把教程 spec 注入 template/tutorial.html，产出单页交互课程。

用法：
    python3 scripts/generate.py <教程key> [输出.html]
    python3 scripts/generate.py list
    python3 scripts/generate.py all <输出目录>
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "tutorial.html"
PLACEHOLDER = "__TUTORIAL_DATA__"


def render_html(spec: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(spec, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


# =====================================================================
# 1) 氧化还原方程式配平（化合价升降法 · 电子守恒 · 双线桥）
# =====================================================================
def build_redox_balancing():
    return {
        "meta": {
            "title": "氧化还原方程式配平",
            "subtitle": "化合价升降法 · 电子守恒 · 双线桥",
            "language": "zh-CN",
            "accent": "amber",
        },
        "cards": [
            {"num": 1, "title": "核心原理", "body": "化合价升降总数相等<br>得失电子守恒"},
            {"num": 2, "title": "配平步骤", "body": "标价→找升降→<br>最小公倍数→定系数"},
            {"num": 3, "title": "双线桥", "body": "同元素间连线<br>标注得/失e⁻"},
            {"num": 4, "title": "本质", "body": "电子转移<br>氧化剂+还原剂"},
        ],
        "steps": [
            # ===== 基础概念 =====
            {
                "tag": "概念", "name": "什么是氧化还原反应",
                "body": "<p><strong>氧化还原反应</strong>的本质是<strong>电子转移</strong>："
                        "失电子 → 化合价<strong>升高</strong>（氧化），得电子 → 化合价<strong>降低</strong>（还原）。</p>"
                        "<p>特征：反应前后元素<strong>化合价发生变化</strong>。</p>",
                "points": {
                    "title": "核心概念",
                    "items": [
                        "<strong>氧化</strong>：失电子，化合价升高",
                        "<strong>还原</strong>：得电子，化合价降低",
                        "<strong>氧化剂</strong>：得电子的物质（本身被还原）",
                        "<strong>还原剂</strong>：失电子的物质（本身被氧化）",
                    ]
                },
                "scene": "concept",
                "sceneArgs": {"title": "氧化还原反应本质", "items": [
                    {"label": "氧化", "desc": "失 e⁻ · 化合价↑", "color": "#ef4444"},
                    {"label": "还原", "desc": "得 e⁻ · 化合价↓", "color": "#34d399"},
                    {"label": "氧化剂", "desc": "得 e⁻ 物质 · 被还原", "color": "#fbbf24"},
                    {"label": "还原剂", "desc": "失 e⁻ 物质 · 被氧化", "color": "#06b6d4"},
                ]}
            },
            {
                "tag": "概念", "name": "化合价判断规则",
                "body": "<p>化合价是元素在化合物中表现出的<strong>电荷数</strong>：</p>"
                        "<p>单质中元素化合价为 <strong>0</strong>；化合物中正负化合价代数和为 <strong>0</strong>；"
                        "离子化合物中，化合价 = 离子电荷。</p>",
                "points": {
                    "title": "常见化合价速记",
                    "items": [
                        "<strong>H</strong>：+1（金属氢化物中 -1）",
                        "<strong>O</strong>：-2（过氧化物中 -1）",
                        "<strong>金属</strong>：Na⁺ K⁺ +1，Mg²⁺ Ca²⁺ +2，Al³⁺ +3",
                        "<strong>Cl</strong>：-1（含氧酸根中 +1~+7）",
                    ]
                },
                "scene": "valences",
                "sceneArgs": {
                    "elements": [
                        {"el": "H", "v": "+1", "example": "H₂O"},
                        {"el": "O", "v": "-2", "example": "H₂O"},
                        {"el": "Na", "v": "+1", "example": "NaCl"},
                        {"el": "Cu", "v": "+2", "example": "CuO"},
                        {"el": "Fe", "v": "+2/+3", "example": "Fe₂O₃"},
                        {"el": "Cl", "v": "-1", "example": "HCl"},
                        {"el": "Mn", "v": "+7", "example": "KMnO₄"},
                        {"el": "S", "v": "+4/+6", "example": "H₂SO₄"},
                    ]
                }
            },
            {
                "tag": "概念", "name": "配平五步法",
                "body": "<p><strong>化合价升降法</strong>配平氧化还原方程式：</p>"
                        "<p><strong>① 标化合价</strong> → ② <strong>找升降</strong> → "
                        "③ 求<strong>最小公倍数</strong>（电子守恒）→ ④ <strong>定系数</strong> → ⑤ <strong>检查守恒</strong></p>",
                "points": {
                    "title": "五步详解",
                    "items": [
                        "① <strong>标注</strong>：标出各元素反应前后化合价",
                        "② <strong>找升降</strong>：找出化合价变化的元素",
                        "③ <strong>最小公倍数</strong>：使升降总数相等（电子守恒）",
                        "④ <strong>定系数</strong>：按最小公倍数确定化学计量数",
                        "⑤ <strong>检查</strong>：原子守恒 + 电荷守恒",
                    ]
                },
                "scene": "steps_diagram",
                "sceneArgs": {
                    "steps": ["标价", "找升降", "公倍数", "定系数", "检验"],
                    "active": -1
                }
            },
            # ===== 示例 1：CuO + H₂ =====
            {
                "tag": "示例1", "name": "CuO + H₂ → Cu + H₂O",
                "body": "<p><strong>CuO + H₂ → Cu + H₂O</strong></p>"
                        "<p>Cu：<strong>+2 → 0</strong>（还原，得 <strong>2e⁻</strong>）</p>"
                        "<p>H：<strong>0 → +1</strong>（氧化，失 <strong>1e⁻ × 2 = 2e⁻</strong>）</p>"
                        "<p>电子守恒：2e⁻，系数已为 1:1:1:1 ✓</p>",
                "points": {
                    "title": "配平分析",
                    "items": [
                        "<strong>CuO</strong>：Cu +2→0，得 2e⁻（还原，氧化剂）",
                        "<strong>H₂</strong>：H 0→+1，失 1e⁻×2=2e⁻（氧化，还原剂）",
                        "<strong>电子守恒</strong>：得失电子数相等 ✓",
                        "<strong>配平结果</strong>：CuO + H₂ → Cu + H₂O",
                    ]
                },
                "scene": "redox_bridge",
                "sceneArgs": {
                    "equation": "CuO + H₂ → Cu + H₂O",
                    "bridges": [
                        {"from": "Cu", "fromV": "+2", "to": "Cu", "toV": "0", "color": "#34d399",
                         "label": "得 2e⁻", "side": "top", "desc": "还原"},
                        {"from": "H₂", "fromV": "0", "to": "H", "toV": "+1", "color": "#ef4444",
                         "label": "失 1e⁻×2", "side": "bottom", "desc": "氧化"},
                    ]
                }
            },
            # ===== 示例 2：Fe + CuSO₄ =====
            {
                "tag": "示例2", "name": "Fe + CuSO₄ → FeSO₄ + Cu",
                "body": "<p><strong>Fe + CuSO₄ → FeSO₄ + Cu</strong></p>"
                        "<p>Fe：<strong>0 → +2</strong>（氧化，失 <strong>2e⁻</strong>）</p>"
                        "<p>Cu：<strong>+2 → 0</strong>（还原，得 <strong>2e⁻</strong>）</p>"
                        "<p>电子守恒：2e⁻ ✓</p>",
                "points": {
                    "title": "配平分析",
                    "items": [
                        "<strong>Fe</strong>：0→+2，失 2e⁻（氧化，还原剂）",
                        "<strong>CuSO₄</strong>：Cu +2→0，得 2e⁻（还原，氧化剂）",
                        "<strong>电子守恒</strong>：得失电子数相等 ✓",
                        "<strong>现象</strong>：铁钉表面析出红色铜",
                    ]
                },
                "scene": "redox_bridge",
                "sceneArgs": {
                    "equation": "Fe + CuSO₄ → FeSO₄ + Cu",
                    "bridges": [
                        {"from": "Fe", "fromV": "0", "to": "Fe", "toV": "+2", "color": "#ef4444",
                         "label": "失 2e⁻", "side": "top", "desc": "氧化"},
                        {"from": "Cu", "fromV": "+2", "to": "Cu", "toV": "0", "color": "#34d399",
                         "label": "得 2e⁻", "side": "bottom", "desc": "还原"},
                    ]
                }
            },
            # ===== 示例 3：Fe₂O₃ + CO =====
            {
                "tag": "示例3", "name": "Fe₂O₃ + CO → Fe + CO₂",
                "body": "<p><strong>Fe₂O₃ + 3CO → 2Fe + 3CO₂</strong></p>"
                        "<p>Fe：<strong>+3 → 0</strong>（还原，得 <strong>3e⁻ × 2 = 6e⁻</strong>）</p>"
                        "<p>C：<strong>+2 → +4</strong>（氧化，失 <strong>2e⁻ × 3 = 6e⁻</strong>）</p>"
                        "<p>最小公倍数：6 ✓</p>",
                "points": {
                    "title": "配平分析",
                    "items": [
                        "<strong>Fe₂O₃</strong>：Fe +3→0，得 3e⁻×2=6e⁻（氧化剂）",
                        "<strong>CO</strong>：C +2→+4，失 2e⁻×3=6e⁻（还原剂）",
                        "<strong>最小公倍数</strong>：6（3×2=6，2×3=6）",
                        "<strong>配平结果</strong>：Fe₂O₃ + 3CO → 2Fe + 3CO₂",
                    ]
                },
                "scene": "redox_bridge",
                "sceneArgs": {
                    "equation": "Fe₂O₃ + 3CO → 2Fe + 3CO₂",
                    "bridges": [
                        {"from": "Fe", "fromV": "+3", "to": "Fe", "toV": "0", "color": "#34d399",
                         "label": "得 3e⁻×2", "side": "top", "desc": "还原"},
                        {"from": "C", "fromV": "+2", "to": "C", "toV": "+4", "color": "#ef4444",
                         "label": "失 2e⁻×3", "side": "bottom", "desc": "氧化"},
                    ]
                }
            },
            # ===== 示例 4：KMnO₄ + HCl（复杂） =====
            {
                "tag": "示例4", "name": "KMnO₄ + HCl（复杂配平）",
                "body": "<p><strong>2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂ + 8H₂O</strong></p>"
                        "<p>Mn：<strong>+7 → +2</strong>（还原，得 <strong>5e⁻ × 2 = 10e⁻</strong>）</p>"
                        "<p>Cl：<strong>-1 → 0</strong>（氧化，失 <strong>1e⁻ × 10 = 10e⁻</strong>）</p>"
                        "<p>10e⁻ 守恒 ✓。注意 Cl 部分被氧化、部分进 KCl/MnCl₂</p>",
                "points": {
                    "title": "复杂配平要点",
                    "items": [
                        "<strong>Mn</strong>：+7→+2，得 5e⁻×2=10e⁻（氧化剂）",
                        "<strong>HCl</strong>：Cl -1→0，失 1e⁻×10=10e⁻（还原剂，部分）",
                        "<strong>关键</strong>：16HCl 仅 10 个 Cl⁻ 被氧化为 Cl₂",
                        "<strong>另 6 个 Cl⁻</strong>：2 进 KCl，4 进 MnCl₂（化合价不变）",
                    ]
                },
                "scene": "redox_bridge",
                "sceneArgs": {
                    "equation": "2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂ + 8H₂O",
                    "bridges": [
                        {"from": "Mn", "fromV": "+7", "to": "Mn", "toV": "+2", "color": "#34d399",
                         "label": "得 5e⁻×2", "side": "top", "desc": "还原"},
                        {"from": "Cl", "fromV": "-1", "to": "Cl", "toV": "0", "color": "#ef4444",
                         "label": "失 1e⁻×10", "side": "bottom", "desc": "氧化"},
                    ]
                }
            },
            # ===== 方法总结 =====
            {
                "tag": "总结", "name": "配平技巧与口诀",
                "body": "<p><strong>配平口诀</strong>：</p>"
                        "<p><code>标变找升降，求小倍定系数；查守恒看电荷，最后氢氧补全。</code></p>"
                        "<p><strong>双线桥画法</strong>：</p>"
                        "<p>① 找出化合价变化的同种元素<br>"
                        "② 反应物指向产物（同元素间连线）<br>"
                        "③ 桥上标：得/失 × n 个 e⁻<br>"
                        "④ 标注氧化/还原反应</p>",
                "points": {
                    "title": "速记卡片",
                    "items": [
                        "<strong>化合价口诀</strong>：一价钾钠氯氢银，二价氧钙钡镁锌",
                        "<strong>得失电子</strong>：失 e⁻ 升价氧化 → 还原剂",
                        "<strong>双线桥</strong>：同元素连线，标注电子数",
                        "<strong>单线桥</strong>：从还原剂指向氧化剂",
                    ]
                },
                "scene": "summary_grid",
                "sceneArgs": {
                    "items": [
                        {"icon": "①", "title": "标价", "desc": "标出各元素化合价", "color": "#a78bfa"},
                        {"icon": "②", "title": "找升降", "desc": "找出变化元素", "color": "#06b6d4"},
                        {"icon": "③", "title": "公倍数", "desc": "升降相等（电子守恒）", "color": "#34d399"},
                        {"icon": "④", "title": "定系数", "desc": "按最小公倍数", "color": "#fbbf24"},
                        {"icon": "⑤", "title": "双线桥", "desc": "同元素连线标注", "color": "#f87171"},
                        {"icon": "⑥", "title": "检验", "desc": "原子+电荷守恒", "color": "#fb923c"},
                    ]
                }
            },
            # ===== 练习环节 =====
            {
                "tag": "练习", "name": "自主练习",
                "body": "<p>尝试用化合价升降法配平以下方程式：</p>"
                        "<p><strong>①</strong> Al + O₂ → Al₂O₃</p>"
                        "<p><strong>②</strong> Cl₂ + NaOH → NaCl + NaClO + H₂O</p>"
                        "<p><strong>③</strong> Cu + HNO₃（稀）→ Cu(NO₃)₂ + NO + H₂O</p>"
                        "<p>提示：标化合价 → 找升降 → 最小公倍数 → 定系数 → 检查</p>",
                "points": {
                    "title": "参考答案",
                    "items": [
                        "① <strong>4Al + 3O₂ → 2Al₂O₃</strong>",
                        "② <strong>Cl₂ + 2NaOH → NaCl + NaClO + H₂O</strong>",
                        "③ <strong>3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO + 4H₂O</strong>",
                    ]
                },
                "scene": "equation",
                "sceneArgs": {
                    "equations": [
                        "Al + O₂ → Al₂O₃",
                        "Cl₂ + NaOH → NaCl + NaClO + H₂O",
                        "Cu + HNO₃ → Cu(NO₃)₂ + NO + H₂O",
                    ],
                    "showAnswers": False
                }
            },
        ],
    }


# =====================================================================
# 2) 金属活动性顺序（置换反应 · 金属与酸/盐）
# =====================================================================
def build_metal_activity():
    return {
        "meta": {
            "title": "金属活动性顺序",
            "subtitle": "K Ca Na Mg Al Zn Fe Sn Pb (H) Cu Hg Ag Pt Au",
            "language": "zh-CN",
            "accent": "emerald",
        },
        "cards": [
            {"num": 1, "title": "活动性顺序", "body": "K Ca Na Mg Al<br>Zn Fe Sn Pb (H)<br>Cu Hg Ag Pt Au"},
            {"num": 2, "title": "规律", "body": "左→右减弱<br>前置换后"},
            {"num": 3, "title": "与酸反应", "body": "H 前金属置换 H₂<br>H 后不反应"},
            {"num": 4, "title": "与盐反应", "body": "前金属置换后金属<br>需可溶性盐"},
        ],
        "steps": [
            {
                "tag": "基础", "name": "金属活动性顺序表",
                "body": "<p><strong>金属活动性顺序</strong>（由强到弱）：</p>"
                        "<p><code>K Ca Na Mg Al Zn Fe Sn Pb (H) Cu Hg Ag Pt Au</code></p>"
                        "<p>位置越<strong>靠左</strong>，金属活动性越<strong>强</strong>，"
                        "越易失去电子变成阳离子。</p>",
                "points": {
                    "title": "记忆口诀",
                    "items": [
                        "<strong>口诀</strong>：钾钙钠镁铝，锌铁锡铅（氢），铜汞银铂金",
                        "<strong>K > Ca > Na</strong>：前三名极其活泼",
                        "<strong>（H）</strong>：氢是非金属，作为参照标准",
                        "<strong>Au</strong>：最不活泼，自然界以单质存在",
                    ]
                },
                "scene": "activity_series",
                "sceneArgs": {
                    "series": [
                        {"el": "K", "active": True},
                        {"el": "Ca", "active": True},
                        {"el": "Na", "active": True},
                        {"el": "Mg", "active": True},
                        {"el": "Al", "active": True},
                        {"el": "Zn", "active": True},
                        {"el": "Fe", "active": True},
                        {"el": "Sn", "active": True},
                        {"el": "Pb", "active": True},
                        {"el": "(H)", "active": False},
                        {"el": "Cu", "active": False},
                        {"el": "Hg", "active": False},
                        {"el": "Ag", "active": False},
                        {"el": "Pt", "active": False},
                        {"el": "Au", "active": False},
                    ]
                }
            },
            {
                "tag": "规律", "name": "金属与酸反应",
                "body": "<p><strong>H 前金属</strong>（K~Pb）能置换出酸中的氢，放出 H₂：</p>"
                        "<p><code>Zn + H₂SO₄ → ZnSO₄ + H₂↑</code></p>"
                        "<p><strong>H 后金属</strong>（Cu~Au）不能与酸反应产生 H₂。</p>"
                        "<p>反应剧烈程度：金属越靠左反应越剧烈。</p>",
                "points": {
                    "title": "典型反应",
                    "items": [
                        "<strong>Mg + 2HCl → MgCl₂ + H₂↑</strong>（剧烈）",
                        "<strong>Zn + 2HCl → ZnCl₂ + H₂↑</strong>（适中）",
                        "<strong>Fe + 2HCl → FeCl₂ + H₂↑</strong>（缓慢）",
                        "<strong>Cu + HCl → 不反应</strong>（H 后）",
                    ]
                },
                "scene": "beaker_reaction",
                "sceneArgs": {
                    "metal": "Zn",
                    "acid": "HCl",
                    "product": "ZnCl₂",
                    "gas": "H₂",
                    "intensity": "medium"
                }
            },
            {
                "tag": "规律", "name": "金属与盐溶液反应",
                "body": "<p>活动性<strong>较强</strong>的金属能将活动性<strong>较弱</strong>的金属"
                        "从它的盐溶液中<strong>置换</strong>出来。</p>"
                        "<p><strong>Fe + CuSO₄ → FeSO₄ + Cu</strong></p>"
                        "<p>现象：铁钉表面析出<strong>红色铜</strong>，溶液由蓝色渐变为浅绿色。</p>",
                "points": {
                    "title": "判断规则",
                    "items": [
                        "<strong>条件</strong>：前置换后（金属活动性）",
                        "<strong>盐须可溶</strong>：盐必须溶于水",
                        "<strong>K/Ca/Na 例外</strong>：过于活泼，先与水反应",
                        "<strong>Fe 变 Fe²⁺</strong>：不是 Fe³⁺",
                    ]
                },
                "scene": "beaker_reaction",
                "sceneArgs": {
                    "metal": "Fe",
                    "solution": "CuSO₄",
                    "product": "FeSO₄",
                    "precipitate": "Cu",
                    "intensity": "slow"
                }
            },
        ],
    }


# =====================================================================
# 3) 电解质的电离（离子反应基础）
# =====================================================================
def build_electrolyte():
    return {
        "meta": {
            "title": "电解质的电离",
            "subtitle": "强电解质 · 弱电解质 · 离子方程式",
            "language": "zh-CN",
            "accent": "cyan",
        },
        "cards": [
            {"num": 1, "title": "电解质", "body": "溶于水或熔融<br>能导电的化合物"},
            {"num": 2, "title": "强电解质", "body": "完全电离<br>→ 不可逆"},
            {"num": 3, "title": "弱电解质", "body": "部分电离<br>⇌ 可逆"},
            {"num": 4, "title": "离子方程式", "body": "写 → 拆 → 删 → 查"},
        ],
        "steps": [
            {
                "tag": "概念", "name": "电解质与非电解质",
                "body": "<p><strong>电解质</strong>：在水溶液或熔融状态下能<strong>导电</strong>的化合物。</p>"
                        "<p><strong>非电解质</strong>：在上述条件下都不能导电的化合物。</p>",
                "points": {
                    "title": "常见分类",
                    "items": [
                        "<strong>强电解质</strong>：强酸(HCl)、强碱(NaOH)、盐(NaCl)",
                        "<strong>弱电解质</strong>：弱酸(CH₃COOH)、弱碱(NH₃·H₂O)、水(H₂O)",
                        "<strong>非电解质</strong>：乙醇(C₂H₅OH)、蔗糖(C₁₂H₂₂O₁₁)",
                        "<strong>注意</strong>：导电≠电解质（金属导电但不是电解质）",
                    ]
                },
                "scene": "concept",
                "sceneArgs": {"title": "电解质判断", "items": [
                    {"label": "强电解质", "desc": "完全电离 → 不可逆", "color": "#34d399"},
                    {"label": "弱电解质", "desc": "部分电离 ⇌ 可逆", "color": "#fbbf24"},
                    {"label": "非电解质", "desc": "不电离 · 不导电", "color": "#f87171"},
                ]}
            },
            {
                "tag": "示例", "name": "离子方程式书写（四步法）",
                "body": "<p><strong>写 → 拆 → 删 → 查</strong></p>"
                        "<p>以 <strong>NaOH + HCl → NaCl + H₂O</strong> 为例：</p>"
                        "<p>① <strong>写</strong>：NaOH + HCl → NaCl + H₂O</p>"
                        "<p>② <strong>拆</strong>：Na⁺+OH⁻ + H⁺+Cl⁻ → Na⁺+Cl⁻ + H₂O</p>"
                        "<p>③ <strong>删</strong>：OH⁻ + H⁺ → H₂O</p>"
                        "<p>④ <strong>查</strong>：原子守恒 + 电荷守恒 ✓</p>",
                "points": {
                    "title": "拆与不拆",
                    "items": [
                        "<strong>拆</strong>：强酸、强碱、可溶性盐 → 离子",
                        "<strong>不拆</strong>：单质、气体、沉淀、弱电解质、水",
                        "<strong>微溶物</strong>：澄清拆，浑浊不拆",
                    ]
                },
                "scene": "equation",
                "sceneArgs": {
                    "equations": [
                        "NaOH + HCl → NaCl + H₂O",
                        "  ↳ OH⁻ + H⁺ → H₂O",
                        "Na₂CO₃ + 2HCl → 2NaCl + CO₂↑ + H₂O",
                        "  ↳ CO₃²⁻ + 2H⁺ → CO₂↑ + H₂O",
                    ]
                }
            },
        ],
    }


# =====================================================================
# REGISTRY
# =====================================================================
REGISTRY = {
    "redox_balancing": build_redox_balancing,
    "metal_activity": build_metal_activity,
    "electrolyte": build_electrolyte,
}


def main(argv):
    if not argv or argv[0] == "list":
        print("已注册教程:")
        for k in REGISTRY:
            print("  -", k)
        return
    if argv[0] == "all":
        out_dir = Path(argv[1]) if len(argv) > 1 else Path.cwd()
        out_dir.mkdir(parents=True, exist_ok=True)
        for k, builder in REGISTRY.items():
            out_path = out_dir / f"tutorial-{k}.html"
            render_html(builder(), out_path)
            print("written:", out_path)
        return
    key = argv[0]
    if key not in REGISTRY:
        print(f"未知教程 {key}；可用: {', '.join(REGISTRY)}")
        sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else Path.cwd() / f"tutorial-{key}.html"
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
