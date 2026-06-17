# -*- coding: utf-8 -*-
"""V12 动画、分镜与动态设计（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V12"; rows=[]
def block(cat,items,tags):
    for zh,en,defs in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",en,"",zh,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("动画原理",[
("挤压拉伸","squash and stretch","通过形变表现重量弹性和冲击力的动画原则"),
("预备动作","anticipation","主要动作前的蓄势姿态，用来提示运动方向"),
("演出布局","staging","清晰安排角色动作和视线焦点的表现原则"),
("关键姿势","pose to pose","先设计关键姿态再补中间帧的动画方法"),
("逐帧动画","straight ahead action","从第一帧连续绘制到最后一帧的动画方法"),
("跟随重叠","follow through overlapping","附属部位滞后或延续运动的自然动态"),
("缓入缓出","ease in ease out","动作起止速度逐渐变化的时间控制"),
("弧线运动","arc motion","让动作沿曲线轨迹运动以显得自然流畅"),
("次要动作","secondary action","辅助主动作表达情绪或质感的小动作"),
("时间节奏","timing","用帧数和间隔控制动作速度与重量感"),
("夸张","exaggeration","放大动作造型以增强戏剧性和可读性"),
("实体造型","solid drawing","保持体积透视一致的角色造型能力"),
("吸引力","appeal","让角色动作和造型具有清晰魅力的原则")],"动画;原理")

block("分镜语言",[
("分镜构图","storyboard framing","在分镜格中规划镜头角度和画面重心"),
("镜头连接","shot continuity","保持动作方向和空间关系连贯的镜头衔接"),
("动态分镜","animatic","把分镜按时间剪成带节奏的预览动画"),
("故事板","storyboard panels","用连续画格预先表达剧情和镜头设计"),
("镜头编号","shot list","为每个镜头标号以便制作沟通和管理"),
("运动轨迹","motion path","标示角色或镜头移动路线的路径线"),
("摄影表","x-sheet exposure sheet","记录帧位对白动作和层级的动画时间表")],"动画;分镜")

block("时间与节奏",[
("时间控制","timing control","通过帧间距安排动作快慢和情绪节拍"),
("节拍停顿","beat pause","在关键动作间加入停顿以突出反应和笑点"),
("速度曲线","speed curve graph editor","用曲线控制动画属性速度变化的工具表达"),
("循环动画","loop cycle","首尾无缝衔接可反复播放的动作段"),
("二次动作","secondary motion","跟随主体运动产生的附加自然动态"),
("预备-动作-缓冲","anticipation action recovery","由蓄势、执行、收势组成的完整动作结构")],"动画;时间")

block("角色绑定",[
("骨骼绑定","skeleton rigging","为角色建立可驱动模型运动的骨架系统"),
("蒙皮权重","skin weight","控制网格随骨骼变形影响范围的数据"),
("表情绑定","facial rig blendshape","用控制器或形变目标驱动面部表情"),
("动作捕捉","motion capture","采集真人运动数据并映射到数字角色"),
("IK反向动力学","inverse kinematics","通过末端控制自动求解关节姿态的方法"),
("控制器","rig controller","供动画师操作骨骼和形变的可视化控件")],"动画;绑定")

block("特效与合成",[
("粒子特效","particle effects","大量小粒子模拟烟尘火花雨雪等效果"),
("流体模拟","fluid smoke simulation","用物理计算生成液体烟雾流动效果"),
("刚体破碎","rigid body destruction","模拟硬物碰撞碎裂和散落的动力学效果"),
("布料模拟","cloth simulation","计算布料受重力碰撞产生的褶皱运动"),
("绿幕抠像","green screen chroma key","去除绿色背景并合成新画面的技术"),
("运动跟踪","motion tracking","追踪画面点位以匹配合成元素的运动"),
("光效叠加","light glow effects","叠加发光眩光强化能量和氛围的效果"),
("烟火特效","pyro fire fx","模拟火焰爆炸烟尘等高能量特效")],"动画;特效")

block("动态图形与风格",[
("MG动画","motion graphics","以图形文字和转场为主体的信息动画"),
("文字动效","kinetic typography","让文字随节奏运动以增强表达的动效"),
("转场动画","animated transition","连接两个画面状态的过渡运动设计"),
("图标动效","animated icon","让图标通过短动作传达状态或反馈"),
("信息动效","animated data viz","用动画呈现数据变化和信息层级"),
("2D逐帧","2d frame animation","平面角色或图形逐帧绘制的动画形式"),
("3D动画","3d animation","在三维空间中驱动模型运动的动画形式"),
("定格动画","stop motion","逐次拍摄实体物件形成连续运动的动画"),
("黏土动画","claymation","用黏土模型定格拍摄的手作质感动画"),
("剪纸动画","cutout animation","用平面分层纸片或贴图操控的动画"),
("转描","rotoscope","描摹实拍动作得到绘制动画的技术"),
("MMD","mmd 3d dance","基于MikuMikuDance生态的三维角色舞蹈动画")],"动画;MG风格")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
