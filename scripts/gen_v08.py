# -*- coding: utf-8 -*-
"""V08 Prompt工程学（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V08"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("提示词结构",[
("主体描述","Subject","核心主体内容","clear subject description","主体描述"),
("风格修饰","Style Modifier","风格限定","style modifier keywords","风格修饰"),
("媒介声明","Medium","媒介类型声明","medium declaration, photo painting render","媒介声明"),
("质量词","Quality Tags","质量提升词","quality boosting tags","质量词"),
("构图描述","Composition Cue","构图说明","composition description in prompt","构图描述"),
("语序优先级","Token Order","靠前权重高","token order priority weighting","语序优先级"),
("权重括号","Weight Emphasis","(词:1.3)加权","attention weighting (token:1.3)","权重括号"),
("分隔符","Separators","逗号分隔标签","comma separated tags","分隔符"),
("模板公式","Prompt Template","主体+风格+质量+参数","prompt formula template","模板公式")],"Prompt;结构")
block("视觉修饰符 / 质量词",[
("杰作","masterpiece","顶级质量","masterpiece","杰作"),
("最佳质量","best quality","最高质量","best quality","最佳质量"),
("超高细节","highly detailed","丰富细节","highly detailed, intricate detail","超高细节"),
("8K超清","8k uhd","超高分辨率","8k uhd, ultra high resolution","8K超清"),
("锐利对焦","sharp focus","清晰锐利","sharp focus","锐利对焦"),
("超写实","ultra realistic","极致写实","ultra realistic, hyperrealistic","超写实"),
("电影感","cinematic","电影质感","cinematic, cinematic lighting","电影感"),
("获奖摄影","award winning","获奖级","award winning photography","获奖级"),
("专业打光","professional lighting","专业布光","professional lighting","专业打光")],"Prompt;质量词")
block("视觉修饰符 / 风格媒介词",[
("概念艺术","concept art","概念设定风","concept art","概念艺术"),
("数字绘画","digital painting","数绘风","digital painting","数字绘画"),
("3D渲染","3d render","三维渲染","3d render, octane","3D渲染"),
("摄影写实","photography","照片风","photography, photo realistic","摄影写实"),
("水彩插画","watercolor illustration","水彩风","watercolor illustration","水彩插画"),
("动漫风","anime style","二次元","anime style, manga","动漫风"),
("像素风","pixel art","复古像素","pixel art","像素风"),
("ArtStation热门","trending on artstation","平台热门风","trending on artstation","ArtStation热门"),
("虚幻引擎","unreal engine","UE渲染风","unreal engine 5 render","虚幻引擎风")],"Prompt;风格词")
block("艺术家与风格参考",[
("艺术家参考","Artist Reference","by/in the style of","in the style of [artist]","艺术家参考"),
("风格混合","Style Mixing","多风格融合","blend of styles","风格混合"),
("流派参考","Movement Reference","艺术流派引用","art movement reference","流派参考")],"Prompt;参考")
block("负向与约束",[
("负向提示词","Negative Prompt","排除不想要的","negative prompt exclusion","负向提示词"),
("低质量负向","lowres bad quality","排除低质","(neg) lowres, low quality, jpeg artifacts","低质量负向"),
("解剖错误负向","bad anatomy","排除畸形","(neg) bad anatomy, extra fingers, deformed","解剖错误负向"),
("水印负向","watermark text","排除水印文字","(neg) watermark, signature, text","水印负向"),
("模糊负向","blurry","排除模糊","(neg) blurry, out of focus","模糊负向")],"Prompt;负向")
block("参数与随机性",[
("随机种子","Seed","复现控制","seed for reproducibility","随机种子"),
("采样步数","Steps","迭代步数","sampling steps","采样步数"),
("引导强度CFG","CFG Scale","贴合提示强度","CFG scale guidance","引导强度CFG"),
("采样器Euler","Euler Sampler","欧拉采样","Euler sampler","Euler采样器"),
("采样器DPM++","DPM++ Sampler","DPM++采样","DPM++ 2M Karras sampler","DPM++采样器"),
("尺寸分辨率","Resolution","出图尺寸","output resolution size","尺寸分辨率"),
("宽高比","Aspect Ratio","画面比例","aspect ratio control","宽高比"),
("去噪强度","Denoising Strength","图生图重绘度","denoising strength img2img","去噪强度")],"Prompt;参数")
block("多模态与控制",[
("图生图","img2img","参考图生成","img2img reference generation","图生图"),
("局部重绘","Inpaint","遮罩重绘","inpainting masked regeneration","局部重绘"),
("扩图","Outpaint","画面外扩","outpainting extend canvas","扩图"),
("ControlNet姿态","ControlNet OpenPose","骨架姿态控制","controlnet openpose control","姿态控制"),
("ControlNet深度","ControlNet Depth","深度图控制","controlnet depth map","深度控制"),
("ControlNet线稿","ControlNet Lineart","线稿控制","controlnet lineart canny","线稿控制"),
("参考图风格迁移","Style Transfer","风格迁移","style transfer reference","风格迁移"),
("区域提示","Regional Prompt","分区控制","regional prompting","区域提示"),
("LoRA触发词","LoRA Trigger","调用微调模型","LoRA trigger word","LoRA触发词"),
("文本反演","Textual Inversion","embedding嵌入","textual inversion embedding","文本反演"),
("IP-Adapter","IP-Adapter","图像提示适配","IP-Adapter image prompt","IP-Adapter")],"Prompt;多模态")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
