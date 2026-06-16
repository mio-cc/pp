# -*- coding: utf-8 -*-
"""V10 建筑、室内与空间设计（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V10"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("建筑风格",[
("古典主义建筑","Classical","柱式对称神庙","classical architecture, columns symmetry","古典主义建筑"),
("哥特建筑","Gothic","尖拱飞扶壁","gothic architecture, pointed arches","哥特建筑"),
("巴洛克建筑","Baroque Arch","华丽曲线装饰","baroque architecture, ornate","巴洛克建筑"),
("现代主义","Modernism","简洁功能","modernist architecture, clean functional","现代主义建筑"),
("包豪斯","Bauhaus","几何功能主义","bauhaus architecture, geometric","包豪斯"),
("极简建筑","Minimalist Arch","极简纯净","minimalist architecture","极简建筑"),
("解构主义","Deconstructivism","扭曲碎裂","deconstructivist architecture","解构主义"),
("粗野主义","Brutalism","裸露混凝土","brutalist concrete architecture","粗野主义"),
("新中式","New Chinese","东方禅意现代","new chinese style architecture","新中式"),
("日式侘寂","Wabi-Sabi","质朴禅意","japanese wabi-sabi architecture","日式侘寂"),
("工业风","Industrial","裸露管线砖墙","industrial loft architecture","工业风"),
("未来主义建筑","Futuristic","流线科幻","futuristic architecture, sci-fi","未来主义建筑"),
("有机建筑","Organic Arch","自然流线","organic architecture flowing","有机建筑")],"建筑;风格")
block("建筑空间",[
("中庭","Atrium","通高中庭","atrium tall central space","中庭"),
("玻璃幕墙","Glass Curtain Wall","通透幕墙","glass curtain wall facade","玻璃幕墙"),
("悬挑结构","Cantilever","悬挑出挑","cantilever structure","悬挑结构"),
("开放平面","Open Plan","开放空间","open floor plan","开放平面"),
("螺旋楼梯","Spiral Stair","旋转楼梯","spiral staircase","螺旋楼梯"),
("拱廊","Arcade","连续拱券","arcade arches","拱廊")],"建筑;空间")
block("室内设计",[
("北欧风","Scandinavian","简约温暖原木","scandinavian interior, light wood","北欧风"),
("极简室内","Minimalist Interior","极简留白","minimalist interior","极简室内"),
("工业风室内","Industrial Interior","裸露做旧","industrial interior loft","工业风室内"),
("日式原木","Japandi","日式素雅","japandi interior","日式原木"),
("奶油风","Cream Style","柔和奶油色","cream style cozy interior","奶油风"),
("法式复古","French Vintage","优雅复古","french vintage interior","法式复古"),
("中古风","Mid-Century","中世纪现代","mid-century modern interior","中古风"),
("侘寂室内","Wabi-Sabi Interior","质朴禅意","wabi-sabi interior","侘寂室内"),
("赛博朋克室内","Cyberpunk Interior","霓虹未来","cyberpunk neon interior","赛博朋克室内")],"建筑;室内")
block("家具与陈设",[
("北欧家具","Scandinavian Furniture","原木简约家具","scandinavian furniture","北欧家具"),
("中古家具","Mid-Century Furniture","复古设计椅","mid-century furniture","中古家具"),
("软装陈设","Soft Furnishing","布艺装饰","soft furnishing decor","软装陈设"),
("绿植装饰","Plants Decor","室内绿植","indoor plants decor","绿植装饰")],"建筑;家具")
block("景观与氛围",[
("城市天际线","Skyline","都市天际线","city skyline","城市天际线"),
("园林景观","Garden Landscape","古典园林","garden landscape","园林景观"),
("中庭光井","Light Well","天光光井","light well atrium glow","光井"),
("空间光影","Spatial Light","光影氛围","spatial light and shadow mood","空间光影"),
("黄昏暖光室内","Golden Interior Light","暖阳室内","warm golden hour interior light","黄昏暖光室内")],"建筑;景观氛围")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
