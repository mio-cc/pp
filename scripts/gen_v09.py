# -*- coding: utf-8 -*-
"""V09 构图与视觉叙事（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V09"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("构图语法",[
("三分法","Rule of Thirds","三分线","rule of thirds composition","三分法"),
("黄金螺旋","Golden Spiral","斐波那契螺旋","golden spiral fibonacci composition","黄金螺旋"),
("中心对称","Central Symmetry","居中对称","central symmetrical composition","中心对称"),
("对角线","Diagonal","对角动感","diagonal dynamic composition","对角线"),
("引导线","Leading Lines","线条引导","leading lines","引导线"),
("框架式","Framing","框架包围","framing composition","框架式"),
("三角构图","Triangular","稳定三角","triangular composition","三角构图"),
("S形曲线","S-Curve","蜿蜒S线","S-curve composition","S形曲线"),
("重复韵律","Repetition","图案节奏","repetition pattern rhythm","重复韵律"),
("放射构图","Radial","中心放射","radial composition","放射构图"),
("水平线构图","Horizontal","平稳水平","horizontal calm composition","水平线构图")],"构图;语法")
block("视觉层级与引导",[
("视觉重心","Visual Weight","注意力重点","visual weight focal emphasis","视觉重心"),
("主次层级","Hierarchy","主次分明","visual hierarchy primary secondary","主次层级"),
("视线引导","Eye Flow","引导视线流","eye flow guidance","视线引导"),
("对比强调","Contrast Emphasis","对比突出主体","contrast emphasis subject pop","对比强调"),
("前中后景","Foreground Layers","空间纵深层次","foreground midground background layers","前中后景"),
("留白呼吸","Negative Space","留白呼吸","negative space breathing room","留白呼吸"),
("视觉引力","Focal Point","视觉焦点","clear focal point","视觉焦点")],"构图;层级")
block("叙事与张力",[
("视觉节奏","Visual Rhythm","元素节奏","visual rhythm pacing","视觉节奏"),
("画面张力","Tension","对立张力","compositional tension","画面张力"),
("叙事留白","Narrative Space","想象空间","narrative space suggestion","叙事留白"),
("方向暗示","Implied Direction","方向运动暗示","implied movement direction","方向暗示"),
("呼应平衡","Balance","视觉平衡","visual balance equilibrium","呼应平衡"),
("打破常规","Breaking Symmetry","破缺张力","broken symmetry tension","打破常规")],"构图;叙事")
block("视角与画幅",[
("平视","Eye Level","中立平视","eye level neutral","平视"),
("俯视","High Angle","向下俯视","high angle down","俯视"),
("仰视","Low Angle","向上仰视气势","low angle up powerful","仰视"),
("鸟瞰","Aerial Top","顶视俯瞰","top-down aerial view","鸟瞰"),
("正方形画幅","Square 1:1","方形构图","square 1:1 framing","正方形画幅"),
("竖幅","Vertical Frame","竖构图","vertical portrait frame","竖幅"),
("宽幅全景","Panorama","超宽全景","wide panoramic frame","宽幅全景")],"构图;视角画幅")
block("心理与格式塔",[
("接近原则","Proximity","邻近成组","gestalt proximity grouping","接近原则"),
("相似原则","Similarity","相似成组","gestalt similarity","相似原则"),
("闭合原则","Closure","自动补全","gestalt closure","闭合原则"),
("连续原则","Continuity","视线连续","gestalt continuity","连续原则"),
("图底关系","Figure-Ground","图与底","figure-ground relationship","图底关系"),
("简化原则","Pragnanz","简洁优先","gestalt pragnanz simplicity","简化原则")],"构图;格式塔")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
open(CSV,"w",encoding="utf-8-sig",newline="").close()
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
