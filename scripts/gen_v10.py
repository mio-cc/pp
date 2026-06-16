# -*- coding: utf-8 -*-
"""V10 建筑、室内与空间设计（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V10"; rows=[]
def simple(cat,items,suf,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en+(" "+suf if suf else ""),"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("建筑风格",[("古典主义","classical architecture columns"),("哥特","gothic architecture"),("罗马式","romanesque architecture"),("巴洛克","baroque architecture"),("洛可可","rococo architecture"),("新古典","neoclassical architecture"),("现代主义","modernist architecture"),("包豪斯","bauhaus architecture"),("国际主义","international style architecture"),("极简","minimalist architecture"),("解构主义","deconstructivist architecture"),("粗野主义","brutalist concrete architecture"),("新中式","new chinese architecture"),("徽派","huizhou chinese architecture"),("日式侘寂","japanese wabi-sabi architecture"),("和风神社","japanese shrine architecture"),("工业风","industrial architecture"),("未来主义","futuristic architecture"),("有机建筑","organic flowing architecture"),("仿生建筑","biomimetic architecture"),("地中海","mediterranean architecture"),("北欧","nordic architecture"),("热带","tropical architecture"),("阿拉伯","islamic arabic architecture")],"architecture","建筑;风格")
simple("建筑空间",[("中庭","atrium"),("玻璃幕墙","glass curtain wall"),("悬挑结构","cantilever"),("开放平面","open floor plan"),("螺旋楼梯","spiral staircase"),("拱廊","arcade arches"),("穹顶","dome"),("通高","double-height space"),("天井","light court"),("廊道","corridor gallery"),("中庭花园","atrium garden"),("挑空客厅","double-height living room"),("落地窗","floor-to-ceiling windows"),("天窗","skylight")],"interior space","建筑;空间")
simple("室内设计",[("北欧风","scandinavian interior"),("极简室内","minimalist interior"),("工业风室内","industrial loft interior"),("日式原木","japandi interior"),("奶油风","cream cozy interior"),("法式复古","french vintage interior"),("中古风","mid-century modern interior"),("侘寂室内","wabi-sabi interior"),("赛博朋克室内","cyberpunk neon interior"),("美式乡村","american country interior"),("地中海风","mediterranean interior"),("新中式室内","new chinese interior"),("轻奢风","light luxury interior"),("ins风","instagram aesthetic interior"),("复古怀旧","retro vintage interior"),("禅意","zen minimalist interior"),("孟菲斯室内","memphis interior")],"interior","建筑;室内")
simple("家具与陈设",[("北欧家具","scandinavian furniture"),("中古家具","mid-century furniture"),("巴洛克家具","baroque furniture"),("软装陈设","soft furnishing decor"),("绿植装饰","indoor plants decor"),("艺术挂画","wall art decor"),("地毯","rug decor"),("吊灯","pendant lighting"),("落地灯","floor lamp")],"furniture","建筑;家具")
simple("景观与氛围",[("城市天际线","city skyline"),("园林景观","classical garden landscape"),("现代景观","modern landscape"),("中庭光井","light well glow"),("空间光影","spatial light shadow"),("黄昏暖光室内","golden hour interior light"),("晨光室内","morning light interior"),("夜景灯光","night architectural lighting"),("雾景建筑","foggy atmospheric architecture")],"landscape mood","建筑;景观氛围")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
