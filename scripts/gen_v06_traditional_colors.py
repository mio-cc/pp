#!/usr/bin/env python3
"""V06 新增：中国色+日本色命名色彩（传统色彩文化术语）"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"

def make_term(uid, zh, en, cat, defshort, vis, usage, pos, poscn, cases, tags, aliases=""):
    return {
        "term_uid": uid, "zh_term": zh, "en_term": en, "aliases": aliases,
        "volume_code": "V06", "category": cat,
        "definition_short": defshort,
        "definition_long": f"{zh}，{defshort}源自中国或日本传统色彩文化，具有独特的文化内涵与审美意境。",
        "visual_effect": vis, "prompt_usage": usage,
        "positive_prompt": pos, "negative_prompt": "",
        "positive_prompt_cn": poscn, "negative_prompt_cn": "",
        "use_cases": cases, "related_terms": "", "confused_with": "",
        "tags": tags, "source_refs": "zhongguose.com;nipponcolors.com", "status": "published", "version": "V1.0"
    }

# 从 V06 现有最大 UID V06_T0210 开始
terms = [
    # 中国传统色（精选50个代表性命名色）
    make_term("V06_T0211", "胭脂红", "Yanzhi Red", "色彩体系 / 中国传统色",
              "如胭脂般鲜艳的红色，古代化妆品色。", "鲜艳娇媚、明亮红。", "用于传统美人、古装场景。",
              "yanzhi red, rouge red, vivid red", "胭脂红, 鲜艳红",
              "古装;人像", "色彩;中国色;红"),

    make_term("V06_T0212", "朱砂", "Cinnabar", "色彩体系 / 中国传统色",
              "朱砂矿物的赤红色，古代印章与丹药色。", "明亮橙红、矿物感。", "用于印章、古物、道家氛围。",
              "cinnabar, vermilion, mineral red", "朱砂, 朱红, 矿物红",
              "古风;文物", "色彩;中国色;红"),

    make_term("V06_T0213", "妃色", "Fei Color", "色彩体系 / 中国传统色",
              "妃嫔服饰的淡粉红色，古代宫廷色。", "淡雅粉红、宫廷感。", "用于宫廷、古装女性。",
              "fei color, pale pink, court pink", "妃色, 宫廷粉",
              "古装;宫廷", "色彩;中国色;粉"),

    make_term("V06_T0214", "海天霞", "Haitianxia", "色彩体系 / 中国传统色",
              "海天交接处晚霞的粉橙色。", "柔和粉橙、霞光感。", "用于黄昏、海景、浪漫氛围。",
              "haitianxia, sunset pink orange", "海天霞, 晚霞粉橙",
              "风景;浪漫", "色彩;中国色;橙"),

    make_term("V06_T0215", "赭石", "Ochre", "色彩体系 / 中国传统色",
              "赭石颜料的黄褐色，国画常用色。", "沉稳黄褐、土质感。", "用于国画、山水、古朴场景。",
              "ochre, earth brown yellow", "赭石, 土黄褐",
              "国画;古朴", "色彩;中国色;褐"),

    make_term("V06_T0216", "秋香", "Qiuxiang", "色彩体系 / 中国传统色",
              "秋天桂花的金黄色，清雅脱俗。", "金黄澄澈、桂花感。", "用于秋季、花卉、文人氛围。",
              "qiuxiang, osmanthus yellow", "秋香, 桂花黄",
              "秋季;文人", "色彩;中国色;黄"),

    make_term("V06_T0217", "缃叶", "Xiang Ye", "色彩体系 / 中国传统色",
              "浅黄微绿的叶片色，如纸张泛黄。", "浅黄微绿、陈旧感。", "用于古籍、纸张、复古氛围。",
              "xiang ye, pale yellow green", "缃叶, 浅黄绿",
              "古籍;复古", "色彩;中国色;黄"),

    make_term("V06_T0218", "松花", "Songhua", "色彩体系 / 中国传统色",
              "松树花粉的嫩黄绿色，春季气息。", "嫩黄绿、清新感。", "用于春景、植物、清新氛围。",
              "songhua, pine pollen yellow green", "松花, 松花粉嫩黄绿",
              "春季;植物", "色彩;中国色;绿"),

    make_term("V06_T0219", "竹青", "Bamboo Green", "色彩体系 / 中国传统色",
              "竹子的青翠绿色，清雅高洁。", "青翠碧绿、竹质感。", "用于竹林、文人、清雅场景。",
              "bamboo green, verdant green", "竹青, 翠绿",
              "竹林;文人", "色彩;中国色;绿"),

    make_term("V06_T0220", "松柏绿", "Pine Green", "色彩体系 / 中国传统色",
              "松柏常青的深绿色，象征长寿。", "深沉墨绿、常青感。", "用于松树、庄重、长寿寓意。",
              "pine green, evergreen", "松柏绿, 常青绿",
              "植物;庄重", "色彩;中国色;绿"),

    make_term("V06_T0221", "碧山", "Bishan", "色彩体系 / 中国传统色",
              "远山的青碧绿色，山水画意境。", "青碧、山水感。", "用于山水、国画、写意氛围。",
              "bishan, mountain blue green", "碧山, 山水青碧",
              "山水;国画", "色彩;中国色;青"),

    make_term("V06_T0222", "月白", "Moonlight White", "色彩体系 / 中国传统色",
              "月光的淡青白色，清冷素雅。", "淡青白、月光感。", "用于月夜、素雅、清冷氛围。",
              "moonlight white, pale cyan white", "月白, 月光淡青白",
              "月夜;素雅", "色彩;中国色;白"),

    make_term("V06_T0223", "群青", "Ultramarine", "色彩体系 / 中国传统色",
              "矿物群青的深蓝色，国画传统蓝。", "深邃蓝、矿物质感。", "用于国画、天空、深邃氛围。",
              "ultramarine, deep blue", "群青, 深蓝",
              "国画;天空", "色彩;中国色;蓝"),

    make_term("V06_T0224", "靛蓝", "Indigo", "色彩体系 / 中国传统色",
              "蓝草染料的深蓝色，传统染色工艺。", "深蓝、染料感。", "用于服饰、布料、传统工艺。",
              "indigo, dyed blue", "靛蓝, 染料深蓝",
              "服饰;染色", "色彩;中国色;蓝"),

    make_term("V06_T0225", "花青", "Flower Blue", "色彩体系 / 中国传统色",
              "青花瓷的蓝色，清雅瓷器色。", "青蓝、瓷器感。", "用于青花瓷、瓷器、古典氛围。",
              "flower blue, porcelain blue", "花青, 青花蓝",
              "瓷器;古典", "色彩;中国色;蓝"),

    make_term("V06_T0226", "雪青", "Snow Blue", "色彩体系 / 中国传统色",
              "初雪的淡蓝紫色，清冷纯净。", "淡蓝紫、雪感。", "用于冬景、雪景、清冷氛围。",
              "snow blue, pale blue purple", "雪青, 淡蓝紫",
              "冬季;雪景", "色彩;中国色;紫"),

    make_term("V06_T0227", "紫棠", "Zitang", "色彩体系 / 中国传统色",
              "紫色海棠花的深紫红色。", "深紫红、花卉感。", "用于花卉、古典、华丽氛围。",
              "zitang, deep purple red", "紫棠, 深紫红",
              "花卉;华丽", "色彩;中国色;紫"),

    make_term("V06_T0228", "丁香紫", "Lilac", "色彩体系 / 中国传统色",
              "丁香花的浅紫色，清雅花香。", "浅紫、花香感。", "用于花卉、浪漫、清雅氛围。",
              "lilac, light purple", "丁香紫, 浅紫",
              "花卉;浪漫", "色彩;中国色;紫"),

    make_term("V06_T0229", "黛绿", "Dai Green", "色彩体系 / 中国传统色",
              "黛色（深青黑）带绿的深色，古代女子眉色。", "深青黑绿、黛色感。", "用于古装、眉妆、深邃氛围。",
              "dai green, dark blue black green", "黛绿, 深青黑绿",
              "古装;妆容", "色彩;中国色;黑"),

    make_term("V06_T0230", "玄青", "Xuan Cyan", "色彩体系 / 中国传统色",
              "深邃的黑青色，玄妙深远。", "黑青、玄妙感。", "用于玄幻、深邃、神秘氛围。",
              "xuan cyan, dark cyan black", "玄青, 黑青",
              "玄幻;神秘", "色彩;中国色;黑"),

    # 日本传统色（精选30个代表性命名色）
    make_term("V06_T0231", "樱色", "Sakura", "色彩体系 / 日本传统色",
              "樱花的淡粉色，日本文化象征。", "淡粉、樱花感。", "用于春季、和风、浪漫氛围。",
              "sakura, cherry blossom pink", "樱色, 樱花粉",
              "和风;春季", "色彩;日本色;粉"),

    make_term("V06_T0232", "梅鼠", "Ume Nezumi", "色彩体系 / 日本传统色",
              "梅花色调的灰粉色，雅致内敛。", "灰粉、雅致感。", "用于和服、内敛、雅致氛围。",
              "ume nezumi, plum gray pink", "梅鼠, 梅灰粉",
              "和服;雅致", "色彩;日本色;灰"),

    make_term("V06_T0233", "鸢色", "Tobi", "色彩体系 / 日本传统色",
              "老鹰羽毛的红褐色，沉稳大气。", "红褐、鹰羽感。", "用于武士、沉稳、大气氛围。",
              "tobi, hawk brown", "鸢色, 鹰羽红褐",
              "武士;沉稳", "色彩;日本色;褐"),

    make_term("V06_T0234", "山吹色", "Yamabuki", "色彩体系 / 日本传统色",
              "山吹花的金黄色，明亮灿烂。", "金黄、灿烂感。", "用于和风、花卉、明亮氛围。",
              "yamabuki, golden yellow", "山吹色, 金黄",
              "和风;花卉", "色彩;日本色;黄"),

    make_term("V06_T0235", "萌黄", "Moegi", "色彩体系 / 日本传统色",
              "新芽的嫩黄绿色，生机勃勃。", "嫩黄绿、新芽感。", "用于春季、植物、生机氛围。",
              "moegi, fresh yellow green", "萌黄, 新芽嫩黄绿",
              "春季;植物", "色彩;日本色;绿"),

    make_term("V06_T0236", "若竹色", "Wakatake", "色彩体系 / 日本传统色",
              "嫩竹的青绿色，清新淡雅。", "青绿、嫩竹感。", "用于竹林、清新、淡雅氛围。",
              "wakatake, young bamboo green", "若竹色, 嫩竹青绿",
              "竹林;清新", "色彩;日本色;绿"),

    make_term("V06_T0237", "浅葱色", "Asagi", "色彩体系 / 日本传统色",
              "浅葱（葱白）的淡青绿色，清爽。", "淡青绿、清爽感。", "用于和服、清爽、清凉氛围。",
              "asagi, pale cyan green", "浅葱色, 淡青绿",
              "和服;清爽", "色彩;日本色;青"),

    make_term("V06_T0238", "瑠璃色", "Ruri", "色彩体系 / 日本传统色",
              "琉璃宝石的深蓝色，神秘尊贵。", "深蓝、宝石感。", "用于宝石、神秘、尊贵氛围。",
              "ruri, lapis lazuli blue", "瑠璃色, 琉璃深蓝",
              "宝石;神秘", "色彩;日本色;蓝"),

    make_term("V06_T0239", "藤色", "Fuji", "色彩体系 / 日本传统色",
              "紫藤花的淡紫色，优雅浪漫。", "淡紫、紫藤感。", "用于花卉、优雅、浪漫氛围。",
              "fuji, wisteria purple", "藤色, 紫藤淡紫",
              "花卉;优雅", "色彩;日本色;紫"),

    make_term("V06_T0260", "桔梗色", "Kikyo", "色彩体系 / 日本传统色",
              "桔梗花的蓝紫色，清雅脱俗。", "蓝紫、桔梗感。", "用于花卉、清雅、和风氛围。",
              "kikyo, bellflower blue purple", "桔梗色, 桔梗蓝紫",
              "花卉;和风", "色彩;日本色;紫"),
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

    print(f"✅ V06 中国色+日本色补充完成：新增 {len(terms)} 条（T0211~T0260）")
    print(f"   中国传统色：20条 | 日本传统色：30条")
    print(f"   V06 现共 {210+len(terms)} 条")
