# -*- coding: utf-8 -*-
"""V11 时尚、服装与造型（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V11"; rows=[]
def block(cat,items,suf,tags):
    for zh,en,defs in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",en+(" "+suf if suf else ""),"",zh,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("服装类别",[
("西装","tailored suit","有翻领和结构肩线的正式套装服饰"),
("连衣裙","dress","上衣与裙摆连成一体的女性服装"),
("晚礼服","evening gown","用于正式晚宴典礼的长款华丽礼服"),
("衬衫","shirt blouse","有领口门襟的基础上装或内搭"),
("T恤","t-shirt","圆领或短袖为主的休闲针织上衣"),
("卫衣","hoodie","带帽或圆领的厚实休闲运动上衣"),
("夹克","jacket","短款外套，用于叠穿并塑造利落轮廓"),
("风衣","trench coat","长款防风外套，常见腰带和肩章结构"),
("大衣","overcoat","厚实长外套，用于秋冬保暖和正式造型"),
("羽绒服","puffer jacket","填充羽绒形成蓬松保暖体积的外套"),
("牛仔裤","jeans","丹宁布制成的耐穿休闲长裤"),
("半身裙","skirt","只覆盖下半身的裙装单品"),
("旗袍","cheongsam qipao","立领盘扣贴身剪裁的中式女性服装"),
("汉服","hanfu","交领宽袖等汉族传统形制的服饰体系"),
("和服","kimono","直线裁片和腰带构成的日本传统服装"),
("制服","uniform","具有机构身份识别的统一制式服装"),
("运动装","sportswear","便于活动排汗的运动功能服装"),
("泳装","swimwear","适合游泳和海滩场景的贴身服装")],"fashion garment","时尚;类别")

block("廓形剪裁",[
("A字廓形","a-line silhouette","上窄下宽呈A形展开的服装轮廓"),
("H字廓形","h-line straight silhouette","上下宽度接近的直筒服装轮廓"),
("X字廓形","x-line cinched waist","肩臀展开并强调腰线的女性化轮廓"),
("O字茧型","cocoon o-line silhouette","中部鼓起两端收窄的茧型廓形"),
("oversize","oversized loose silhouette","刻意放大的宽松尺码与松弛轮廓"),
("修身","slim fit","贴合身体线条的窄身剪裁"),
("公主线","princess seam","从肩胸延伸到下摆的塑形剪裁线"),
("收腰","cinched waist","在腰部内收以强调身体比例的剪裁"),
("垫肩","padded shoulder","肩部加入衬垫强化宽肩和气场"),
("鱼尾","mermaid silhouette","臀部贴合下摆外扩如鱼尾的礼服廓形"),
("蓬蓬","puffy voluminous","通过褶量或填充形成蓬松体积的廓形")],"silhouette","时尚;廓形")

block("面料与纹样",[
("丝绸","silk fabric sheen","表面顺滑带自然光泽的高档纤维面料"),
("针织","knit fabric","线圈结构形成弹性和柔软手感的面料"),
("牛仔丹宁","denim","斜纹棉布制成的结实蓝色休闲面料"),
("皮革","leather","动物皮或仿皮制成的坚韧光泽材质"),
("雪纺","chiffon sheer","轻薄透明并带飘逸垂感的织物"),
("天鹅绒","velvet","短密绒毛形成柔软光泽的厚实面料"),
("蕾丝","lace","镂空花纹构成的精致装饰性织物"),
("羊毛","wool","保暖性强且质感柔韧的天然纤维面料"),
("亚麻","linen","透气干爽并带自然皱感的植物纤维面料"),
("缎面","satin","表面平滑高反光的华丽织物组织"),
("格纹","plaid tartan","纵横交错色条形成的格子图案"),
("条纹","stripe pattern","平行线条重复排列形成的图案"),
("波点","polka dot","圆点规律分布形成的经典装饰纹样"),
("印花","floral print","将花卉或图案印在面料表面的装饰"),
("豹纹","leopard animal print","模仿豹皮斑点的野性动物纹样"),
("亮片","sequins sparkle","缝缀反光小片形成闪耀效果的装饰"),
("提花","jacquard","通过织造结构直接形成复杂花纹的面料"),
("扎染","tie-dye","捆扎后染色形成晕染纹理的手工效果")],"fabric pattern","时尚;面料纹样")

block("风格流派",[
("街头风","streetwear","源自滑板嘻哈文化的宽松休闲穿搭"),
("极简风","minimalist fashion","少装饰低色彩的干净克制服装风格"),
("复古风","vintage fashion","借鉴旧年代单品和剪裁的怀旧穿搭"),
("朋克风","punk fashion studs","铆钉皮革破坏感构成的反叛造型"),
("波西米亚","bohemian boho","流苏印花和宽松层叠形成的自由风格"),
("学院风","preppy academia","衬衫针织和格纹构成的校园精英风格"),
("哥特风","gothic dark fashion","黑色蕾丝皮革与宗教感元素的暗黑风格"),
("洛丽塔","lolita fashion","蓬裙蕾丝蝴蝶结构成的甜美洋装风格"),
("赛博朋克时装","cyberpunk techwear","机能材质与霓虹未来感结合的时装"),
("机能风","techwear functional","强调防水口袋绑带等功能结构的穿搭"),
("国潮汉服","hanfu chinese","传统中式服饰元素与潮流语汇结合"),
("高定礼服","haute couture gown","高级定制工艺制作的华丽礼服"),
("法式","french chic","自然松弛与精致单品平衡的优雅风格"),
("韩系","korean fashion","柔和色彩与利落版型构成的清爽穿搭"),
("日系原宿","harajuku japanese","多层混搭和个性配色的原宿街头风"),
("甜美","sweet girly","粉色蕾丝蝴蝶结等元素构成的可爱风格"),
("中性风","androgynous unisex","弱化性别特征的宽松利落穿搭"),
("运动休闲","athleisure","运动单品融入日常穿着的舒适风格"),
("优雅淑女","elegant lady","修身剪裁和柔和配饰塑造的端庄风格"),
("嘻哈","hip hop fashion","宽大廓形首饰球鞋构成的街头造型")],"fashion style","时尚;风格")

block("时代时尚",[
("20年代Gatsby","1920s flapper art deco","流苏珠饰与低腰裙体现的爵士时代造型"),
("30年代","1930s elegant","斜裁长裙和柔顺线条构成的优雅年代风"),
("50年代","1950s full skirt","收腰大摆裙和复古家居感的女性造型"),
("60年代","1960s mod","迷你裙几何图案与太空感的摩登风格"),
("70年代","1970s disco hippie","喇叭裤流苏和迪斯科亮片的自由年代风"),
("80年代","1980s bold shoulder","宽肩亮色与强势廓形主导的年代造型"),
("90年代","1990s grunge minimal","格纹牛仔与极简吊带并存的怀旧风格"),
("Y2K千禧","y2k millennium","金属色低腰和未来感配饰的千禧美学")],"era fashion","时尚;时代")

block("配饰发妆",[
("帽饰","hat headwear","佩戴在头部用于装饰或遮阳的配饰"),
("珠宝首饰","jewelry","金属宝石等材质制作的身体装饰物"),
("项链","necklace","环绕颈部佩戴的线性首饰"),
("耳环","earrings","佩戴在耳部用于修饰脸型的首饰"),
("箱包","designer handbag","用于携物并强化造型身份的包袋配饰"),
("墨镜","sunglasses","带深色镜片的遮阳与造型眼镜"),
("丝巾","scarf","柔软织物围系在颈部或头部的配饰"),
("腰带","belt","束在腰部固定衣物并强调比例的配饰"),
("手套","gloves","覆盖手部的功能性或礼仪性配饰"),
("浓妆","bold dramatic makeup","高对比色彩和强轮廓塑造的妆容"),
("裸妆","natural nude makeup","接近自然肤色的轻薄日常妆容"),
("烟熏妆","smoky eye","深色眼影晕染形成的迷离眼妆"),
("复古红唇","vintage red lip","饱满红色唇妆营造的经典复古感"),
("欧美妆","western glam makeup","强调修容眼妆和立体五官的妆容"),
("日系妆","japanese makeup","轻透底妆与柔和腮红构成的清新妆容"),
("韩系妆","korean makeup","水光底妆和自然眉眼形成的柔亮妆容"),
("舞台妆","stage makeup","适应强灯光和远距离观看的夸张妆容"),
("盘发","elegant updo","将头发向上收拢固定的正式发型"),
("波浪长发","long wavy hair","长发形成连续波纹卷曲的柔美发型"),
("短发","short bob hair","长度在下颌或肩上附近的利落发型"),
("编发","braided hair","将发束交织编成纹理结构的发型"),
("丸子头","bun hairstyle","头发盘成圆形发髻的轻便发型")],"accessory makeup","时尚;配饰发妆")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
