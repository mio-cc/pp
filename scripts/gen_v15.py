# -*- coding: utf-8 -*-
"""V15 视觉风格、审美标签与时代风格（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V15"; rows=[]
def simple(cat,items,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en+" aesthetic","",zh,"","","","",tags,"整理","published","V1.0"])))
simple("类型与审美标签",[("赛博朋克","cyberpunk neon dystopia"),("蒸汽朋克","steampunk victorian gears"),("柴油朋克","dieselpunk interwar"),("生物朋克","biopunk organic tech"),("废土风","post-apocalyptic wasteland"),("国潮","chinese guochao trendy"),("侘寂","wabi-sabi rustic imperfect"),("极简主义","minimalist"),("孟菲斯","memphis bold geometric"),("蒸汽波","vaporwave retro digital"),("故障波","glitchcore"),("Y2K千禧","y2k metallic millennium"),("暗黑哥特","dark gothic"),("治愈系","cozy healing"),("梦核","dreamcore surreal nostalgic"),("怪核","weirdcore uncanny"),("阈限空间","liminal space eerie"),("故障艺术","glitch art"),("低多边形","low poly"),("扁平化","flat design"),("拟物化","skeuomorphic"),("3D潮玩","3d blind box toy render"),("黏土风","clay render claymation"),("赛博格","cyborg aesthetic"),("国风水墨","chinese ink wash aesthetic"),("和风浮世","japanese ukiyo aesthetic"),("克苏鲁","lovecraftian cosmic horror"),("暗黑奇幻","dark fantasy grimdark"),("童话梦幻","fairytale whimsical"),("未来主义","futuristic"),("复古未来","retrofuturism"),("故障朋克","glitchpunk"),("超扁平","superflat takashi style")],"风格;标签")
simple("时代美学",[("50年代","1950s retro aesthetic"),("60年代","1960s mod psychedelic"),("70年代","1970s funk disco"),("80年代","1980s neon synthwave"),("90年代","1990s nostalgic"),("千禧Y2K","y2k 2000s"),("世纪中期现代","mid-century modern"),("维多利亚","victorian era"),("装饰艺术时代","art deco era 1920s"),("古典复兴","classical revival")],"风格;时代")
simple("地域与网络美学",[("日系","japanese clean aesthetic"),("韩系","korean soft aesthetic"),("欧美","western aesthetic"),("中式","chinese aesthetic"),("和风","traditional japanese"),("北欧","scandinavian aesthetic"),("地中海","mediterranean aesthetic"),("热带","tropical aesthetic"),("cottagecore田园","cottagecore rural cozy"),("暗黑学院","dark academia"),("浅色学院","light academia"),("精灵核","fairycore"),("海洋核","oceancore"),("绿野核","goblincore"),("城市废墟","urbex urban decay"),("赛博绿洲","solarpunk green utopia")],"风格;地域网络")
simple("品牌调性与媒介",[("高级感","premium luxury"),("科技感","futuristic tech"),("年轻活力","youthful vibrant"),("温暖治愈","warm healing"),("简约高效","clean efficient"),("奢华金属","luxury metallic"),("自然有机","natural organic"),("复古怀旧","retro nostalgic"),("拼贴混媒","mixed media collage"),("手绘+数字","hand-drawn digital hybrid"),("3D+2D混合","3d 2d hybrid"),("实拍+CG","live action cg composite")],"风格;品牌媒介")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
