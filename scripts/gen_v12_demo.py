#!/usr/bin/env python3
"""V12 演示补充 —— 帧率、曲线、转场（遵循文档规范）"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"

def simple(uid, zh, en, cat, defshort, vis, usage, pos, poscn, cases, tags, aliases="", rel="", conf=""):
    """遵循21列契约"""
    return {
        "term_uid": uid, "zh_term": zh, "en_term": en, "aliases": aliases,
        "volume_code": "V12", "category": cat,
        "definition_short": defshort,
        "definition_long": f"{zh}，{defshort}在动画制作中用于控制运动流畅度、视觉风格和观看体验。",
        "visual_effect": vis, "prompt_usage": usage,
        "positive_prompt": pos, "negative_prompt": "",
        "positive_prompt_cn": poscn, "negative_prompt_cn": "",
        "use_cases": cases, "related_terms": rel, "confused_with": conf,
        "tags": tags, "source_refs": "整理", "status": "published", "version": "V1.0"
    }

terms = [
    # 帧率枚举（原子化到具体数值）
    simple("V12_T0053", "24帧动画", "24fps Animation", "动画基础 / 帧率",
           "电影标准帧率，流畅且有电影质感。", "流畅自然、电影感。", "用于电影级动画项目。",
           "24fps, cinematic framerate", "24帧, 电影帧率",
           "电影动画;流畅", "30帧动画;12帧动画", "30帧动画", "动画;帧率;24fps"),

    simple("V12_T0054", "30帧动画", "30fps Animation", "动画基础 / 帧率",
           "电视和网络视频常用帧率，高流畅度。", "高流畅、清晰动作。", "用于电视动画、网络视频。",
           "30fps, television framerate", "30帧, 电视帧率",
           "电视动画;流畅", "24帧动画;60帧动画", "24帧动画", "动画;帧率;30fps"),

    simple("V12_T0055", "60帧动画", "60fps Animation", "动画基础 / 帧率",
           "超高流畅度帧率，常用于游戏和高速运动。", "极致流畅、无顿挫。", "用于游戏动画、体育场景。",
           "60fps, ultra smooth", "60帧, 超流畅",
           "游戏动画;高速", "30帧动画;120帧动画", "", "动画;帧率;60fps"),

    simple("V12_T0056", "12帧动画", "12fps Animation", "动画基础 / 帧率",
           "经典逐帧动画帧率，有明显顿挫感和手绘质感。", "顿挫感、手绘质感。", "用于传统手绘动画。",
           "12fps, traditional animation", "12帧, 传统动画",
           "手绘动画;复古", "24帧动画;8帧动画", "15帧动画", "动画;帧率;12fps"),

    simple("V12_T0057", "8帧动画", "8fps Animation", "动画基础 / 帧率",
           "超低帧率，强烈顿挫感，极度风格化。", "强烈顿挫、实验性。", "用于实验动画、像素风格。",
           "8fps, experimental low framerate", "8帧, 实验低帧率",
           "实验动画;像素", "12帧动画;6帧动画", "", "动画;帧率;8fps"),

    # 动画曲线类型（原子化到具体曲线）
    simple("V12_T0058", "线性曲线", "Linear Curve", "动画基础 / 动画曲线",
           "匀速运动曲线，无加减速。", "机械匀速、无惯性。", "用于机械运动、特殊效果。",
           "linear curve, constant speed", "线性曲线, 匀速",
           "机械动画;曲线", "贝塞尔曲线;缓入缓出", "", "动画;曲线;线性"),

    simple("V12_T0059", "贝塞尔曲线", "Bezier Curve", "动画基础 / 动画曲线",
           "可自由调节控制点的平滑曲线，实现自定义缓动。", "自由可调、平滑过渡。", "用于所有需要缓动的动画。",
           "bezier curve, custom easing", "贝塞尔曲线, 自定义缓动",
           "动画曲线;时间控制", "线性曲线;弹性曲线", "", "动画;曲线;贝塞尔"),

    simple("V12_T0060", "弹性曲线", "Elastic Curve", "动画基础 / 动画曲线",
           "超过目标后回弹的曲线，模拟弹簧效果。", "超调回弹、弹性。", "用于UI动画、弹性物体。",
           "elastic curve, spring easing", "弹性曲线, 弹簧缓动",
           "UI动画;弹性", "贝塞尔曲线;反弹曲线", "", "动画;曲线;弹性"),

    simple("V12_T0061", "反弹曲线", "Bounce Curve", "动画基础 / 动画曲线",
           "到达目标后多次小幅回弹并逐渐衰减的曲线。", "多次回弹、衰减。", "用于掉落、碰撞动画。",
           "bounce curve, bouncing easing", "反弹曲线, 弹跳缓动",
           "物理动画;碰撞", "弹性曲线;贝塞尔曲线", "", "动画;曲线;反弹"),

    # 转场类型细分（原子化到具体转场方式）
    simple("V12_T0062", "淡入淡出转场", "Fade Transition", "动态图形 / 转场类型",
           "前画面淡出、后画面淡入的柔和过渡。", "柔和渐变、平滑衔接。", "用于时间流逝、场景切换。",
           "fade in fade out, dissolve", "淡入淡出, 溶解",
           "视频剪辑;转场", "推拉转场;擦除转场", "", "转场;淡化;MG"),

    simple("V12_T0063", "推拉转场", "Push Transition", "动态图形 / 转场类型",
           "新画面推开旧画面的转场效果。", "推挤位移、方向感强。", "用于空间切换、画面替换。",
           "push transition, slide wipe", "推拉转场, 推挤",
           "视频剪辑;转场", "淡入淡出;擦除转场", "", "转场;位移;MG"),

    simple("V12_T0064", "擦除转场", "Wipe Transition", "动态图形 / 转场类型",
           "新画面从一侧擦过遮住旧画面。", "擦过遮挡、线性推进。", "用于快速切换、节奏明快场景。",
           "wipe transition, linear reveal", "擦除转场, 线性擦过",
           "视频剪辑;转场", "推拉转场;淡入淡出", "", "转场;擦除;MG"),

    simple("V12_T0065", "旋转转场", "Rotation Transition", "动态图形 / 转场类型",
           "画面旋转翻转切换到新画面。", "旋转翻转、动感强烈。", "用于节奏快、活力场景。",
           "rotation transition, spin reveal", "旋转转场, 旋转翻转",
           "视频剪辑;转场", "缩放转场;擦除转场", "", "转场;旋转;MG"),

    simple("V12_T0066", "缩放转场", "Zoom Transition", "动态图形 / 转场类型",
           "画面放大或缩小过渡到新画面。", "放大缩小、聚焦感。", "用于强调、焦点变化。",
           "zoom transition, scale reveal", "缩放转场, 缩放过渡",
           "视频剪辑;转场", "旋转转场;淡入淡出", "", "转场;缩放;MG"),

    simple("V12_T0067", "分割转场", "Split Transition", "动态图形 / 转场类型",
           "画面从中间或多处分割展开新画面。", "分割展开、层次感。", "用于揭示、对比场景。",
           "split transition, curtain reveal", "分割转场, 分裂展开",
           "视频剪辑;转场", "擦除转场;推拉转场", "", "转场;分割;MG"),
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

    print(f"✅ V12 补充完成：新增 {len(terms)} 条（T0053~T0067），V12 现共 {52+len(terms)} 条")
