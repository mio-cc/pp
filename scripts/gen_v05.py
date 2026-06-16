# -*- coding: utf-8 -*-
"""V05 平面设计与版式（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V05"; rows=[]
def simple(cat,items,suf,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en.title(),"",V,cat,zh+"。","","","",en+(" "+suf if suf else ""),"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("字体与排印 / 字体分类",[("衬线体","serif typeface"),("无衬线体","sans-serif typeface"),("板衬线","slab serif"),("手写体","script typeface"),("哥特黑体","blackletter gothic"),("等宽字体","monospace typeface"),("展示体","display typeface"),("圆体","rounded typeface"),("宋体","song serif chinese"),("黑体","hei sans chinese"),("楷体","kai chinese"),("书法字体","calligraphy type"),("像素字体","pixel bitmap font"),("可变字体","variable font")],"typography","平面;字体")
simple("字体与排印 / 排印属性",[("字重层级","font weight hierarchy"),("字距调整","kerning tracking"),("行距","leading line spacing"),("字号层级","type scale hierarchy"),("基线网格","baseline grid"),("首字下沉","drop cap"),("对齐排版","text alignment"),("两端对齐","justified text"),("竖排","vertical typesetting"),("文字环绕","text wrap"),("字偶距","letter spacing")],"typography","平面;排印")
simple("版式与网格",[("网格系统","grid system layout"),("瑞士国际主义","swiss international typographic style"),("黄金比例版式","golden ratio layout"),("对齐","alignment ordered"),("留白","white space negative"),("分栏","multi-column layout"),("对称布局","symmetrical layout"),("非对称布局","asymmetrical dynamic layout"),("模块化版式","modular grid"),("杂志版式","editorial magazine layout"),("拼贴版式","collage layout"),("满版出血","full bleed layout"),("网格破坏","broken grid"),("黄金螺旋版式","golden spiral layout")],"layout","平面;版式")
simple("品牌视觉",[("字标logo","wordmark logo"),("图形标志","abstract logomark"),("徽章logo","emblem badge logo"),("组合标志","combination mark"),("字母标","lettermark monogram"),("品牌主色","brand color palette"),("VI系统","visual identity system"),("吉祥物","brand mascot"),("辅助图形","brand graphic pattern"),("品牌字体","brand typeface")],"branding","平面;品牌")
simple("海报与广告",[("极简海报","minimalist poster"),("瑞士海报","swiss grid poster"),("拼贴海报","collage poster"),("大字标题海报","big typographic poster"),("主视觉","hero key visual"),("复古海报","vintage retro poster"),("电影海报","movie poster"),("音乐节海报","music festival poster"),("日式海报","japanese poster design"),("孟菲斯海报","memphis style poster"),("渐变海报","gradient poster"),("故障海报","glitch poster")],"poster","平面;海报")
simple("信息设计",[("信息图","infographic"),("图表","data chart"),("数据可视化","data visualization"),("图标系统","icon set"),("标识系统","wayfinding signage"),("流程图","flowchart"),("地图设计","map design"),("时间线","timeline graphic"),("仪表盘","dashboard UI")],"infographic","平面;信息")
simple("印刷工艺",[("CMYK印刷","CMYK print"),("专色印刷","pantone spot color"),("烫金","gold foil stamping"),("UV局部光油","spot UV gloss"),("压凹凸","emboss deboss"),("特种纸","textured specialty paper"),("出血","print bleed"),("Riso孔版","risograph print"),("丝网印刷","screen print"),("击凸","embossing"),("镂空","die cut"),("覆膜","lamination")],"print","平面;印刷")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
