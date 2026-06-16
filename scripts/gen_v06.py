# -*- coding: utf-8 -*-
"""V06 灯光与色彩科学（穷举，颜色细分到具体色与深浅浓淡）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V06"; rows=[]
def add(cat,zh,en,defs,pen,pcn,tags):
    rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items: add(cat,zh,en,defs,pen,pcn,tags)

# 色温整档
for k,cn,en in [("1800K","烛光极暖","candlelight warm 1800K"),("2700K","暖白居家","warm white 2700K"),("3200K","钨丝灯暖","tungsten 3200K warm"),("4000K","中性暖白","neutral warm 4000K"),("5500K","正午日光","daylight 5500K"),("6500K","标准冷白","cool daylight 6500K"),("8000K","阴天冷蓝","overcast cool blue 8000K"),("10000K","极冷蓝调","deep blue 10000K")]:
    add("光度与照度 / 色温",k+"色温",k+" Color Temp",k+"，"+cn,k+" color temperature, "+en,k+" 色温, "+cn,"色彩;色温")
block("光度与照度 / 光的属性",[
("高显色CRI","High CRI","高显色还原真实","high CRI accurate color rendering","高显色 CRI"),
("光通量","Luminous Flux","光输出总量","luminous flux brightness","光通量"),
("照度","Illuminance","表面受光强度","illuminance lux on surface","照度"),
("硬光","Hard Light","小光源锐利阴影","hard light crisp shadows","硬光"),
("柔光","Soft Light","大光源柔和","soft diffused light","柔光"),
("体积光","Volumetric Light","可见光束丁达尔","volumetric god rays light beams","体积光, 丁达尔")],"色彩;光度")

# 色彩模型与三属性
block("色彩科学 / 色彩模型",[
("RGB加色","RGB Additive","红绿蓝加色","RGB additive color","RGB加色"),
("CMYK减色","CMYK Subtractive","印刷减色","CMYK subtractive print color","CMYK减色"),
("HSL色彩","HSL Model","色相饱和明度","HSL hue saturation lightness","HSL"),
("Lab色彩","Lab Color","设备无关色彩","Lab device independent color","Lab色彩"),
("色相","Hue","颜色种类","hue, color family","色相"),
("饱和度","Saturation","色彩鲜艳度","saturation, color intensity","饱和度"),
("明度","Brightness","明暗程度","brightness value","明度")],"色彩;模型")
block("色彩科学 / 色彩空间",[
("sRGB","sRGB","标准网络色域","sRGB standard gamut","sRGB"),
("Adobe RGB","Adobe RGB","广色域印刷","Adobe RGB wide gamut","Adobe RGB"),
("DCI-P3","DCI-P3","电影广色域","DCI-P3 cinema gamut","DCI-P3"),
("Rec.2020","Rec.2020","超广色域HDR","Rec.2020 ultra wide HDR","Rec.2020")],"色彩;色域")

# 颜色体系：按色相穷举 + 深浅浓淡
COLORS={
"红色系":[("正红","Pure Red","vivid pure red"),("深红","Deep Red","deep crimson red"),("酒红","Wine Red","wine burgundy red"),("绯红","Scarlet","scarlet bright red"),("砖红","Brick Red","muted brick red"),("浅粉红","Light Pink","soft light pink"),("玫红","Rose Red","rose magenta red"),("珊瑚红","Coral","warm coral pink")],
"橙黄系":[("橙色","Orange","vivid orange"),("橘红","Orange Red","orange red"),("焦糖","Caramel","warm caramel brown-orange"),("柠檬黄","Lemon Yellow","bright lemon yellow"),("金黄","Golden Yellow","rich golden yellow"),("土黄","Ochre","earthy ochre yellow"),("米黄","Cream","soft cream beige"),("芥末黄","Mustard","muted mustard yellow")],
"绿色系":[("翠绿","Emerald","vivid emerald green"),("墨绿","Dark Green","deep dark green"),("薄荷绿","Mint","light mint green"),("橄榄绿","Olive","muted olive green"),("草绿","Grass Green","fresh grass green"),("青绿","Teal Green","blue-green teal"),("抹茶绿","Matcha","soft matcha green")],
"蓝青系":[("天蓝","Sky Blue","light sky blue"),("宝蓝","Royal Blue","vivid royal blue"),("藏青","Navy","deep navy blue"),("普鲁士蓝","Prussian Blue","dark prussian blue"),("克莱因蓝","Klein Blue","intense klein blue"),("蒂芙尼蓝","Tiffany Blue","tiffany robin-egg blue"),("浅蓝","Pale Blue","pale soft blue"),("青色","Cyan","bright cyan")],
"紫粉系":[("紫罗兰","Violet","vivid violet"),("丁香紫","Lilac","soft lilac purple"),("深紫","Deep Purple","deep royal purple"),("薰衣草","Lavender","pale lavender"),("品红","Magenta","vivid magenta"),("藕粉","Dusty Pink","muted dusty pink")],
"中性系":[("纯黑","Pure Black","pure black"),("纯白","Pure White","pure white"),("浅灰","Light Gray","light neutral gray"),("深灰","Charcoal","dark charcoal gray"),("驼色","Camel","warm camel tan"),("米白","Off White","warm off-white"),("大地棕","Earth Brown","earthy brown")],
}
for fam,lst in COLORS.items():
    for zh,en,pen in lst:
        add("色彩体系 / "+fam, zh, en, zh+"，具体取色", pen+" color", zh+", "+("浓郁" if "深" in zh or "墨" in zh else "")+ "色", "色彩;颜色")

# 色彩搭配
block("色彩搭配",[
("互补色","Complementary","对比强烈撞色","complementary color contrast","互补色撞色"),
("邻近色","Analogous","和谐相邻","analogous harmonious colors","邻近色"),
("三角配色","Triadic","三等分平衡","triadic color scheme","三角配色"),
("分裂互补","Split-Complementary","柔和对比","split complementary scheme","分裂互补"),
("单色系","Monochromatic","同色深浅","monochromatic shades","单色系"),
("同类色","Tonal","同色调微差","tonal subtle palette","同类色")],"色彩;搭配")

# 色彩心理/流行色调
block("色调与氛围",[
("暖色调","Warm Tone","温暖橙红黄","warm color tone, orange red yellow","暖色调"),
("冷色调","Cool Tone","清冷蓝青","cool color tone, blue cyan","冷色调"),
("高饱和活力","High Saturation","鲜艳活力","high saturation vivid vibrant","高饱和"),
("低饱和高级","Muted/Desaturated","低饱和高级感","muted desaturated, sophisticated","低饱和, 高级灰"),
("莫兰迪色","Morandi Palette","灰调柔和","morandi muted gray palette","莫兰迪色"),
("马卡龙色","Macaron Pastel","粉嫩马卡龙","macaron pastel soft colors","马卡龙色"),
("复古胶片色","Retro Film Tone","怀旧暖褪色","retro faded film tone","复古胶片色"),
("赛博霓虹色","Cyberpunk Neon","紫粉青霓虹","cyberpunk neon purple pink cyan","赛博霓虹色"),
("撞色","Color Blocking","高对比色块","bold color blocking","撞色"),
("黑金奢华","Black Gold Luxe","黑金高奢","black and gold luxury","黑金奢华")],"色彩;色调")

# 色彩管理与感知
block("色彩管理与感知",[
("白平衡","White Balance","校正色温偏色","white balance correction","白平衡"),
("色调映射","Tone Mapping","HDR压缩动态","HDR tone mapping","色调映射"),
("色彩对比","Color Contrast","冷暖明暗对比","color contrast warm cool","色彩对比"),
("同时对比","Simultaneous Contrast","相邻色相互影响","simultaneous color contrast","同时对比"),
("高动态范围","HDR","明暗皆有细节","high dynamic range detail","HDR")],"色彩;管理感知")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
