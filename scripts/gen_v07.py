# -*- coding: utf-8 -*-
"""V07 材质与渲染（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V07"; rows=[]
def add(cat,zh,en,defs,pen,pcn,tags):
    rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items: add(cat,zh,en,defs,pen,pcn,tags)
def simple(cat,items,suffix_en,tags):
    for zh,en in items: add(cat,zh,en.title(),zh,en+" "+suffix_en,zh,tags)

block("PBR材质 / 通道属性",[
("基础色","Albedo","固有色","PBR albedo base color","基础色"),
("金属度","Metallic","金属非金属","metallic workflow","金属度"),
("粗糙度","Roughness","光滑粗糙","roughness map","粗糙度"),
("法线贴图","Normal Map","表面凹凸","normal map detail","法线贴图"),
("环境光遮蔽","AO","缝隙暗部","ambient occlusion","环境光遮蔽"),
("置换贴图","Displacement","真实位移","displacement map","置换贴图"),
("次表面散射","SSS","透光皮肤玉石","subsurface scattering","次表面散射"),
("透明折射","Refraction","玻璃折射","transparency refraction","透明折射"),
("自发光","Emissive","材质发光","emissive glow","自发光"),
("清漆层","Clearcoat","车漆涂层","clearcoat layer","清漆层"),
("各向异性","Anisotropy","拉丝高光","anisotropic highlight","各向异性"),
("光泽度","Sheen","织物绒光","sheen fabric","光泽度")],"材质;PBR")

simple("材质类型 / 金属",[("黄金","gold"),("白银","silver"),("紫铜","copper"),("黄铜","brass"),("青铜","bronze"),("铸铁","cast iron"),("不锈钢","stainless steel"),("铝","aluminum"),("钛","titanium"),("镀铬","chrome"),("枪铁","gunmetal"),("锡","pewter"),("玫瑰金","rose gold")],"metal material","材质;金属")
simple("材质类型 / 石材",[("大理石","marble"),("花岗岩","granite"),("砂岩","sandstone"),("板岩","slate"),("玄武岩","basalt"),("石灰岩","limestone"),("水磨石","terrazzo"),("鹅卵石","cobblestone"),("水晶","crystal"),("玉石","jade")],"stone material","材质;石材")
simple("材质类型 / 木材",[("橡木","oak wood"),("胡桃木","walnut wood"),("松木","pine wood"),("竹","bamboo"),("桃花心木","mahogany"),("桦木","birch wood"),("做旧木","weathered wood"),("炭化木","charred wood"),("胶合板","plywood")],"texture","材质;木材")
simple("材质类型 / 织物",[("棉布","cotton"),("羊毛","wool"),("丝绸","silk"),("亚麻","linen"),("天鹅绒","velvet"),("牛仔丹宁","denim"),("灯芯绒","corduroy"),("雪纺","chiffon"),("针织","knit"),("蕾丝","lace"),("皮革","leather"),("麂皮","suede"),("毛呢","tweed")],"fabric texture","材质;织物")
simple("材质类型 / 玻璃陶瓷",[("透明玻璃","clear glass"),("磨砂玻璃","frosted glass"),("彩色玻璃","stained glass"),("陶瓷","ceramic"),("瓷器","porcelain"),("釉面","glazed"),("赤陶","terracotta"),("珐琅","enamel")],"material","材质;玻璃陶瓷")
simple("材质类型 / 合成与其他",[("混凝土","concrete"),("水泥","cement"),("塑料","plastic"),("亚克力","acrylic"),("橡胶","rubber"),("硅胶","silicone"),("碳纤维","carbon fiber"),("纸张","paper"),("纸板","cardboard"),("泡沫","foam"),("沥青","asphalt"),("石膏","plaster")],"material","材质;合成")
simple("材质类型 / 自然有机",[("皮肤","skin"),("毛发","fur"),("鳞片","scales"),("羽毛","feathers"),("树叶","leaves"),("花瓣","flower petals"),("水面","water surface"),("冰","ice"),("雪","snow"),("沙","sand"),("泥","mud"),("岩浆","lava")],"organic material","材质;自然有机")

simple("表面处理",[("抛光","polished"),("拉丝","brushed"),("磨砂哑光","matte"),("镜面","mirror glossy"),("做旧风化","weathered"),("生锈","rusted"),("氧化","oxidized"),("磨损划痕","scratched worn"),("湿润反光","wet glossy"),("油污","greasy"),("灰尘污渍","dusty grimy"),("苔藓附着","mossy"),("龟裂","cracked"),("锤纹","hammered")],"surface finish","材质;表面")

block("渲染算法",[
("光线追踪","Ray Tracing","真实反射","ray tracing reflections","光线追踪"),
("路径追踪","Path Tracing","物理路径","path tracing","路径追踪"),
("全局光照","Global Illumination","间接弹射","global illumination GI","全局光照"),
("光栅化","Rasterization","实时","real-time rasterization","光栅化"),
("体积渲染","Volumetric","体积雾光","volumetric fog","体积渲染"),
("焦散","Caustics","聚焦光斑","caustics","焦散"),
("屏幕空间反射","SSR","屏幕反射","screen space reflections","SSR"),
("环境光遮蔽渲染","SSAO","屏幕遮蔽","SSAO","SSAO"),
("光子映射","Photon Mapping","光子GI","photon mapping","光子映射")],"材质;渲染算法")
block("引擎与质量",[
("虚幻引擎5","Unreal Engine 5","实时影视级","unreal engine 5 cinematic render","虚幻引擎5"),
("Octane","Octane Render","GPU物理","octane render","Octane"),
("Arnold","Arnold","影视离线","arnold render","Arnold"),
("Redshift","Redshift","GPU产品级","redshift render","Redshift"),
("Blender Cycles","Cycles","路径追踪","blender cycles","Cycles"),
("V-Ray","V-Ray","建筑可视化","vray render","V-Ray"),
("照片级写实","Photorealistic","照片真实","photorealistic","照片级写实"),
("8K高细节","8K Detail","超高细节","8k highly detailed","8K高细节"),
("PBR写实","PBR Realistic","基于物理","physically based render","PBR写实")],"材质;引擎")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
