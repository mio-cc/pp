# -*- coding: utf-8 -*-
"""V02 电影摄影体系（穷举，联网研究整理）。合并模式：保留其他卷，仅替换 V02。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V02"; rows=[]
def add(cat,zh,en,defs,pen,pcn,tags):
    rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items: add(cat,zh,en,defs,pen,pcn,tags)

block("景别",[
("大远景","Extreme Long Shot","宏大全景、人物渺小","extreme long shot, vast scale, tiny subject","大远景, 宏大全景"),
("远景","Long Shot","交代环境全身","long shot, full environment","远景, 环境全身"),
("全景","Full Shot","人物全身","full shot, head to toe","全景, 全身"),
("中全景","Medium Long Shot","膝盖以上","medium long shot, knees up","中全景, 膝上"),
("中景","Medium Shot","腰部以上","medium shot, waist up","中景, 腰上"),
("中近景","Medium Close-Up","胸部以上","medium close-up, chest up","中近景, 胸上"),
("近景","Close Shot","肩部以上","close shot, shoulders up","近景, 肩上"),
("特写","Close-Up","面部表情","close-up, face emotion","特写, 面部"),
("大特写","Extreme Close-Up","眼睛局部强度","extreme close-up, eye detail intensity","大特写, 眼部局部"),
("插入镜头","Insert Shot","细节插入","insert shot, detail cutaway","插入镜头, 细节"),
("定场镜头","Establishing Shot","开场交代时空","establishing shot, sets location","定场镜头, 交代时空")],"电影;景别")

block("机位运动",[
("推镜","Dolly In","推进逼近主体","dolly in, push toward subject","推镜, 逼近"),
("拉镜","Dolly Out","拉远抽离","dolly out, pull away reveal","拉镜, 拉远抽离"),
("横摇","Pan","水平摇摄","pan, horizontal sweep","横摇, 水平摇"),
("纵摇","Tilt","垂直俯仰摇","tilt, vertical up down","纵摇, 俯仰"),
("移镜","Tracking/Trucking","平行平移跟随","tracking shot, lateral move","移镜, 平移跟随"),
("跟镜","Follow Shot","跟随主体运动","follow shot, moving with subject","跟镜, 跟随"),
("升降镜","Pedestal/Boom","垂直升降","pedestal boom up down","升降镜, 垂直升降"),
("摇臂镜头","Crane Shot","摇臂大幅运动","crane shot, sweeping move","摇臂镜头"),
("斯坦尼康","Steadicam","稳定器平滑跟拍","steadicam smooth following","斯坦尼康, 平滑跟拍"),
("手持镜头","Handheld","手持晃动纪实感","handheld shaky documentary feel","手持镜头, 晃动纪实"),
("轨道车","Dolly Track","轨道平滑移动","dolly track smooth move","轨道车, 平滑移动"),
("变焦推拉","Zoom","变焦改变视野","zoom, focal length change","变焦推拉"),
("希区柯克变焦","Dolly Zoom","眩晕反向变焦","dolly zoom, vertigo effect","希区柯克变焦, 眩晕"),
("甩镜","Whip Pan","急速甩动转场","whip pan, fast blur transition","甩镜, 急速转场"),
("环绕镜头","Arc Shot","环绕主体旋转","arc shot, orbit around subject","环绕镜头, 旋转"),
("航拍运动","Aerial/Drone","无人机高空运动","aerial drone moving shot","航拍运动, 无人机"),
("一镜到底","Long Take/Oner","不间断长镜头","long take, oner, continuous","一镜到底, 长镜头")],"电影;运动")

block("镜头语言",[
("主镜头","Master Shot","完整场景主镜","master shot, full scene","主镜头"),
("正反打","Shot Reverse Shot","对话正反打","shot reverse shot, dialogue","正反打, 对话"),
("过肩镜头","Over-the-Shoulder","过肩对话","over-the-shoulder dialogue","过肩镜头"),
("主观镜头","POV Shot","第一人称主观","POV first person subjective","主观镜头, 第一人称"),
("反应镜头","Reaction Shot","人物反应","reaction shot, response","反应镜头"),
("双人镜头","Two Shot","两人同框","two shot, two subjects","双人镜头"),
("空镜头","Cutaway/Empty","无人物空境","empty cutaway scenery","空镜头"),
("长镜头","Long Take","长时间不切","long take, extended duration","长镜头"),
("180度轴线","180-Degree Rule","保持轴线一致","180 degree axis consistent screen direction","180度轴线"),
("深焦镜头","Deep Focus","前后皆清晰调度","deep focus, all planes sharp","深焦, 纵深清晰"),
("对焦转移","Rack Focus","焦点在前后景转移","rack focus, focus pull shift","对焦转移, 焦点转移")],"电影;镜头语言")

block("电影布光与影调",[
("三点布光","Three-Point Lighting","主辅轮廓","three-point lighting key fill rim","三点布光"),
("高调影像","High Key","明亮低反差","high key bright low contrast","高调影像"),
("低调影像","Low Key","暗调高反差戏剧","low key dark high contrast dramatic","低调影像, 戏剧"),
("明暗对照","Chiaroscuro","强烈光暗对比","chiaroscuro, strong light dark contrast","明暗对照"),
("动机光","Motivated Lighting","符合场景光源逻辑","motivated lighting, realistic source","动机光"),
("实用光源","Practical Lighting","画面内灯具光","practical lights in scene","实用光源"),
("逆光剪影","Backlit Silhouette","逆光黑剪影","backlit silhouette","逆光剪影"),
("边缘光","Rim/Kicker Light","勾勒轮廓边缘","rim kicker light edge glow","边缘光, 轮廓"),
("夜戏蓝调","Day-for-Night","蓝调假夜","day-for-night blue moonlight","夜戏蓝调, 假夜"),
("霓虹混光","Neon Mixed Light","彩色混合光赛博","neon mixed colored light cyberpunk","霓虹混光, 赛博"),
("柔光氛围","Soft Diffused","柔和电影氛围","soft diffused cinematic mood","柔光氛围"),
("硬光戏剧","Hard Dramatic","硬光强阴影","hard light dramatic shadows","硬光戏剧")],"电影;布光")

block("画幅与画格",[
("学院画幅1.37","Academy 1.37","经典学院比例","academy ratio 1.37:1","学院画幅 1.37"),
("遮幅1.85","Widescreen 1.85","标准宽银幕","1.85:1 widescreen","遮幅 1.85"),
("变形宽银幕2.39","Anamorphic 2.39","电影感超宽","2.39:1 anamorphic widescreen cinematic","变形宽银幕 2.39"),
("16:9","16:9","高清标准","16:9 HD standard","16:9 宽高比"),
("4:3","4:3","复古方正","4:3 retro boxy","4:3 复古"),
("竖屏9:16","Vertical 9:16","手机竖屏","9:16 vertical mobile","竖屏 9:16"),
("IMAX 1.43","IMAX 1.43","巨幕高画幅","IMAX 1.43 tall frame","IMAX 1.43 巨幕"),
("变形椭圆散景","Anamorphic Bokeh","椭圆形焦外","anamorphic oval bokeh","变形椭圆散景"),
("变形蓝色眩光","Anamorphic Flare","水平蓝色光条","anamorphic horizontal blue flare","变形蓝色眩光")],"电影;画幅")

block("胶片与数字格式",[
("35mm电影胶片","35mm Film","标准电影胶片质感","35mm film grain cinematic","35mm 电影胶片"),
("16mm胶片","16mm Film","颗粒粗复古","16mm film, coarse grain vintage","16mm 胶片"),
("Super 8","Super 8","家庭录像复古","super 8 home movie retro","Super 8 复古"),
("65mm/IMAX胶片","65mm Film","极致细节大画幅","65mm large format extreme detail","65mm 胶片"),
("数字RAW","Digital RAW","无损高宽容度","digital RAW high latitude","数字 RAW"),
("LOG灰片","LOG Profile","低对比待调色","flat LOG profile for grading","LOG 灰片"),
("胶片颗粒","Film Grain","电影胶片颗粒","cinematic film grain","胶片颗粒")],"电影;格式")

block("帧率与时间",[
("24帧电影感","24fps","标准电影感运动模糊","24fps cinematic motion blur","24帧 电影感"),
("升格慢动作","Slow Motion","高帧慢放","slow motion high frame rate","升格慢动作"),
("120帧极慢","120fps","极致慢动作","120fps extreme slow motion","120帧 极慢"),
("延时摄影","Timelapse","时间压缩流动","timelapse, compressed time","延时摄影"),
("定格动画","Stop Motion","逐帧定格","stop motion frame by frame","定格动画"),
("子弹时间","Bullet Time","环绕凝固时间","bullet time, frozen orbit","子弹时间")],"电影;时间")

block("场面调度与转场",[
("场面调度","Mise-en-scène","画面元素布置","mise-en-scene, staged composition","场面调度"),
("纵深调度","Deep Staging","前中后景纵深","deep staging, layered depth","纵深调度"),
("前景遮挡","Foreground Framing","前景元素框遮","foreground framing occlusion","前景遮挡"),
("叠化转场","Dissolve","画面交叠过渡","dissolve transition","叠化转场"),
("淡入淡出","Fade","渐显渐隐","fade in out","淡入淡出"),
("划像转场","Wipe","划过切换","wipe transition","划像转场"),
("匹配剪辑","Match Cut","形态匹配切换","match cut, graphic match","匹配剪辑")],"电影;调度")

# 合并写回
existing=[]
if CSV.exists():
    existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} generated: {len(rows)} | total CSV: {len(allrows)}")
