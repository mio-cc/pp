# -*- coding: utf-8 -*-
"""生成 V01 摄影体系 正式术语数据（互联网研究 + 整理）。
每条术语：原子化、路径分类(任意深度)、中英双语提示词与术语对应、无负向。"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "raw" / "terms_seed.csv"
FIELDS = ["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short",
          "definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt",
          "positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with",
          "tags","source_refs","status","version"]
# (路径, 中文名, 英文名, 一句话定义, 正向英文, 正向中文, 标签)
D = [
# ===== 曝光控制 / 光圈 =====
("曝光控制 / 光圈","f/1.4 极浅景深","f/1.4 Aperture","最大光圈之一，极浅景深、强烈背景虚化。","f/1.4 aperture, extremely shallow depth of field, creamy bokeh","f/1.4 大光圈, 极浅景深, 奶油散景","曝光;光圈;景深"),
("曝光控制 / 光圈","f/2.8 浅景深","f/2.8 Aperture","常用大光圈，浅景深、主体分离。","f/2.8 aperture, shallow depth of field, subject isolation","f/2.8 光圈, 浅景深, 主体分离","曝光;光圈"),
("曝光控制 / 光圈","f/8 适中景深","f/8 Aperture","风光与日常常用，画质锐利、景深适中。","f/8 aperture, balanced depth of field, sharp detail","f/8 光圈, 适中景深, 锐利","曝光;光圈"),
("曝光控制 / 光圈","f/16 大景深","f/16 Aperture","小光圈，大景深、前后皆清晰。","f/16 aperture, deep depth of field, everything in focus","f/16 小光圈, 大景深, 全景清晰","曝光;光圈;风光"),
# ===== 曝光控制 / 快门 =====
("曝光控制 / 快门","高速快门凝固","Fast Shutter Freeze","1/2000s 凝固高速运动，画面清晰无拖影。","fast shutter speed 1/2000s, frozen motion, sharp action","高速快门 1/2000秒, 凝固动作, 清晰","曝光;快门;运动"),
("曝光控制 / 快门","慢门动态模糊","Slow Shutter Motion Blur","慢速快门记录运动轨迹，产生动感拖影。","slow shutter speed, motion blur, dynamic streaks","慢速快门, 动态模糊, 拖影","曝光;快门"),
("曝光控制 / 快门","长曝光丝绢流水","Long Exposure Silky Water","数秒长曝光，水面雾化成丝绢质感。","long exposure, silky smooth water, misty motion","长曝光, 丝绢流水, 雾化","曝光;快门;风光"),
("曝光控制 / 快门","长曝光车流光轨","Light Trails","夜间长曝光记录车灯轨迹成光带。","long exposure light trails, car light streaks at night","长曝光车流光轨, 夜景光带","曝光;快门;夜景"),
("曝光控制 / 快门","星轨","Star Trails","超长曝光记录星空旋转轨迹。","star trails, ultra long exposure rotating night sky","星轨, 超长曝光星空","曝光;快门;天文"),
("曝光控制 / 快门","追焦","Panning","跟随移动主体平移相机，主体清晰背景动感模糊。","panning shot, sharp subject with motion-blurred background","追焦, 主体清晰背景拖影","曝光;快门;运动"),
# ===== 曝光控制 / 感光度 =====
("曝光控制 / 感光度","低ISO纯净","Low ISO Clean","ISO100 低感光，画面纯净无噪点。","low ISO 100, clean image, no noise, smooth","低 ISO 100, 纯净无噪点","曝光;ISO;画质"),
("曝光控制 / 感光度","高ISO噪点","High ISO Noise","高感光弱光拍摄，伴随明显噪点颗粒。","high ISO, visible digital noise, grainy low light","高 ISO, 噪点, 弱光颗粒","曝光;ISO;弱光"),
# ===== 曝光控制 / 测光与影调 =====
("曝光控制 / 测光与影调","高调曝光","High Key","整体明亮、低对比、通透干净。","high key exposure, bright, low contrast, airy clean","高调, 明亮通透, 低对比","曝光;影调"),
("曝光控制 / 测光与影调","低调曝光","Low Key","整体暗调、高对比、戏剧性阴影。","low key exposure, dark, dramatic shadows, high contrast","低调, 暗调, 戏剧阴影","曝光;影调"),
("曝光控制 / 测光与影调","剪影","Silhouette","逆光使主体成黑色剪影，背景明亮。","silhouette, backlit dark subject against bright background","剪影, 逆光黑主体亮背景","曝光;影调;逆光"),
("曝光控制 / 测光与影调","包围曝光HDR","HDR Bracketing","多张不同曝光合成，保留高光与阴影细节。","HDR bracketed exposure, high dynamic range detail","包围曝光 HDR, 高动态范围","曝光;HDR"),
# ===== 镜头与光学 / 焦距 =====
("镜头与光学 / 焦距","14mm超广角","14mm Ultra-Wide","超广视角，开阔空间、夸张透视。","14mm ultra-wide angle lens, expansive exaggerated perspective","14mm 超广角, 开阔, 夸张透视","镜头;焦距;广角"),
("镜头与光学 / 焦距","24mm广角","24mm Wide","广角交代环境，画面信息丰富。","24mm wide angle lens, environmental, broad scene","24mm 广角, 环境交代","镜头;焦距;广角"),
("镜头与光学 / 焦距","35mm人文","35mm Lens","接近视野的人文焦段，自然不夸张。","35mm lens, documentary street, natural wide perspective","35mm 人文镜头, 自然视角","镜头;焦距;人文"),
("镜头与光学 / 焦距","50mm标准","50mm Standard","接近人眼透视的标准镜头。","50mm standard lens, natural perspective like human eye","50mm 标准镜头, 接近人眼","镜头;焦距;标准"),
("镜头与光学 / 焦距","85mm人像","85mm Portrait","经典人像焦段，压缩讨喜、虚化柔美。","85mm portrait lens, flattering compression, creamy bokeh","85mm 人像镜头, 压缩讨喜, 奶油散景","镜头;焦距;人像"),
("镜头与光学 / 焦距","135mm长焦人像","135mm Telephoto","中长焦人像，强背景压缩、主体突出。","135mm telephoto portrait, strong background compression","135mm 长焦人像, 强压缩","镜头;焦距;人像"),
("镜头与光学 / 焦距","200mm长焦","200mm Telephoto","长焦透视压缩，拉近远处主体。","200mm telephoto lens, compressed perspective","200mm 长焦, 透视压缩","镜头;焦距;长焦"),
("镜头与光学 / 焦距","400mm超长焦","400mm Super-Tele","超长焦打鸟与运动，极致压缩。","400mm super telephoto, wildlife, extreme compression","400mm 超长焦, 打鸟, 极致压缩","镜头;焦距;长焦"),
# ===== 镜头与光学 / 镜头类型 =====
("镜头与光学 / 镜头类型","定焦镜头","Prime Lens","固定焦距，大光圈、画质锐利。","prime lens, fixed focal length, sharp wide aperture","定焦镜头, 大光圈锐利","镜头;类型"),
("镜头与光学 / 镜头类型","变焦镜头","Zoom Lens","可变焦距，构图灵活。","zoom lens, variable focal length, flexible framing","变焦镜头, 灵活构图","镜头;类型"),
("镜头与光学 / 镜头类型","微距镜头","Macro Lens","1:1 放大，极致近摄细节。","macro lens, 1:1 reproduction, extreme close-up detail","微距镜头, 1:1 放大, 极致细节","镜头;类型;微距"),
("镜头与光学 / 镜头类型","鱼眼镜头","Fisheye Lens","约180度视角，强烈桶形畸变。","fisheye lens, 180 degree view, extreme barrel distortion","鱼眼镜头, 180度, 桶形畸变","镜头;类型;畸变"),
("镜头与光学 / 镜头类型","移轴镜头","Tilt-Shift Lens","透视校正与微缩模型效果。","tilt-shift lens, miniature effect, perspective control","移轴镜头, 微缩效果, 透视校正","镜头;类型"),
# ===== 镜头与光学 / 景深与虚化 =====
("镜头与光学 / 景深与虚化","浅景深","Shallow DoF","清晰范围窄，背景虚化、主体分离。","shallow depth of field, blurred background, subject isolation","浅景深, 背景虚化, 主体分离","镜头;景深"),
("镜头与光学 / 景深与虚化","深景深","Deep DoF","清晰范围大，前后景皆清晰。","deep depth of field, sharp from foreground to background","深景深, 前后全清","镜头;景深"),
("镜头与光学 / 景深与虚化","奶油散景","Creamy Bokeh","焦外柔滑如奶油，过渡自然。","creamy smooth bokeh, soft out-of-focus background","奶油般散景, 柔滑焦外","镜头;散景"),
("镜头与光学 / 景深与虚化","旋焦散景","Swirly Bokeh","老镜旋转状焦外，复古氛围。","swirly bokeh, vintage Helios lens look","旋焦散景, 复古老镜","镜头;散景"),
("镜头与光学 / 景深与虚化","焦外光斑","Bokeh Balls","焦外高光化为圆形光斑。","bokeh balls, circular out-of-focus highlights","焦外光斑, 圆形高光","镜头;散景"),
# ===== 镜头与光学 / 光学缺陷与效果 =====
("镜头与光学 / 光学缺陷与效果","桶形畸变","Barrel Distortion","广角常见，画面中心向外鼓起。","barrel distortion, wide-angle lens bulging center","桶形畸变, 广角中心鼓起","镜头;畸变"),
("镜头与光学 / 光学缺陷与效果","枕形畸变","Pincushion Distortion","长焦常见，画面中心向内凹陷。","pincushion distortion, telephoto pinched center","枕形畸变, 长焦中心凹陷","镜头;畸变"),
("镜头与光学 / 光学缺陷与效果","色散紫边","Chromatic Aberration","高反差边缘出现紫绿色边。","chromatic aberration, purple green fringing","色散, 紫边","镜头;缺陷"),
("镜头与光学 / 光学缺陷与效果","暗角","Vignetting","画面四角变暗，聚焦中心。","vignetting, darkened corners","暗角, 四角压暗","镜头;效果"),
("镜头与光学 / 光学缺陷与效果","镜头眩光","Lens Flare","强光入镜产生光晕与光斑。","lens flare, sun streaks, anamorphic flare","镜头眩光, 光晕光斑","镜头;效果;逆光"),
("镜头与光学 / 光学缺陷与效果","星芒","Sunstar","小光圈下点光源呈放射星芒。","sunstar starburst from small aperture point light","星芒, 放射光芒","镜头;效果"),
# ===== 相机与感光 / 画幅 =====
("相机与感光 / 画幅","全画幅","Full Frame","35mm 画幅，浅景深控制好、画质纯净。","full frame 35mm sensor, shallow depth control, clean","全画幅 35mm, 浅景深, 纯净","相机;画幅"),
("相机与感光 / 画幅","中画幅","Medium Format","大于全画幅，超高分辨率、细腻过渡。","medium format, ultra high resolution, smooth tonal gradation","中画幅, 超高分辨率, 细腻过渡","相机;画幅"),
("相机与感光 / 画幅","APS-C画幅","APS-C","裁切画幅，约1.5x 等效系数。","APS-C crop sensor, 1.5x crop factor","APS-C 画幅, 1.5倍裁切","相机;画幅"),
("相机与感光 / 画幅","大画幅","Large Format","4x5 及以上，极致细节、可控透视。","large format 4x5 view camera, extreme detail","大画幅 4x5, 极致细节","相机;画幅"),
# ===== 相机与感光 / 相机类型 =====
("相机与感光 / 相机类型","旁轴相机","Rangefinder","徕卡式旁轴，纪实人文质感。","rangefinder camera, Leica look, documentary feel","旁轴相机, 徕卡, 人文质感","相机;类型"),
("相机与感光 / 相机类型","拍立得","Instant Polaroid","即影即有，白边、柔和褪色。","instant film polaroid, white border, soft faded tones","拍立得, 宝丽来白边, 柔和褪色","相机;类型;胶片"),
("相机与感光 / 相机类型","针孔相机","Pinhole","无镜头成像，柔焦梦幻、无限景深。","pinhole camera, soft dreamy, infinite depth of field","针孔相机, 柔焦梦幻","相机;类型"),
("相机与感光 / 相机类型","CCD数码","CCD Digital","早期 CCD 传感器，独特色彩与质感。","early CCD digital camera, distinctive color rendering","CCD 数码, 复古数码色","相机;类型"),
# ===== 布光与用光 / 自然光 =====
("布光与用光 / 自然光","黄金时刻","Golden Hour","日出日落暖调柔光，长投影。","golden hour, warm soft directional sunlight, long shadows","黄金时刻, 暖阳柔光, 长投影","布光;自然光"),
("布光与用光 / 自然光","蓝调时刻","Blue Hour","日落后冷调暮光，柔和均匀。","blue hour, cool twilight, soft even light","蓝调时刻, 冷色暮光","布光;自然光"),
("布光与用光 / 自然光","正午硬光","Harsh Midday","正午直射硬光，硬阴影、高反差。","harsh midday sun, hard shadows, high contrast","正午硬光, 硬阴影, 高反差","布光;自然光"),
("布光与用光 / 自然光","阴天柔光","Overcast Soft","阴天散射柔光，低反差均匀。","overcast soft diffused light, low contrast, even","阴天柔光, 散射均匀","布光;自然光"),
("布光与用光 / 自然光","窗光","Window Light","窗户侧入柔和方向光，经典人像。","window light, soft directional portrait light","窗光, 柔和方向光","布光;自然光;人像"),
("布光与用光 / 自然光","逆光","Backlight","光源在主体后方，轮廓发光。","backlight, glowing rim light, lens flare","逆光, 轮廓光, 发光边缘","布光;自然光"),
("布光与用光 / 自然光","侧光","Side Light","侧向光，强化质感与立体。","side light, emphasizing texture and dimension","侧光, 质感立体","布光;自然光"),
# ===== 布光与用光 / 影室布光 =====
("布光与用光 / 影室布光","伦勃朗光","Rembrandt Lighting","暗侧颊部出现倒三角光，戏剧人像。","Rembrandt lighting, triangle of light on cheek, dramatic","伦勃朗光, 颊部三角光, 戏剧","布光;影室;人像"),
("布光与用光 / 影室布光","蝴蝶光","Butterfly Lighting","正上方主光，鼻下蝴蝶状阴影，魅力人像。","butterfly paramount lighting, glamour, under-nose shadow","蝴蝶光, 魅力人像, 鼻下蝶影","布光;影室;人像"),
("布光与用光 / 影室布光","环形光","Loop Lighting","主光约45度，鼻侧小环形阴影，万用。","loop lighting, small nose shadow, versatile portrait","环形光, 鼻侧小阴影, 万用","布光;影室;人像"),
("布光与用光 / 影室布光","分割光","Split Lighting","光只照半边脸，强戏剧对比。","split lighting, half face lit, dramatic contrast","分割光, 半面光, 戏剧","布光;影室;人像"),
("布光与用光 / 影室布光","三点布光","Three-Point Lighting","主光+辅光+轮廓光的标准布光。","three-point lighting, key fill and rim light","三点布光, 主辅轮廓","布光;影室"),
("布光与用光 / 影室布光","蛤蜊光","Clamshell Lighting","上下夹光，均匀通透，美妆人像。","clamshell beauty lighting, key over fill, even glow","蛤蜊光, 美妆, 上下夹光","布光;影室;人像"),
# ===== 布光与用光 / 光质与修饰 =====
("布光与用光 / 光质与修饰","柔光","Soft Light","大光源，过渡柔和、阴影边缘模糊。","soft light, large source, gentle gradation soft shadows","柔光, 柔和过渡","布光;光质"),
("布光与用光 / 光质与修饰","硬光","Hard Light","小光源，边缘锐利、阴影分明。","hard light, small source, crisp defined shadows","硬光, 锐利阴影","布光;光质"),
("布光与用光 / 光质与修饰","霓虹灯光","Neon Lighting","彩色霓虹辉光，赛博朋克夜感。","neon lighting, colorful glow, cyberpunk night","霓虹灯光, 彩色辉光, 赛博朋克","布光;色彩;氛围"),
("布光与用光 / 光质与修饰","实用光源","Practical Lights","画面内可见灯具作为光源。","practical lights in frame, visible lamps glow","画面内实用光源, 灯具","布光;氛围"),
# ===== 构图与取景 / 构图法则 =====
("构图与取景 / 构图法则","三分法","Rule of Thirds","主体置于三分线交点，平衡耐看。","rule of thirds composition, subject on grid intersection","三分法构图, 三分线交点","构图;法则"),
("构图与取景 / 构图法则","中心构图","Centered Composition","主体居中，稳定庄重、对称感。","centered symmetrical composition, balanced","中心构图, 居中稳定","构图;法则"),
("构图与取景 / 构图法则","对角线构图","Diagonal Composition","沿对角线排布，富动感张力。","diagonal composition, dynamic tension","对角线构图, 动感","构图;法则"),
("构图与取景 / 构图法则","引导线","Leading Lines","线条引导视线指向主体。","leading lines guiding the eye to subject","引导线, 视线引导","构图;法则"),
("构图与取景 / 构图法则","框架构图","Framing","用前景元素框住主体。","framing composition, natural frame around subject","框架式构图, 前景框","构图;法则"),
("构图与取景 / 构图法则","负空间","Negative Space","大面积留白突出主体，极简。","negative space, minimalist, breathing room","负空间, 留白, 极简","构图;法则"),
("构图与取景 / 构图法则","对称构图","Symmetry","镜像对称，秩序与庄严。","symmetry, mirrored composition, order","对称构图, 镜像","构图;法则"),
# ===== 构图与取景 / 视角机位 =====
("构图与取景 / 视角机位","俯拍","High Angle","机位高于主体向下拍，弱化主体。","high angle shot looking down","俯拍, 高机位向下","构图;视角"),
("构图与取景 / 视角机位","仰拍","Low Angle","机位低于主体向上拍，强化气势。","low angle shot looking up, powerful imposing","仰拍, 低机位向上, 气势","构图;视角"),
("构图与取景 / 视角机位","鸟瞰","Bird's Eye","正上方俯视的鸟瞰视角。","bird's eye view, top-down aerial perspective","鸟瞰, 顶视俯瞰","构图;视角"),
("构图与取景 / 视角机位","荷兰角","Dutch Angle","倾斜地平线，制造不安与张力。","dutch angle, tilted horizon, unease tension","荷兰角, 倾斜地平线","构图;视角"),
("构图与取景 / 视角机位","第一人称视角","POV Shot","第一人称主观视角。","first person POV shot, subjective view","第一人称视角, 主观","构图;视角"),
# ===== 构图与取景 / 景别 =====
("构图与取景 / 景别","特写","Close-Up","聚焦局部细节的特写景别。","close-up shot, tight framing on detail","特写, 局部细节","构图;景别"),
("构图与取景 / 景别","中景","Medium Shot","腰部以上的中景。","medium shot, waist up framing","中景, 腰部以上","构图;景别"),
("构图与取景 / 景别","全身","Full Shot","容纳完整人物的全身景别。","full body shot, whole figure in frame","全身景别, 完整人物","构图;景别"),
("构图与取景 / 景别","远景","Wide Shot","交代环境的远景/全景。","wide establishing shot, environment context","远景, 环境交代","构图;景别"),
# ===== 拍摄题材 =====
("拍摄题材 / 人物","人像","Portrait","以人物神态情绪为核心的人像。","portrait photography, expressive subject","人像摄影","题材;人像"),
("拍摄题材 / 人物","环境人像","Environmental Portrait","结合环境交代身份的人像。","environmental portrait, subject in context","环境人像","题材;人像"),
("拍摄题材 / 人物","时尚大片","Fashion Editorial","时尚杂志风格的造型大片。","fashion editorial photography, stylized","时尚大片, 杂志风","题材;时尚"),
("拍摄题材 / 风景","风光","Landscape","壮阔自然景观的风光摄影。","landscape photography, sweeping vista","风光摄影, 壮阔","题材;风光"),
("拍摄题材 / 风景","夜景","Night Cityscape","城市夜景与灯光。","night photography, city lights glow","夜景摄影, 城市灯光","题材;夜景"),
("拍摄题材 / 风景","天文银河","Astrophotography","星空银河的天文摄影。","astrophotography, milky way starry sky","天文摄影, 银河星空","题材;天文"),
("拍摄题材 / 纪实","街拍","Street","街头抓拍的决定性瞬间。","street photography, candid decisive moment","街头摄影, 抓拍瞬间","题材;街拍"),
("拍摄题材 / 纪实","纪实","Documentary","真实记录的纪实摄影。","documentary photography, authentic","纪实摄影, 真实记录","题材;纪实"),
("拍摄题材 / 自然","微距","Macro","昆虫花卉的极致近摄。","macro photography, extreme close-up tiny subject","微距摄影, 极致近摄","题材;微距"),
("拍摄题材 / 自然","野生动物","Wildlife","长焦捕捉野生动物。","wildlife photography, telephoto animals","野生动物摄影, 长焦","题材;野生"),
("拍摄题材 / 商业","产品","Product","影室布光的产品摄影。","product photography, studio lit, clean","产品摄影, 影室布光","题材;商业"),
("拍摄题材 / 商业","美食","Food","诱人质感的美食摄影。","food photography, appetizing texture","美食摄影, 诱人质感","题材;商业"),
("拍摄题材 / 空间","建筑","Architecture","线条与几何的建筑摄影。","architecture photography, lines and geometry","建筑摄影, 线条几何","题材;建筑"),
("拍摄题材 / 空间","航拍","Aerial Drone","无人机高空航拍视角。","aerial drone photography, high altitude","航拍, 无人机高空","题材;航拍"),
# ===== 胶片与质感 / 胶片类型 =====
("胶片与质感 / 胶片类型","柯达Portra","Kodak Portra","暖调自然肤色、细颗粒、宽容度高。","Kodak Portra film, warm natural skin tones, fine grain","柯达 Portra, 暖调自然肤色, 细颗粒","胶片;质感"),
("胶片与质感 / 胶片类型","CineStill 800T","CineStill 800T","钨调冷色，强光处红色光晕，电影感。","CineStill 800T, tungsten cool tones, red halation glow","CineStill 800T, 钨调冷色, 红色光晕","胶片;质感;电影感"),
("胶片与质感 / 胶片类型","富士经典铬","Fuji Classic Chrome","偏青绿、低饱和的纪实胶片色。","Fujifilm Classic Chrome, muted green-leaning documentary","富士经典铬, 青绿低饱和","胶片;质感"),
("胶片与质感 / 胶片类型","黑白胶片","B&W Film","Ilford 风黑白颗粒单色。","black and white film, Ilford grainy monochrome","黑白胶片, 颗粒单色","胶片;质感;黑白"),
("胶片与质感 / 胶片类型","过期胶片","Expired Film","偏色、漏光的过期胶片复古感。","expired film, color shift, light leaks, vintage","过期胶片, 偏色漏光, 复古","胶片;质感"),
# ===== 胶片与质感 / 质感 =====
("胶片与质感 / 质感","胶片颗粒","Film Grain","细腻的胶片颗粒质感。","film grain texture, analog","胶片颗粒, 模拟质感","质感"),
("胶片与质感 / 质感","漏光","Light Leaks","暖色漏光条纹叠加。","light leaks, warm streaks overlay","漏光, 暖色条纹","质感"),
("胶片与质感 / 质感","黑白单色","Monochrome","去色的黑白单色影调。","monochrome black and white tones","黑白单色, 去色影调","质感;黑白"),
]
rows=[]
for i,(cat,zh,en,defs,pen,pcn,tags) in enumerate(D,1):
    rows.append({"term_uid":f"V01_T{i:04d}","zh_term":zh,"en_term":en,"aliases":"","volume_code":"V01",
        "category":cat,"definition_short":defs,"definition_long":"","visual_effect":"","prompt_usage":"",
        "positive_prompt":pen,"negative_prompt":"","positive_prompt_cn":pcn,"negative_prompt_cn":"",
        "use_cases":"","related_terms":"","confused_with":"","tags":tags,"source_refs":"互联网研究整理","status":"published","version":"V1.0"})
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
print(f"V01 generated: {len(rows)} terms")
