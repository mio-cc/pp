# -*- coding: utf-8 -*-
"""V08 Prompt工程学（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V08"; rows=[]
def simple(cat,items,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en,"",zh,"","","","",tags,"整理","published","V1.0"])))
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("提示词结构",[
("主体描述","Subject","核心主体","clear subject description","主体描述"),
("风格修饰","Style Modifier","风格限定","style modifier","风格修饰"),
("媒介声明","Medium","媒介类型","medium declaration","媒介声明"),
("质量词","Quality Tags","质量提升","quality tags","质量词"),
("构图描述","Composition","构图说明","composition cue","构图描述"),
("环境描述","Environment","场景背景","environment setting description","环境描述"),
("光照描述","Lighting Cue","光照说明","lighting description","光照描述"),
("镜头描述","Camera Cue","镜头机位","camera shot description","镜头描述"),
("情绪氛围词","Mood","情绪基调","mood atmosphere keyword","情绪氛围词"),
("语序优先级","Token Order","靠前权重高","token order priority","语序优先级"),
("权重括号","Weight","(词:1.3)加权","attention weighting","权重括号"),
("分隔符","Separators","逗号分隔","comma separators","分隔符"),
("模板公式","Template","主体+风格+质量+参数","prompt formula template","模板公式"),
("正向语法","Emphasis Syntax","加强强调","emphasis syntax","正向语法"),
("BREAK分段","BREAK","提示词分段","BREAK keyword separation","BREAK分段")],"Prompt;结构")
simple("视觉修饰符 / 质量词",[("杰作","masterpiece"),("最佳质量","best quality"),("高质量","high quality"),("超高细节","highly detailed"),("精细细节","intricate details"),("极致细节","ultra detailed"),("8K超清","8k uhd"),("4K","4k"),("HDR高动态","hdr"),("锐利对焦","sharp focus"),("清晰","crisp clear"),("超写实","ultra realistic"),("照片级写实","photorealistic"),("超真实","hyperrealistic"),("电影感","cinematic"),("专业级","professional"),("获奖级","award winning"),("惊艳","stunning"),("震撼","breathtaking"),("精致","exquisite"),("完美构图","perfect composition"),("ArtStation热门","trending on artstation"),("Behance精选","featured on behance"),("Octane渲染","octane render"),("虚幻引擎渲染","unreal engine 5 render"),("光线追踪","ray tracing"),("体积光","volumetric lighting"),("戏剧光","dramatic lighting"),("影棚光","studio lighting"),("柔光","soft lighting"),("景深虚化","depth of field bokeh")],"Prompt;质量词")
simple("视觉修饰符 / 风格媒介词",[("概念艺术","concept art"),("数字绘画","digital painting"),("油画风","oil painting"),("水彩风","watercolor"),("3D渲染","3d render"),("摄影写实","photography"),("动漫风","anime style"),("漫画风","manga style"),("卡通","cartoon style"),("像素风","pixel art"),("矢量插画","vector illustration"),("线稿","line art"),("素描","sketch"),("赛博朋克风","cyberpunk style"),("蒸汽朋克风","steampunk style"),("奇幻艺术","fantasy art"),("科幻风","sci-fi style"),("超现实风","surreal style"),("黏土风","claymation style"),("低多边形","low poly")],"Prompt;风格词")
block("艺术家与风格参考",[
("艺术家参考","Artist Reference","by/in the style of","in the style of [artist]","艺术家参考"),
("风格混合","Style Mixing","多风格融合","blend of art styles","风格混合"),
("流派参考","Movement Reference","流派引用","art movement reference","流派参考"),
("工作室风格","Studio Style","如皮克斯/吉卜力","pixar ghibli studio style","工作室风格")],"Prompt;参考")
simple("负向与约束",[("低分辨率(负)","lowres"),("最差质量(负)","worst quality"),("低质量(负)","low quality"),("普通质量(负)","normal quality"),("JPEG伪影(负)","jpeg artifacts"),("解剖错误(负)","bad anatomy"),("手部畸形(负)","bad hands"),("多指(负)","extra fingers"),("缺指(负)","missing fingers"),("多肢(负)","extra limbs"),("畸形(负)","deformed disfigured"),("变异(负)","mutated"),("丑陋(负)","ugly"),("模糊(负)","blurry"),("失焦(负)","out of focus"),("水印(负)","watermark"),("签名(负)","signature"),("文字(负)","text"),("logo(负)","logo"),("裁切不当(负)","cropped"),("重复(负)","duplicate"),("噪点(负)","grainy noisy"),("过曝(负)","overexposed"),("欠曝(负)","underexposed")],"Prompt;负向")
block("参数与随机性",[
("随机种子","Seed","复现控制","seed reproducibility","随机种子"),
("采样步数","Steps","迭代步数","sampling steps","采样步数"),
("引导强度CFG","CFG Scale","贴合提示度","CFG scale guidance","引导强度CFG"),
("去噪强度","Denoising","图生图重绘度","denoising strength","去噪强度"),
("尺寸分辨率","Resolution","出图尺寸","output resolution","尺寸分辨率"),
("宽高比","Aspect Ratio","画面比例","aspect ratio","宽高比"),
("批量数量","Batch Count","批量出图","batch count","批量数量"),
("Clip跳过","Clip Skip","CLIP层跳过","clip skip","Clip跳过")],"Prompt;参数")
simple("参数 / 采样器",[("Euler","euler sampler"),("Euler a","euler ancestral sampler"),("DPM++ 2M","dpm++ 2m karras"),("DPM++ SDE","dpm++ sde karras"),("DDIM","ddim sampler"),("UniPC","unipc sampler"),("LMS","lms sampler"),("Heun","heun sampler")],"Prompt;采样器")
block("多模态与控制",[
("图生图","img2img","参考图生成","img2img","图生图"),
("局部重绘","Inpaint","遮罩重绘","inpainting","局部重绘"),
("扩图","Outpaint","画面外扩","outpainting","扩图"),
("ControlNet姿态","OpenPose","骨架姿态","controlnet openpose","姿态控制"),
("ControlNet深度","Depth","深度图","controlnet depth","深度控制"),
("ControlNet线稿","Lineart","线稿","controlnet lineart","线稿控制"),
("ControlNet边缘","Canny","边缘检测","controlnet canny","边缘控制"),
("ControlNet涂鸦","Scribble","涂鸦控制","controlnet scribble","涂鸦控制"),
("ControlNet法线","Normal","法线控制","controlnet normal map","法线控制"),
("ControlNet分割","Segmentation","语义分割","controlnet segmentation","分割控制"),
("参考图风格迁移","Style Transfer","风格迁移","style transfer reference","风格迁移"),
("区域提示","Regional Prompt","分区控制","regional prompting","区域提示"),
("LoRA触发词","LoRA Trigger","调用微调","LoRA trigger word","LoRA触发词"),
("文本反演","Textual Inversion","embedding","textual inversion embedding","文本反演"),
("IP-Adapter","IP-Adapter","图像提示","IP-adapter image prompt","IP-Adapter"),
("人脸迁移","Face Swap","换脸保ID","face swap identity","人脸迁移")],"Prompt;多模态")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
