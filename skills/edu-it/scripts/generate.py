#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把 IT 课程 spec 注入 template/board-it.html，产出单页交互课程。
    16 个教程覆盖全部 6 个教学模块。
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board-it.html"
PLACEHOLDER = "__TUTORIAL_DATA__"


def render_html(spec: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(spec, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


# =====================================================================
# 1) 冒泡排序
# =====================================================================
def build_bubble_sort():
    data = [5, 3, 8, 4, 2, 7, 1, 6]
    return {
        "meta": {"title": "冒泡排序", "subtitle": "相邻比较 · 依次冒泡 · O(n²)", "module": "algorithm", "accent": "indigo"},
        "cards": [
            {"num": 1, "title": "核心思想", "body": '相邻元素两两比较<br>大数逐步"冒泡"到末尾'},
            {"num": 2, "title": "时间复杂度", "body": "最坏 O(n²)<br>最好 O(n)"},
            {"num": 3, "title": "空间复杂度", "body": "O(1)<br>原地排序"},
            {"num": 4, "title": "稳定性", "body": "稳定排序<br>相等不交换"},
        ],
        "steps": [
            {"tag": "概念", "name": "算法思想",
             "body": "<p><strong>冒泡排序</strong>反复遍历序列，依次比较相邻元素，逆序则交换。每轮最大值像气泡一样浮到末尾。</p>",
             "points": {"title": "核心思想", "items": ["相邻比较：比较 arr[j] 和 arr[j+1]", "条件交换：若顺序不对则交换", "每轮冒泡：最大值沉底", "多轮直到：全部有序"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "冒泡排序流程图",
                 "nodes": [
                     {"id": 0, "x": 200, "y": 40, "w": 120, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 200, "y": 110, "w": 160, "h": 44, "label": "i = 0 to n-2"},
                     {"id": 2, "x": 200, "y": 180, "w": 160, "h": 44, "label": "j = 0 to n-2-i"},
                     {"id": 3, "x": 200, "y": 250, "w": 160, "h": 44, "label": "arr[j] > arr[j+1]?", "type": "decision"},
                     {"id": 4, "x": 40, "y": 250, "w": 120, "h": 40, "label": "交换 arr[j] ↔ arr[j+1]"},
                     {"id": 5, "x": 200, "y": 330, "w": 120, "h": 40, "label": "结束", "type": "startend"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4, "是"], [4, 2], [3, 5, "否"]], "active": -1,
             }},
            {"tag": "概念", "name": "算法步骤",
             "body": "<p><strong>外层循环</strong> i = 0 → n-2（共 n-1 轮）</p><p><strong>内层循环</strong> j = 0 → n-2-i</p><p>每轮比较相邻元素，逆序交换。</p>",
             "points": {"title": "伪代码", "items": ["for i = 0 to n-2:", "  for j = 0 to n-2-i:", "    if arr[j] > arr[j+1]:", "      swap(arr[j], arr[j+1])"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "冒泡排序四要素",
                 "items": [
                     {"icon": "🔄", "label": "相邻比较", "desc": "相邻元素两两对比", "color": "#6366f1"},
                     {"icon": "🔄", "label": "条件交换", "desc": "逆序则交换位置", "color": "#fbbf24"},
                     {"icon": "⬆️", "label": "冒泡", "desc": "大数逐渐浮到末尾", "color": "#f87171"},
                     {"icon": "✅", "label": "多轮有序", "desc": "n-1 轮后完全有序", "color": "#34d399"},
                 ]}},
            {"tag": "演示", "name": "手动模拟",
             "body": "<p>拖动滑块观察排序过程：黄=比较中，红=交换中，绿=已排序。</p>",
             "points": {"title": "观察", "items": ["每轮最大值沉底", "已排序区逐步扩大", "比较次数 = n×(n-1)/2"]},
             "scene": "sort_bars", "sceneArgs": {
                 "data": data, "title": "冒泡排序演示",
                 "param": {"name": "排序进度", "min": 0, "max": 1, "step": 0.01, "value": 0},
                 "readouts": [{"label": "数组长度", "value": str(len(data))}]}},
            {"tag": "分析", "name": "复杂度分析",
             "body": "<p>最坏 O(n²)（逆序），最好 O(n)（已有序+优化），平均 O(n²)。空间 O(1)。</p>",
             "points": {"title": "复杂度", "items": ["最坏：O(n²) — 数组逆序", "最好：O(n) — 已有序", "空间：O(1) 原地", "稳定：✓"]},
             "scene": "complexity_chart", "sceneArgs": {
                 "title": "冒泡排序复杂度",
                 "items": [{"name": "冒泡排序", "best": "O(n)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": True}]}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p><strong>口诀</strong>：相邻循环比大小，逆序就交换；一轮沉底一个数，多轮自然有序。</p>",
             "points": {"title": "速记", "items": ["口诀：相邻比，逆序换，轮轮沉底", "最好 O(n)，最坏 O(n²)", "稳定排序"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "冒泡排序总结",
                 "items": [
                     {"icon": "💡", "label": "核心", "desc": "相邻比较大数冒泡", "color": "#6366f1"},
                     {"icon": "⏱️", "label": "时间", "desc": "最好 O(n) 最坏 O(n²)", "color": "#fbbf24"},
                     {"icon": "📦", "label": "空间", "desc": "O(1) 原地排序", "color": "#34d399"},
                 ]}},
        ],
    }


# =====================================================================
# 2) 选择排序
# =====================================================================
def build_selection_sort():
    data = [5, 3, 8, 4, 2, 7, 1, 6]
    return {
        "meta": {"title": "选择排序", "subtitle": "每轮选最小 · 依次放前面 · O(n²)", "module": "algorithm", "accent": "amber"},
        "cards": [
            {"num": 1, "title": "核心思想", "body": "每轮选出最小<br>放到已排序末尾"},
            {"num": 2, "title": "时间复杂度", "body": "始终 O(n²)"},
            {"num": 3, "title": "空间复杂度", "body": "O(1) 原地排序"},
            {"num": 4, "title": "稳定性", "body": "不稳定排序"},
        ],
        "steps": [
            {"tag": "概念", "name": "算法思想",
             "body": "<p>① 在未排序序列中找到最小元素</p><p>② 放到已排序末尾</p><p>③ 重复直到全部有序。每轮只做一次交换。</p>",
             "points": {"title": "核心", "items": ["每轮找最小值", "一次交换到位", "冒泡重比较，选择重查找"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "选择排序流程图",
                 "nodes": [
                     {"id": 0, "x": 200, "y": 40, "w": 120, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 200, "y": 110, "w": 180, "h": 44, "label": "i = 0 to n-2"},
                     {"id": 2, "x": 200, "y": 180, "w": 180, "h": 44, "label": "minIdx = i"},
                     {"id": 3, "x": 200, "y": 250, "w": 200, "h": 44, "label": "j = i+1 to n-1"},
                     {"id": 4, "x": 200, "y": 320, "w": 180, "h": 44, "label": "arr[j] < arr[minIdx]?", "type": "decision"},
                     {"id": 5, "x": 40, "y": 320, "w": 100, "h": 40, "label": "minIdx = j"},
                     {"id": 6, "x": 200, "y": 400, "w": 140, "h": 40, "label": "swap(i, minIdx)"},
                     {"id": 7, "x": 200, "y": 470, "w": 120, "h": 40, "label": "结束", "type": "startend"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5, "是"], [5, 3], [4, 6, "否"], [6, 1], [1, 7]], "active": -1,
             }},
            {"tag": "演示", "name": "手动模拟",
             "body": "<p>拖动滑块观察选择排序过程。</p>",
             "points": {"title": "观察", "items": ["每轮只做一次交换", "已排序区从左侧扩大", "比较次数固定"]},
             "scene": "sort_bars", "sceneArgs": {
                 "data": data, "title": "选择排序演示",
                 "param": {"name": "排序进度", "min": 0, "max": 1, "step": 0.01, "value": 0},
                 "readouts": [{"label": "数组长度", "value": str(len(data))}]}},
            {"tag": "对比", "name": "冒泡 vs 选择",
             "body": "<p>交换次数：选择 n-1 → 冒泡 最坏 n²/2。选择不稳定。</p>",
             "points": {"title": "对比", "items": ["交换次数：选择远少于冒泡", "比较次数：相同", "冒泡稳定，选择不稳定"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "冒泡 vs 选择",
                 "left": {"title": "冒泡", "color": "#f87171", "items": ["相邻比较+交换", "每轮多次交换", "稳定", "可提前终止"]},
                 "right": {"title": "选择", "color": "#fbbf24", "items": ["查找最小值", "每轮一次交换", "不稳定", "比较固定"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p><strong>口诀</strong>：每轮扫一遍，记住最小下标；换到已排序尾，n-1 轮完成。</p>",
             "points": {"title": "速记", "items": ["每轮一换", "不稳定", "原地 O(1)", "始终 O(n²)"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "选择排序总结",
                 "items": [
                     {"icon": "🔍", "label": "核心", "desc": "每轮选最小放前面", "color": "#f59e0b"},
                     {"icon": "⏱️", "label": "时间", "desc": "始终 O(n²)", "color": "#fbbf24"},
                     {"icon": "🔄", "label": "交换", "desc": "仅 n-1 次", "color": "#06b6d4"},
                 ]}},
        ],
    }


# =====================================================================
# 3) 二分查找
# =====================================================================
def build_binary_search():
    data = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]
    target = 23
    return {
        "meta": {"title": "二分查找", "subtitle": "每次排除一半 · O(log n)", "module": "algorithm", "accent": "emerald"},
        "cards": [
            {"num": 1, "title": "前置条件", "body": "有序数组"},
            {"num": 2, "title": "核心思想", "body": "取中值比较缩小一半"},
            {"num": 3, "title": "时间复杂度", "body": "O(log n) 极快"},
            {"num": 4, "title": "空间复杂度", "body": "O(1) 迭代"},
        ],
        "steps": [
            {"tag": "概念", "name": "算法思想",
             "body": "<p>在有序数组中：取中间值比较，相等→找到；小于目标→右侧；大于目标→左侧。每次排除一半。</p>",
             "points": {"title": "要点", "items": ["前提：数组必须有序", "每次排除一半", "O(log n) vs O(n) 线性"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "二分查找流程图",
                 "nodes": [
                     {"id": 0, "x": 200, "y": 30, "w": 120, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 200, "y": 95, "w": 160, "h": 44, "label": "left=0, right=n-1"},
                     {"id": 2, "x": 200, "y": 165, "w": 100, "h": 44, "label": "left≤right?", "type": "decision"},
                     {"id": 3, "x": 200, "y": 240, "w": 120, "h": 44, "label": "mid=(left+right)/2"},
                     {"id": 4, "x": 200, "y": 310, "w": 120, "h": 44, "label": "arr[mid]==target?", "type": "decision"},
                     {"id": 5, "x": 40, "y": 310, "w": 100, "h": 44, "label": "返回 mid"},
                     {"id": 6, "x": 200, "y": 390, "w": 120, "h": 44, "label": "arr[mid]<target?", "type": "decision"},
                     {"id": 7, "x": 40, "y": 390, "w": 80, "h": 40, "label": "left=mid+1"},
                     {"id": 8, "x": 360, "y": 390, "w": 80, "h": 40, "label": "right=mid-1"},
                     {"id": 9, "x": 200, "y": 470, "w": 140, "h": 40, "label": "返回 -1（未找到）"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3, "是"], [3, 4], [4, 5, "是"], [4, 6, "否"], [6, 7, "是"], [6, 8, "否"], [7, 2], [8, 2], [2, 9, "否"]],
                 "active": -1,
             }},
            {"tag": "演示", "name": "查找演示",
             "body": "<p>拖动滑块观察二分查找：黄=mid，暗=排除区，绿=找到。</p>",
             "points": {"title": "观察", "items": ["范围每次缩小一半", "log₂(11)≈4 次", "效率极高"]},
             "scene": "search_visual", "sceneArgs": {
                 "data": data, "target": target, "type": "binary", "title": "二分查找过程",
                 "param": {"name": "查找进度", "min": 0, "max": 1, "step": 0.01, "value": 0},
                 "readouts": [{"label": "长度", "value": str(len(data))}, {"label": "目标", "value": str(target)}]}},
            {"tag": "对比", "name": "线性 vs 二分",
             "body": "<p>线性 O(n)，二分 O(log n)。n=1000 时：线性 1000 vs 二分 10。</p>",
             "points": {"title": "对比", "items": ["线性：无序也可", "二分：必须有序", "n=10⁶：线性百万 vs 二分 20"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "对比", "left": {"title": "线性", "color": "#f87171", "items": ["逐个检查 O(n)", "不要求有序"]},
                 "right": {"title": "二分", "color": "#34d399", "items": ["每次排除一半 O(log n)", "必须有序"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p><strong>口诀</strong>：左右夹逼，中值比较；大则右移，小则左移。</p>",
             "points": {"title": "速记", "items": ["前提：有序", "mid = left + (right-left)/2", "O(log n)"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "二分查找总结",
                 "items": [
                     {"icon": "🎯", "label": "核心", "desc": "每次排除一半", "color": "#34d399"},
                     {"icon": "⚡", "label": "复杂度", "desc": "O(log n)", "color": "#fbbf24"},
                     {"icon": "📋", "label": "前提", "desc": "必须有序", "color": "#f87171"},
                 ]}},
        ],
    }


# =====================================================================
# 4) 插入排序
# =====================================================================
def build_insertion_sort():
    data = [5, 3, 8, 4, 2, 7, 1, 6]
    return {
        "meta": {"title": "插入排序", "subtitle": "像打扑克 · 插到已排序区 · O(n²)", "module": "algorithm", "accent": "sky"},
        "cards": [
            {"num": 1, "title": "核心思想", "body": "把元素插入到已排序序列"},
            {"num": 2, "title": "时间复杂度", "body": "最坏 O(n²) 最好 O(n)"},
            {"num": 3, "title": "空间复杂度", "body": "O(1) 原地"},
            {"num": 4, "title": "稳定性", "body": "稳定"},
        ],
        "steps": [
            {"tag": "概念", "name": "算法思想",
             "body": "<p>像打扑克牌：从右向左扫描已排序区，找到位置插入。稳定排序，实际效率在 O(n²) 中最好。</p>",
             "points": {"title": "核心", "items": ["类比：打扑克抓牌插入", "已排序区左侧扩大", "后移腾出空间"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "插入排序流程图",
                 "nodes": [
                     {"id": 0, "x": 200, "y": 30, "w": 120, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 200, "y": 95, "w": 180, "h": 44, "label": "i = 1 to n-1"},
                     {"id": 2, "x": 200, "y": 165, "w": 180, "h": 44, "label": "key = arr[i]"},
                     {"id": 3, "x": 200, "y": 235, "w": 160, "h": 44, "label": "j = i-1"},
                     {"id": 4, "x": 200, "y": 305, "w": 180, "h": 44, "label": "j≥0 and arr[j]>key?", "type": "decision"},
                     {"id": 5, "x": 40, "y": 305, "w": 120, "h": 44, "label": "arr[j+1]=arr[j]; j--"},
                     {"id": 6, "x": 200, "y": 385, "w": 120, "h": 40, "label": "arr[j+1] = key"},
                     {"id": 7, "x": 200, "y": 460, "w": 120, "h": 40, "label": "结束", "type": "startend"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5, "是"], [5, 4], [4, 6, "否"], [6, 1], [1, 7]], "active": -1,
             }},
            {"tag": "演示", "name": "模拟",
             "body": "<p>拖动滑块观察插入排序。黄=待插入 key，红=后移中，绿=已排序。</p>",
             "points": {"title": "观察", "items": ["已排序区扩大", "key 找到位置插入", "最好 O(n)"]},
             "scene": "sort_bars", "sceneArgs": {
                 "data": data, "title": "插入排序",
                 "param": {"name": "排序进度", "min": 0, "max": 1, "step": 0.01, "value": 0}}},
            {"tag": "对比", "name": "O(n²) 对比",
             "body": "<p>插入 > 选择 > 冒泡（实际效率）。插入稳定系数小。</p>",
             "points": {"title": "对比", "items": ["冒泡：交换多稳定", "选择：交换少不稳定", "插入：系数小稳定"]},
             "scene": "complexity_chart", "sceneArgs": {
                 "title": "O(n²) 排序对比",
                 "items": [
                     {"name": "冒泡", "best": "O(n)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": True},
                     {"name": "选择", "best": "O(n²)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": False},
                     {"name": "插入", "best": "O(n)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": True},
                 ]}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p><strong>口诀</strong>：抓牌插入已排序，大牌后移腾空位。</p>",
             "points": {"title": "速记", "items": ["最好 O(n)", "最坏 O(n²)", "稳定"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "插入排序总结",
                 "items": [
                     {"icon": "🃏", "label": "核心", "desc": "像打扑克插入", "color": "#06b6d4"},
                     {"icon": "⏱️", "label": "时间", "desc": "最好 O(n) 最坏 O(n²)", "color": "#fbbf24"},
                     {"icon": "📦", "label": "空间", "desc": "O(1) 原地", "color": "#34d399"},
                 ]}},
        ],
    }


# =====================================================================
# 5) 算法复杂度分析
# =====================================================================
def build_algorithm_complexity():
    return {
        "meta": {"title": "算法复杂度分析", "subtitle": "大 O · 时间空间 · 增长趋势", "module": "algorithm", "accent": "violet"},
        "cards": [
            {"num": 1, "title": "大 O", "body": "描述增长趋势"},
            {"num": 2, "title": "时间复杂度", "body": "运行时间 vs 规模"},
            {"num": 3, "title": "空间复杂度", "body": "额外内存 vs 规模"},
            {"num": 4, "title": "常见复杂度", "body": "O(1)<O(log n)<O(n)<O(n²)"},
        ],
        "steps": [
            {"tag": "概念", "name": "什么是大 O",
             "body": "<p>大 O 表示法描述算法效率随输入规模增长的趋势。忽略常数 O(2n)→O(n)，忽略低阶 O(n²+n)→O(n²)。</p>",
             "points": {"title": "规则", "items": ["忽略常数", "忽略低阶", "关注最坏"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "复杂度分析",
                 "items": [
                     {"icon": "📈", "label": "时间", "desc": "运行时间 vs 输入规模", "color": "#6366f1"},
                     {"icon": "💾", "label": "空间", "desc": "额外内存 vs 输入规模", "color": "#34d399"},
                     {"icon": "🎯", "label": "大 O", "desc": "关注增长趋势", "color": "#fbbf24"},
                 ]}},
            {"tag": "概念", "name": "常见复杂度",
             "body": "<p>O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)</p>",
             "points": {"title": "速查", "items": ["O(1)：随机访问", "O(log n)：二分查找", "O(n)：线性查找", "O(n²)：冒泡排序"]},
             "scene": "chart", "sceneArgs": {
                 "title": "增长趋势对比", "type": "line",
                 "data": [1, 7, 10, 66, 100],
                 "labels": ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)"],
                 "colors": ["#34d399", "#06b6d4", "#6366f1", "#fbbf24", "#f87171"]}},
            {"tag": "对比", "name": "排序复杂度",
             "body": "<p>O(n²) 适合小数据，O(n log n) 适合大数据。</p>",
             "points": {"title": "建议", "items": ["n<100：插入排序", "n<10⁵：快速排序", "需稳定：归并排序"]},
             "scene": "complexity_chart", "sceneArgs": {
                 "title": "排序算法复杂度全景",
                 "items": [
                     {"name": "冒泡", "best": "O(n)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": True},
                     {"name": "选择", "best": "O(n²)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": False},
                     {"name": "插入", "best": "O(n)", "worst": "O(n²)", "avg": "O(n²)", "space": "O(1)", "stable": True},
                     {"name": "快速", "best": "O(n log n)", "worst": "O(n²)", "avg": "O(n log n)", "space": "O(log n)", "stable": False},
                     {"name": "归并", "best": "O(n log n)", "worst": "O(n log n)", "avg": "O(n log n)", "space": "O(n)", "stable": True},
                 ]}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>大 O 描述增长趋势，忽略常数和低阶。O(2ⁿ) 指数爆炸基本不可用。</p>",
             "points": {"title": "口诀", "items": ["常数对数线性：1, log n, n", "线性对数平方：n log n, n²", "指数爆炸：2ⁿ 不可用"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "总结",
                 "items": [
                     {"icon": "🎯", "label": "大 O", "desc": "增长趋势", "color": "#6366f1"},
                     {"icon": "⚡", "label": "最优", "desc": "O(1) 常数", "color": "#34d399"},
                     {"icon": "🐌", "label": "避免", "desc": "O(2ⁿ) 爆炸", "color": "#f87171"},
                 ]}},
        ],
    }


# =====================================================================
# 6) 流程图基础
# =====================================================================
def build_flowchart_basics():
    return {
        "meta": {"title": "流程图基础", "subtitle": "符号 · 顺序 · 分支 · 循环", "module": "algorithm", "accent": "cyan"},
        "cards": [
            {"num": 1, "title": "流程图", "body": "图形符号描述算法"},
            {"num": 2, "title": "符号", "body": "起止·处理·判断·IO"},
            {"num": 3, "title": "结构", "body": "顺序·分支·循环"},
            {"num": 4, "title": "作用", "body": "直观展示逻辑"},
        ],
        "steps": [
            {"tag": "概念", "name": "基本符号",
             "body": "<p>起止框（圆角矩形）、处理框（矩形）、判断框（菱形）、IO框（平行四边形）、流程线（箭头）。</p>",
             "points": {"title": "符号", "items": ["起止框：开始/结束", "处理框：计算/赋值", "判断框：条件", "IO框：输入/输出"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "基本符号",
                 "nodes": [
                     {"id": 0, "x": 120, "y": 30, "w": 100, "h": 40, "label": "开始", "type": "startend", "color": "#34d399"},
                     {"id": 1, "x": 280, "y": 30, "w": 100, "h": 40, "label": "处理", "type": "process", "color": "#6366f1"},
                     {"id": 2, "x": 440, "y": 30, "w": 100, "h": 40, "label": "判断", "type": "decision", "color": "#fbbf24"},
                     {"id": 3, "x": 120, "y": 110, "w": 100, "h": 40, "label": "输入", "type": "io", "color": "#06b6d4"},
                     {"id": 4, "x": 280, "y": 110, "w": 100, "h": 40, "label": "结束", "type": "startend", "color": "#f87171"},
                 ], "edges": [], "active": -1,
             }},
            {"tag": "概念", "name": "三种结构",
             "body": "<p>任何算法都可分解为：顺序（依次执行）、分支（if-else）、循环（for/while）。</p>",
             "points": {"title": "结构", "items": ["顺序：一条路走到底", "分支：二选一", "循环：重复直到假"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "三种结构",
                 "items": [
                     {"icon": "➡️", "label": "顺序", "desc": "依次执行", "color": "#34d399"},
                     {"icon": "🔀", "label": "分支", "desc": "条件二选一", "color": "#fbbf24"},
                     {"icon": "🔄", "label": "循环", "desc": "重复直到条件假", "color": "#6366f1"},
                 ]}},
            {"tag": "示例", "name": "分支：奇偶判断",
             "body": "<p>判断框两个出口：是（偶数）和否（奇数）。</p>",
             "points": {"title": "要点", "items": ["菱形判断", "标注是/否", "两出口不同处理"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "奇偶判断",
                 "nodes": [
                     {"id": 0, "x": 150, "y": 20, "w": 100, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 150, "y": 80, "w": 120, "h": 44, "label": "输入 num"},
                     {"id": 2, "x": 150, "y": 150, "w": 140, "h": 44, "label": "num%2==0?", "type": "decision"},
                     {"id": 3, "x": 40, "y": 150, "w": 80, "h": 40, "label": "偶数"},
                     {"id": 4, "x": 280, "y": 150, "w": 80, "h": 40, "label": "奇数"},
                     {"id": 5, "x": 150, "y": 230, "w": 100, "h": 40, "label": "结束", "type": "startend"},
                 ], "edges": [[0, 1], [1, 2], [2, 3, "是"], [2, 4, "否"], [3, 5], [4, 5]], "active": -1,
             }},
            {"tag": "示例", "name": "循环：1~100 求和",
             "body": "<p>三要素：初始条件 (sum=0,i=1)、条件 (i≤100)、更新 (i++)。</p>",
             "points": {"title": "三要素", "items": ["初始条件", "循环条件", "变量更新"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "1~100 求和",
                 "nodes": [
                     {"id": 0, "x": 150, "y": 20, "w": 100, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 150, "y": 80, "w": 140, "h": 44, "label": "sum=0, i=1"},
                     {"id": 2, "x": 150, "y": 150, "w": 100, "h": 44, "label": "i≤100?", "type": "decision"},
                     {"id": 3, "x": 280, "y": 150, "w": 120, "h": 44, "label": "sum+=i; i++"},
                     {"id": 4, "x": 150, "y": 240, "w": 100, "h": 40, "label": "输出 sum"},
                     {"id": 5, "x": 150, "y": 310, "w": 100, "h": 40, "label": "结束", "type": "startend"},
                 ], "edges": [[0, 1], [1, 2], [2, 3, "是"], [3, 2], [2, 4, "否"], [4, 5]], "active": -1,
             }},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>标准符号 + 三种结构 = 任意复杂算法。</p>",
             "points": {"title": "口诀", "items": ["起止圆角处理矩形", "判断菱形 IO 斜边", "方向箭头指流向"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "总结",
                 "items": [
                     {"icon": "📐", "label": "符号", "desc": "起止·处理·判断", "color": "#6366f1"},
                     {"icon": "🔀", "label": "分支", "desc": "条件二选一", "color": "#fbbf24"},
                     {"icon": "🔄", "label": "循环", "desc": "重复直到结束", "color": "#06b6d4"},
                 ]}},
        ],
    }


# =====================================================================
# 7) Python 基础
# =====================================================================
def build_python_basics():
    return {
        "meta": {"title": "Python 基础", "subtitle": "变量 · 条件 · 循环 · 函数", "module": "programming", "accent": "blue"},
        "cards": [
            {"num": 1, "title": "Python", "body": "简洁易读动态语言"},
            {"num": 2, "title": "变量", "body": "动态类型无需声明"},
            {"num": 3, "title": "控制流", "body": "if/for/while"},
            {"num": 4, "title": "函数", "body": "def 定义 return 返回"},
        ],
        "steps": [
            {"tag": "概念", "name": "变量与类型",
             "body": "<p>Python 动态类型：<code>x=5</code> int，<code>y=3.14</code> float，<code>name='Alice'</code> str，<code>ok=True</code> bool。</p>",
             "points": {"title": "类型", "items": ["int：整数", "float：浮点数", "str：字符串", "bool：布尔值"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "基本类型",
                 "items": [
                     {"icon": "🔢", "label": "int", "desc": "x = 5", "color": "#6366f1"},
                     {"icon": "🎯", "label": "float", "desc": "y = 3.14", "color": "#34d399"},
                     {"icon": "📝", "label": "str", "desc": "name = 'Alice'", "color": "#fbbf24"},
                     {"icon": "✅", "label": "bool", "desc": "ok = True", "color": "#06b6d4"},
                 ]}},
            {"tag": "概念", "name": "条件语句",
             "body": "<p><code>if score >= 60:</code><br><code>    print('及格')</code><br><code>else:</code><br><code>    print('不及格')</code><br>注意缩进（4空格）表示代码块。</p>",
             "points": {"title": "要点", "items": ["条件后加冒号", "4空格缩进", "elif 多分支"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "判断成绩",
                 "nodes": [
                     {"id": 0, "x": 150, "y": 20, "w": 100, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 150, "y": 80, "w": 120, "h": 44, "label": "输入 score"},
                     {"id": 2, "x": 150, "y": 150, "w": 140, "h": 44, "label": "score≥60?", "type": "decision"},
                     {"id": 3, "x": 40, "y": 150, "w": 80, "h": 40, "label": "及格"},
                     {"id": 4, "x": 280, "y": 150, "w": 80, "h": 40, "label": "不及格"},
                     {"id": 5, "x": 150, "y": 230, "w": 100, "h": 40, "label": "结束", "type": "startend"},
                 ], "edges": [[0, 1], [1, 2], [2, 3, "是"], [2, 4, "否"], [3, 5], [4, 5]], "active": -1,
             }},
            {"tag": "概念", "name": "循环",
             "body": "<p><code>for i in range(5):</code><br><code>    print(i)</code><br><code>while n > 0:</code><br><code>    print(n); n -= 1</code></p>",
             "points": {"title": "循环", "items": ["for：遍历 range/列表", "while：条件循环", "break 退出", "continue 跳过"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "循环",
                 "items": [
                     {"icon": "🔄", "label": "for", "desc": "遍历序列", "color": "#6366f1"},
                     {"icon": "🔄", "label": "while", "desc": "条件控制", "color": "#fbbf24"},
                     {"icon": "⏹️", "label": "break", "desc": "退出循环", "color": "#f87171"},
                     {"icon": "⏭️", "label": "continue", "desc": "跳过本轮", "color": "#34d399"},
                 ]}},
            {"tag": "概念", "name": "函数",
             "body": "<p><code>def add(a, b):</code><br><code>    return a + b</code><br><code>result = add(1, 2)</code></p>",
             "points": {"title": "要点", "items": ["def 定义", "return 返回值", "参数传递"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "函数示例",
                 "left": {"title": "定义", "color": "#6366f1", "items": ["def greet(name):", "    return 'Hi '+name"]},
                 "right": {"title": "调用", "color": "#34d399", "items": ["msg = greet('Alice')", "print(msg)  # Hi Alice"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>动态类型·缩进代码块·丰富内置库。Python 是 AI/数据分析的首选语言。</p>",
             "points": {"title": "速记", "items": ["变量直接赋值", "4空格缩进", "if/for/while 控制", "def 函数"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "Python 总结",
                 "items": [
                     {"icon": "🐍", "label": "动态", "desc": "变量直接赋值", "color": "#6366f1"},
                     {"icon": "🔀", "label": "控制", "desc": "if/for/while", "color": "#fbbf24"},
                     {"icon": "📦", "label": "函数", "desc": "def 复用", "color": "#06b6d4"},
                 ]}},
        ],
    }


# =====================================================================
# 8) Scratch 基础
# =====================================================================
def build_scratch_basics():
    return {
        "meta": {"title": "Scratch 基础", "subtitle": "积木编程 · 事件驱动 · 角色舞台", "module": "programming", "accent": "green"},
        "cards": [
            {"num": 1, "title": "Scratch", "body": "积木式编程语言"},
            {"num": 2, "title": "角色舞台", "body": "Sprite+Backdrop"},
            {"num": 3, "title": "积木分类", "body": "运动·外观·控制"},
            {"num": 4, "title": "事件驱动", "body": "绿旗点击触发"},
        ],
        "steps": [
            {"tag": "概念", "name": "Scratch 界面",
             "body": "<p>舞台（Stage）480×360 + 角色（Sprite）+ 积木（10类）+ 脚本拼接。</p>",
             "points": {"title": "元素", "items": ["舞台：表演区域", "角色：可编程对象", "积木：功能块", "脚本：拼接结果"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "Scratch 架构",
                 "blocks": [
                     {"x": 40, "y": 60, "w": 120, "h": 50, "label": "舞台", "color": "#6366f1"},
                     {"x": 200, "y": 60, "w": 120, "h": 50, "label": "角色", "color": "#34d399"},
                     {"x": 360, "y": 60, "w": 120, "h": 50, "label": "积木", "color": "#fbbf24"},
                     {"x": 120, "y": 140, "w": 120, "h": 50, "label": "脚本", "color": "#06b6d4"},
                 ], "arrows": [
                     {"x1": 160, "y1": 110, "x2": 160, "y2": 135, "color": "#6366f1"},
                     {"x1": 260, "y1": 110, "x2": 260, "y2": 135, "color": "#34d399"},
                     {"x1": 420, "y1": 110, "x2": 340, "y2": 135, "color": "#fbbf24"},
                 ]}},
            {"tag": "概念", "name": "积木分类",
             "body": "<p>运动（移动/旋转）、外观（造型/说话）、控制（等待/循环）、侦测（碰到/询问）、运算（加减/比较）、变量。</p>",
             "points": {"title": "常用", "items": ["运动：移动10步", "外观：说 Hello", "控制：重复执行", "事件：当绿旗点击"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "积木分类",
                 "items": [
                     {"icon": "🏃", "label": "运动", "desc": "移动·旋转", "color": "#6366f1"},
                     {"icon": "🎨", "label": "外观", "desc": "造型·说话", "color": "#34d399"},
                     {"icon": "🔄", "label": "控制", "desc": "循环·条件", "color": "#fbbf24"},
                     {"icon": "🔢", "label": "运算", "desc": "加减·比较", "color": "#f87171"},
                 ]}},
            {"tag": "示例", "name": "小猫散步",
             "body": "<p>当绿旗点击 → 重复执行：移动10步，碰到边缘反弹。</p>",
             "points": {"title": "逻辑", "items": ["绿旗启动", "循环执行", "移动+反弹", "事件驱动"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "小猫散步",
                 "nodes": [
                     {"id": 0, "x": 150, "y": 30, "w": 120, "h": 40, "label": "绿旗点击", "type": "startend"},
                     {"id": 1, "x": 150, "y": 100, "w": 120, "h": 44, "label": "重复执行", "type": "decision"},
                     {"id": 2, "x": 150, "y": 180, "w": 100, "h": 40, "label": "移动10步"},
                     {"id": 3, "x": 150, "y": 250, "w": 120, "h": 44, "label": "碰到边缘?", "type": "decision"},
                     {"id": 4, "x": 40, "y": 250, "w": 80, "h": 40, "label": "反弹"},
                     {"id": 5, "x": 150, "y": 330, "w": 120, "h": 40, "label": "结束", "type": "startend"},
                 ], "edges": [[0, 1], [1, 2, "是"], [2, 3], [3, 4, "是"], [4, 1], [3, 1, "否"]], "active": -1,
             }},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>积木拼接代替写代码，事件驱动，适合编程入门。</p>",
             "points": {"title": "核心", "items": ["角色+舞台", "积木拼接", "事件驱动", "并行执行"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "总结",
                 "items": [
                     {"icon": "🧩", "label": "积木", "desc": "拼接代替写代码", "color": "#34d399"},
                     {"icon": "🎭", "label": "角色", "desc": "可编程对象", "color": "#6366f1"},
                     {"icon": "⚡", "label": "事件", "desc": "绿旗触发", "color": "#fbbf24"},
                 ]}},
        ],
    }


# =====================================================================
# 9) C++ 基础
# =====================================================================
def build_cpp_basics():
    return {
        "meta": {"title": "C++ 基础", "subtitle": "静态类型 · main · 数组 · 循环", "module": "programming", "accent": "red"},
        "cards": [
            {"num": 1, "title": "C++", "body": "高效静态类型"},
            {"num": 2, "title": "main", "body": "int main() 入口"},
            {"num": 3, "title": "变量", "body": "先声明类型"},
            {"num": 4, "title": "编译", "body": "源码→编译→执行"},
        ],
        "steps": [
            {"tag": "概念", "name": "程序结构",
             "body": "<p><code>#include &lt;iostream&gt;</code><br><code>int main() {</code><br><code>    cout << 'Hello' << endl;</code><br><code>    return 0;</code><br><code>}</code></p>",
             "points": {"title": "结构", "items": ["#include 引入头文件", "int main() 入口", "cout 输出", "return 0 退出"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "C++ 结构",
                 "items": [
                     {"icon": "📄", "label": "头文件", "desc": "#include", "color": "#6366f1"},
                     {"icon": "🚪", "label": "main", "desc": "程序入口", "color": "#34d399"},
                     {"icon": "📤", "label": "cout", "desc": "输出", "color": "#fbbf24"},
                     {"icon": "✅", "label": "return", "desc": "退出码", "color": "#06b6d4"},
                 ]}},
            {"tag": "概念", "name": "变量类型",
             "body": "<p>静态类型：<code>int x=5</code>、<code>double y=3.14</code>、<code>char c='A'</code>、<code>bool b=true</code>。</p>",
             "points": {"title": "类型", "items": ["int 整数", "double 浮点", "char 字符", "bool 布尔"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "C++ vs Python",
                 "left": {"title": "C++", "color": "#f87171", "items": ["静态类型", "需编译", "手动内存", "效率高"]},
                 "right": {"title": "Python", "color": "#34d399", "items": ["动态类型", "解释执行", "自动内存", "开发快"]}}},
            {"tag": "概念", "name": "数组与循环",
             "body": "<p><code>int arr[5]={1,2,3,4,5};</code><br><code>for(int i=0; i<5; i++)</code><br><code>    cout << arr[i];</code><br>下标从0开始。</p>",
             "points": {"title": "要点", "items": ["type name[size]: 声明", "下标 0~size-1", "配合循环遍历", "注意越界"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "数组与循环",
                 "items": [
                     {"icon": "📊", "label": "数组", "desc": "连续内存", "color": "#6366f1"},
                     {"icon": "🔄", "label": "for", "desc": "遍历数组", "color": "#34d399"},
                     {"icon": "⚠️", "label": "越界", "desc": "不检查范围", "color": "#f87171"},
                 ]}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>C++ 高效静态类型，适合系统编程/游戏/竞赛。学习路线：变量→控制流→函数→指针→类。</p>",
             "points": {"title": "速记", "items": ["静态类型", "编译运行", "STL 标准库", "手动内存"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "C++ 总结",
                 "items": [
                     {"icon": "⚡", "label": "高效", "desc": "编译型运行快", "color": "#f87171"},
                     {"icon": "📐", "label": "静态", "desc": "类型安全", "color": "#6366f1"},
                     {"icon": "🎯", "label": "适用", "desc": "系统·游戏·竞赛", "color": "#fbbf24"},
                 ]}},
        ],
    }


# =====================================================================
# 10) Excel 数据处理
# =====================================================================
def build_excel_data():
    return {
        "meta": {"title": "Excel 数据处理", "subtitle": "表格 · 公式 · 图表 · 排序筛选", "module": "data", "accent": "emerald"},
        "cards": [
            {"num": 1, "title": "Excel", "body": "电子表格软件"},
            {"num": 2, "title": "公式", "body": "=SUM() =AVERAGE()"},
            {"num": 3, "title": "图表", "body": "柱状图·折线图·饼图"},
            {"num": 4, "title": "排序筛选", "body": "快速数据整理"},
        ],
        "steps": [
            {"tag": "概念", "name": "Excel 基础",
             "body": "<p>工作簿(.xlsx) → 工作表(Sheet) → 单元格(A1) → 区域(A1:C10)。</p>",
             "points": {"title": "概念", "items": ["工作簿=文件", "工作表=Sheet", "单元格=A1地址"]},
             "scene": "data_table", "sceneArgs": {
                 "title": "成绩表",
                 "headers": ["姓名", "语文", "数学", "英语", "总分"],
                 "rows": [["张三", "85", "92", "78", "255"], ["李四", "91", "88", "95", "274"], ["王五", "76", "85", "82", "243"]],
                 "highlight": []}},
            {"tag": "概念", "name": "常用公式",
             "body": "<p>=SUM() 求和、=AVERAGE() 平均、=MAX()/MIN() 最大最小、=IF(条件,值1,值2) 条件。</p>",
             "points": {"title": "公式", "items": ["SUM 求和", "AVERAGE 平均值", "MAX/MIN 最大最小", "IF 条件"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "Excel 公式",
                 "items": [
                     {"icon": "➕", "label": "SUM", "desc": "求和", "color": "#6366f1"},
                     {"icon": "📊", "label": "AVERAGE", "desc": "平均", "color": "#34d399"},
                     {"icon": "📈", "label": "MAX/MIN", "desc": "最大最小", "color": "#fbbf24"},
                 ]}},
            {"tag": "概念", "name": "图表",
             "body": "<p>柱状图（对比）、折线图（趋势）、饼图（占比）、散点图（相关）。</p>",
             "points": {"title": "选择", "items": ["柱状：对比大小", "折线：趋势变化", "饼图：占比分布"]},
             "scene": "chart", "sceneArgs": {
                 "title": "各科平均分", "type": "bar",
                 "data": [84, 88, 85], "labels": ["语文", "数学", "英语"],
                 "colors": ["#6366f1", "#34d399", "#fbbf24"]}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>核心流程：输入→公式计算→排序筛选→图表展示。</p>",
             "points": {"title": "速记", "items": ["= 开头公式", "F4 引用类型", "Ctrl+Shift+L 筛选"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "总结",
                 "items": [
                     {"icon": "📊", "label": "表格", "desc": "行列组织", "color": "#6366f1"},
                     {"icon": "🔢", "label": "公式", "desc": "=SUM()", "color": "#34d399"},
                     {"icon": "📈", "label": "图表", "desc": "可视化", "color": "#fbbf24"},
                 ]}},
        ],
    }


# =====================================================================
# 11) 数据库初步
# =====================================================================
def build_database_intro():
    return {
        "meta": {"title": "数据库初步", "subtitle": "表 · SQL · 增删改查", "module": "data", "accent": "teal"},
        "cards": [
            {"num": 1, "title": "数据库", "body": "结构化存储"},
            {"num": 2, "title": "表", "body": "行记录+列字段"},
            {"num": 3, "title": "SQL", "body": "查询语言"},
            {"num": 4, "title": "CRUD", "body": "增删改查"},
        ],
        "steps": [
            {"tag": "概念", "name": "数据库基础",
             "body": "<p>表(Table) → 行(Row/记录) → 列(Column/字段)。主键唯一标识每行。常见：MySQL、PostgreSQL。</p>",
             "points": {"title": "核心", "items": ["表：数据集合", "行：一条记录", "列：一个字段", "主键：唯一标识"]},
             "scene": "data_table", "sceneArgs": {
                 "title": "students 表",
                 "headers": ["id", "name", "age", "class"],
                 "rows": [["1", "张三", "18", "高三1班"], ["2", "李四", "17", "高三2班"], ["3", "王五", "18", "高三1班"]],
                 "highlight": [0]}},
            {"tag": "概念", "name": "SQL 语言",
             "body": "<p>SELECT 查询、INSERT 插入、UPDATE 更新、DELETE 删除、CREATE TABLE 建表。</p>",
             "points": {"title": "分类", "items": ["DDL：表结构", "DML：数据操作", "SELECT：查询", "WHERE：条件"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "SQL 操作",
                 "items": [
                     {"icon": "📋", "label": "SELECT", "desc": "查询", "color": "#34d399"},
                     {"icon": "➕", "label": "INSERT", "desc": "插入", "color": "#6366f1"},
                     {"icon": "✏️", "label": "UPDATE", "desc": "修改", "color": "#fbbf24"},
                     {"icon": "❌", "label": "DELETE", "desc": "删除", "color": "#f87171"},
                 ]}},
            {"tag": "示例", "name": "基本查询",
             "body": "<p>SELECT * FROM students<br>SELECT name, age FROM students WHERE age>17<br>ORDER BY age DESC</p>",
             "points": {"title": "要点", "items": ["* 所有列", "WHERE 过滤", "ORDER BY 排序"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "查询执行顺序",
                 "blocks": [
                     {"x": 30, "y": 60, "w": 100, "h": 45, "label": "FROM", "color": "#6366f1"},
                     {"x": 160, "y": 60, "w": 100, "h": 45, "label": "WHERE", "color": "#fbbf24"},
                     {"x": 290, "y": 60, "w": 100, "h": 45, "label": "ORDER BY", "color": "#34d399"},
                     {"x": 420, "y": 60, "w": 100, "h": 45, "label": "SELECT", "color": "#06b6d4"},
                 ],
                 "arrows": [
                     {"x1": 130, "y1": 82, "x2": 155, "y2": 82, "color": "#475569"},
                     {"x1": 260, "y1": 82, "x2": 285, "y2": 82, "color": "#475569"},
                     {"x1": 390, "y1": 82, "x2": 415, "y2": 82, "color": "#475569"},
                 ]}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>表→SQL→CRUD。学习路径：建表→插入→查询→更新→删除。</p>",
             "points": {"title": "速记", "items": ["表为核心：行+列", "SQL 通用语言", "SELECT 最常用", "WHERE 过滤"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "数据库总结",
                 "items": [
                     {"icon": "📊", "label": "表", "desc": "行+列", "color": "#6366f1"},
                     {"icon": "🔍", "label": "SQL", "desc": "查询语言", "color": "#34d399"},
                     {"icon": "🔑", "label": "主键", "desc": "唯一标识", "color": "#fbbf24"},
                 ]}},
        ],
    }


# =====================================================================
# 12) 机器学习概念
# =====================================================================
def build_ml_concepts():
    return {
        "meta": {"title": "机器学习概念", "subtitle": "监督 · 无监督 · 神经网络", "module": "ai", "accent": "purple"},
        "cards": [
            {"num": 1, "title": "机器学习", "body": "从数据中学习"},
            {"num": 2, "title": "监督学习", "body": "有标签训练"},
            {"num": 3, "title": "无监督", "body": "无标签聚类"},
            {"num": 4, "title": "神经网络", "body": "模拟人脑"},
        ],
        "steps": [
            {"tag": "概念", "name": "什么是 ML",
             "body": "<p>传统编程：数据+规则→答案。机器学习：数据+答案→规则。三大类型：监督、无监督、强化。</p>",
             "points": {"title": "三大类型", "items": ["监督：有标签分类回归", "无监督：无标签聚类", "强化：试错学习"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "ML 类型",
                 "items": [
                     {"icon": "📋", "label": "监督", "desc": "分类/回归", "color": "#6366f1"},
                     {"icon": "🔍", "label": "无监督", "desc": "聚类", "color": "#34d399"},
                     {"icon": "🎮", "label": "强化", "desc": "试错奖励", "color": "#fbbf24"},
                 ]}},
            {"tag": "概念", "name": "监督学习",
             "body": "<p>分类（预测类别：垃圾邮件）和回归（预测数值：房价）。流程：收集→标注→训练→预测。</p>",
             "points": {"title": "流程", "items": ["收集标签数据", "划分训练/测试", "训练模型", "评估准确率"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "分类 vs 回归",
                 "left": {"title": "分类", "color": "#6366f1", "items": ["离散类别", "猫狗识别", "垃圾邮件"]},
                 "right": {"title": "回归", "color": "#34d399", "items": ["连续数值", "房价预测", "温度预测"]}}},
            {"tag": "概念", "name": "神经网络",
             "body": "<p>输入层→隐藏层→输出层。权重自动学习。层数多→深度学习。</p>",
             "points": {"title": "结构", "items": ["输入：原始数据", "隐藏：特征提取", "输出：最终结果", "权重：训练学习"]},
             "scene": "neural_net", "sceneArgs": {"title": "神经网络", "layers": [3, 5, 4, 2], "highlight": [], "inputLayer": 0}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>数据驱动：用数据训练模型，而非编程规则。更多数据→更好模型。</p>",
             "points": {"title": "速记", "items": ["监督有标签", "无监督没标签", "神经网络多层连接", "数据量和质量关键"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "ML 总结",
                 "items": [
                     {"icon": "🧠", "label": "核心", "desc": "从数据学习", "color": "#6366f1"},
                     {"icon": "📋", "label": "监督", "desc": "分类+回归", "color": "#34d399"},
                     {"icon": "🔗", "label": "神经网络", "desc": "多层连接", "color": "#fbbf24"},
                 ]}},
        ],
    }


# =====================================================================
# 13) 语音识别
# =====================================================================
def build_voice_recognition():
    return {
        "meta": {"title": "语音识别", "subtitle": "声学特征 · 声学模型 · 端到端", "module": "ai", "accent": "pink"},
        "cards": [
            {"num": 1, "title": "ASR", "body": "声音→文字"},
            {"num": 2, "title": "声学模型", "body": "声音→音素"},
            {"num": 3, "title": "语言模型", "body": "文字序列概率"},
            {"num": 4, "title": "应用", "body": "智能助手·输入"},
        ],
        "steps": [
            {"tag": "概念", "name": "ASR 流程",
             "body": "<p>音频采集→特征提取(MFCC)→声学模型(声音→音素)→语言模型(音素→文字)→文本输出。</p>",
             "points": {"title": "五步", "items": ["采集：麦克风", "特征：MFCC", "声学：声音→音素", "语言：音素→文字"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "语音识别流程",
                 "blocks": [
                     {"x": 20, "y": 55, "w": 80, "h": 45, "label": "采集", "color": "#6366f1"},
                     {"x": 120, "y": 55, "w": 80, "h": 45, "label": "MFCC", "color": "#fbbf24"},
                     {"x": 220, "y": 55, "w": 80, "h": 45, "label": "声学模型", "color": "#34d399"},
                     {"x": 320, "y": 55, "w": 80, "h": 45, "label": "语言模型", "color": "#06b6d4"},
                     {"x": 420, "y": 55, "w": 80, "h": 45, "label": "文本", "color": "#f87171"},
                 ],
                 "arrows": [
                     {"x1": 100, "y1": 77, "x2": 115, "y2": 77, "color": "#475569"},
                     {"x1": 200, "y1": 77, "x2": 215, "y2": 77, "color": "#475569"},
                     {"x1": 300, "y1": 77, "x2": 315, "y2": 77, "color": "#475569"},
                     {"x1": 400, "y1": 77, "x2": 415, "y2": 77, "color": "#475569"},
                 ]}},
            {"tag": "概念", "name": "MFCC 特征",
             "body": "<p>MFCC（梅尔频率倒谱系数）模拟人耳对频率的敏感度，每10ms一帧，通常13维。</p>",
             "points": {"title": "要点", "items": ["MFCC 最常用", "模拟人耳感知", "每10ms一帧"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "声学特征",
                 "items": [
                     {"icon": "🎵", "label": "MFCC", "desc": "梅尔频率系数", "color": "#6366f1"},
                     {"icon": "👂", "label": "人耳模拟", "desc": "对数频率感知", "color": "#34d399"},
                     {"icon": "📊", "label": "分帧", "desc": "连续帧覆盖", "color": "#fbbf24"},
                 ]}},
            {"tag": "对比", "name": "传统 vs 端到端",
             "body": "<p>传统：声学+发音+语言模型独立训练。端到端：音频→文字一步到位（DeepSpeech、Whisper）。</p>",
             "points": {"title": "对比", "items": ["传统：多组件独立", "端到端：一体化网络", "需语言学知识 vs 纯数据驱动"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "传统 vs 端到端",
                 "left": {"title": "传统", "color": "#f87171", "items": ["多组件独立", "发音词典", "复杂管线"]},
                 "right": {"title": "端到端", "color": "#34d399", "items": ["单一网络", "音频→文字", "联合优化"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>语音识别让机器听懂人类语言。应用：Siri、小爱同学、语音输入。</p>",
             "points": {"title": "速记", "items": ["ASR：Audio→Text", "MFCC 特征提取", "端到端深度学习趋势"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "语音识别总结",
                 "items": [
                     {"icon": "🎤", "label": "ASR", "desc": "语音转文字", "color": "#6366f1"},
                     {"icon": "🔊", "label": "特征", "desc": "MFCC 提取", "color": "#34d399"},
                     {"icon": "📱", "label": "应用", "desc": "助手·输入", "color": "#06b6d4"},
                 ]}},
        ],
    }


# =====================================================================
# 14) 图像识别
# =====================================================================
def build_image_recognition():
    return {
        "meta": {"title": "图像识别", "subtitle": "CNN · 图像分类 · 目标检测", "module": "ai", "accent": "orange"},
        "cards": [
            {"num": 1, "title": "图像识别", "body": "让计算机看懂图像"},
            {"num": 2, "title": "CNN", "body": "卷积神经网络"},
            {"num": 3, "title": "分类", "body": "识别图像类别"},
            {"num": 4, "title": "检测", "body": "定位+识别"},
        ],
        "steps": [
            {"tag": "概念", "name": "图像识别基础",
             "body": "<p>三大任务：分类（什么类别）、检测（在哪+是什么）、分割（逐像素）。图像=数字矩阵（RGB三通道）。</p>",
             "points": {"title": "任务", "items": ["分类：整体识别", "检测：定位+识别", "分割：逐像素"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "视觉任务",
                 "items": [
                     {"icon": "🏷️", "label": "分类", "desc": "整图类别", "color": "#6366f1"},
                     {"icon": "📦", "label": "检测", "desc": "框出物体", "color": "#fbbf24"},
                     {"icon": "🔪", "label": "分割", "desc": "逐像素", "color": "#34d399"},
                 ]}},
            {"tag": "概念", "name": "CNN",
             "body": "<p>卷积层（特征提取）→ 池化层（降维）→ 全连接层（分类）。浅层检测边缘，深层检测复杂特征。</p>",
             "points": {"title": "结构", "items": ["卷积：特征提取", "池化：降维", "全连接：分类", "层级特征"]},
             "scene": "neural_net", "sceneArgs": {"title": "CNN 结构", "layers": [4, 6, 8, 6, 4], "highlight": [], "inputLayer": 0}},
            {"tag": "对比", "name": "CNN vs 全连接",
             "body": "<p>CNN：局部连接+权值共享+平移不变性，更适合图像任务。</p>",
             "points": {"title": "优势", "items": ["局部连接：参数少", "权值共享：效率高", "平移不变：位置不敏感"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "CNN vs 全连接",
                 "left": {"title": "全连接", "color": "#f87171", "items": ["全连接参数爆炸", "忽略空间结构", "不适合图像"]},
                 "right": {"title": "CNN", "color": "#34d399", "items": ["局部感受野", "权值共享", "图像首选"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>图像识别让计算机看懂世界。应用：人脸识别、自动驾驶、医学影像。</p>",
             "points": {"title": "速记", "items": ["图像＝数字矩阵", "CNN 核心技术", "分类→检测→分割"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "图像识别总结",
                 "items": [
                     {"icon": "👁️", "label": "核心", "desc": "看懂图像", "color": "#6366f1"},
                     {"icon": "🔲", "label": "CNN", "desc": "卷积神经网络", "color": "#34d399"},
                     {"icon": "🚗", "label": "应用", "desc": "人脸·自动驾驶", "color": "#06b6d4"},
                 ]}},
        ],
    }


# =====================================================================
# 15) 计算机组成
# =====================================================================
def build_computer_architecture():
    return {
        "meta": {"title": "计算机组成", "subtitle": "CPU · 内存 · 存储 · I/O", "module": "hardware", "accent": "slate"},
        "cards": [
            {"num": 1, "title": "冯·诺依曼", "body": "存储程序顺序执行"},
            {"num": 2, "title": "CPU", "body": "ALU+控制+寄存器"},
            {"num": 3, "title": "存储器", "body": "Cache·RAM·SSD"},
            {"num": 4, "title": "总线", "body": "数据·地址·控制"},
        ],
        "steps": [
            {"tag": "概念", "name": "冯·诺依曼架构",
             "body": "<p>五大部件：运算器(ALU)+控制器+存储器+输入+输出。核心思想：存储程序。</p>",
             "points": {"title": "五大部件", "items": ["运算器：计算", "控制器：指挥", "存储器：存放", "I/O：人机交互"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "冯·诺依曼架构",
                 "blocks": [
                     {"x": 100, "y": 40, "w": 140, "h": 50, "label": "控制器", "color": "#fbbf24"},
                     {"x": 280, "y": 40, "w": 140, "h": 50, "label": "运算器", "color": "#6366f1"},
                     {"x": 190, "y": 120, "w": 140, "h": 50, "label": "主存储器", "color": "#34d399"},
                     {"x": 50, "y": 200, "w": 120, "h": 50, "label": "输入设备", "color": "#06b6d4"},
                     {"x": 350, "y": 200, "w": 120, "h": 50, "label": "输出设备", "color": "#f87171"},
                 ],
                 "arrows": [
                     {"x1": 170, "y1": 90, "x2": 170, "y2": 115, "color": "#475569"},
                     {"x1": 350, "y1": 90, "x2": 260, "y2": 115, "color": "#475569"},
                     {"x1": 110, "y1": 170, "x2": 110, "y2": 195, "color": "#475569"},
                     {"x1": 410, "y1": 170, "x2": 410, "y2": 195, "color": "#475569"},
                 ]}},
            {"tag": "概念", "name": "CPU 内部",
             "body": "<p>ALU 计算 + 控制单元译码 + 寄存器（最快）+ Cache(L1/L2/L3)。执行周期：取指→译码→执行→写回。</p>",
             "points": {"title": "CPU 组成", "items": ["ALU：算术逻辑", "控制单元：指令控制", "寄存器：最快", "Cache：速度缓冲"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "CPU 部件",
                 "items": [
                     {"icon": "🧮", "label": "ALU", "desc": "算术逻辑", "color": "#6366f1"},
                     {"icon": "🎛️", "label": "控制", "desc": "取指译码", "color": "#fbbf24"},
                     {"icon": "⚡", "label": "Cache", "desc": "L1/L2/L3", "color": "#06b6d4"},
                 ]}},
            {"tag": "概念", "name": "存储层次",
             "body": "<p>寄存器(1ns) > Cache(2~50ns) > 内存(100ns) > SSD(50µs) > HDD(10ms)。速度越快越贵越小。</p>",
             "points": {"title": "层次", "items": ["寄存器最快", "Cache 几 MB", "RAM GB 级别", "SSD/HDD TB 级别"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "存储层次",
                 "left": {"title": "快小贵", "color": "#f87171", "items": ["寄存器 ~1ns", "L1 ~2ns", "L2 ~10ns"]},
                 "right": {"title": "慢大便宜", "color": "#34d399", "items": ["内存 ~100ns", "SSD ~50µs", "HDD ~10ms"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>CPU + 存储器 + I/O，通过总线连接。冯·诺依曼存储程序思想仍是基础。</p>",
             "points": {"title": "速记", "items": ["CPU=ALU+控制+寄存器", "存储：Cache>RAM>SSD", "总线：数据·地址·控制"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "组成总结",
                 "items": [
                     {"icon": "🧠", "label": "CPU", "desc": "ALU+控制+寄存器", "color": "#6366f1"},
                     {"icon": "💾", "label": "存储", "desc": "Cache·RAM·SSD", "color": "#34d399"},
                     {"icon": "🔌", "label": "总线", "desc": "连接通道", "color": "#fbbf24"},
                 ]}},
        ],
    }


# =====================================================================
# 16) 网络基础
# =====================================================================
def build_network_basics():
    return {
        "meta": {"title": "网络基础", "subtitle": "IP · TCP/IP · HTTP · 拓扑", "module": "hardware", "accent": "indigo"},
        "cards": [
            {"num": 1, "title": "网络", "body": "计算机互联"},
            {"num": 2, "title": "IP", "body": "设备标识"},
            {"num": 3, "title": "TCP/IP", "body": "核心协议栈"},
            {"num": 4, "title": "HTTP", "body": "网页传输"},
        ],
        "steps": [
            {"tag": "概念", "name": "网络概念",
             "body": "<p>IP地址标识设备，端口标识应用（HTTP=80），DNS域名解析，路由器连接不同网络。</p>",
             "points": {"title": "要素", "items": ["IP：设备标识", "端口：应用标识", "DNS：域名转IP", "路由：数据转发"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "网络拓扑",
                 "blocks": [
                     {"x": 30, "y": 50, "w": 100, "h": 45, "label": "电脑A", "color": "#6366f1"},
                     {"x": 150, "y": 50, "w": 100, "h": 45, "label": "电脑B", "color": "#6366f1"},
                     {"x": 270, "y": 50, "w": 100, "h": 45, "label": "电脑C", "color": "#6366f1"},
                     {"x": 120, "y": 130, "w": 120, "h": 45, "label": "交换机", "color": "#34d399"},
                     {"x": 300, "y": 130, "w": 100, "h": 45, "label": "路由器", "color": "#fbbf24"},
                     {"x": 400, "y": 130, "w": 80, "h": 45, "label": "互联网", "color": "#f87171"},
                 ],
                 "arrows": [
                     {"x1": 80, "y1": 95, "x2": 170, "y2": 125, "color": "#475569"},
                     {"x1": 200, "y1": 95, "x2": 190, "y2": 125, "color": "#475569"},
                     {"x1": 320, "y1": 95, "x2": 220, "y2": 125, "color": "#475569"},
                     {"x1": 360, "y1": 130, "x2": 395, "y2": 130, "color": "#475569"},
                 ]}},
            {"tag": "概念", "name": "TCP/IP 四层",
             "body": "<p>应用层(HTTP/FTP) → 传输层(TCP/UDP) → 网络层(IP) → 网络接口层(以太网/WiFi)。</p>",
             "points": {"title": "四层", "items": ["应用：HTTP/FTP", "传输：TCP/UDP", "网络：IP路由", "接口：物理传输"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "TCP/IP 模型",
                 "items": [
                     {"icon": "📱", "label": "应用层", "desc": "HTTP·FTP", "color": "#6366f1"},
                     {"icon": "📦", "label": "传输层", "desc": "TCP·UDP", "color": "#34d399"},
                     {"icon": "🌐", "label": "网络层", "desc": "IP路由", "color": "#fbbf24"},
                     {"icon": "🔌", "label": "接口层", "desc": "以太网·WiFi", "color": "#06b6d4"},
                 ]}},
            {"tag": "对比", "name": "TCP vs UDP",
             "body": "<p>TCP：可靠有序面向连接（网页/邮件）。UDP：快速无连接（直播/游戏）。</p>",
             "points": {"title": "对比", "items": ["TCP：可靠但慢", "UDP：快但丢包", "TCP 三次握手", "UDP 直接发"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "TCP vs UDP",
                 "left": {"title": "TCP", "color": "#6366f1", "items": ["面向连接", "可靠传输", "有序到达"]},
                 "right": {"title": "UDP", "color": "#fbbf24", "items": ["无连接", "不可靠", "低延迟"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>计算机网络是数字时代的基础设施。IP标识、DNS解析、TCP可靠、HTTP网页。</p>",
             "points": {"title": "速记", "items": ["IP 设备标识", "DNS 域名转IP", "TCP 可靠 UDP 快速", "HTTP 网页基础"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "网络总结",
                 "items": [
                     {"icon": "🌐", "label": "IP", "desc": "设备标识", "color": "#6366f1"},
                     {"icon": "📦", "label": "TCP/IP", "desc": "四层协议", "color": "#34d399"},
                     {"icon": "🌍", "label": "DNS", "desc": "域名解析", "color": "#06b6d4"},
                 ]}},
        ],
    }


# =====================================================================
# 17) 设计流程
# =====================================================================
def build_design_process():
    return {
        "meta": {"title": "设计流程", "subtitle": "需求 · 方案 · 原型 · 测试 · 迭代", "module": "tech", "accent": "amber"},
        "cards": [
            {"num": 1, "title": "流程", "body": "系统解决问题"},
            {"num": 2, "title": "需求", "body": "明确问题"},
            {"num": 3, "title": "方案", "body": "头脑风暴选择"},
            {"num": 4, "title": "迭代", "body": "测试改进"},
        ],
        "steps": [
            {"tag": "概念", "name": "设计流程",
             "body": "<p>需求分析→方案设计→原型制作→测试评估→改进迭代。用户中心+快速迭代。</p>",
             "points": {"title": "五步", "items": ["需求：明确问题", "方案：创意设计", "原型：动手制作", "测试：验证功能", "迭代：持续改进"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "设计流程",
                 "nodes": [
                     {"id": 0, "x": 160, "y": 20, "w": 100, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 160, "y": 80, "w": 120, "h": 44, "label": "需求分析"},
                     {"id": 2, "x": 160, "y": 145, "w": 120, "h": 44, "label": "方案设计"},
                     {"id": 3, "x": 160, "y": 210, "w": 120, "h": 44, "label": "原型制作"},
                     {"id": 4, "x": 160, "y": 275, "w": 120, "h": 44, "label": "测试评估"},
                     {"id": 5, "x": 160, "y": 340, "w": 120, "h": 44, "label": "满足要求?", "type": "decision"},
                     {"id": 6, "x": 360, "y": 340, "w": 80, "h": 40, "label": "修改"},
                     {"id": 7, "x": 160, "y": 415, "w": 100, "h": 40, "label": "完成", "type": "startend"},
                 ],
                 "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6, "否"], [6, 4], [5, 7, "是"]], "active": -1,
             }},
            {"tag": "概念", "name": "需求分析",
             "body": "<p>明确问题→用户研究→功能需求→约束条件。好的需求分析避免方向错误。</p>",
             "points": {"title": "四问", "items": ["什么问题？", "谁用？", "要什么功能？", "有什么限制？"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "需求分析",
                 "items": [
                     {"icon": "🎯", "label": "问题", "desc": "核心目标", "color": "#6366f1"},
                     {"icon": "👥", "label": "用户", "desc": "用户研究", "color": "#34d399"},
                     {"icon": "⚠️", "label": "约束", "desc": "时间成本", "color": "#f87171"},
                 ]}},
            {"tag": "概念", "name": "原型迭代",
             "body": "<p>头脑风暴→草图→方案评估→原型制作→用户测试→改进。低成本快速验证。</p>",
             "points": {"title": "要点", "items": ["头脑风暴多方案", "草图快速可视化", "原型验证想法", "测试获得反馈"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "设计与原型",
                 "left": {"title": "方案设计", "color": "#6366f1", "items": ["头脑风暴", "绘制草图", "方案评估"]},
                 "right": {"title": "原型制作", "color": "#fbbf24", "items": ["低成本材料", "快速制作", "用户测试"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>好的设计是迭代出来的。用户中心 + 快速迭代。</p>",
             "points": {"title": "设计思维", "items": ["共情→定义→构思→原型→测试"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "设计总结",
                 "items": [
                     {"icon": "🎯", "label": "需求", "desc": "明确问题", "color": "#6366f1"},
                     {"icon": "💡", "label": "方案", "desc": "创意设计", "color": "#fbbf24"},
                     {"icon": "🔄", "label": "迭代", "desc": "测试改进", "color": "#34d399"},
                 ]}},
        ],
    }


# =====================================================================
# 18) 材料与工具
# =====================================================================
def build_materials_tools():
    return {
        "meta": {"title": "材料与工具", "subtitle": "材料分类 · 性能 · 工具 · 安全", "module": "tech", "accent": "orange"},
        "cards": [
            {"num": 1, "title": "材料", "body": "金属·非金属·复合"},
            {"num": 2, "title": "性能", "body": "强度·硬度·韧性"},
            {"num": 3, "title": "工具", "body": "测量·切割·连接"},
            {"num": 4, "title": "安全", "body": "防护装备"},
        ],
        "steps": [
            {"tag": "概念", "name": "材料分类",
             "body": "<p>金属（钢铝铜）、无机非金属（陶瓷玻璃）、有机高分子（塑料橡胶）、复合材料（玻璃钢碳纤维）。</p>",
             "points": {"title": "四大类", "items": ["金属：强度高导电", "非金属：耐热绝缘", "高分子：轻便", "复合材料：综合"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "材料分类",
                 "items": [
                     {"icon": "⚙️", "label": "金属", "desc": "钢铝铜合金", "color": "#6366f1"},
                     {"icon": "🏺", "label": "非金属", "desc": "陶瓷玻璃", "color": "#f87171"},
                     {"icon": "🧪", "label": "高分子", "desc": "塑料橡胶", "color": "#34d399"},
                 ]}},
            {"tag": "概念", "name": "材料性能",
             "body": "<p>强度（抗破坏）、硬度（抗划伤）、韧性（抗冲击）、导电性、导热性。</p>",
             "points": {"title": "指标", "items": ["强度：抗破坏", "硬度：抗划伤", "韧性：抗冲击", "导电导热"]},
             "scene": "data_table", "sceneArgs": {
                 "title": "材料性能对比",
                 "headers": ["材料", "强度", "硬度", "导电", "加工"],
                 "rows": [["钢材", "高", "高", "低", "中"], ["铝材", "中", "中", "高", "易"], ["铜", "中", "中", "很高", "易"], ["陶瓷", "低", "很高", "绝缘", "难"], ["塑料", "低", "低", "绝缘", "易"]],
                 "highlight": []}},
            {"tag": "概念", "name": "加工工具",
             "body": "<p>测量（钢尺/卡尺）、划线（划针）、切割（手锯/美工刀）、锉削（锉刀）、钻孔（手电钻）、连接（螺丝/胶）。</p>",
             "points": {"title": "分类", "items": ["测量：精确到mm", "切割：手锯·美工刀", "钻孔：手电钻", "连接：螺丝·胶粘"]},
             "scene": "comparison", "sceneArgs": {
                 "title": "手动 vs 电动",
                 "left": {"title": "手动", "color": "#6366f1", "items": ["手锯·锉刀·锤子", "成本低易控制", "适合精细"]},
                 "right": {"title": "电动", "color": "#fbbf24", "items": ["电钻·角磨机", "效率高省力", "注意安全"]}}},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>选材：性能匹配+成本可控+加工可行。安全：护目镜+夹紧+归位。</p>",
             "points": {"title": "安全口诀", "items": ["护目镜必须戴", "工件夹紧再操作", "工具用后归位"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "材料与工具总结",
                 "items": [
                     {"icon": "🧱", "label": "材料", "desc": "金属·非金属", "color": "#6366f1"},
                     {"icon": "🔧", "label": "工具", "desc": "手动·电动", "color": "#fbbf24"},
                     {"icon": "🛡️", "label": "安全", "desc": "防护装备", "color": "#f87171"},
                 ]}},
        ],
    }


# =====================================================================
# 19) 电子控制技术
# =====================================================================
def build_electronic_control():
    return {
        "meta": {"title": "电子控制技术", "subtitle": "传感器 · 控制器 · 执行器 · 反馈", "module": "tech", "accent": "red"},
        "cards": [
            {"num": 1, "title": "电子控制", "body": "传感器+控制+执行"},
            {"num": 2, "title": "传感器", "body": "光敏·温度·红外"},
            {"num": 3, "title": "控制器", "body": "单片机·PLC"},
            {"num": 4, "title": "执行器", "body": "电机·LED·蜂鸣器"},
        ],
        "steps": [
            {"tag": "概念", "name": "控制系统",
             "body": "<p>输入（传感器）→ 控制（控制器）→ 输出（执行器）。加反馈→闭环控制。</p>",
             "points": {"title": "组成", "items": ["输入：传感器采集", "控制：单片机决策", "输出：执行器动作", "反馈：闭环精确"]},
             "scene": "block_diagram", "sceneArgs": {
                 "title": "电子控制系统",
                 "blocks": [
                     {"x": 40, "y": 60, "w": 100, "h": 50, "label": "传感器", "color": "#34d399"},
                     {"x": 180, "y": 60, "w": 100, "h": 50, "label": "控制器", "color": "#6366f1"},
                     {"x": 320, "y": 60, "w": 100, "h": 50, "label": "执行器", "color": "#f87171"},
                     {"x": 180, "y": 150, "w": 100, "h": 40, "label": "反馈", "color": "#06b6d4"},
                 ],
                 "arrows": [
                     {"x1": 140, "y1": 85, "x2": 175, "y2": 85, "color": "#475569"},
                     {"x1": 280, "y1": 85, "x2": 315, "y2": 85, "color": "#475569"},
                     {"x1": 230, "y1": 145, "x2": 230, "y2": 170, "color": "#475569"},
                     {"x1": 190, "y1": 170, "x2": 145, "y2": 95, "color": "#475569"},
                 ]}},
            {"tag": "概念", "name": "常见传感器",
             "body": "<p>光敏（光线→电阻）、温度（热敏/DS18B20）、红外(PIR人体感应)、超声波（测距）、压力。</p>",
             "points": {"title": "类型", "items": ["光敏：光线检测", "温度：测温", "红外：人体感应", "超声波：测距"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "传感器",
                 "items": [
                     {"icon": "☀️", "label": "光敏", "desc": "光线→电阻", "color": "#fbbf24"},
                     {"icon": "🌡️", "label": "温度", "desc": "温度→电压", "color": "#f87171"},
                     {"icon": "📡", "label": "超声波", "desc": "声波测距", "color": "#34d399"},
                 ]}},
            {"tag": "示例", "name": "自动路灯",
             "body": "<p>光敏电阻检测环境光 → 低于阈值开灯 → 高于阈值关灯。开环控制典型。</p>",
             "points": {"title": "原理", "items": ["光敏检测亮度", "比较器判断", "低于阈值开", "高于阈值关"]},
             "scene": "flowchart", "sceneArgs": {
                 "title": "自动灯控",
                 "nodes": [
                     {"id": 0, "x": 150, "y": 20, "w": 100, "h": 40, "label": "开始", "type": "startend"},
                     {"id": 1, "x": 150, "y": 80, "w": 120, "h": 44, "label": "读取光敏"},
                     {"id": 2, "x": 150, "y": 150, "w": 140, "h": 44, "label": "光强 < 阈值?", "type": "decision"},
                     {"id": 3, "x": 40, "y": 150, "w": 80, "h": 40, "label": "开灯"},
                     {"id": 4, "x": 280, "y": 150, "w": 80, "h": 40, "label": "关灯"},
                     {"id": 5, "x": 150, "y": 230, "w": 100, "h": 40, "label": "结束", "type": "startend"},
                 ], "edges": [[0, 1], [1, 2], [2, 3, "是"], [2, 4, "否"], [3, 5], [4, 5]], "active": -1,
             }},
            {"tag": "总结", "name": "要点回顾",
             "body": "<p>电子控制是信息技术与物理世界的桥梁。传感器→控制器→执行器。</p>",
             "points": {"title": "速记", "items": ["输入→控制→输出", "传感器感知", "控制器决策", "执行器动作"]},
             "scene": "concept_cards", "sceneArgs": {
                 "title": "电子控制总结",
                 "items": [
                     {"icon": "📥", "label": "输入", "desc": "传感器", "color": "#34d399"},
                     {"icon": "🧠", "label": "控制", "desc": "单片机", "color": "#6366f1"},
                     {"icon": "📤", "label": "输出", "desc": "执行器", "color": "#f87171"},
                 ]}},
        ],
    }


# =====================================================================
# REGISTRY
# =====================================================================
REGISTRY = {
    "bubble_sort": build_bubble_sort,
    "selection_sort": build_selection_sort,
    "binary_search": build_binary_search,
    "insertion_sort": build_insertion_sort,
    "algorithm_complexity": build_algorithm_complexity,
    "flowchart_basics": build_flowchart_basics,
    "python_basics": build_python_basics,
    "scratch_basics": build_scratch_basics,
    "cpp_basics": build_cpp_basics,
    "excel_data": build_excel_data,
    "database_intro": build_database_intro,
    "ml_concepts": build_ml_concepts,
    "voice_recognition": build_voice_recognition,
    "image_recognition": build_image_recognition,
    "computer_architecture": build_computer_architecture,
    "network_basics": build_network_basics,
    "design_process": build_design_process,
    "materials_tools": build_materials_tools,
    "electronic_control": build_electronic_control,
}


def main(argv):
    if not argv or argv[0] == "list":
        print("已注册教程 (%d):" % len(REGISTRY))
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
    out = Path(argv[1]) if len(argv) > 1 else Path.cwd() / f"tutorial-{k}.html"
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
