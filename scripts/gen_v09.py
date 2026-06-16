# -*- coding: utf-8 -*-
"""V09 构图与视觉叙事（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V09"; rows=[]
def simple(cat,items,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en+" composition","",zh,"","","","",tags,"整理","published","V1.0"])))
simple("构图语法",[("三分法","rule of thirds"),("黄金螺旋","golden spiral fibonacci"),("黄金分割","golden ratio"),("中心对称","central symmetry"),("对角线","diagonal dynamic"),("引导线","leading lines"),("框架式","framing"),("三角构图","triangular"),("S形曲线","s-curve"),("C形构图","c-curve"),("重复韵律","repetition rhythm"),("放射构图","radial"),("水平线","horizontal calm"),("垂直线","vertical"),("曲线引导","curved lines"),("螺旋构图","spiral"),("井字构图","grid nine"),("L形构图","l-shaped"),("满构图","full frame fill"),("极简构图","minimalist")],"构图;语法")
simple("视觉层级与引导",[("视觉重心","visual weight focal"),("主次层级","visual hierarchy"),("视线引导","eye flow guidance"),("对比强调","contrast emphasis"),("前中后景","foreground midground background layers"),("留白呼吸","negative space"),("视觉焦点","focal point"),("景深层次","depth layering"),("大小对比","scale contrast"),("明暗对比","tonal contrast"),("色彩引导","color guidance")],"构图;层级")
simple("叙事与张力",[("视觉节奏","visual rhythm pacing"),("画面张力","compositional tension"),("叙事留白","narrative space"),("方向暗示","implied direction"),("呼应平衡","visual balance"),("打破常规","broken symmetry"),("对称平衡","symmetrical balance"),("非对称平衡","asymmetrical balance"),("动态平衡","dynamic balance"),("视觉重量分布","weight distribution"),("故事性瞬间","decisive moment")],"构图;叙事")
simple("视角与画幅",[("平视","eye level"),("俯视","high angle"),("仰视","low angle heroic"),("鸟瞰","top-down aerial"),("虫视","worm eye view"),("荷兰角","dutch tilt"),("正方形画幅","square 1:1"),("竖幅","vertical portrait"),("横幅","horizontal landscape"),("宽幅全景","panoramic"),("超宽画幅","ultrawide cinematic")],"构图;视角画幅")
simple("心理与格式塔",[("接近原则","gestalt proximity"),("相似原则","gestalt similarity"),("闭合原则","gestalt closure"),("连续原则","gestalt continuity"),("图底关系","figure-ground"),("简化原则","gestalt pragnanz"),("共同命运","common fate"),("对称原则","gestalt symmetry"),("焦点引力","focal attraction")],"构图;格式塔")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
