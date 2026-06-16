# -*- coding: utf-8 -*-
"""V12 动画、分镜与动态设计（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V12"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("动画原理",[
("挤压拉伸","Squash and Stretch","弹性变形","squash and stretch","挤压拉伸"),
("预备动作","Anticipation","蓄力预备","anticipation","预备动作"),
("演出布局","Staging","清晰演出","staging clear posing","演出布局"),
("关键姿势","Pose to Pose","关键帧姿势","pose to pose key poses","关键姿势"),
("跟随重叠","Follow Through","惯性跟随","follow through overlapping action","跟随重叠"),
("缓入缓出","Ease In Out","加速减速","ease in ease out, slow in out","缓入缓出"),
("弧线运动","Arcs","自然弧线","arc motion path","弧线运动"),
("次要动作","Secondary Action","辅助动作","secondary action","次要动作"),
("时间节奏","Timing","节奏快慢","timing spacing","时间节奏"),
("夸张","Exaggeration","夸张强调","exaggeration","夸张"),
("实体造型","Solid Drawing","体积结构","solid drawing volume","实体造型"),
("吸引力","Appeal","角色魅力","appeal charisma","吸引力")],"动画;原理")
block("分镜语言",[
("分镜构图","Storyboard Framing","分镜画面","storyboard frame composition","分镜构图"),
("镜头连接","Shot Continuity","镜头衔接","shot to shot continuity","镜头连接"),
("动态分镜","Animatic","动态预演","animatic motion storyboard","动态分镜"),
("故事板","Storyboard","叙事板","storyboard panels","故事板"),
("镜头编号","Shot List","镜头表","shot list breakdown","镜头编号")],"动画;分镜")
block("特效与合成",[
("粒子特效","Particle FX","粒子系统","particle effects","粒子特效"),
("流体模拟","Fluid Sim","液体烟雾","fluid smoke simulation","流体模拟"),
("刚体破碎","Rigid Body","破碎倒塌","rigid body destruction","刚体破碎"),
("绿幕抠像","Chroma Key","抠像合成","green screen chroma key","绿幕抠像"),
("运动跟踪","Motion Tracking","跟踪合成","motion tracking compositing","运动跟踪"),
("光效叠加","Light FX","光效辉光","light glow effects overlay","光效叠加")],"动画;特效")
block("动态图形",[
("MG动画","Motion Graphics","图形动效","motion graphics animation","MG动画"),
("文字动效","Kinetic Typography","动态文字","kinetic typography","文字动效"),
("转场动画","Transition","流畅转场","animated transition","转场动画"),
("图标动效","Icon Animation","图标动画","animated icon micro-interaction","图标动效"),
("信息动效","Data Animation","数据动画","animated data visualization","信息动效")],"动画;MG")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
