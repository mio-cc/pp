# -*- coding: utf-8 -*-
"""V05 平面设计与版式（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V05"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("字体与排印 / 字体分类",[
("衬线体","Serif","古典衬线","serif typeface, classic","衬线体"),
("无衬线体","Sans-serif","现代简洁","sans-serif typeface, modern clean","无衬线体"),
("衬线粗体标题","Slab Serif","厚重板衬","slab serif bold headline","板衬线"),
("手写体","Script","优雅手写","script handwritten typeface","手写体"),
("哥特黑letter","Blackletter","哥特黑体","blackletter gothic type","哥特黑体"),
("等宽字体","Monospace","等宽代码感","monospace typeface","等宽字体"),
("display展示体","Display Type","夸张展示字","display decorative typeface","展示体")],"平面;字体")
block("字体与排印 / 排印属性",[
("字重层级","Font Weight","粗细对比","font weight hierarchy bold light","字重层级"),
("字距调整","Kerning/Tracking","字间距","kerning tracking letter spacing","字距"),
("行距","Leading","行间距节奏","leading line spacing","行距"),
("字号层级","Type Scale","大小层级","type scale hierarchy","字号层级"),
("文字排版网格","Baseline Grid","基线网格","baseline grid typography","基线网格"),
("首字下沉","Drop Cap","装饰首字","drop cap initial","首字下沉")],"平面;排印")
block("版式与网格",[
("网格系统","Grid System","栅格布局","grid system layout","网格系统"),
("瑞士国际主义","Swiss Style","客观网格无衬线","swiss international typographic style","瑞士国际主义"),
("黄金比例版式","Golden Layout","黄金分割排版","golden ratio layout","黄金比例版式"),
("对齐","Alignment","对齐秩序","alignment, ordered","对齐"),
("留白","White Space","负空间呼吸","white space, breathing room","留白, 负空间"),
("分栏","Columns","多栏排版","multi-column layout","分栏"),
("对称布局","Symmetrical Layout","对称平衡","symmetrical balanced layout","对称布局"),
("非对称布局","Asymmetrical Layout","动态非对称","asymmetrical dynamic layout","非对称布局"),
("模块化版式","Modular Layout","模块拼接","modular grid layout","模块化版式")],"平面;版式")
block("品牌视觉",[
("字标logo","Wordmark","文字标志","wordmark logo typographic","字标"),
("图形标志","Logomark","抽象图形标","abstract logomark symbol","图形标志"),
("徽章logo","Emblem","徽章式标志","emblem badge logo","徽章logo"),
("品牌主色","Brand Color","品牌色彩","brand color palette","品牌主色"),
("VI系统","Visual Identity","视觉识别系统","visual identity system","VI系统"),
("吉祥物","Mascot","品牌吉祥物","brand mascot character","吉祥物")],"平面;品牌")
block("海报与广告",[
("极简海报","Minimal Poster","极简留白海报","minimalist poster, white space","极简海报"),
("瑞士海报","Swiss Poster","网格无衬线海报","swiss grid poster","瑞士海报"),
("拼贴海报","Collage Poster","拼贴混搭","collage mixed media poster","拼贴海报"),
("大字标题","Big Type","巨型标题字","oversized typographic headline","大字标题"),
("视觉锤主体","Hero Visual","主视觉冲击","hero key visual impact","主视觉"),
("复古海报","Vintage Poster","复古印刷感","vintage retro poster print","复古海报")],"平面;海报")
block("信息设计",[
("信息图","Infographic","数据信息图","infographic data visual","信息图"),
("图表","Chart","数据图表","data chart diagram","图表"),
("数据可视化","Data Viz","数据可视化","data visualization","数据可视化"),
("图标系统","Icon Set","统一图标组","consistent icon set","图标系统"),
("标识系统","Signage","导视系统","wayfinding signage system","标识系统"),
("流程图","Flowchart","流程示意","flowchart diagram","流程图")],"平面;信息")
block("印刷工艺",[
("CMYK印刷","CMYK Print","四色印刷","CMYK print color","CMYK印刷"),
("专色印刷","Spot Color","Pantone专色","pantone spot color print","专色印刷"),
("烫金","Gold Foil","烫金工艺","gold foil stamping","烫金"),
("UV局部光油","Spot UV","局部光油","spot UV gloss","UV局部光油"),
("压凹凸","Emboss","压印浮凸","emboss deboss texture","压凹凸"),
("特种纸","Textured Paper","纸张质感","textured specialty paper","特种纸"),
("出血","Bleed","出血边","print bleed edge","出血"),
("Riso印刷","Risograph","复古孔版套色","risograph print, retro overprint","Riso孔版")],"平面;印刷")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
