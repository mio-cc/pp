# -*- coding: utf-8 -*-
"""V08 Prompt工程学（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V08"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("提示词结构",[
("主体描述","Subject","描述画面对象核心内容的提示词部分","clear subject description","主体描述"),
("风格修饰","Style Modifier","限定画面视觉风格的修饰关键词","style modifier keyword","风格修饰"),
("媒介声明","Medium","声明创作媒介类型的提示词词","medium declaration material","媒介声明"),
("质量词","Quality Tags","提升生成画质的强化标签","quality tags boost","质量词"),
("构图描述","Composition","指导画面布局结构的提示词","composition cue layout","构图描述"),
("环境描述","Environment","描述场景背景与空间环境的词","environment setting background","环境描述"),
("光照描述","Lighting Cue","描述光线类型与效果的提示词","lighting description cue","光照描述"),
("镜头描述","Camera Cue","模拟摄影镜头机位参数的词","camera shot description","镜头描述"),
("情绪氛围词","Mood","传递画面情感氛围的提示词","mood atmosphere keyword","情绪氛围词"),
("语序优先级","Token Order","提示词中靠前的词权重更高","token order priority weight","语序优先级"),
("权重括号","Weight","用括号调整单个词权重的语法","(keyword:1.3) weighting syntax","权重括号"),
("分隔符","Separators","逗号等分隔提示词不同段落的标点","comma separators","分隔符"),
("模板公式","Template","主体+风格+质量+参数的固定公式","prompt formula template","模板公式"),
("正向语法","Emphasis Syntax","加强强调特定词的语法手段","emphasis syntax strengthen","正向语法"),
("BREAK分段","BREAK","将提示词硬分段隔离影响的标记","BREAK keyword section","BREAK分段")],"Prompt;结构")
block("视觉修饰符 / 质量词",[
("杰作","Masterpiece","最高质量等级的强力提升标签","masterpiece top quality","杰作"),
("最佳质量","Best Quality","整体品质最佳的通用提升词","best quality overall","最佳质量"),
("高质量","High Quality","画面精细度高于平均水平的标签","high quality above average","高质量"),
("超高细节","Highly Detailed","画面充满丰富微细节的描述","highly detailed intricate","超高细节"),
("精细细节","Intricate Details","局部纹理和结构精致的标签","intricate fine texture details","精细细节"),
("极致细节","Ultra Detailed","最大化细节密度的极端标签","ultra detailed maximum","极致细节"),
("8K超清","8K UHD","极高分辨率超清画质标签","8k ultra hd resolution","8K超清"),
("4K","4K","高分辨率清晰画质标签","4k high resolution","4K"),
("HDR高动态","HDR","高动态范围影调丰富的标签","hdr high dynamic range","HDR高动态"),
("锐利对焦","Sharp Focus","主体边缘清晰锐利的标签","sharp focus crisp edge","锐利对焦"),
("清晰","Crisp Clear","画面通透无模糊的标签","crisp clear artifact-free","清晰"),
("超写实","Ultra Realistic","超越照片般逼真的渲染标签","ultra realistic beyond photo","超写实"),
("照片级写实","Photorealistic","如同照片般真实的生成质量","photorealistic camera-like","照片级写实"),
("超真实","Hyperrealistic","极度精确到令人不安的逼真","hyperrealistic unsettling real","超真实"),
("电影感","Cinematic","宽银幕光影叙事感的画面风格","cinematic filmic atmosphere","电影感"),
("专业级","Professional","专业水准的作品质量标签","professional studio grade","专业级"),
("获奖级","Award Winning","顶级获奖作品质量的形容","award winning top tier","获奖级"),
("惊艳","Stunning","视觉冲击力极强的品质标签","stunning striking impact","惊艳"),
("震撼","Breathtaking","宏大震撼到屏息的画面效果","breathtaking grand awe","震撼"),
("精致","Exquisite","细节精良考究的高品质标签","exquisite refined crafted","精致"),
("完美构图","Perfect Composition","画面构图精确平衡的标签","perfect composition balanced","完美构图"),
("ArtStation热门","Trending ArtStation","ArtStation平台热门级质量","trending on artstation","ArtStation热门"),
("Behance精选","Featured Behance","Behance精选级品质标签","featured on behance","Behance精选"),
("Octane渲染","Octane Render","Octane引擎渲染的写实品质","octane render quality","Octane渲染"),
("虚幻引擎渲染","UE5 Render","虚幻引擎5渲染的电影级品质","unreal engine 5 render","虚幻引擎渲染"),
("光线追踪","Ray Tracing","使用光线追踪的物理光照品质","ray tracing lighting quality","光线追踪"),
("体积光","Volumetric Lighting","可见光束穿透雾气的大气效果","volumetric lighting god rays","体积光"),
("戏剧光","Dramatic Lighting","强烈明暗对比的戏剧化光效","dramatic lighting high contrast","戏剧光"),
("影棚光","Studio Lighting","专业影棚布光的人像级光效","studio lighting professional","影棚光"),
("柔光","Soft Lighting","柔和漫射低反差的均匀光效","soft lighting diffused gentle","柔光"),
("景深虚化","Depth of Field Bokeh","背景虚化前景清晰的景深效果","depth of field bokeh blur","景深虚化")],"Prompt;质量词")
block("视觉修饰符 / 风格媒介词",[
("概念艺术","Concept Art","前期概念设计阶段的插画风格","concept art design illustration","概念艺术"),
("数字绘画","Digital Painting","电脑数位板创作的绘画风格","digital painting tablet art","数字绘画"),
("油画风","Oil Painting Style","模拟油画笔触厚涂的古典画风","oil painting thick brush","油画风"),
("水彩风","Watercolor Style","模拟水彩晕染透明感的画风","watercolor wash transparent","水彩风"),
("3D渲染","3D Render","三维软件渲染出的立体画面","3d render cg modeled","3D渲染"),
("摄影写实","Photography","模拟真实照片质感的生成风格","photography realistic camera","摄影写实"),
("动漫风","Anime Style","日本动画风格的扁平渲染","anime style cel-shaded","动漫风"),
("漫画风","Manga Style","黑白线条网点纸的漫画风格","manga style halftone ink","漫画风"),
("卡通","Cartoon Style","简化的夸张卡通渲染风格","cartoon style simplified","卡通"),
("像素风","Pixel Art","复古像素点阵的低分辨率风格","pixel art retro 8bit","像素风"),
("矢量插画","Vector Illustration","色块平铺无渐变的矢量图形风格","vector illustration flat clean","矢量插画"),
("线稿","Line Art","纯线条勾勒、无填色的白描风格","line art clean outline","线稿"),
("素描","Sketch","铅笔排线条的速写素描风格","sketch pencil graphite","素描"),
("赛博朋克风","Cyberpunk Style","霓虹暗城高科技反乌托邦风格","cyberpunk neon dystopia","赛博朋克风"),
("蒸汽朋克风","Steampunk Style","齿轮蒸汽维多利亚复古科幻风格","steampunk brass gears victorian","蒸汽朋克风"),
("奇幻艺术","Fantasy Art","魔法史诗的幻想世界绘画风格","fantasy art magical epic","奇幻艺术"),
("科幻风","Sci-Fi Style","未来科技太空的科幻画面风格","sci-fi futuristic space","科幻风"),
("超现实风","Surreal Style","达利式梦境扭曲的超现实画面","surreal dreamlike bizarre","超现实风"),
("黏土风","Claymation Style","橡皮泥偶定格动画的质感风格","claymation stop-motion clay","黏土风"),
("低多边形","Low Poly","面数极少的几何简约3D风格","low poly geometric minimal","低多边形")],"Prompt;风格词")
block("艺术家与风格参考",[
("艺术家参考","Artist Reference","引用特定艺术家画风控制生成方向","in the style of artist","艺术家参考"),
("风格混合","Style Mixing","将多种艺术风格融合在同一画面","blend of multiple art styles","风格混合"),
("流派参考","Movement Reference","引用特定艺术流派的特征来限定风格","art movement reference","流派参考"),
("工作室风格","Studio Style","模仿特定动画工作室的标志性画风","pixar ghibli studio style","工作室风格")],"Prompt;参考")
block("负向与约束",[
("低分辨率(负)","Lowres","阻止生成低分辨率画面的负向词","lowres negative quality","低分辨率(负)"),
("最差质量(负)","Worst Quality","排斥最差品质输出的强力负向词","worst quality negative","最差质量(负)"),
("低质量(负)","Low Quality","避免低质模糊的通用负向词","low quality negative","低质量(负)"),
("普通质量(负)","Normal Quality","排除平庸品质的负向词","normal quality negative","普通质量(负)"),
("JPEG伪影(负)","JPEG Artifacts","阻止JPEG压缩产生的块状伪影","jpeg artifacts negative","JPEG伪影(负)"),
("解剖错误(负)","Bad Anatomy","排除人体结构比例错误的负向词","bad anatomy negative","解剖错误(负)"),
("手部畸形(负)","Bad Hands","防止生成畸形手部的常用负向词","bad hands negative","手部畸形(负)"),
("多指(负)","Extra Fingers","阻止生成多余手指的负向词","extra fingers negative","多指(负)"),
("缺指(负)","Missing Fingers","排除手指缺失的负向词","missing fingers negative","缺指(负)"),
("多肢(负)","Extra Limbs","防止生成多余肢体的负向词","extra limbs negative","多肢(负)"),
("畸形(负)","Deformed","排除身体变形扭曲的负向词","deformed disfigured negative","畸形(负)"),
("变异(负)","Mutated","防止生成异形变异画面的负向词","mutated abnormal negative","变异(负)"),
("丑陋(负)","Ugly","排斥不美观面部的负向词","ugly negative","丑陋(负)"),
("模糊(负)","Blurry","阻止画面模糊不清的负向词","blurry unfocused negative","模糊(负)"),
("失焦(负)","Out of Focus","排除焦点不实画面的负向词","out of focus negative","失焦(负)"),
("水印(负)","Watermark","防止生成水印标记的负向词","watermark negative","水印(负)"),
("签名(负)","Signature","排除画面中出现签名的负向词","signature negative","签名(负)"),
("文字(负)","Text","阻止画面中出现文字的负向词","text typography negative","文字(负)"),
("logo(负)","Logo","排除画面中出现商标logo的负向词","logo negative","logo(负)"),
("裁切不当(负)","Cropped","防止主体被不当裁切的负向词","cropped cut-off negative","裁切不当(负)"),
("重复(负)","Duplicate","阻止重复图案或多个主体的负向词","duplicate repetition negative","重复(负)"),
("噪点(负)","Grainy","排除画面噪点颗粒的负向词","grainy noisy negative","噪点(负)"),
("过曝(负)","Overexposed","防止亮部过曝死白的负向词","overexposed blown negative","过曝(负)"),
("欠曝(负)","Underexposed","排除暗部欠曝死黑的负向词","underexposed crushed negative","欠曝(负)")],"Prompt;负向")
block("参数与随机性",[
("随机种子","Seed","控制生成随机性的数值种子","seed reproducibility control","随机种子"),
("采样步数","Steps","扩散模型去噪迭代次数","sampling steps iterations","采样步数"),
("引导强度CFG","CFG Scale","提示词对生成的贴合程度","CFG scale guidance strength","引导强度CFG"),
("去噪强度","Denoising","图生图模式下重绘原图的程度","denoising strength img2img","去噪强度"),
("尺寸分辨率","Resolution","输出图像的宽高像素尺寸","output resolution size","尺寸分辨率"),
("宽高比","Aspect Ratio","图像宽与高的比例","aspect ratio width height","宽高比"),
("批量数量","Batch Count","单次生成多少张图像","batch count number","批量数量"),
("Clip跳过","Clip Skip","跳过CLIP末端层影响文本编码","clip skip CLIP layer","Clip跳过")],"Prompt;参数")
block("参数 / 采样器",[
("Euler","Euler Sampler","最常用的高速稳定采样器","euler sampler simple fast","Euler"),
("Euler a","Euler Ancestral","带祖先采样的随机变体Euler","euler ancestral stochastic","Euler a"),
("DPM++ 2M","DPM++ 2M Karras","高质量带余弦退火的扩散采样器","dpm++ 2m karras quality","DPM++ 2M"),
("DPM++ SDE","DPM++ SDE Karras","含随机微分方程的高质采样器","dpm++ sde karras stochastic","DPM++ SDE"),
("DDIM","DDIM Sampler","去噪扩散隐模型的确定性采样器","ddim deterministic sampler","DDIM"),
("UniPC","UniPC Sampler","一步预测校正的快速采样器","unipc fast predictor corrector","UniPC"),
("LMS","LMS Sampler","线性多步法的经典采样器","lms linear multistep","LMS"),
("Heun","Heun Sampler","Heun二阶方法的高精度采样器","heun second-order accurate","Heun")],"Prompt;采样器")
block("多模态与控制",[
("图生图","img2img","用参考图像引导生成新图像","img2img reference generation","图生图"),
("局部重绘","Inpaint","仅重绘遮罩区域保留其余画面","inpainting masked region edit","局部重绘"),
("扩图","Outpaint","向画面边缘外延扩展内容","outpainting extend beyond edge","扩图"),
("ControlNet姿态","OpenPose","用人体骨架控制人物姿态的ControlNet","controlnet openpose skeleton","姿态控制"),
("ControlNet深度","Depth","用深度图控制空间纵深的ControlNet","controlnet depth map spatial","深度控制"),
("ControlNet线稿","Lineart","用线稿图控制画面轮廓的ControlNet","controlnet lineart outline","线稿控制"),
("ControlNet边缘","Canny","用Canny边缘检测控制结构的ControlNet","controlnet canny edge detect","边缘控制"),
("ControlNet涂鸦","Scribble","用手绘涂鸦控制画面结构的ControlNet","controlnet scribble rough","涂鸦控制"),
("ControlNet法线","Normal","用法线贴图控制表面起伏的ControlNet","controlnet normal map surface","法线控制"),
("ControlNet分割","Segmentation","用语义分割控制区域归属的ControlNet","controlnet segmentation semantic","分割控制"),
("参考图风格迁移","Style Transfer","将参考图风格迁移到生成结果","style transfer reference","风格迁移"),
("区域提示","Regional Prompt","将不同提示词分配到画面不同区域","regional prompting zone","区域提示"),
("LoRA触发词","LoRA Trigger","激活特定LoRA微调模型的触发词","LoRA trigger word activation","LoRA触发词"),
("文本反演","Textual Inversion","用自定义embedding表达特定概念","textual inversion embedding","文本反演"),
("IP-Adapter","IP-Adapter","用图像替代文字引导生成的适配器","IP-adapter image prompt","IP-Adapter"),
("人脸迁移","Face Swap","将参考人脸替换到生成图中保持一致性","face swap identity transfer","人脸迁移")],"Prompt;多模态")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
