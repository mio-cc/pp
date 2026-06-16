# -*- coding: utf-8 -*-
"""V13 后期、调色与影像处理（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V13"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("调色风格",[
("青橙调","Teal and Orange","冷暖对比电影色","teal and orange cinematic grade","青橙调"),
("复古褪色","Faded Retro","低对比褪色","faded retro film grade","复古褪色"),
("电影感调色","Cinematic Grade","电影色调","cinematic color grading","电影感调色"),
("黑金调","Black Gold","黑金奢华调","black and gold grade","黑金调"),
("胶片模拟","Film Emulation","模拟胶片色","film emulation LUT","胶片模拟"),
("莫兰迪灰调","Muted Grade","低饱和灰调","muted desaturated grade","莫兰迪灰调"),
("高饱和鲜艳","Vivid Grade","浓艳调色","vivid saturated grade","高饱和鲜艳"),
("暗黑冷调","Dark Moody","暗调冷色","dark moody cool grade","暗黑冷调"),
("阳光暖调","Warm Sunny","温暖阳光调","warm sunny grade","阳光暖调"),
("色调分离","Split Toning","高光阴影分色","split toning highlights shadows","色调分离")],"后期;调色")
block("调色技术",[
("一级校色","Primary Correction","整体曝光白平衡","primary color correction","一级校色"),
("二级调色","Secondary Grade","局部选区调色","secondary selective grade","二级调色"),
("LUT","Look-Up Table","调色查找表","LUT color lookup","LUT"),
("曲线调整","Curves","曲线对比","curves tone adjustment","曲线调整"),
("HSL调整","HSL Adjust","分色相调整","HSL color adjustment","HSL调整")],"后期;调色技术")
block("修图润饰",[
("磨皮","Skin Retouch","皮肤光滑","skin retouching smooth","磨皮"),
("液化","Liquify","形体调整","liquify reshape","液化"),
("瑕疵修复","Healing","去瑕疵","blemish healing removal","瑕疵修复"),
("锐化","Sharpening","增强清晰","sharpening clarity","锐化"),
("降噪","Denoise","去噪点","noise reduction","降噪"),
("中性灰精修","Dodge and Burn","明暗精修","dodge and burn retouch","中性灰精修")],"后期;修图")
block("合成与滤镜",[
("抠像合成","Compositing","多层合成","layer compositing","抠像合成"),
("景深雾化","Depth Haze","后期景深","post depth of field haze","景深雾化"),
("胶片颗粒","Film Grain Post","后期颗粒","film grain overlay","胶片颗粒"),
("漏光叠加","Light Leak","漏光效果","light leak overlay","漏光叠加"),
("光晕眩光","Glow Bloom","柔光辉光","glow bloom effect","光晕眩光"),
("暗角","Vignette Post","后期暗角","vignette post effect","暗角"),
("故障艺术","Glitch","数字故障","glitch art effect","故障艺术"),
("HDR合成","HDR Merge","高动态合成","HDR tone merge","HDR合成")],"后期;合成滤镜")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
