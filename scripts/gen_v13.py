# -*- coding: utf-8 -*-
"""V13 后期、调色与影像处理（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V13"; rows=[]
def simple(cat,items,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en,"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("调色风格",[("青橙调","teal and orange cinematic grade"),("复古褪色","faded retro film grade"),("电影感调色","cinematic color grading"),("黑金调","black and gold grade"),("胶片模拟","film emulation grade"),("莫兰迪灰调","muted morandi grade"),("高饱和鲜艳","vivid saturated grade"),("暗黑冷调","dark moody cool grade"),("阳光暖调","warm sunny grade"),("色调分离","split toning"),("漂白旁路","bleach bypass grade"),("赛博霓虹调","cyberpunk neon grade"),("日系清新","japanese fresh clean grade"),("港风复古","hong kong retro grade"),("奶油胶片","creamy film grade"),("黑白单色","black and white monochrome"),("褐调怀旧","sepia tone"),("低饱和高级灰","desaturated muted grade")],"后期;调色风格")
simple("调色技术",[("一级校色","primary color correction"),("二级调色","secondary selective grade"),("LUT","LUT lookup table"),("曲线调整","curves adjustment"),("HSL调整","hsl adjustment"),("色轮","color wheels grade"),("肤色保护","skin tone protection"),("匹配镜头","shot matching")],"后期;调色技术")
simple("修图润饰",[("磨皮","skin retouching smooth"),("液化","liquify reshape"),("瑕疵修复","blemish healing"),("锐化","sharpening"),("降噪","noise reduction"),("中性灰精修","dodge and burn"),("双曲线磨皮","dual curve retouch"),("高低频","frequency separation"),("牙齿美白","teeth whitening"),("眼神光","catchlight enhance")],"后期;修图")
simple("合成与滤镜",[("抠像合成","compositing layers"),("景深雾化","post depth of field haze"),("胶片颗粒","film grain overlay"),("漏光叠加","light leak overlay"),("光晕眩光","glow bloom lens flare"),("暗角","vignette"),("故障艺术","glitch art effect"),("HDR合成","hdr merge"),("双重曝光","double exposure"),("镜头光晕","lens flare overlay"),("色差","chromatic aberration effect"),("扫描线","scanline crt effect"),("做旧划痕","film scratches dust")],"后期;合成滤镜")
simple("输出与交付",[("导出格式","export format"),("色彩空间交付","color space delivery"),("锐化输出","output sharpening"),("压缩优化","compression optimization"),("打印输出","print output")],"后期;输出")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
