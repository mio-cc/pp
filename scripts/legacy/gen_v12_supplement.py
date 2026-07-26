#!/usr/bin/env python3
"""V12 动画、分镜与动态设计 —— 补充术语（动画基础分支穷举）"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"

def simple(uid, zh, en, cat, defshort, vis, usage, pos, poscn, cases, tags, aliases="", rel="", conf=""):
    return {
        "term_uid": uid, "zh_term": zh, "en_term": en, "aliases": aliases,
        "volume_code": "V12", "category": cat,
        "definition_short": defshort,
        "definition_long": f"{zh}的详细技术说明，涵盖原理、应用场景与视觉影响。",
        "visual_effect": vis, "prompt_usage": usage,
        "positive_prompt": pos, "negative_prompt": "",
        "positive_prompt_cn": poscn, "negative_prompt_cn": "",
        "use_cases": cases, "related_terms": rel, "confused_with": conf,
        "tags": tags, "source_refs": "整理", "status": "published", "version": "V1.0"
    }

terms = [
    # 动画原则（12条原则）
    simple("V12_T0053", "挤压与拉伸", "Squash and Stretch", "动画基础 / 动画原则",
           "通过形变强调物体的弹性和重量感。", "形体压扁拉长、富有弹性。", "用于角色动作、物体碰撞。",
           "squash and stretch, elastic deformation", "挤压与拉伸, 弹性形变",
           "角色动画;物理动画", "预备动作;跟随动作", "", "动画;原则;12原则"),

    simple("V12_T0054", "预备动作", "Anticipation", "动画基础 / 动画原则",
           "动作前的蓄力准备，提示观众即将发生的动作。", "动作前的反向蓄力、清晰预示。", "用于跳跃、投掷、转身前的准备。",
           "anticipation, wind-up motion", "预备动作, 蓄力",
           "角色动画;动作设计", "挤压与拉伸;跟随动作", "", "动画;原则;12原则"),

    simple("V12_T0055", "演出布局", "Staging", "动画基础 / 动画原则",
           "通过构图、角度、景深突出主要动作和情绪。", "主体清晰、焦点明确、层次分明。", "用于关键帧、分镜设计。",
           "staging, clear presentation", "演出布局, 清晰呈现",
           "分镜;构图", "构图语法;视觉层级", "", "动画;原则;12原则"),

    simple("V12_T0056", "连续运动与姿态对应", "Straight Ahead and Pose to Pose", "动画基础 / 动画原则",
           "两种绘制方法：逐帧绘制或先定关键姿态再补中间帧。", "流畅连贯或精准控制的动作节奏。", "用于动画绘制工作流。",
           "straight ahead action, pose to pose", "连续运动, 姿态对应",
           "动画制作;工作流", "关键帧动画;逐帧动画", "", "动画;原则;12原则"),

    simple("V12_T0057", "跟随动作与重叠动作", "Follow Through and Overlapping", "动画基础 / 动画原则",
           "不同部位运动速率不同，产生拖尾和延迟效果。", "头发、衣摆、耳朵等附属部位滞后摆动。", "用于角色动画、布料、毛发。",
           "follow through, overlapping action", "跟随动作, 重叠动作",
           "角色动画;物理模拟", "挤压与拉伸;次要动作", "", "动画;原则;12原则"),

    simple("V12_T0058", "缓入缓出", "Ease In and Ease Out", "动画基础 / 动画原则",
           "动作起止时加减速，中间匀速，符合物理惯性。", "动作启动和停止时的自然过渡。", "用于所有动画曲线。",
           "ease in, ease out, slow in slow out", "缓入缓出, 渐快渐慢",
           "动画曲线;时间控制", "时间节奏;动画曲线", "", "动画;原则;12原则"),

    simple("V12_T0059", "弧形运动", "Arc", "动画基础 / 动画原则",
           "大多数自然动作沿弧线而非直线运动。", "流畅弧形轨迹、自然摆动。", "用于手臂、头部、身体转动。",
           "arc motion, curved path", "弧形运动, 曲线轨迹",
           "角色动画;运动路径", "跟随动作;缓入缓出", "", "动画;原则;12原则"),

    simple("V12_T0060", "次要动作", "Secondary Action", "动画基础 / 动画原则",
           "辅助主动作的附加动作，丰富角色性格和情绪。", "表情、手势、道具互动等辅助细节。", "用于角色表演、情绪表达。",
           "secondary action, supporting gesture", "次要动作, 辅助动作",
           "角色表演;细节", "跟随动作;演出布局", "", "动画;原则;12原则"),

    simple("V12_T0061", "时间节奏", "Timing", "动画基础 / 动画原则",
           "通过帧数控制动作的速度、重量感和情绪。", "快慢对比、节奏张弛。", "用于所有动画时间控制。",
           "timing, frame spacing", "时间节奏, 帧间距",
           "动画节奏;时间控制", "缓入缓出;夸张", "", "动画;原则;12原则"),

    simple("V12_T0062", "夸张", "Exaggeration", "动画基础 / 动画原则",
           "放大动作幅度和表情强度，增强戏剧性和可读性。", "超越现实的形变、表情、动作幅度。", "用于卡通动画、喜剧表演。",
           "exaggeration, pushed pose", "夸张, 夸大表现",
           "卡通动画;表演", "挤压与拉伸;次要动作", "", "动画;原则;12原则"),

    simple("V12_T0063", "扎实的绘画功底", "Solid Drawing", "动画基础 / 动画原则",
           "理解形体、重量、体积、空间的三维绘制能力。", "有体积感、透视准确、结构扎实的角色。", "用于角色设计、关键帧绘制。",
           "solid drawing, volume and structure", "扎实绘画, 体积感",
           "角色设计;绘画基础", "造型语言;透视", "", "动画;原则;12原则"),

    simple("V12_T0064", "吸引力", "Appeal", "动画基础 / 动画原则",
           "角色设计和动作具有魅力，吸引观众注意。", "讨喜、有性格、视觉舒适的角色形象。", "用于角色设计、动作表演。",
           "appeal, charisma", "吸引力, 魅力",
           "角色设计;视觉吸引", "角色设计;演出布局", "", "动画;原则;12原则"),

    # 帧率
    simple("V12_T0065", "24帧动画", "24fps Animation", "动画基础 / 帧率",
           "电影标准帧率，流畅且有电影感。", "流畅自然、电影质感。", "用于电影动画、高品质项目。",
           "24fps, cinematic framerate", "24帧, 电影帧率",
           "电影动画;流畅", "30帧动画;12帧动画", "30帧动画", "动画;帧率;24fps"),

    simple("V12_T0066", "30帧动画", "30fps Animation", "动画基础 / 帧率",
           "电视和网络视频常用帧率，流畅度高。", "高流畅度、清晰动作。", "用于电视动画、网络视频。",
           "30fps, television framerate", "30帧, 电视帧率",
           "电视动画;流畅", "24帧动画;60帧动画", "24帧动画", "动画;帧率;30fps"),

    simple("V12_T0067", "60帧动画", "60fps Animation", "动画基础 / 帧率",
           "超高流畅度，常用于游戏和高速运动。", "极致流畅、无顿挫感。", "用于游戏动画、体育、动作场景。",
           "60fps, ultra smooth", "60帧, 超流畅",
           "游戏动画;高速", "30帧动画;24帧动画", "", "动画;帧率;60fps"),

    simple("V12_T0068", "15帧动画", "15fps Animation", "动画基础 / 帧率",
           "低帧率动画，有顿挫感，常用于风格化表现。", "轻微顿挫、风格化节奏。", "用于独立动画、风格化项目。",
           "15fps, stylized low framerate", "15帧, 风格化低帧率",
           "风格化;独立动画", "12帧动画;24帧动画", "", "动画;帧率;15fps"),

    simple("V12_T0069", "12帧动画", "12fps Animation", "动画基础 / 帧率",
           "经典逐帧动画帧率，有明显顿挫感和手绘质感。", "顿挫感、手绘质感、复古。", "用于传统手绘动画、风格化。",
           "12fps, traditional animation", "12帧, 传统动画",
           "手绘动画;复古", "24帧动画;8帧动画", "15帧动画", "动画;帧率;12fps"),

    simple("V12_T0070", "8帧动画", "8fps Animation", "动画基础 / 帧率",
           "超低帧率，强烈顿挫感，极度风格化。", "强烈顿挫、极简帧数、实验性。", "用于实验动画、像素动画。",
           "8fps, experimental low framerate", "8帧, 实验低帧率",
           "实验动画;像素", "12帧动画;15帧动画", "", "动画;帧率;8fps"),

    # 绘制方式
    simple("V12_T0071", "逐帧动画", "Frame-by-Frame Animation", "动画基础 / 绘制方式",
           "每一帧都单独绘制，工作量大但表现力最强。", "手绘质感、流畅自然、细节丰富。", "用于传统动画、高品质场景。",
           "frame by frame, full animation", "逐帧动画, 全动画",
           "手绘动画;传统", "关键帧动画;补间动画", "关键帧动画", "动画;绘制;逐帧"),

    simple("V12_T0072", "关键帧动画", "Keyframe Animation", "动画基础 / 绘制方式",
           "先绘制关键姿态，再补充中间帧。", "精准控制、节省工作量、姿态清晰。", "用于大多数动画制作。",
           "keyframe animation, pose to pose", "关键帧动画, 姿态动画",
           "动画制作;工作流", "逐帧动画;补间动画", "", "动画;绘制;关键帧"),

    simple("V12_T0073", "补间动画", "Tweening", "动画基础 / 绘制方式",
           "软件自动计算关键帧之间的中间帧。", "自动补间、节省时间、适合简单运动。", "用于 Flash 动画、MG 动画。",
           "tweening, auto inbetween", "补间动画, 自动中间帧",
           "MG动画;Flash", "关键帧动画;骨骼动画", "", "动画;绘制;补间"),

    simple("V12_T0074", "骨骼动画", "Rigging Animation", "动画基础 / 绘制方式",
           "通过骨骼绑定驱动角色部件，适合重复动作。", "骨骼驱动、分层控制、适合循环。", "用于游戏动画、低成本项目。",
           "rigging, skeletal animation", "骨骼动画, 绑定动画",
           "游戏动画;绑定", "关键帧动画;补间动画", "", "动画;绘制;骨骼"),

    # 动画曲线
    simple("V12_T0075", "线性曲线", "Linear Curve", "动画基础 / 动画曲线",
           "匀速运动曲线，无加减速。", "机械匀速、缺乏惯性。", "用于机械运动、特殊效果。",
           "linear curve, constant speed", "线性曲线, 匀速",
           "机械动画;曲线", "缓入缓出;贝塞尔曲线", "", "动画;曲线;线性"),

    simple("V12_T0076", "贝塞尔曲线", "Bezier Curve", "动画基础 / 动画曲线",
           "可自由调节的平滑曲线，控制动画加减速。", "自由可调、平滑过渡。", "用于所有需要缓入缓出的动画。",
           "bezier curve, smooth easing", "贝塞尔曲线, 平滑缓动",
           "动画曲线;时间控制", "线性曲线;缓入缓出", "", "动画;曲线;贝塞尔"),

    simple("V12_T0077", "弹性曲线", "Elastic Curve", "动画基础 / 动画曲线",
           "超过目标后回弹的曲线，模拟弹簧效果。", "超调回弹、富有弹性。", "用于 UI 动画、弹性物体。",
           "elastic curve, bounce easing", "弹性曲线, 回弹缓动",
           "UI动画;弹性", "贝塞尔曲线;反弹曲线", "", "动画;曲线;弹性"),

    simple("V12_T0078", "反弹曲线", "Bounce Curve", "动画基础 / 动画曲线",
           "到达目标后多次小幅回弹的曲线。", "多次回弹、逐渐衰减。", "用于掉落、碰撞动画。",
           "bounce curve, bouncing easing", "反弹曲线, 弹跳缓动",
           "物理动画;碰撞", "弹性曲线;贝塞尔曲线", "", "动画;曲线;反弹"),
]


if __name__ == "__main__":
    existing = []
    with open(CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        existing = list(reader)

    existing.extend(terms)

    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(existing)

    print(f"✅ V12 补充完成，新增 {len(terms)} 条（V12_T0053~V12_T0078），V12 现共 {52+len(terms)} 条")
