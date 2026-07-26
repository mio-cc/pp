# -*- coding: utf-8 -*-
"""V01 摄影体系 正式术语（穷举档位 + 完整分类，联网研究整理）。原子化/路径分类/中英双语/无负向。"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"
FIELDS = ["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short",
          "definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt",
          "positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with",
          "tags","source_refs","status","version"]
rows=[]
def enrich_def(cat, zh, defs):
    if len(defs.strip()) >= 8:
        return defs
    d = defs.strip().rstrip("。.；;，, ")
    if "快门速度" in cat:
        return f"{zh}用于记录持续光轨的快门档位。"
    if "景深与虚化" in cat:
        return f"{d}塑造主体分离的景深效果。"
    if "光学缺陷与效果" in cat:
        return f"{d}形成镜头成像缺陷或光学效果。"
    if "画幅" in cat:
        return f"{d}影响噪点景深和便携性的画幅规格。"
    if "相机类型" in cat:
        return f"{d}形成对应拍摄体验的相机类型。"
    if "自然光" in cat:
        return f"{d}塑造自然场景明暗气氛的光线。"
    if "影室布光" in cat:
        return f"{d}塑造人像明暗结构的布光方法。"
    if "光质与修饰器" in cat:
        return f"{d}控制光线形态与阴影边界的工具。"
    if "构图法则" in cat:
        return f"{d}组织画面重心与视线的构图法。"
    if "视角机位" in cat:
        return f"{d}改变主体气势和空间关系的视角。"
    if "景别" in cat:
        return f"{d}范围入画以控制叙事距离的景别。"
    if "拍摄题材" in cat:
        return f"以{d}为核心内容的摄影题材。"
    if "胶片与质感" in cat:
        return f"{d}形成复古影像气质的胶片质感。"
    return f"{d}说明{zh}的核心视觉特征。"

def add(cat,zh,en,defs,pen,pcn,tags):
    defs = enrich_def(cat, zh, defs)
    rows.append(dict(zip(FIELDS,["",zh,en,"","V01",cat,defs,"","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))

# ===== 曝光控制 / 光圈：整档 f 值穷举 =====
AP=[("f/1.0","焦平面极薄、梦幻虚化","razor-thin depth of field, dreamy bokeh"),
("f/1.2","极浅景深、柔美奶油虚化","ultra shallow depth of field, creamy bokeh"),
("f/1.4","极浅景深、强背景分离","very shallow depth of field, strong subject separation"),
("f/1.8","浅景深、人像常用","shallow depth of field, classic portrait"),
("f/2.0","浅景深、柔和背景","shallow depth of field, soft background"),
("f/2.8","中浅景深、恒定大光圈变焦","moderately shallow depth of field"),
("f/3.5","适中偏浅景深","slightly shallow depth of field"),
("f/4","适中景深","moderate depth of field"),
("f/5.6","适中偏大景深、画质佳","balanced sharp depth of field"),
("f/8","大景深、最佳画质甜点","deep depth of field, sweet spot sharpness"),
("f/11","大景深、风光常用","deep depth of field, landscape"),
("f/16","大景深、点光源星芒","deep depth of field, sunstars"),
("f/22","极大景深、轻微衍射变软","very deep depth of field, mild diffraction softening"),
("f/32","极致景深、微距大画幅","extreme depth of field, macro large format")]
for v,cn,en in AP:
    add("曝光控制 / 光圈", v+" 光圈", v+" Aperture", v+"，"+cn+"。",
        v+" aperture, "+en, v+" 光圈, "+cn, "曝光;光圈")

# ===== 曝光控制 / 快门速度：整档穷举 =====
SH=[("1/8000秒","凝固极高速运动","freeze ultra-fast motion 1/8000s"),
("1/4000秒","凝固高速运动","freeze fast motion 1/4000s"),
("1/2000秒","凝固快速运动","freeze action 1/2000s"),
("1/1000秒","凝固运动","freeze motion 1/1000s"),
("1/500秒","凝固一般运动","sharp motion 1/500s"),
("1/250秒","日常手持安全","handheld sharp 1/250s"),
("1/125秒","手持人像","handheld portrait 1/125s"),
("1/60秒","室内手持极限","indoor handheld 1/60s"),
("1/30秒","轻微拖影风险","slight motion blur 1/30s"),
("1/15秒","动态模糊","motion blur 1/15s"),
("1/8秒","明显动态模糊","obvious motion blur 1/8s"),
("1/4秒","需稳定的慢门","slow shutter 1/4s tripod"),
("1秒","长曝光","long exposure 1s"),
("5秒","丝绢流水光轨","long exposure 5s silky water light trails"),
("15秒","超长曝光","long exposure 15s"),
("30秒","夜景超长曝光","night long exposure 30s"),
("B门长曝","Bulb 任意时长星轨","bulb long exposure star trails")]
for v,cn,en in SH:
    add("曝光控制 / 快门速度", v, ("Bulb" if v=="B门长曝" else v.replace("秒","s")),
        v+"，"+cn+"。", en, v+", "+cn, "曝光;快门")

# ===== 曝光控制 / 感光度 ISO：整档穷举 =====
ISO=[("ISO 50","极致纯净、最低原生","ultra clean, base low ISO"),
("ISO 100","基准纯净无噪","clean base ISO, no noise"),
("ISO 200","纯净","clean low noise"),
("ISO 400","通用、轻微颗粒","versatile, slight grain"),
("ISO 800","弱光、轻噪","low light, mild noise"),
("ISO 1600","弱光噪点","low light visible noise"),
("ISO 3200","高噪点","high ISO noise grain"),
("ISO 6400","强噪点","strong noise"),
("ISO 12800","极高噪点","very high ISO heavy noise"),
("ISO 25600","极限弱光、极重噪","extreme low light, extreme noise")]
for v,cn,en in ISO:
    add("曝光控制 / 感光度", v, v, v+"，"+cn+"。", v+", "+en, v+", "+cn, "曝光;ISO")

# ===== 曝光控制 / 测光与影调 =====
for zh,en,defs,pen,pcn in [
("高调","High Key","明亮通透、低对比","high key, bright airy, low contrast","高调, 明亮通透, 低对比"),
("低调","Low Key","暗调、高对比、戏剧阴影","low key, dark, dramatic shadows, high contrast","低调, 暗调, 戏剧阴影"),
("剪影","Silhouette","逆光黑剪影、亮背景","silhouette, backlit dark subject, bright background","剪影, 逆光黑主体"),
("HDR包围曝光","HDR Bracketing","高动态范围、阴影高光皆有细节","HDR, high dynamic range, detail in shadows and highlights","HDR, 高动态范围细节"),
("曝光过曝","Overexposed High Key","刻意过曝、洗白通透","intentionally overexposed, blown highlights, airy","过曝, 洗白通透"),
("欠曝暗调","Underexposed Moody","刻意欠曝、压暗氛围","underexposed, moody dark tones","欠曝, 压暗氛围")]:
    add("曝光控制 / 测光与影调", zh, en, defs+"。", pen, pcn, "曝光;影调")

# ===== 镜头与光学 / 焦距：整段穷举 =====
FL=[("8mm","鱼眼超广、180度","fisheye ultra-wide 180 degree"),
("14mm","超广角、夸张透视","14mm ultra-wide, exaggerated perspective"),
("16mm","超广角","16mm ultra-wide angle"),
("20mm","广角","20mm wide angle"),
("24mm","广角、环境交代","24mm wide angle environmental"),
("28mm","小广角","28mm mild wide angle"),
("35mm","人文、自然视角","35mm documentary natural perspective"),
("40mm","准标准","40mm near standard"),
("50mm","标准、接近人眼","50mm standard, human eye perspective"),
("60mm","微距标准","60mm macro standard"),
("85mm","人像、压缩讨喜","85mm portrait, flattering compression"),
("105mm","中长焦人像","105mm short telephoto portrait"),
("135mm","长焦人像、强压缩","135mm telephoto portrait, strong compression"),
("200mm","长焦、透视压缩","200mm telephoto, compressed perspective"),
("300mm","超长焦","300mm super telephoto"),
("400mm","超长焦打鸟","400mm super telephoto wildlife"),
("600mm","极长焦","600mm extreme telephoto")]
for v,cn,en in FL:
    add("镜头与光学 / 焦距", v+"焦距", v+" Lens", v+"，"+cn+"。",
        v+" lens, "+en, v+" 镜头, "+cn, "镜头;焦距")

# ===== 镜头与光学 / 镜头类型 =====
for zh,en,defs,pen,pcn in [
("定焦镜头","Prime Lens","固定焦距、大光圈锐利","prime lens, fixed focal length, sharp wide aperture","定焦镜头, 大光圈锐利"),
("变焦镜头","Zoom Lens","可变焦距、灵活","zoom lens, variable focal length","变焦镜头, 灵活"),
("微距镜头","Macro Lens","1:1 放大极致近摄","macro lens, 1:1 reproduction extreme close-up","微距镜头, 1:1放大"),
("鱼眼镜头","Fisheye Lens","约180度强桶形畸变","fisheye lens, 180 degree, barrel distortion","鱼眼镜头, 桶形畸变"),
("移轴镜头","Tilt-Shift Lens","透视校正、微缩效果","tilt-shift lens, perspective control, miniature effect","移轴镜头, 微缩效果"),
("折返镜头","Mirror Lens","环形焦外、轻便超长焦","mirror lens, ring bokeh, compact telephoto","折返镜头, 环形焦外"),
("柔焦镜头","Soft Focus Lens","柔化梦幻、复古人像","soft focus lens, dreamy glow vintage portrait","柔焦镜头, 梦幻")]:
    add("镜头与光学 / 镜头类型", zh, en, defs+"。", pen, pcn, "镜头;类型")

# ===== 镜头与光学 / 景深与虚化 =====
for zh,en,defs,pen,pcn in [
("浅景深","Shallow DoF","背景虚化、主体分离","shallow depth of field, blurred background, subject isolation","浅景深, 背景虚化"),
("深景深","Deep DoF","前后皆清晰","deep depth of field, sharp front to back","深景深, 前后全清"),
("奶油散景","Creamy Bokeh","柔滑焦外","creamy smooth bokeh","奶油散景, 柔滑焦外"),
("旋焦散景","Swirly Bokeh","老镜旋转焦外","swirly bokeh, vintage Helios","旋焦散景, 复古"),
("焦外光斑","Bokeh Balls","圆形焦外高光","bokeh balls, circular out-of-focus highlights","焦外光斑"),
("二线性散景","Nervous Bokeh","焦外勾边生硬","harsh nervous bokeh, double-line edges","二线性散景"),
("移轴微缩","Tilt-Shift Miniature","选择性对焦微缩玩具感","tilt-shift miniature, toy-like selective focus","移轴微缩, 玩具感")]:
    add("镜头与光学 / 景深与虚化", zh, en, defs+"。", pen, pcn, "镜头;散景")

# ===== 镜头与光学 / 光学缺陷与效果 =====
for zh,en,defs,pen,pcn in [
("桶形畸变","Barrel Distortion","广角中心鼓起","barrel distortion, wide-angle bulge","桶形畸变, 广角鼓起"),
("枕形畸变","Pincushion Distortion","长焦中心凹陷","pincushion distortion, telephoto pinch","枕形畸变"),
("色散紫边","Chromatic Aberration","高反差紫绿边","chromatic aberration, purple green fringing","色散, 紫边"),
("暗角","Vignetting","四角压暗","vignetting, darkened corners","暗角, 四角压暗"),
("镜头眩光","Lens Flare","强光光晕光斑","lens flare, sun streaks","镜头眩光, 光斑"),
("变形宽银幕眩光","Anamorphic Flare","水平蓝色光条","anamorphic horizontal blue flare","变形宽银幕蓝色眩光"),
("星芒","Sunstar","小光圈放射星芒","sunstar starburst, small aperture","星芒, 放射"),
("光晕Halation","Halation","强光红色光晕","halation, red glow around highlights","红色光晕, halation")]:
    add("镜头与光学 / 光学缺陷与效果", zh, en, defs+"。", pen, pcn, "镜头;效果")

# ===== 相机与感光 / 画幅 =====
for zh,en,defs,pen,pcn in [
("全画幅","Full Frame","35mm、浅景深控制好","full frame 35mm sensor, shallow depth control, clean","全画幅 35mm, 纯净"),
("中画幅","Medium Format","超高分辨率细腻过渡","medium format, ultra high resolution, smooth gradation","中画幅, 超高分辨率"),
("APS-C画幅","APS-C","1.5x 裁切","APS-C crop sensor 1.5x","APS-C, 1.5倍裁切"),
("M4/3画幅","Micro Four Thirds","2x 裁切轻便","micro four thirds, 2x crop, compact","M4/3, 2倍裁切"),
("大画幅","Large Format","4x5 极致细节","large format 4x5 view camera, extreme detail","大画幅 4x5, 极致细节"),
("1英寸传感器","1-inch Sensor","便携相机画幅","1-inch sensor compact camera","1英寸传感器")]:
    add("相机与感光 / 画幅", zh, en, defs+"。", pen, pcn, "相机;画幅")

# ===== 相机与感光 / 相机类型 =====
for zh,en,defs,pen,pcn in [
("单反相机","DSLR","光学取景单反","DSLR camera","单反相机"),
("无反相机","Mirrorless","电子取景无反","mirrorless camera","无反相机"),
("旁轴相机","Rangefinder","徕卡式人文质感","rangefinder camera, Leica look, documentary feel","旁轴相机, 徕卡质感"),
("胶片相机","Film Camera","模拟胶片质感","analog film camera look","胶片相机"),
("拍立得","Instant Polaroid","白边柔和褪色","instant polaroid, white border, faded soft tones","拍立得, 白边褪色"),
("针孔相机","Pinhole","柔焦梦幻无限景深","pinhole camera, soft dreamy, infinite focus","针孔相机, 柔焦"),
("CCD数码","CCD Digital","复古数码色彩","early CCD digital, vintage digital color","CCD 复古数码色"),
("运动相机","Action Cam","超广鱼眼第一人称","action camera, ultra-wide fisheye POV","运动相机, 鱼眼第一视角")]:
    add("相机与感光 / 相机类型", zh, en, defs+"。", pen, pcn, "相机;类型")

# ===== 布光与用光 / 自然光 =====
for zh,en,defs,pen,pcn in [
("黄金时刻","Golden Hour","暖阳柔光长影","golden hour, warm soft directional sunlight, long shadows","黄金时刻, 暖阳柔光长影"),
("蓝调时刻","Blue Hour","冷色暮光均匀","blue hour, cool twilight even light","蓝调时刻, 冷色暮光"),
("正午硬光","Harsh Midday","硬阴影高反差","harsh midday sun, hard shadows, high contrast","正午硬光, 硬阴影"),
("阴天柔光","Overcast Soft","散射均匀低反差","overcast soft diffused even light","阴天柔光, 散射"),
("窗光","Window Light","柔和方向光人像","window light, soft directional portrait","窗光, 柔和方向光"),
("逆光","Backlight","轮廓发光","backlight, glowing rim light","逆光, 轮廓光"),
("侧逆光","Rim/Edge Light","边缘镶光","rim backlight, edge glow","侧逆光, 边缘镶光"),
("侧光","Side Light","质感立体","side light, texture and dimension","侧光, 质感立体"),
("顶光","Top Light","正上方光","top overhead light","顶光"),
("丁达尔光","God Rays","体积光束、晨雾林间","god rays, volumetric light beams, misty","丁达尔光, 体积光束"),
("斑驳光影","Dappled Light","树影斑驳","dappled light, leaf shadows","斑驳树影光")]:
    add("布光与用光 / 自然光", zh, en, defs+"。", pen, pcn, "布光;自然光")

# ===== 布光与用光 / 影室布光 =====
for zh,en,defs,pen,pcn in [
("伦勃朗光","Rembrandt","颊部三角光戏剧人像","Rembrandt lighting, triangle of light on cheek, dramatic","伦勃朗光, 颊部三角光"),
("蝴蝶光","Butterfly/Paramount","鼻下蝶影魅力人像","butterfly paramount lighting, glamour, under-nose shadow","蝴蝶光, 鼻下蝶影"),
("环形光","Loop","鼻侧小阴影万用","loop lighting, small nose shadow, versatile","环形光, 鼻侧小阴影"),
("分割光","Split","半面光强戏剧","split lighting, half face lit, dramatic","分割光, 半面光"),
("三点布光","Three-Point","主辅轮廓","three-point lighting, key fill rim","三点布光"),
("蛤蜊光","Clamshell","上下夹光美妆","clamshell beauty lighting, even glow","蛤蜊光, 美妆"),
("宽位光","Broad Lighting","近侧受光显脸宽","broad lighting, near side lit","宽位光"),
("窄位光","Short Lighting","远侧受光显脸瘦","short lighting, far side lit, slimming","窄位光, 显瘦"),
("高调布光","High-Key Studio","全亮白少阴影","high-key studio, bright white minimal shadow","高调布光"),
("低调布光","Low-Key Studio","单灯深阴影","low-key studio, single source deep shadows","低调布光")]:
    add("布光与用光 / 影室布光", zh, en, defs+"。", pen, pcn, "布光;影室;人像")

# ===== 布光与用光 / 光质与修饰器 =====
for zh,en,defs,pen,pcn in [
("柔光","Soft Light","大光源柔和过渡","soft light, large source, gentle gradation","柔光, 柔和过渡"),
("硬光","Hard Light","小光源锐利阴影","hard light, small source, crisp shadows","硬光, 锐利阴影"),
("柔光箱","Softbox","柔和方向光","softbox soft directional light","柔光箱"),
("八角柔光箱","Octabox","圆形眼神光","octabox, round catchlight","八角柔光箱, 圆形眼神光"),
("束光筒","Snoot","聚焦光束","snoot, focused spotlight beam","束光筒, 聚光束"),
("雷达罩","Beauty Dish","半硬美妆光","beauty dish, semi-hard glamour light","雷达罩, 美妆光"),
("反光板补光","Reflector Fill","柔化阴影","reflector fill, soften shadows","反光板补光"),
("网格控光","Grid","收束防溢光","grid, controlled directional beam","网格控光"),
("霓虹灯光","Neon","彩色辉光赛博朋克","neon lighting, colorful glow cyberpunk","霓虹灯光, 赛博朋克"),
("实用光源","Practical Lights","画面内灯具","practical lights in frame","画面内实用光源")]:
    add("布光与用光 / 光质与修饰器", zh, en, defs+"。", pen, pcn, "布光;光质")

# ===== 构图与取景 / 构图法则 =====
for zh,en,defs,pen,pcn in [
("三分法","Rule of Thirds","三分线交点","rule of thirds composition","三分法构图"),
("中心构图","Centered","居中稳定对称","centered symmetrical composition","中心构图"),
("对角线构图","Diagonal","动感张力","diagonal composition, dynamic","对角线构图"),
("引导线","Leading Lines","线条引导视线","leading lines guiding the eye","引导线"),
("框架构图","Framing","前景框主体","framing, natural frame around subject","框架式构图"),
("黄金比例","Golden Ratio","螺旋黄金分割","golden ratio spiral composition","黄金比例构图"),
("负空间","Negative Space","留白极简","negative space, minimalist","负空间, 留白"),
("对称构图","Symmetry","镜像对称","symmetry, mirrored composition","对称构图"),
("三角构图","Triangular","稳定三角","triangular composition, stable","三角构图"),
("重复韵律","Pattern Rhythm","重复图案韵律","repeating pattern, rhythm","重复图案韵律"),
("框中框","Frame in Frame","层层框架","frame within a frame","框中框")]:
    add("构图与取景 / 构图法则", zh, en, defs+"。", pen, pcn, "构图;法则")

# ===== 构图与取景 / 视角机位 =====
for zh,en,defs,pen,pcn in [
("平视","Eye-Level","与人眼等高的平直自然视角","eye-level view","平视"),
("俯拍","High Angle","从上向下俯视、弱化主体","high angle looking down","俯拍"),
("仰拍","Low Angle","向上气势","low angle looking up, powerful","仰拍, 气势"),
("鸟瞰","Bird's Eye","顶视俯瞰","bird's eye top-down view","鸟瞰俯视"),
("蠕虫视角","Worm's Eye","贴地仰视","worm's eye ground-level up view","蠕虫贴地视角"),
("荷兰角","Dutch Angle","倾斜地平线不安","dutch angle, tilted horizon","荷兰角倾斜"),
("第一人称视角","POV","主观第一人称","first person POV subjective","第一人称视角"),
("过肩视角","Over-the-Shoulder","过肩","over-the-shoulder view","过肩视角")]:
    add("构图与取景 / 视角机位", zh, en, defs+"。", pen, pcn, "构图;视角")

# ===== 构图与取景 / 景别 =====
for zh,en,defs,pen,pcn in [
("大特写","Extreme Close-Up","局部极致放大","extreme close-up macro detail","大特写"),
("特写","Close-Up","聚焦局部","close-up shot","特写"),
("近景","Medium Close-Up","胸部以上","medium close-up, chest up","近景"),
("中景","Medium Shot","腰部以上","medium shot, waist up","中景"),
("全身","Full Shot","完整人物","full body shot","全身"),
("远景","Wide Shot","交代环境","wide establishing shot","远景"),
("大远景","Extreme Wide","宏大全景","extreme wide landscape shot","大远景")]:
    add("构图与取景 / 景别", zh, en, defs+"。", pen, pcn, "构图;景别")

# ===== 拍摄题材 =====
GEN=[("人物","人像","Portrait","表情情绪人像","portrait photography, expressive"),
("人物","环境人像","Environmental Portrait","结合环境","environmental portrait in context"),
("人物","时尚大片","Fashion Editorial","杂志造型","fashion editorial, stylized"),
("人物","婚纱","Wedding","婚礼纪实","wedding photography"),
("风景","风光","Landscape","壮阔自然","landscape, sweeping vista"),
("风景","夜景","Night Cityscape","城市灯光","night city photography, lights"),
("风景","天文银河","Astrophotography","银河星空","astrophotography, milky way"),
("风景","海景","Seascape","海岸长曝","seascape, long exposure ocean"),
("纪实","街拍","Street","决定性瞬间","street photography, candid decisive moment"),
("纪实","纪实","Documentary","真实记录","documentary photography"),
("纪实","新闻","Photojournalism","记录事件现场的新闻摄影","photojournalism, news"),
("自然","微距","Macro","极致近摄","macro photography, extreme close-up"),
("自然","野生动物","Wildlife","长焦动物","wildlife photography, telephoto"),
("自然","生态","Nature","花鸟自然","nature flora fauna photography"),
("商业","产品","Product","影室静物","product photography, studio"),
("商业","美食","Food","诱人质感","food photography, appetizing"),
("商业","珠宝","Jewelry","高反光微距","jewelry macro, reflective"),
("空间","建筑","Architecture","线条几何","architecture photography, geometry"),
("空间","室内","Interior","空间陈设","interior photography"),
("空间","航拍","Aerial Drone","无人机高空","aerial drone photography")]
for top,zh,en,cn_d,pen in GEN:
    add("拍摄题材 / "+top, zh, en, cn_d+"。", pen+" photography" if not pen.endswith("photography") and "photography" not in pen else pen, zh+", "+cn_d, "题材;"+top)

# ===== 胶片与质感 =====
for zh,en,defs,pen,pcn in [
("柯达Portra","Kodak Portra","暖调自然肤色细颗粒","Kodak Portra film, warm natural skin tones, fine grain","柯达Portra, 暖调自然肤色"),
("CineStill 800T","CineStill 800T","钨调冷色红色光晕","CineStill 800T, tungsten cool tones, red halation","CineStill 800T, 钨调红光晕"),
("富士经典铬","Fuji Classic Chrome","青绿低饱和纪实","Fujifilm Classic Chrome, muted green documentary","富士经典铬, 青绿低饱和"),
("富士Velvia","Fuji Velvia","高饱和风光反转片","Fuji Velvia, high saturation landscape slide","富士Velvia, 高饱和"),
("柯达Ektar","Kodak Ektar","高饱和细腻","Kodak Ektar, vivid saturated fine grain","柯达Ektar, 高饱和细腻"),
("黑白胶片","B&W Film","Ilford颗粒单色","black and white film, Ilford grainy monochrome","黑白胶片, 颗粒单色"),
("过期胶片","Expired Film","偏色漏光复古","expired film, color shift light leaks vintage","过期胶片, 偏色漏光"),
("胶片颗粒","Film Grain","模拟颗粒质感","film grain texture, analog","胶片颗粒"),
("漏光","Light Leaks","暖色漏光条纹","light leaks, warm streaks","漏光, 暖色条纹"),
("黑白单色","Monochrome","去色影调","monochrome black and white","黑白单色"),
("褪色复古","Faded Vintage","低饱和褪色","faded vintage, low saturation retro","褪色复古")]:
    add("胶片与质感 / "+("胶片类型" if en in("Kodak Portra","CineStill 800T","Fuji Classic Chrome","Fuji Velvia","Kodak Ektar","B&W Film","Expired Film") else "质感效果"), zh, en, defs+"。", pen, pcn, "胶片;质感")

# 合并模式：保留其它卷，只重写本卷，卷内重编号。
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!="V01"]
for i,r in enumerate(rows,1): r["term_uid"]=f"V01_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"V01 穷举: {len(rows)} | total: {len(allrows)}")
