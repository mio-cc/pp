# -*- coding: utf-8 -*-
"""V02 电影摄影体系（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V02"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("景别",[
("大远景","Extreme Long Shot","宏大全景人物渺小","extreme long shot, vast scale","大远景"),
("远景","Long Shot","环境全身","long shot, full environment","远景"),
("全景","Full Shot","人物全身","full shot head to toe","全景"),
("中全景","Medium Long Shot","膝上","medium long shot, knees up","中全景"),
("中景","Medium Shot","腰上","medium shot, waist up","中景"),
("中近景","Medium Close-Up","胸上","medium close-up, chest up","中近景"),
("近景","Close Shot","肩上","close shot, shoulders up","近景"),
("特写","Close-Up","面部","close-up, face","特写"),
("大特写","Extreme Close-Up","眼部局部","extreme close-up, eye detail","大特写"),
("插入镜头","Insert Shot","细节插入","insert detail shot","插入镜头"),
("定场镜头","Establishing Shot","开场交代时空","establishing shot","定场镜头"),
("双人镜头","Two Shot","两人同框","two shot","双人镜头"),
("三人镜头","Three Shot","三人同框","three shot","三人镜头"),
("群像镜头","Group Shot","多人群像","group ensemble shot","群像镜头"),
("主视点镜头","POV Shot","第一人称","POV first person view","主视点镜头")],"电影;景别")
block("机位运动",[
("推镜","Dolly In","推进","dolly in push","推镜"),
("拉镜","Dolly Out","拉远","dolly out reveal","拉镜"),
("横摇","Pan","水平摇","pan horizontal","横摇"),
("纵摇","Tilt","俯仰摇","tilt vertical","纵摇"),
("移镜","Tracking","平移跟随","tracking lateral","移镜"),
("跟镜","Follow","跟随主体","follow shot","跟镜"),
("升降镜","Pedestal","垂直升降","pedestal boom","升降镜"),
("摇臂","Crane","大幅摇臂","crane sweeping","摇臂"),
("斯坦尼康","Steadicam","平滑跟拍","steadicam smooth","斯坦尼康"),
("手持","Handheld","晃动纪实","handheld shaky","手持"),
("轨道车","Dolly Track","轨道平滑","dolly track","轨道车"),
("变焦推拉","Zoom","变焦","zoom in out","变焦推拉"),
("急推变焦","Crash Zoom","急速变焦","crash zoom","急推变焦"),
("希区柯克变焦","Dolly Zoom","眩晕反向","dolly zoom vertigo","希区柯克变焦"),
("甩镜","Whip Pan","急速甩转","whip pan blur","甩镜"),
("环绕镜头","Arc Shot","环绕旋转","arc orbit shot","环绕镜头"),
("航拍","Aerial Drone","无人机高空","aerial drone shot","航拍"),
("FPV穿越","FPV Drone","穿越机俯冲","FPV drone flythrough","FPV穿越"),
("车载镜头","Car Mount","车体固定","car mount shot","车载镜头"),
("肩扛","Shoulder Rig","肩扛纪实","shoulder rig","肩扛"),
("一镜到底","Long Take","不间断长镜","oner long take","一镜到底"),
("俯冲镜头","Top-Down Dive","俯冲向下","top down diving shot","俯冲镜头")],"电影;运动")
block("镜头类型与光学",[
("球面镜头","Spherical Lens","常规球面","spherical lens","球面镜头"),
("变形镜头","Anamorphic Lens","椭圆散景蓝条","anamorphic lens, oval bokeh blue flare","变形镜头"),
("超广角","Ultra Wide","开阔夸张","ultra wide angle lens","超广角"),
("广角","Wide Lens","广角","wide angle lens","广角"),
("标准镜头","Standard Lens","自然视角","standard 50mm lens","标准镜头"),
("长焦","Telephoto","压缩远摄","telephoto compression","长焦"),
("微距","Macro","极近特写","macro extreme closeup","微距"),
("移轴","Tilt-Shift","微缩透视","tilt-shift miniature","移轴"),
("柔焦镜头","Soft Focus","梦幻柔焦","soft focus dreamy","柔焦镜头"),
("复古镜头","Vintage Lens","老镜旋焦","vintage lens swirly bokeh","复古镜头"),
("鱼眼","Fisheye","极度桶形","fisheye 180 distortion","鱼眼")],"电影;镜头光学")
block("镜头语言",[
("主镜头","Master Shot","完整场景","master shot","主镜头"),
("正反打","Shot Reverse","对话切换","shot reverse shot","正反打"),
("过肩镜头","Over-the-Shoulder","过肩","over the shoulder","过肩镜头"),
("反应镜头","Reaction Shot","人物反应","reaction shot","反应镜头"),
("空镜头","Cutaway","无人空境","empty cutaway","空镜头"),
("长镜头","Long Take","长时不切","long take","长镜头"),
("180度轴线","180 Rule","保持轴线","180 degree axis","180度轴线"),
("深焦","Deep Focus","纵深清晰","deep focus","深焦"),
("对焦转移","Rack Focus","焦点转移","rack focus pull","对焦转移"),
("交叉剪辑","Cross-Cutting","并行交叉","cross cutting parallel","交叉剪辑"),
("蒙太奇","Montage","快速拼接","montage sequence","蒙太奇"),
("闪回","Flashback","回忆插叙","flashback dreamy","闪回")],"电影;镜头语言")
block("电影布光与影调",[
("三点布光","Three-Point","主辅轮廓","three-point lighting","三点布光"),
("高调影像","High Key","明亮低反差","high key","高调影像"),
("低调影像","Low Key","暗调戏剧","low key dramatic","低调影像"),
("明暗对照","Chiaroscuro","强光暗对比","chiaroscuro","明暗对照"),
("动机光","Motivated Light","符合场景源","motivated lighting","动机光"),
("实用光源","Practical Light","画面内灯","practical lights","实用光源"),
("逆光剪影","Backlit Silhouette","黑剪影","backlit silhouette","逆光剪影"),
("边缘光","Rim Light","轮廓边缘","rim light edge","边缘光"),
("顶光","Top Light","顶部下打","top light","顶光"),
("底光","Underlight","底部恐怖光","underlight horror","底光"),
("夜戏蓝调","Day-for-Night","蓝假夜","day for night blue","夜戏蓝调"),
("霓虹混光","Neon Mixed","彩色赛博","neon mixed cyberpunk","霓虹混光"),
("火光","Firelight","暖跳动火光","flickering firelight","火光"),
("月光","Moonlight","冷蓝月光","cool moonlight","月光"),
("频闪","Strobe","闪烁频闪","strobe flashing","频闪"),
("柔光氛围","Soft Mood","柔和电影感","soft cinematic mood","柔光氛围"),
("硬光戏剧","Hard Dramatic","硬光阴影","hard dramatic shadows","硬光戏剧")],"电影;布光")
block("画幅与画格",[
("学院1.37","Academy 1.37","经典学院","academy 1.37","学院画幅"),
("遮幅1.66","1.66:1","欧洲遮幅","1.66:1 widescreen","遮幅1.66"),
("遮幅1.85","1.85:1","标准宽银幕","1.85:1 widescreen","遮幅1.85"),
("变形2.39","Anamorphic 2.39","电影超宽","2.39:1 anamorphic cinematic","变形2.39"),
("Ultra Panavision 2.76","2.76:1","超宽史诗","2.76:1 ultra panavision","超宽2.76"),
("16:9","16:9","高清","16:9 HD","16:9"),
("4:3","4:3","复古方正","4:3 retro","4:3"),
("竖屏9:16","9:16","手机竖屏","9:16 vertical","竖屏"),
("IMAX 1.43","IMAX 1.43","巨幕","IMAX 1.43","IMAX"),
("变形椭圆散景","Anamorphic Bokeh","椭圆焦外","anamorphic oval bokeh","变形椭圆散景"),
("变形蓝条眩光","Anamorphic Flare","水平蓝光","horizontal blue anamorphic flare","变形蓝条")],"电影;画幅")
block("胶片数字与帧率",[
("35mm胶片","35mm Film","电影胶片","35mm film cinematic","35mm胶片"),
("16mm胶片","16mm Film","粗颗粒复古","16mm grainy vintage","16mm胶片"),
("Super 8","Super 8","家庭复古","super 8 retro","Super 8"),
("65mm胶片","65mm Film","大画幅细节","65mm large format","65mm胶片"),
("数字RAW","RAW","高宽容度","digital RAW","RAW"),
("LOG灰片","LOG","低对比待调","flat LOG","LOG"),
("胶片颗粒","Film Grain","电影颗粒","film grain","胶片颗粒"),
("24帧","24fps","电影感","24fps cinematic","24帧"),
("25帧","25fps","PAL","25fps","25帧"),
("30帧","30fps","视频","30fps video","30帧"),
("48帧高帧","48fps","高帧流畅","48fps high frame","48帧"),
("60帧","60fps","流畅","60fps smooth","60帧"),
("120帧极慢","120fps","极致慢动作","120fps extreme slowmo","120帧"),
("升格慢动作","Slow Motion","慢放","slow motion","升格"),
("延时摄影","Timelapse","时间压缩","timelapse","延时"),
("定格动画","Stop Motion","逐帧","stop motion","定格"),
("子弹时间","Bullet Time","环绕凝固","bullet time","子弹时间")],"电影;格式帧率")
block("场面调度与转场",[
("场面调度","Mise-en-scène","画面布置","mise-en-scene staging","场面调度"),
("纵深调度","Deep Staging","前中后纵深","deep staging layered","纵深调度"),
("前景遮挡","Foreground Frame","前景框遮","foreground framing","前景遮挡"),
("叠化","Dissolve","交叠过渡","dissolve transition","叠化"),
("淡入淡出","Fade","渐显隐","fade in out","淡入淡出"),
("划像","Wipe","划过切","wipe transition","划像"),
("匹配剪辑","Match Cut","形态匹配","match cut","匹配剪辑"),
("跳切","Jump Cut","突兀跳接","jump cut","跳切"),
("硬切","Hard Cut","直接切","hard cut","硬切")],"电影;调度转场")
block("电影调色风格",[
("青橙调","Teal and Orange","冷暖对比","teal and orange grade","青橙调"),
("漂白旁路","Bleach Bypass","高反差去饱和","bleach bypass desaturated","漂白旁路"),
("黑色电影调","Film Noir","高反差黑白","film noir high contrast bw","黑色电影"),
("复古暖调","Warm Vintage","怀旧暖","warm vintage grade","复古暖调"),
("冷峻科幻调","Cold Sci-Fi","冷蓝科幻","cold blue sci-fi grade","冷峻科幻")],"电影;调色")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
