#!/usr/bin/env python3
"""二次修复：扩展 <8字 的 definition_short 到 8-30字"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"

def expand_def(row):
    """针对性扩展短定义"""
    uid = row["term_uid"]
    zh = row["zh_term"]
    en = row["en_term"]
    defshort = row["definition_short"]
    vol = row["volume_code"]
    cat = row["category"]

    # 已经够长，跳过
    if len(defshort) >= 8:
        return defshort

    # V01 摄影体系
    if vol == "V01":
        # 快门速度
        if "快门" in cat:
            if "秒" in zh or "s" in en:
                return f"{zh}快门速度，适合{('运动捕捉' if '1/' in zh else '长曝光创作')}。"
        # 景深与虚化
        if "景深" in cat or "散景" in cat:
            if "深景深" in zh: return "前后景物皆清晰的大景深效果。"
            if "浅景深" in zh: return "主体清晰背景虚化的小景深效果。"
            if "奶油散景" in zh: return "柔美奶油质感的圆润虚化效果。"
            if "旋焦散景" in zh: return "旋转漩涡状的特殊虚化效果。"
            if "光斑" in zh: return "虚化区域点光源形成的光斑形状。"
            if "二线性" in zh: return "虚化边缘出现双线描边的不良散景。"
        # 镜头畸变
        if "畸变" in cat or "畸变" in zh:
            if "桶形" in zh: return "画面向外凸起的广角镜头畸变。"
            if "枕形" in zh: return "画面向内凹陷的长焦镜头畸变。"
        # 镜头缺陷
        if "色散" in zh or "紫边" in zh: return "高反差边缘出现的彩色色差。"
        if "暗角" in zh: return "画面四角光量衰减变暗的现象。"
        if "眩光" in zh: return "强光源在镜头内反射形成的光斑。"
        if "变形宽银幕" in zh: return "模拟变形宽银幕镜头的水平眩光。"
        if "光晕" in zh or "Halation" in en: return "强光在胶片乳剂层扩散的光晕效果。"
        # 传感器与相机
        if "传感器" in zh or "英寸" in zh: return f"{zh}画幅传感器的尺寸规格。"
        if "单反" in zh: return "反光板取景的传统数码单反相机。"
        if "无反" in zh: return "无反光板的电子取景微单相机。"
        if "胶片" in zh: return "使用胶卷感光的传统胶片相机。"
        if "拍立得" in zh: return "即拍即得的一次成像相机。"
        if "CCD" in zh: return "CCD传感器的数码相机成像特性。"
        # 光线时刻
        if "黄金时刻" in zh: return "日出日落时暖调柔光的摄影黄金时段。"
        if "蓝调时刻" in zh: return "黎明黄昏时冷蓝调的摄影魔幻时段。"

    # V02 电影摄影
    if vol == "V02":
        # 景别
        if "景别" in cat:
            if "大特写" in zh: return "极端近距离拍摄局部细节的景别。"
            if "特写" in zh: return "面部或物体细节占满画面的景别。"
            if "近景" in zh: return "胸部以上或物体主体的景别。"
            if "中景" in zh: return "腰部以上或场景中景的景别。"
            if "全景" in zh: return "人物全身或场景全貌的景别。"
            if "远景" in zh: return "环境为主人物较小的景别。"
            if "大远景" in zh: return "广阔环境人物极小的景别。"
        # 机位运动
        if "运动" in cat or "镜头运动" in cat:
            if "推" in zh: return "镜头向前推进靠近主体的运动。"
            if "拉" in zh: return "镜头向后拉远离主体的运动。"
            if "摇" in zh: return "镜头水平或垂直旋转扫视的运动。"
            if "移" in zh: return "镜头平行移动跟随主体的运动。"
            if "跟" in zh: return "镜头跟随移动主体保持距离的运动。"
            if "升降" in zh: return "镜头垂直升降改变高度的运动。"
            if "环绕" in zh: return "镜头围绕主体旋转拍摄的运动。"
            if "甩" in zh: return "快速摇动镜头产生模糊过渡的运动。"
            if "变焦" in zh: return "改变焦距放大缩小的镜头运动。"
            if "手持" in zh: return "手持拍摄产生晃动真实感的运动。"
            if "斯坦尼康" in zh: return "稳定器平滑流畅的移动拍摄。"
            if "航拍" in zh: return "空中俯瞰的无人机或直升机拍摄。"
        # 影调
        if "影调" in cat or "布光" in cat:
            if "高调" in zh: return "明亮轻快的高调光效影调。"
            if "低调" in zh: return "暗沉浓重的低调光效影调。"
            if "伦勃朗" in zh: return "三角形亮斑的经典人像布光。"
            if "蝴蝶光" in zh: return "鼻下蝴蝶形阴影的美妆布光。"
            if "边缘光" in zh: return "勾勒轮廓分离背景的侧后方光。"
            if "顶光" in zh: return "垂直向下投射的头顶光源。"
            if "侧光" in zh: return "来自侧方强调质感的光线。"
            if "轮廓光" in zh: return "背后勾勒边缘的分离光。"

    # V06 灯光与色彩
    if vol == "V06":
        # 色相细分
        if "色相" in cat:
            if "深" in zh: return f"深浓的{zh.replace('深','')}色调。"
            if "中" in zh: return f"适中的{zh.replace('中','')}色调。"
            if "浅" in zh: return f"浅淡的{zh.replace('浅','')}色调。"
            if "浓" in zh: return f"高饱和的浓郁{zh.replace('浓','')}色。"
            if "淡" in zh: return f"低饱和的柔和{zh.replace('淡','')}色。"
        # 颜色
        if "红" in zh or "Red" in en: return f"{zh}的暖调色彩。"
        if "橙" in zh or "Orange" in en: return f"{zh}的温暖活力色彩。"
        if "黄" in zh or "Yellow" in en: return f"{zh}的明快色彩。"
        if "绿" in zh or "Green" in en: return f"{zh}的自然生机色彩。"
        if "青" in zh or "Cyan" in en: return f"{zh}的清新色彩。"
        if "蓝" in zh or "Blue" in en: return f"{zh}的冷静色彩。"
        if "紫" in zh or "Purple" in en: return f"{zh}的神秘色彩。"
        if "品红" in zh or "Magenta" in en: return f"{zh}的艳丽色彩。"
        # 色温
        if "色温" in cat or "K" in zh:
            return f"{zh}的色温氛围，用于特定照明场景。"

    # V07 材质与渲染
    if vol == "V07":
        if "金属" in zh: return f"{zh}的金属光泽与反射特性。"
        if "石" in zh or "岩" in zh: return f"{zh}的粗糙质感与自然纹理。"
        if "木" in zh: return f"{zh}的天然纹理与温润质感。"
        if "布" in zh or "织物" in zh: return f"{zh}的柔软质感与编织纹理。"
        if "玻璃" in zh: return f"{zh}的透明与折射光学特性。"
        if "PBR" in en or "渲染" in zh: return f"{zh}的渲染算法与光照计算方式。"

    # V08 Prompt工程
    if vol == "V08":
        if "质量" in cat: return f"{zh}提示词，提升生成图像质量。"
        if "负向" in cat: return f"负向提示词，抑制{zh.replace('负向','')}。"
        if "采样" in cat: return f"{zh}采样算法的生成特性。"
        if "ControlNet" in cat: return f"{zh}控制方式的条件生成。"

    # 兜底：补充到8字
    if len(defshort) < 4:
        return f"{zh}的视觉特征与应用方式。"
    else:
        return defshort + f"在{vol.replace('V0','V').replace('V1','V1')}体系中的应用。"

if __name__ == "__main__":
    rows = []
    fixed = 0
    with open(CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        for row in reader:
            old = row["definition_short"]
            if len(old) < 8:
                row["definition_short"] = expand_def(row)
                if len(row["definition_short"]) > len(old):
                    fixed += 1
            rows.append(row)

    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ 二次修复完成，扩展了 {fixed} 条短定义")
