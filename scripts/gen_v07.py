# -*- coding: utf-8 -*-
"""V07 材质与渲染（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V07"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("PBR材质 / 通道属性",[
("基础色","Albedo","PBR中定义材质固有色的基础贴图通道","PBR albedo base color texture","基础色"),
("金属度","Metallic","控制表面金属/非金属属性的PBR参数","metallic workflow parameter","金属度"),
("粗糙度","Roughness","控制表面光滑与粗糙程度的PBR贴图","roughness map microsurface detail","粗糙度"),
("法线贴图","Normal Map","模拟表面微凹凸的光照欺骗贴图","normal map surface detail","法线贴图"),
("环境光遮蔽","AO","在角落缝隙处暗化间接光照的效果","ambient occlusion crevice darkening","环境光遮蔽"),
("置换贴图","Displacement","真正改变几何网格位移的贴图","displacement map geometry shift","置换贴图"),
("次表面散射","SSS","光线穿透半透明材质后的散射效果","subsurface scattering skin jade","次表面散射"),
("透明折射","Refraction","透明材质使光线偏转弯折的光学效果","transparency refraction glass","透明折射"),
("自发光","Emissive","材质自身主动发出光线的着色通道","emissive glow self-lit","自发光"),
("清漆层","Clearcoat","在基色之上额外加透明漆层的效果","clearcoat varnish layer","清漆层"),
("各向异性","Anisotropy","高光方向随观察角改变的拉丝效果","anisotropic highlight brushed","各向异性"),
("光泽度","Sheen","织物绒毛等软表面的边缘光泽","sheen fabric velvet fuzz","光泽度")],"材质;PBR")
block("材质类型 / 金属",[
("黄金","Gold","贵重软金属、高反射暖黄色光泽","gold metal reflective warm yellow","黄金"),
("白银","Silver","高反射亮白冷调的贵金属","silver metal bright reflective","白银"),
("紫铜","Copper","氧化后呈青绿的暖红棕金属","copper oxidized reddish metal","紫铜"),
("黄铜","Brass","铜锌合金、低反射暖黄色调","brass alloy warm subdued","黄铜"),
("青铜","Bronze","铜锡合金、深沉暗绿褐的古典金属","bronze alloy dark patina","青铜"),
("铸铁","Cast Iron","粗颗粒低反射的工业黑灰金属","cast iron matte dark grainy","铸铁"),
("不锈钢","Stainless Steel","抗腐蚀高反射的现代银白金属","stainless steel bright modern","不锈钢"),
("铝","Aluminum","轻量中等反射的银灰金属","aluminum light silver metal","铝"),
("钛","Titanium","高强度低密度的暗灰耐用金属","titanium dark durable metal","钛"),
("镀铬","Chrome","极高反射如镜面的银亮电镀层","chrome mirror finish plating","镀铬"),
("枪铁","Gunmetal","低反射深灰的铸铁合金","gunmetal dark matte alloy","枪铁"),
("锡","Pewter","低反射柔灰的锡铅软合金","pewter soft muted gray alloy","锡"),
("玫瑰金","Rose Gold","金铜合金的柔暖粉金色调","rose gold pink metallic","玫瑰金")],"材质;金属")
block("材质类型 / 石材",[
("大理石","Marble","灰纹流动的高贵石灰变质岩","marble veined polished stone","大理石"),
("花岗岩","Granite","斑点颗粒密布的硬质火成岩","granite speckled hard stone","花岗岩"),
("砂岩","Sandstone","温暖粗粒风化感的沉积岩","sandstone warm rough grainy","砂岩"),
("板岩","Slate","层片状易劈裂的暗灰变质岩","slate layered dark stone","板岩"),
("玄武岩","Basalt","细密深黑的火山喷出岩","basalt fine dark volcanic","玄武岩"),
("石灰岩","Limestone","浅色多孔的沉积钙质岩","limestone porous pale rock","石灰岩"),
("水磨石","Terrazzo","碎大理石嵌在水泥里的复古地面材料","terrazzo chip composite floor","水磨石"),
("鹅卵石","Cobblestone","圆润光滑的河床天然石","cobblestone smooth rounded river","鹅卵石"),
("水晶","Crystal","透明闪烁的天然石英矿物","crystal clear sparkling mineral","水晶"),
("玉石","Jade","温润半透明的绿白玉石质感","jade translucent green gem","玉石")],"材质;石材")
block("材质类型 / 木材",[
("橡木","Oak Wood","纹理粗犷明亮的浅棕硬木","oak wood light brown grain","橡木"),
("胡桃木","Walnut Wood","深沉暗棕、纹理华贵的硬木","walnut dark rich brown","胡桃木"),
("松木","Pine Wood","浅色松软、结疤明显的软木","pine wood light soft knotty","松木"),
("竹","Bamboo","纵向纤维清晰的中空草本植物","bamboo hollow fibrous stalk","竹"),
("桃花心木","Mahogany","红棕深沉、光泽温润的名贵硬木","mahogany reddish brown luxury","桃花心木"),
("桦木","Birch Wood","浅黄白、纹理细腻均匀的轻木","birch pale fine grain wood","桦木"),
("做旧木","Weathered Wood","风化开裂灰白斑驳的老化木","weathered wood aged cracked","做旧木"),
("炭化木","Charred Wood","表面烧焦碳化的防腐木处理","charred wood burnt surface","炭化木"),
("胶合板","Plywood","薄木片交错层压的工程板材","plywood layered veneer board","胶合板")],"材质;木材")
block("材质类型 / 织物",[
("棉布","Cotton","天然柔软透气的植物纤维织物","cotton soft natural woven","棉布"),
("羊毛","Wool","动物毛发纺成的蓬松保暖织物","wool fluffy warm fiber","羊毛"),
("丝绸","Silk","光泽顺滑的蛋白纤维高级织物","silk shiny smooth lustrous","丝绸"),
("亚麻","Linen","天然挺括微皱的植物纤维织物","linen crisp natural texture","亚麻"),
("天鹅绒","Velvet","绒毛直立、光影随变的厚实织物","velvet plush soft sheen","天鹅绒"),
("牛仔丹宁","Denim","靛蓝染色的耐磨斜纹棉布","denim indigo durable twill","牛仔丹宁"),
("灯芯绒","Corduroy","纵向绒条凸起的耐磨棉织物","corduroy ridged waled cotton","灯芯绒"),
("雪纺","Chiffon","轻薄透明飘逸的人造丝织物","chiffon sheer lightweight flowy","雪纺"),
("针织","Knit","纱线线圈套结的弹性织物","knit stretchy looped yarn","针织"),
("蕾丝","Lace","镂空花纹的精致装饰织物","lace ornamental openwork","蕾丝"),
("皮革","Leather","鞣制动物皮的柔韧耐用面料","leather tanned hide durable","皮革"),
("麂皮","Suede","磨砂起绒的柔软动物皮面","suede napped soft velvety","麂皮"),
("毛呢","Tweed","粗纺混色、纹理粗犷的保暖织物","tweed coarse twilled wool","毛呢")],"材质;织物")
block("材质类型 / 玻璃陶瓷",[
("透明玻璃","Clear Glass","全透明、高反射的硅质材料","clear glass transparent reflective","透明玻璃"),
("磨砂玻璃","Frosted Glass","表面蚀刻后透光不透影的玻璃","frosted glass translucent diffused","磨砂玻璃"),
("彩色玻璃","Stained Glass","嵌入金属框的彩色拼花玻璃","stained glass colored leaded","彩色玻璃"),
("陶瓷","Ceramic","黏土烧制的无机非金属材料","ceramic fired clay material","陶瓷"),
("瓷器","Porcelain","高温烧制的高致密白色陶瓷","porcelain fine white ceramic","瓷器"),
("釉面","Glazed","表面覆玻璃质光泽层的陶瓷表面","glazed glossy vitreous coat","釉面"),
("赤陶","Terracotta","低温烧制的红橙多孔陶土","terracotta unglazed porous red","赤陶"),
("珐琅","Enamel","高温熔结在金属表面的玻璃质涂层","enamel fused glass coating","珐琅")],"材质;玻璃陶瓷")
block("材质类型 / 合成与其他",[
("混凝土","Concrete","水泥骨料混合的灰色粗质建材","concrete cement aggregate gray","混凝土"),
("水泥","Cement","混凝土的灰色粉末胶凝材料","cement powder binder gray","水泥"),
("塑料","Plastic","高分子合成可塑的轻量材料","plastic synthetic polymer","塑料"),
("亚克力","Acrylic","透明坚韧的有机玻璃板材","acrylic clear rigid plexiglass","亚克力"),
("橡胶","Rubber","高弹性可拉伸的高分子材料","rubber elastic stretchy","橡胶"),
("硅胶","Silicone","耐温柔软的有机硅弹性体","silicone heat-resistant soft","硅胶"),
("碳纤维","Carbon Fiber","碳丝编织的超轻高强复合材料","carbon fiber lightweight strong","碳纤维"),
("纸张","Paper","纤维素制成的薄平面材料","paper thin cellulose sheet","纸张"),
("纸板","Cardboard","多层厚纸压合的刚性板材","cardboard thick layered rigid","纸板"),
("泡沫","Foam","充气发泡的轻质多孔材料","foam lightweight porous","泡沫"),
("沥青","Asphalt","石油提炼的黑色铺路粘合材料","asphalt black paving binder","沥青"),
("石膏","Plaster","白色粉末加水凝固的塑形材料","plaster white moldable set","石膏")],"材质;合成")
block("材质类型 / 自然有机",[
("皮肤","Skin","人体外层、有毛孔纹理的有机表面","skin organic pore texture","皮肤"),
("毛发","Fur","动物皮毛的细密柔软丝状质感","fur soft animal hair coat","毛发"),
("鳞片","Scales","爬行类鱼类的叠瓦状硬质角蛋白","scales overlapping hard keratin","鳞片"),
("羽毛","Feathers","鸟类覆盖体表的轻盈羽枝结构","feathers lightweight barbed plumage","羽毛"),
("树叶","Leaves","植物光合作用的薄绿片状器官","leaves green veined flat","树叶"),
("花瓣","Flower Petals","花朵周围柔软透明的彩色片","flower petals soft translucent","花瓣"),
("水面","Water Surface","流体透明、可反射折射的水平面","water surface transparent reflective","水面"),
("冰","Ice","水凝固后的透明坚硬晶体","ice frozen clear solid crystal","冰"),
("雪","Snow","冰晶聚集的白色蓬松颗粒","snow white fluffy crystal granule","雪"),
("沙","Sand","细碎矿物颗粒的松散堆积","sand fine loose mineral grain","沙"),
("泥","Mud","水与土混合的粘稠湿软物质","mud wet sticky earth mixture","泥"),
("岩浆","Lava","地壳涌出的高温熔融岩石","lava molten hot volcanic rock","岩浆")],"材质;自然有机")
block("表面处理",[
("抛光","Polished","打磨至镜面般光滑的表面处理","polished mirror smooth finish","抛光"),
("拉丝","Brushed","定向打磨出细密平行纹路的处理","brushed directional grain finish","拉丝"),
("磨砂哑光","Matte","低光泽、均匀散射的柔粗表面","matte low gloss diffused surface","磨砂哑光"),
("镜面","Mirror Glossy","极高光反射如同镜面的表面","mirror glossy reflective finish","镜面"),
("做旧风化","Weathered","模拟自然老化、褪色磨损的效果","weathered aged worn patina","做旧风化"),
("生锈","Rusted","金属表面氧化腐蚀的铁锈质感","rusted iron oxide corrosion","生锈"),
("氧化","Oxidized","表面与氧反应产生色彩变化的效果","oxidized patina color shift","氧化"),
("磨损划痕","Scratched Worn","使用留下的随机划痕与磨损","scratched worn distressed marks","磨损划痕"),
("湿润反光","Wet Glossy","表面附水膜后的高反射湿润感","wet glossy water film sheen","湿润反光"),
("油污","Greasy","附着一层油渍的暗光脏污质感","greasy oily stain darkened","油污"),
("灰尘污渍","Dusty Grimy","表面覆满灰尘与污垢的脏旧质感","dusty grimy dirt covered","灰尘污渍"),
("苔藓附着","Mossy","表面生长绿色苔藓的潮湿老化效果","mossy green overgrowth damp","苔藓附着"),
("龟裂","Cracked","表面因干燥或老化产生的网状裂纹","cracked surface fracture pattern","龟裂"),
("锤纹","Hammered","手工锤击留下的凹坑金属纹","hammered dimpled metal texture","锤纹")],"材质;表面")
block("渲染算法",[
("光线追踪","Ray Tracing","逐光线计算反射折射的全局光照算法","ray tracing reflections refractions","光线追踪"),
("路径追踪","Path Tracing","随机采样光路径的物理精确渲染算法","path tracing physically accurate","路径追踪"),
("全局光照","Global Illumination","模拟光在场景中多次弹射的间接照明","global illumination GI indirect bounce","全局光照"),
("光栅化","Rasterization","逐像素光栅化的高速实时渲染方式","real-time rasterization fast","光栅化"),
("体积渲染","Volumetric","渲染烟雾云雾等体积参与介质的效果","volumetric fog smoke cloud render","体积渲染"),
("焦散","Caustics","光线经曲面聚焦形成的亮斑图案","caustics focused light pattern","焦散"),
("屏幕空间反射","SSR","利用屏幕深度信息模拟反射的实时技术","screen space reflections SSR","SSR"),
("环境光遮蔽渲染","SSAO","屏幕空间估算间接光照遮蔽的后处理","SSAO ambient occlusion post","SSAO"),
("光子映射","Photon Mapping","预发射光子建立间接光照的两遍算法","photon mapping two-pass GI","光子映射")],"材质;渲染算法")
block("引擎与质量",[
("虚幻引擎5","Unreal Engine 5","支持Nanite/Lumen的实时影视级引擎","unreal engine 5 cinematic real-time","虚幻引擎5"),
("Octane","Octane Render","GPU加速的无偏光线追踪渲染器","octane render GPU unbiased","Octane"),
("Arnold","Arnold","好莱坞影视工业标准的离线渲染器","arnold render production offline","Arnold"),
("Redshift","Redshift","GPU加速的生产级有偏渲染器","redshift render GPU production","Redshift"),
("Blender Cycles","Cycles","Blender内置的路径追踪渲染引擎","blender cycles path tracer","Cycles"),
("V-Ray","V-Ray","建筑可视化领域主流的渲染引擎","vray render arch-viz standard","V-Ray"),
("照片级写实","Photorealistic","肉眼难辨真伪的超逼真渲染质量","photorealistic indistinguishable","照片级写实"),
("8K高细节","8K Detail","极高分辨率的丰富纹理细节呈现","8k highly detailed resolution","8K高细节"),
("PBR写实","PBR Realistic","基于物理参数的写实材质渲染","physically based realistic render","PBR写实")],"材质;引擎")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
