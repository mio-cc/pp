# -*- coding: utf-8 -*-
"""V13 后期、调色与影像处理（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V13"; rows=[]
def block(cat,items,tags):
    for zh,en,defs in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",en,"",zh,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("调色风格",[
("青橙调","teal and orange cinematic grade","用青色阴影和橙色肤光形成电影冷暖对比"),
("复古褪色","faded retro film grade","降低对比和饱和制造老照片褪色质感"),
("电影感调色","cinematic color grading","用对比、色偏和层次塑造影院式影调"),
("黑金调","black and gold grade","以深黑和金色高光形成奢华强对比"),
("胶片模拟","film emulation grade","模拟胶片色彩曲线颗粒和宽容度的调色"),
("莫兰迪灰调","muted morandi grade","低饱和带灰度的柔和高级色彩倾向"),
("高饱和鲜艳","vivid saturated grade","提高色彩纯度形成明快强烈的画面"),
("暗黑冷调","dark moody cool grade","压低亮度并偏冷形成阴郁氛围"),
("阳光暖调","warm sunny grade","提升暖色高光形成明亮日晒感"),
("色调分离","split toning","给阴影和高光分别加入不同色相"),
("漂白旁路","bleach bypass grade","保留银盐感形成低饱和高反差影调"),
("赛博霓虹调","cyberpunk neon grade","用紫蓝粉霓虹高光形成未来都市感"),
("日系清新","japanese fresh clean grade","高明度低对比呈现通透柔和的清新色"),
("港风复古","hong kong retro grade","暖黄红绿偏色营造旧港片街头氛围"),
("奶油胶片","creamy film grade","柔和暖白与低反差形成奶油般胶片感"),
("黑白单色","black and white monochrome","去除色彩只用明暗灰阶表达画面"),
("褐调怀旧","sepia tone","整体偏棕褐色的旧照片怀旧影调"),
("低饱和高级灰","desaturated muted grade","降低色彩纯度并保留灰调层次的克制调色")],"后期;调色风格")

block("调色技术",[
("一级校色","primary color correction","整体修正曝光白平衡和基础对比的校色"),
("二级调色","secondary selective grade","针对局部颜色或区域进行选择性调色"),
("LUT","LUT lookup table","用查找表快速映射色彩和影调的预设"),
("曲线调整","curves adjustment","通过曲线控制亮度和通道色彩的工具"),
("HSL调整","hsl adjustment","按色相饱和度明度单独修改颜色"),
("色轮","color wheels grade","用阴影中间调高光色轮控制色偏"),
("肤色保护","skin tone protection","调色时保持肤色自然不偏色的处理"),
("匹配镜头","shot matching","让不同镜头曝光色彩保持连续统一")],"后期;调色技术")

block("修图润饰",[
("磨皮","skin retouching smooth","柔化皮肤纹理并减少瑕疵的修饰"),
("液化","liquify reshape","通过局部推拉改变轮廓形状的修图"),
("瑕疵修复","blemish healing","去除痘印污点和多余细节的修复"),
("锐化","sharpening","增强边缘对比提升细节清晰度的处理"),
("降噪","noise reduction","减少高ISO或压缩产生的颗粒噪点"),
("中性灰精修","dodge and burn","用明暗涂抹精修皮肤和形体起伏"),
("双曲线磨皮","dual curve retouch","用两条曲线分离修正明暗瑕疵的磨皮法"),
("高低频","frequency separation","分离颜色与纹理频率进行精细修图"),
("牙齿美白","teeth whitening","提升牙齿亮度并减少黄色情况的修饰"),
("眼神光","catchlight enhance","增强瞳孔高光让眼睛更有神采")],"后期;修图")

block("合成与滤镜",[
("抠像合成","compositing layers","分离主体并与其他背景或元素合成"),
("景深雾化","post depth of field haze","后期添加虚化和雾气增强空间纵深"),
("胶片颗粒","film grain overlay","叠加细小颗粒模拟胶片质感"),
("漏光叠加","light leak overlay","加入边缘漏光色斑形成复古意外感"),
("光晕眩光","glow bloom lens flare","扩散高光并加入镜头眩光效果"),
("暗角","vignette","压暗画面边缘以聚焦中心主体"),
("故障艺术","glitch art effect","用错位色差和数字噪声制造故障感"),
("HDR合成","hdr merge","合并多张曝光保留亮暗细节的技术"),
("双重曝光","double exposure","将两层图像叠加成诗意合成效果"),
("镜头光晕","lens flare overlay","模拟强光进入镜头产生的光斑"),
("色差","chromatic aberration effect","让红绿蓝边缘错位形成镜头失真感"),
("扫描线","scanline crt effect","加入水平线条模拟CRT屏幕显示质感"),
("做旧划痕","film scratches dust","叠加灰尘划痕制造老胶片损耗感")],"后期;合成滤镜")

block("输出与交付",[
("导出格式","export format","按用途选择JPEG/PNG/TIFF等文件格式"),
("色彩空间交付","color space delivery","按屏幕或印刷需求指定交付色彩空间"),
("锐化输出","output sharpening","在最终尺寸上补偿清晰度的锐化步骤"),
("压缩优化","compression optimization","控制码率和体积以兼顾质量和传输"),
("打印输出","print output","按纸张墨色和分辨率准备实体打印文件")],"后期;输出")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
