# -*- coding: utf-8 -*-
"""V11 时尚、服装与造型（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V11"; rows=[]
def simple(cat,items,suf,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en+(" "+suf if suf else ""),"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("服装类别",[("西装","tailored suit"),("连衣裙","dress"),("晚礼服","evening gown"),("衬衫","shirt blouse"),("T恤","t-shirt"),("卫衣","hoodie"),("夹克","jacket"),("风衣","trench coat"),("大衣","overcoat"),("羽绒服","puffer jacket"),("牛仔裤","jeans"),("半身裙","skirt"),("旗袍","cheongsam qipao"),("汉服","hanfu"),("和服","kimono"),("制服","uniform"),("运动装","sportswear"),("泳装","swimwear")],"fashion garment","时尚;类别")
simple("廓形剪裁",[("A字廓形","a-line silhouette"),("H字廓形","h-line straight silhouette"),("X字廓形","x-line cinched waist"),("O字茧型","cocoon o-line silhouette"),("oversize","oversized loose silhouette"),("修身","slim fit"),("公主线","princess seam"),("收腰","cinched waist"),("垫肩","padded shoulder"),("鱼尾","mermaid silhouette"),("蓬蓬","puffy voluminous")],"silhouette","时尚;廓形")
simple("面料与纹样",[("丝绸","silk fabric sheen"),("针织","knit fabric"),("牛仔丹宁","denim"),("皮革","leather"),("雪纺","chiffon sheer"),("天鹅绒","velvet"),("蕾丝","lace"),("羊毛","wool"),("亚麻","linen"),("缎面","satin"),("格纹","plaid tartan"),("条纹","stripe pattern"),("波点","polka dot"),("印花","floral print"),("豹纹","leopard animal print"),("亮片","sequins sparkle"),("提花","jacquard"),("扎染","tie-dye")],"fabric pattern","时尚;面料纹样")
simple("风格流派",[("街头风","streetwear"),("极简风","minimalist fashion"),("复古风","vintage fashion"),("朋克风","punk fashion studs"),("波西米亚","bohemian boho"),("学院风","preppy academia"),("哥特风","gothic dark fashion"),("洛丽塔","lolita fashion"),("赛博朋克时装","cyberpunk techwear"),("机能风","techwear functional"),("国潮汉服","hanfu chinese"),("高定礼服","haute couture gown"),("法式","french chic"),("韩系","korean fashion"),("日系原宿","harajuku japanese"),("甜美","sweet girly"),("中性风","androgynous unisex"),("运动休闲","athleisure"),("优雅淑女","elegant lady"),("嘻哈","hip hop fashion")],"fashion style","时尚;风格")
simple("时代时尚",[("20年代Gatsby","1920s flapper art deco"),("30年代","1930s elegant"),("50年代","1950s full skirt"),("60年代","1960s mod"),("70年代","1970s disco hippie"),("80年代","1980s bold shoulder"),("90年代","1990s grunge minimal"),("Y2K千禧","y2k millennium")],"era fashion","时尚;时代")
simple("配饰发妆",[("帽饰","hat headwear"),("珠宝首饰","jewelry"),("项链","necklace"),("耳环","earrings"),("箱包","designer handbag"),("墨镜","sunglasses"),("丝巾","scarf"),("腰带","belt"),("手套","gloves"),("浓妆","bold dramatic makeup"),("裸妆","natural nude makeup"),("烟熏妆","smoky eye"),("复古红唇","vintage red lip"),("欧美妆","western glam makeup"),("日系妆","japanese makeup"),("韩系妆","korean makeup"),("舞台妆","stage makeup"),("盘发","elegant updo"),("波浪长发","long wavy hair"),("短发","short bob hair"),("编发","braided hair"),("丸子头","bun hairstyle")],"accessory makeup","时尚;配饰发妆")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
