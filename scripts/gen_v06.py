# -*- coding: utf-8 -*-
"""V06 灯光与色彩科学（穷举级：色相×深浅浓淡系统化 + 命名色 + 色温/模型/搭配/管理）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V06"; rows=[]
def add(cat,zh,en,defs,pen,pcn,tags):
    rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items: add(cat,zh,en,defs,pen,pcn,tags)

# ===== 色温整档 =====
for k,cn,en in [("1800K","烛光极暖","candlelight warm 1800K"),("2200K","落日暖橙","sunset warm 2200K"),("2700K","暖白居家","warm white 2700K"),("3200K","钨丝灯暖","tungsten 3200K warm"),("4000K","中性暖白","neutral warm 4000K"),("5000K","标准白","standard white 5000K"),("5500K","正午日光","daylight 5500K"),("6500K","标准冷白","cool daylight 6500K"),("7500K","阴天蓝","shade blue 7500K"),("10000K","极冷蓝调","deep blue 10000K")]:
    add("光度与照度 / 色温",k,k+" Color Temp",k+"，"+cn,k+" color temperature, "+en,k+" 色温, "+cn,"色彩;色温")

# ===== 颜色体系：色相族 × 变体 系统化穷举 =====
HUES=[("红色系","红","red"),("橙色系","橙","orange"),("黄色系","黄","yellow"),("黄绿系","黄绿","chartreuse"),("绿色系","绿","green"),("青绿系","青绿","teal"),("青色系","青","cyan"),("蓝色系","蓝","blue"),("靛蓝系","靛蓝","indigo"),("紫色系","紫","purple"),("品红系","品红","magenta"),("粉色系","粉","pink"),("棕色系","棕","brown"),("灰中性系","灰","gray")]
VARIANTS=[("正","pure","vivid pure"),("深","deep","deep dark"),("浅","light","light pale"),("暗","dark","dark muted"),("亮","bright","bright vivid"),("柔","soft","soft pastel"),("浓","rich","rich saturated"),("灰","muted","muted grayish"),("淡","pale","pale washed")]
for fam,zh,en in HUES:
    for vz,ve,vp in VARIANTS:
        name=vz+zh+"色" if vz!="正" else zh+"色"
        add("色彩体系 / "+fam, name, (ve.title()+" "+en.title()).strip(), name+"，具体取色", vp+" "+en+" color", name, "色彩;颜色")

# ===== 命名特色色 =====
block("色彩体系 / 命名色",[
("克莱因蓝","Klein Blue","强烈纯净蓝","intense international klein blue","克莱因蓝"),
("蒂芙尼蓝","Tiffany Blue","知更鸟蛋青蓝","tiffany robin egg blue","蒂芙尼蓝"),
("普鲁士蓝","Prussian Blue","深邃普鲁士蓝","dark prussian blue","普鲁士蓝"),
("孔雀蓝","Peacock Blue","孔雀蓝绿","peacock blue-green","孔雀蓝"),
("藏青","Navy","深海军蓝","deep navy blue","藏青"),
("湖蓝","Lake Blue","清澈湖蓝","clear lake blue","湖蓝"),
("酒红","Burgundy","葡萄酒红","wine burgundy red","酒红"),
("绯红","Scarlet","鲜亮绯红","bright scarlet red","绯红"),
("胭脂红","Carmine","胭脂深红","carmine crimson","胭脂红"),
("珊瑚粉","Coral","暖珊瑚粉","warm coral pink","珊瑚粉"),
("藕荷色","Dusty Lilac","灰调藕荷","muted dusty lilac","藕荷色"),
("薰衣草紫","Lavender","柔和薰衣草","soft lavender purple","薰衣草紫"),
("丁香紫","Lilac","浅丁香紫","light lilac","丁香紫"),
("莫兰迪灰粉","Morandi Pink","灰调莫兰迪粉","morandi muted pink","莫兰迪灰粉"),
("祖母绿","Emerald","浓郁祖母绿","rich emerald green","祖母绿"),
("墨绿","Pine Green","深墨绿","deep pine green","墨绿"),
("橄榄绿","Olive","灰橄榄绿","muted olive green","橄榄绿"),
("薄荷绿","Mint","清新薄荷绿","fresh mint green","薄荷绿"),
("抹茶绿","Matcha","柔抹茶绿","soft matcha green","抹茶绿"),
("芥末黄","Mustard","复古芥末黄","retro mustard yellow","芥末黄"),
("姜黄","Turmeric","暖姜黄","warm turmeric yellow","姜黄"),
("土黄赭石","Ochre","大地赭黄","earthy ochre","土黄赭石"),
("驼色","Camel","暖驼色","warm camel tan","驼色"),
("焦糖色","Caramel","焦糖棕橙","caramel brown","焦糖色"),
("巧克力棕","Chocolate","深巧克力棕","dark chocolate brown","巧克力棕"),
("米白","Off White","暖米白","warm off-white cream","米白"),
("象牙白","Ivory","柔象牙白","soft ivory white","象牙白"),
("炭黑","Charcoal","深炭黑灰","dark charcoal","炭黑"),
("银灰","Silver Gray","金属银灰","metallic silver gray","银灰"),
("玫瑰金","Rose Gold","暖玫瑰金","rose gold","玫瑰金"),
("香槟金","Champagne","柔香槟金","champagne gold","香槟金")],"色彩;命名色")

# ===== 模型/空间 =====
block("色彩科学 / 色彩模型与空间",[
("RGB加色","RGB Additive","红绿蓝加色","RGB additive color","RGB"),
("CMYK减色","CMYK Subtractive","印刷减色","CMYK subtractive print","CMYK"),
("HSL","HSL Model","色相饱和明度","HSL hue saturation lightness","HSL"),
("Lab","Lab Color","设备无关","Lab device independent","Lab"),
("色相","Hue","颜色种类","hue color family","色相"),
("饱和度","Saturation","鲜艳度","saturation intensity","饱和度"),
("明度","Value","明暗","brightness value","明度"),
("sRGB","sRGB","标准网络色域","sRGB gamut","sRGB"),
("Adobe RGB","Adobe RGB","广色域","Adobe RGB wide gamut","Adobe RGB"),
("DCI-P3","DCI-P3","电影色域","DCI-P3 cinema gamut","DCI-P3"),
("Rec.2020","Rec.2020","超广HDR色域","Rec.2020 HDR gamut","Rec.2020")],"色彩;模型空间")

# ===== 搭配 =====
block("色彩搭配",[
("互补色","Complementary","对比撞色","complementary contrast","互补色"),
("邻近色","Analogous","和谐相邻","analogous harmony","邻近色"),
("三角配色","Triadic","三等分","triadic scheme","三角配色"),
("分裂互补","Split-Complementary","柔和对比","split complementary","分裂互补"),
("四角配色","Tetradic","双互补","tetradic scheme","四角配色"),
("单色系","Monochromatic","同色深浅","monochromatic shades","单色系"),
("同类色","Tonal","同调微差","tonal palette","同类色"),
("无彩色","Achromatic","黑白灰","achromatic black white gray","无彩色")],"色彩;搭配")

# ===== 色调氛围 =====
block("色调与氛围",[
("暖色调","Warm Tone","橙红黄暖","warm tone orange red","暖色调"),
("冷色调","Cool Tone","蓝青冷","cool tone blue cyan","冷色调"),
("高饱和活力","High Saturation","鲜艳活力","high saturation vivid","高饱和"),
("低饱和高级","Muted","低饱和高级","muted desaturated sophisticated","低饱和"),
("莫兰迪色","Morandi","灰调柔和","morandi muted gray palette","莫兰迪色"),
("马卡龙色","Macaron","粉嫩马卡龙","macaron pastel","马卡龙色"),
("复古胶片色","Retro Film","怀旧褪色","retro faded film tone","复古胶片色"),
("赛博霓虹色","Cyber Neon","紫粉青霓虹","cyberpunk neon palette","赛博霓虹色"),
("撞色","Color Blocking","高对比色块","bold color blocking","撞色"),
("黑金奢华","Black Gold","黑金高奢","black and gold luxury","黑金奢华"),
("大地色系","Earth Tone","自然大地色","earth tone palette","大地色系"),
("糖果色","Candy Color","明快糖果","bright candy colors","糖果色")],"色彩;色调")

# ===== 光质 + 管理感知 =====
block("光度与照度 / 光的属性",[
("高显色CRI","High CRI","高显色还原","high CRI accurate rendering","高显色"),
("硬光","Hard Light","锐利阴影","hard light crisp shadows","硬光"),
("柔光","Soft Light","柔和散射","soft diffused light","柔光"),
("体积光","Volumetric Light","丁达尔光束","volumetric god rays","体积光"),
("逆光","Backlight","轮廓逆光","backlight rim glow","逆光"),
("散射光","Diffused","均匀散射","diffused even light","散射光")],"色彩;光质")
block("色彩管理与感知",[
("白平衡","White Balance","校正偏色","white balance correction","白平衡"),
("色调映射","Tone Mapping","HDR压缩","HDR tone mapping","色调映射"),
("色彩对比","Color Contrast","冷暖明暗对比","color contrast","色彩对比"),
("同时对比","Simultaneous Contrast","相邻互影响","simultaneous contrast","同时对比"),
("HDR","HDR","高动态细节","high dynamic range","HDR"),
("色彩恒常","Color Constancy","知觉恒常","color constancy perception","色彩恒常")],"色彩;管理感知")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
