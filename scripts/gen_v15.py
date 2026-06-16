# -*- coding: utf-8 -*-
"""V15 视觉风格、审美标签与时代风格（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V15"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("类型与审美标签",[
("赛博朋克","Cyberpunk","霓虹高科技低生活","cyberpunk, neon high-tech dystopia","赛博朋克"),
("蒸汽朋克","Steampunk","维多利亚蒸汽齿轮","steampunk, victorian gears steam","蒸汽朋克"),
("柴油朋克","Dieselpunk","战间柴油工业","dieselpunk, interwar diesel","柴油朋克"),
("废土风","Wasteland","末世荒废","post-apocalyptic wasteland aesthetic","废土风"),
("国潮","Guochao","中式潮流","chinese guochao trendy style","国潮"),
("侘寂","Wabi-Sabi","质朴残缺美","wabi-sabi imperfect rustic","侘寂"),
("极简主义","Minimalism","极简留白","minimalist aesthetic","极简主义"),
("孟菲斯","Memphis","几何撞色波普","memphis design bold geometric","孟菲斯"),
("蒸汽波","Vaporwave","紫粉复古数码","vaporwave, retro digital pink purple","蒸汽波"),
("Y2K千禧","Y2K","千禧金属未来","Y2K, metallic millennium futurism","Y2K"),
("暗黑哥特","Dark Gothic","暗黑哥特","dark gothic aesthetic","暗黑哥特"),
("治愈系","Healing/Cozy","温暖治愈","cozy healing aesthetic","治愈系"),
("梦核","Dreamcore","梦境超现实","dreamcore surreal nostalgic","梦核"),
("怪核","Weirdcore","诡异不安","weirdcore uncanny","怪核"),
("故障艺术","Glitch Art","数字故障美学","glitch art aesthetic","故障艺术"),
("低多边形","Low Poly","低面几何","low poly geometric","低多边形"),
("扁平化","Flat Design","扁平简洁","flat design illustration","扁平化"),
("3D盲盒潮玩","3D Toy","C4D潮玩质感","3d blind box toy render","3D潮玩"),
("黏土风","Clay Render","黏土质感","clay render claymation style","黏土风")],"风格;标签")
block("时代美学",[
("80年代复古","80s Retro","霓虹合成器波","1980s retro neon synthwave","80年代复古"),
("90年代","90s","千禧前怀旧","1990s nostalgic aesthetic","90年代"),
("复古未来主义","Retrofuturism","旧时代想象未来","retrofuturism","复古未来主义"),
("世纪中期现代","Mid-Century Modern","50-60年代现代","mid-century modern aesthetic","世纪中期现代")],"风格;时代")
block("地域与网络美学",[
("日系","Japanese Aesthetic","清新日系","japanese aesthetic clean","日系"),
("韩系","Korean Aesthetic","柔和韩系","korean soft aesthetic","韩系"),
("和风浮世","Japanese Traditional","和风传统","traditional japanese aesthetic","和风"),
("cottagecore田园","Cottagecore","田园温馨","cottagecore rural cozy","田园核"),
("暗黑学院","Dark Academia","复古学术","dark academia aesthetic","暗黑学院"),
("阈限空间","Liminal Space","空旷诡异过渡","liminal space eerie empty","阈限空间")],"风格;地域网络")
block("品牌调性与媒介",[
("高级感","Premium/Luxe","高级奢华","premium luxury aesthetic","高级感"),
("科技感","Tech/Futuristic","未来科技","futuristic tech aesthetic","科技感"),
("年轻活力","Youthful Vibrant","青春活力","youthful vibrant playful","年轻活力"),
("拼贴混媒","Mixed Media Collage","拼贴混合","mixed media collage","拼贴混媒"),
("手绘+数字","Hand-drawn Digital","手绘数字结合","hand-drawn digital hybrid","手绘数字")],"风格;品牌媒介")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
