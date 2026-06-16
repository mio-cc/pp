# -*- coding: utf-8 -*-
"""V07 材质与渲染（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V07"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("PBR材质 / 通道属性",[
("基础色","Albedo/Base Color","固有色","PBR albedo base color","基础色"),
("金属度","Metallic","金属非金属","metallic workflow","金属度"),
("粗糙度","Roughness","表面光滑粗糙","roughness glossy matte","粗糙度"),
("法线贴图","Normal Map","表面凹凸细节","normal map surface detail","法线贴图"),
("环境光遮蔽","Ambient Occlusion","缝隙暗部","ambient occlusion AO","环境光遮蔽"),
("置换贴图","Displacement","真实位移凹凸","displacement height map","置换贴图"),
("次表面散射","Subsurface Scattering","皮肤玉石透光","subsurface scattering SSS skin jade","次表面散射"),
("透明折射","Transparency/Refraction","玻璃透明折射","transparency refraction glass","透明折射"),
("自发光","Emissive","材质发光","emissive glow material","自发光"),
("清漆涂层","Clearcoat","车漆清漆层","clearcoat car paint layer","清漆涂层")],"材质;PBR")
block("材质类型",[
("抛光金属","Polished Metal","镜面金属反射","polished reflective metal","抛光金属"),
("拉丝金属","Brushed Metal","拉丝纹理金属","brushed metal texture","拉丝金属"),
("生锈金属","Rusted Metal","锈蚀斑驳","rusted weathered metal","生锈金属"),
("木材","Wood","木纹质感","wood grain texture","木材"),
("织物布料","Fabric","布料纤维","woven fabric cloth texture","织物布料"),
("皮革","Leather","皮革纹理","leather texture","皮革"),
("玻璃","Glass","透明玻璃","clear glass material","玻璃"),
("陶瓷","Ceramic","光滑陶瓷釉面","glazed ceramic","陶瓷"),
("大理石","Marble","纹理大理石","veined marble stone","大理石"),
("混凝土","Concrete","粗糙水泥","rough concrete","混凝土"),
("水面液体","Water/Liquid","流动液体","flowing water liquid surface","水面液体"),
("塑料","Plastic","光滑塑料","glossy plastic material","塑料"),
("橡胶","Rubber","哑光橡胶","matte rubber","橡胶"),
("皮肤","Skin","真实皮肤次表面","realistic skin subsurface","皮肤"),
("毛发","Fur/Hair","毛发丝状","fur hair strands","毛发"),
("有机植物","Foliage","叶片植被","organic foliage leaves","有机植物")],"材质;类型")
block("材质做旧与质感",[
("做旧风化","Weathering","风化痕迹","weathered aged surface","做旧风化"),
("磨损划痕","Scratches","边角磨损","worn scratches edge wear","磨损划痕"),
("湿润反光","Wet Look","潮湿高光","wet glossy reflective","湿润反光"),
("灰尘污渍","Grime/Dust","脏污积灰","grime dust dirt","灰尘污渍"),
("苔藓附着","Moss","苔藓覆盖","moss overgrowth","苔藓")],"材质;做旧")
block("渲染算法",[
("光线追踪","Ray Tracing","真实光线反射","ray tracing realistic reflections","光线追踪"),
("路径追踪","Path Tracing","物理路径渲染","path tracing physically based","路径追踪"),
("全局光照","Global Illumination","间接光弹射","global illumination GI bounce light","全局光照"),
("光栅化","Rasterization","实时光栅","real-time rasterization","光栅化"),
("体积渲染","Volumetric","体积雾光","volumetric fog lighting","体积渲染"),
("焦散","Caustics","光线聚焦光斑","caustics light focusing","焦散"),
("环境光遮蔽渲染","SSAO","屏幕空间遮蔽","screen space ambient occlusion","SSAO")],"材质;渲染")
block("引擎与质量",[
("虚幻引擎渲染","Unreal Engine","UE5实时影视级","unreal engine 5 render, cinematic","虚幻引擎"),
("Octane渲染","Octane Render","GPU物理渲染","octane render","Octane渲染"),
("Arnold渲染","Arnold","影视级离线渲染","arnold cinematic render","Arnold渲染"),
("Blender Cycles","Cycles","Blender路径追踪","blender cycles render","Cycles渲染"),
("3D渲染","3D Render","三维渲染感","3D render, CGI","3D渲染"),
("照片级写实","Photorealistic","照片级真实","photorealistic render","照片级写实"),
("8K高细节","8K Detail","超高分辨率细节","8k highly detailed","8K高细节")],"材质;引擎")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
