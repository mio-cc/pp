# -*- coding: utf-8 -*-
"""V11 时尚、服装与造型（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V11"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("廓形剪裁",[
("A字廓形","A-Line","上窄下宽","A-line silhouette","A字廓形"),
("H字廓形","H-Line","直筒","H-line straight silhouette","H字廓形"),
("X字廓形","X-Line","收腰","X-line cinched waist","X字廓形"),
("O字廓形","Cocoon","茧型","cocoon O-line silhouette","O字廓形"),
("oversize廓形","Oversized","宽松超大","oversized loose silhouette","oversize廓形"),
("修身剪裁","Slim Fit","贴身","slim tailored fit","修身剪裁")],"时尚;廓形")
block("面料与纹样",[
("丝绸","Silk","顺滑光泽","silk fabric, sheen drape","丝绸"),
("针织","Knit","毛线针织","knit fabric texture","针织"),
("牛仔丹宁","Denim","丹宁","denim fabric","牛仔丹宁"),
("皮革","Leather Garment","皮衣","leather garment","皮革"),
("雪纺","Chiffon","轻薄飘逸","chiffon sheer flowing","雪纺"),
("格纹","Plaid","格子纹","plaid tartan pattern","格纹"),
("条纹","Stripes","条纹","stripe pattern","条纹"),
("印花","Floral Print","花卉印花","floral print","印花"),
("豹纹","Animal Print","动物纹","leopard animal print","豹纹"),
("亮片","Sequins","闪片","sequins sparkle","亮片")],"时尚;面料纹样")
block("风格流派",[
("街头风","Streetwear","潮流街头","streetwear style","街头风"),
("极简风","Minimalist Fashion","极简","minimalist fashion","极简风"),
("复古风","Vintage Fashion","怀旧复古","vintage retro fashion","复古风"),
("朋克风","Punk","叛逆铆钉","punk fashion, studs","朋克风"),
("波西米亚","Boho","民族流苏","bohemian boho style","波西米亚"),
("学院风","Preppy","学院制服","preppy academia style","学院风"),
("哥特风","Gothic Fashion","暗黑哥特","gothic dark fashion","哥特风"),
("洛丽塔","Lolita","蓬裙甜美","lolita fashion","洛丽塔"),
("赛博朋克时装","Cyberpunk Fashion","未来机能","cyberpunk techwear fashion","赛博朋克时装"),
("机能风","Techwear","功能机能","techwear functional","机能风"),
("国潮汉服","Hanfu","中式汉服","hanfu chinese traditional","国潮汉服"),
("高定礼服","Haute Couture","高级定制","haute couture gown","高定礼服")],"时尚;风格")
block("时代时尚",[
("20年代Gatsby","1920s Flapper","流苏装饰艺术","1920s flapper art deco fashion","20年代"),
("50年代","1950s","蓬裙优雅","1950s elegant full skirt","50年代"),
("70年代","1970s","嬉皮迪斯科","1970s disco hippie","70年代"),
("80年代","1980s","夸张垫肩","1980s bold shoulder pad","80年代"),
("90年代","1990s","极简grunge","1990s grunge minimal","90年代"),
("Y2K千禧","Y2K","千禧未来感","Y2K millennium fashion","Y2K千禧")],"时尚;时代")
block("配饰发妆",[
("帽饰","Hats","帽子配饰","hat headwear accessory","帽饰"),
("珠宝首饰","Jewelry","项链耳环","jewelry necklace earrings","珠宝首饰"),
("箱包","Handbag","手袋","designer handbag","箱包"),
("墨镜","Sunglasses","太阳镜","sunglasses","墨镜"),
("浓妆","Bold Makeup","浓艳妆容","bold dramatic makeup","浓妆"),
("裸妆","Natural Makeup","自然裸妆","natural nude makeup","裸妆"),
("烟熏妆","Smoky Eye","烟熏眼妆","smoky eye makeup","烟熏妆"),
("复古红唇","Red Lip","复古红唇","vintage red lip","复古红唇"),
("盘发","Updo","盘起发型","elegant updo hairstyle","盘发"),
("波浪长发","Wavy Hair","波浪卷发","long wavy hair","波浪长发")],"时尚;配饰发妆")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
