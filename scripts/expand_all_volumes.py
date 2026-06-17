#!/usr/bin/env python3
"""全库深挖：基于网络提示词库（Civitai/Midjourney/Lexica）补充高频可用术语"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"

def t(uid, zh, en, vol, cat, defshort, vis, usage, pos, poscn, cases, tags, aliases=""):
    return {
        "term_uid": uid, "zh_term": zh, "en_term": en, "aliases": aliases,
        "volume_code": vol, "category": cat,
        "definition_short": defshort,
        "definition_long": f"{zh}，{defshort}是AI图像生成与视觉创作中的高频术语。",
        "visual_effect": vis, "prompt_usage": usage,
        "positive_prompt": pos, "negative_prompt": "",
        "positive_prompt_cn": poscn, "negative_prompt_cn": "",
        "use_cases": cases, "related_terms": "", "confused_with": "",
        "tags": tags, "source_refs": "Civitai;Midjourney;网络提示词库", "status": "published", "version": "V1.0"
    }

# 按卷补充（从网络搜索和知识库整理的高频术语）
terms = [
    # V01 摄影体系 - 现188/500，补充摄影题材与风格
    t("V01_T0189", "街头摄影", "Street Photography", "V01", "摄影题材",
      "捕捉街头真实瞬间的纪实摄影风格。", "真实随机、瞬间抓拍。", "用于纪实、城市、人文场景。",
      "street photography, candid", "街头摄影, 抓拍", "纪实;城市", "摄影;街拍"),

    t("V01_T0190", "长曝光", "Long Exposure", "V01", "摄影技术",
      "使用慢速快门捕捉运动轨迹或光绘。", "光轨丝滑、运动模糊。", "用于夜景、车流、星轨。",
      "long exposure, light trails", "长曝光, 光轨", "夜景;星空", "摄影;曝光"),

    t("V01_T0191", "HDR摄影", "HDR Photography", "V01", "摄影技术",
      "高动态范围合成技术，保留明暗细节。", "明暗细节丰富、层次分明。", "用于风光、建筑、逆光场景。",
      "HDR photography, high dynamic range", "HDR摄影, 高动态范围", "风光;建筑", "摄影;HDR"),

    # V02 电影摄影 - 现119/800，补充电影感关键词
    t("V02_T0120", "电影感", "Cinematic", "V02", "电影风格",
      "具有电影质感的画面氛围与叙事性。", "电影质感、叙事性强。", "用于电影化场景、故事叙事。",
      "cinematic, movie quality", "电影感, 电影质感", "电影;叙事", "电影;质感"),

    t("V02_T0121", "电影级照明", "Cinematic Lighting", "V02", "电影布光",
      "好莱坞级别的专业布光与影调。", "戏剧光效、专业布光。", "用于电影级场景、人像特写。",
      "cinematic lighting, Hollywood lighting", "电影级照明, 好莱坞布光", "电影;人像", "电影;布光"),

    t("V02_T0122", "胶片颗粒", "Film Grain", "V02", "电影质感",
      "胶片摄影的颗粒质感，增加复古感。", "颗粒质感、复古感。", "用于复古、胶片、怀旧氛围。",
      "film grain, analog texture", "胶片颗粒, 胶片质感", "复古;胶片", "电影;颗粒"),

    # V03 绘画与艺术流派 - 现117/600，补充知名艺术家与流派细分
    t("V03_T0118", "新海诚风格", "Makoto Shinkai Style", "V03", "代表性风格",
      "新海诚的动画电影视觉风格，光影细腻唯美。", "光影细腻、天空唯美、动画感。", "用于动画、唯美、治愈场景。",
      "Makoto Shinkai style, anime sky", "新海诚风格, 动画天空", "动画;唯美", "艺术;动画"),

    t("V03_T0119", "宫崎骏风格", "Hayao Miyazaki Style", "V03", "代表性风格",
      "宫崎骏的手绘动画风格，温暖治愈。", "手绘质感、温暖治愈、奇幻。", "用于吉卜力、奇幻、治愈场景。",
      "Hayao Miyazaki style, Ghibli", "宫崎骏风格, 吉卜力", "动画;治愈", "艺术;吉卜力"),

    t("V03_T0120", "水墨风", "Ink Wash Painting", "V03", "绘画媒介",
      "中国传统水墨画的晕染写意风格。", "水墨晕染、写意留白。", "用于国风、山水、写意场景。",
      "ink wash painting, Chinese ink", "水墨风, 中国水墨", "国风;写意", "艺术;水墨"),

    # V08 Prompt工程 - 现126/1000，补充质量词、艺术家、平台风格
    t("V08_T0127", "杰作", "Masterpiece", "V08", "质量修饰词",
      "顶级质量提示词，要求生成最高品质。", "精致完美、顶级品质。", "所有高质量生成场景。",
      "masterpiece, best quality", "杰作, 最高品质", "质量;通用", "提示词;质量"),

    t("V08_T0128", "8K分辨率", "8K Resolution", "V08", "质量修饰词",
      "超高清8K分辨率的细节要求。", "超高清、细节丰富。", "用于高清壁纸、商业作品。",
      "8K resolution, ultra detailed", "8K分辨率, 超高清", "高清;细节", "提示词;分辨率"),

    t("V08_T0129", "ArtStation风格", "ArtStation Trending", "V08", "平台风格",
      "ArtStation平台热门的概念艺术风格。", "概念艺术感、专业完成度。", "用于概念设计、游戏原画。",
      "trending on ArtStation, concept art", "ArtStation风格, 概念艺术", "概念;专业", "提示词;平台"),

    t("V08_T0130", "虚幻引擎渲染", "Unreal Engine", "V08", "渲染引擎",
      "虚幻引擎级别的3D渲染质感。", "写实渲染、光追效果。", "用于3D场景、游戏画面。",
      "Unreal Engine, photorealistic render", "虚幻引擎渲染, 写实渲染", "3D;写实", "提示词;引擎"),

    t("V08_T0131", "超细节", "Extremely Detailed", "V08", "质量修饰词",
      "极致细节刻画的质量要求。", "极致细节、纤毫毕现。", "用于所有需要高细节的场景。",
      "extremely detailed, intricate", "超细节, 极致细节", "细节;通用", "提示词;质量"),

    t("V08_T0132", "Greg Rutkowski风格", "Greg Rutkowski Style", "V08", "艺术家风格",
      "Greg Rutkowski的奇幻概念艺术风格。", "奇幻史诗、光影戏剧。", "用于奇幻、史诗、概念场景。",
      "by Greg Rutkowski, fantasy art", "Greg Rutkowski风格, 奇幻艺术", "奇幻;概念", "提示词;艺术家"),

    t("V08_T0133", "Artgerm风格", "Artgerm Style", "V08", "艺术家风格",
      "Artgerm（Stanley Lau）的精致人物插画风格。", "精致人物、光泽肌肤。", "用于人物、美女、插画。",
      "by Artgerm, character illustration", "Artgerm风格, 角色插画", "人物;插画", "提示词;艺术家"),

    # V14 AI模型参数 - 现63/650，补充常用采样器与ControlNet
    t("V14_T0064", "DPM++2M Karras", "DPM++2M Karras", "V14", "采样器",
      "DPM++2M Karras采样器，平衡质量与速度。", "平衡采样、质量稳定。", "通用采样，适合大多数场景。",
      "DPM++ 2M Karras sampler", "DPM++2M Karras采样器", "采样;通用", "AI;采样器"),

    t("V14_T0065", "Euler a", "Euler Ancestral", "V14", "采样器",
      "Euler祖先采样器，创意性强但不稳定。", "创意性强、随机性高。", "用于探索、创意生成。",
      "Euler a sampler, creative", "Euler a采样器, 创意", "采样;创意", "AI;采样器"),

    t("V14_T0066", "ControlNet Canny", "ControlNet Canny", "V14", "控制方式",
      "基于边缘检测的精准结构控制。", "边缘精准、结构保持。", "用于线稿转绘、结构控制。",
      "ControlNet Canny edge", "ControlNet边缘控制", "控制;边缘", "AI;ControlNet"),

    t("V14_T0067", "ControlNet Depth", "ControlNet Depth", "V14", "控制方式",
      "基于深度图的空间结构控制。", "深度保持、空间准确。", "用于3D转2D、空间控制。",
      "ControlNet depth map", "ControlNet深度控制", "控制;深度", "AI;ControlNet"),

    t("V14_T0068", "ControlNet OpenPose", "ControlNet OpenPose", "V14", "控制方式",
      "基于骨骼姿态的人物姿势控制。", "姿态精准、骨骼控制。", "用于人物姿势、角色绘制。",
      "ControlNet OpenPose skeleton", "ControlNet姿态控制", "控制;姿态", "AI;ControlNet"),

    # V15 视觉风格 - 现71/600，补充网络美学与混合风格
    t("V15_T0072", "Lo-Fi美学", "Lo-Fi Aesthetic", "V15", "网络美学",
      "低保真复古的视听美学，温暖怀旧。", "复古温暖、低保真、怀旧。", "用于插画、音乐封面、氛围图。",
      "lo-fi aesthetic, nostalgic warm", "Lo-Fi美学, 复古温暖", "美学;怀旧", "风格;Lo-Fi"),

    t("V15_T0073", "暗黑学院风", "Dark Academia", "V15", "网络美学",
      "古典学术与哥特美学结合，深沉文艺。", "古典学术、哥特暗黑、文艺。", "用于学院、图书馆、文艺场景。",
      "dark academia, gothic scholarly", "暗黑学院风, 哥特学术", "美学;学院", "风格;Dark Academia"),

    t("V15_T0074", "赛璐珞动画", "Cel Animation", "V15", "视觉风格",
      "传统手绘动画的平涂高饱和风格。", "平涂、高饱和、动画感。", "用于动画、卡通、复古动画。",
      "cel animation, flat colors", "赛璐珞动画, 平涂", "动画;复古", "风格;赛璐珞"),
]

if __name__ == "__main__":
    existing = []
    with open(CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        existing = list(reader)
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

    by_vol = {}
    for t in terms:
        by_vol.setdefault(t["volume_code"], []).append(t["zh_term"])

    print(f"✅ 全库深挖补充完成：新增 {len(terms)} 条")
    for vol in sorted(by_vol.keys()):
        print(f"   {vol}: +{len(by_vol[vol])} 条")
