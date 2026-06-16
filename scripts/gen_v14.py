# -*- coding: utf-8 -*-
"""V14 AI图像模型参数与工作流（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V14"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"整理","published","V1.0"])))
block("模型类型",[
("SD1.5","Stable Diffusion 1.5","经典开源底模","Stable Diffusion 1.5 model","SD1.5"),
("SDXL","SDXL","高分辨率底模","SDXL model","SDXL"),
("SD3","Stable Diffusion 3","新一代底模","Stable Diffusion 3","SD3"),
("Flux","Flux","高质量新模型","Flux model","Flux"),
("Midjourney","Midjourney","美学强商业模型","Midjourney style","Midjourney"),
("DALL-E 3","DALL-E 3","语义理解强","DALL-E 3","DALL-E3"),
("扩散模型","Diffusion Model","去噪生成原理","diffusion model","扩散模型"),
("GAN","GAN","对抗生成","GAN generative adversarial","GAN")],"AI;模型")
block("采样与调度",[
("采样器Euler a","Euler a","欧拉祖先采样","Euler a sampler","Euler a"),
("采样器DPM++ 2M","DPM++ 2M","常用采样器","DPM++ 2M Karras","DPM++ 2M"),
("采样器DDIM","DDIM","确定性采样","DDIM sampler","DDIM"),
("调度器Karras","Karras Scheduler","噪声调度","Karras scheduler","Karras调度"),
("采样步数","Steps","迭代步数","sampling steps 20-40","采样步数"),
("CFG引导强度","CFG Scale","贴合提示度","CFG scale 7","CFG引导"),
("种子Seed","Seed","随机种子复现","seed reproducibility","种子")],"AI;采样")
block("控制与条件生成",[
("ControlNet","ControlNet","结构条件控制","controlnet conditioning","ControlNet"),
("Canny边缘","Canny","边缘线控制","controlnet canny edge","Canny边缘"),
("深度图Depth","Depth","深度控制","controlnet depth","深度图"),
("OpenPose姿态","OpenPose","骨架姿态","controlnet openpose","OpenPose"),
("线稿Lineart","Lineart","线稿控制","controlnet lineart","线稿"),
("T2I-Adapter","T2I-Adapter","轻量条件","T2I adapter","T2I-Adapter"),
("IP-Adapter","IP-Adapter","图像提示","IP-adapter image prompt","IP-Adapter"),
("区域控制","Regional Control","分区生成","regional prompt control","区域控制")],"AI;控制")
block("微调与定制",[
("LoRA","LoRA","低秩微调","LoRA fine-tune","LoRA"),
("DreamBooth","DreamBooth","主体定制","dreambooth subject training","DreamBooth"),
("文本反演","Textual Inversion","嵌入定制","textual inversion embedding","文本反演"),
("Hypernetwork","Hypernetwork","风格微调","hypernetwork","Hypernetwork"),
("微调训练","Fine-tuning","底模微调","model fine-tuning training","微调训练")],"AI;微调")
block("放大与修复",[
("超分放大","Upscale","分辨率放大","AI upscaling super resolution","超分放大"),
("Hires fix","Hires Fix","高清修复","hires fix high-res","Hires fix"),
("Tiled放大","Tiled Diffusion","分块放大","tiled diffusion upscale","Tiled放大"),
("面部修复","Face Restore","修脸","face restoration GFPGAN","面部修复"),
("ADetailer","ADetailer","自动细节修复","adetailer auto detail","ADetailer"),
("局部重绘","Inpaint","遮罩重绘","inpainting","局部重绘")],"AI;放大修复")
block("工作流与自动化",[
("ComfyUI节点","ComfyUI Node","节点式工作流","comfyui node workflow","ComfyUI节点"),
("工作流编排","Workflow","流程编排","generation workflow pipeline","工作流编排"),
("批处理","Batch","批量生成","batch generation","批处理"),
("API调用","API","接口集成","generation API integration","API调用"),
("提示词矩阵","XYZ Plot","参数对比图","XYZ plot parameter grid","参数矩阵")],"AI;工作流")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
