# -*- coding: utf-8 -*-
"""V12 动画、分镜与动态设计（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V12"; rows=[]
def simple(cat,items,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en,"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("动画原理",[("挤压拉伸","squash and stretch"),("预备动作","anticipation"),("演出布局","staging"),("关键姿势","pose to pose"),("逐帧动画","straight ahead action"),("跟随重叠","follow through overlapping"),("缓入缓出","ease in ease out"),("弧线运动","arc motion"),("次要动作","secondary action"),("时间节奏","timing"),("夸张","exaggeration"),("实体造型","solid drawing"),("吸引力","appeal")],"动画;原理")
simple("分镜语言",[("分镜构图","storyboard framing"),("镜头连接","shot continuity"),("动态分镜","animatic"),("故事板","storyboard panels"),("镜头编号","shot list"),("运动轨迹","motion path"),("摄影表","x-sheet exposure sheet")],"动画;分镜")
simple("时间与节奏",[("时间控制","timing control"),("节拍停顿","beat pause"),("速度曲线","speed curve graph editor"),("循环动画","loop cycle"),("二次动作","secondary motion"),("预备-动作-缓冲","anticipation action recovery")],"动画;时间")
simple("角色绑定",[("骨骼绑定","skeleton rigging"),("蒙皮权重","skin weight"),("表情绑定","facial rig blendshape"),("动作捕捉","motion capture"),("IK反向动力学","inverse kinematics"),("控制器","rig controller")],"动画;绑定")
simple("特效与合成",[("粒子特效","particle effects"),("流体模拟","fluid smoke simulation"),("刚体破碎","rigid body destruction"),("布料模拟","cloth simulation"),("绿幕抠像","green screen chroma key"),("运动跟踪","motion tracking"),("光效叠加","light glow effects"),("烟火特效","pyro fire fx")],"动画;特效")
simple("动态图形与风格",[("MG动画","motion graphics"),("文字动效","kinetic typography"),("转场动画","animated transition"),("图标动效","animated icon"),("信息动效","animated data viz"),("2D逐帧","2d frame animation"),("3D动画","3d animation"),("定格动画","stop motion"),("黏土动画","claymation"),("剪纸动画","cutout animation"),("转描","rotoscope"),("MMD","mmd 3d dance")],"动画;MG风格")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
