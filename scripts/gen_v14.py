# -*- coding: utf-8 -*-
"""V14 AI图像模型参数与工作流（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V14"; rows=[]
def simple(cat,items,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,zh+"。","","","",en,"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("模型类型",[("SD1.5","stable diffusion 1.5"),("SD2.1","stable diffusion 2.1"),("SDXL","sdxl"),("SD3","stable diffusion 3"),("Flux","flux model"),("Midjourney","midjourney"),("DALL-E 3","dall-e 3"),("Imagen","google imagen"),("扩散模型","diffusion model"),("GAN","gan generative adversarial"),("VAE","vae variational autoencoder"),("Latent扩散","latent diffusion"),("一致性模型","consistency model"),("级联扩散","cascade diffusion")],"AI;模型")
simple("采样与调度",[("Euler采样","euler sampler"),("Euler a采样","euler a sampler"),("DPM++ 2M","dpm++ 2m karras"),("DPM++ SDE","dpm++ sde"),("DDIM","ddim"),("UniPC","unipc"),("LCM","lcm fast sampler"),("Karras调度","karras scheduler"),("采样步数","sampling steps"),("CFG引导","cfg scale"),("种子","seed"),("Clip跳过","clip skip")],"AI;采样")
simple("控制与条件",[("ControlNet","controlnet"),("Canny边缘","controlnet canny"),("深度Depth","controlnet depth"),("OpenPose姿态","controlnet openpose"),("线稿Lineart","controlnet lineart"),("涂鸦Scribble","controlnet scribble"),("法线Normal","controlnet normalmap"),("语义分割Seg","controlnet segmentation"),("软边缘HED","controlnet softedge hed"),("T2I-Adapter","t2i adapter"),("IP-Adapter","ip-adapter"),("区域控制","regional prompt control"),("Reference参考","controlnet reference")],"AI;控制")
simple("微调与定制",[("LoRA","lora finetune"),("LyCORIS","lycoris"),("DreamBooth","dreambooth"),("文本反演","textual inversion embedding"),("Hypernetwork","hypernetwork"),("全量微调","full finetune"),("DoRA","dora"),("数据集准备","dataset captioning")],"AI;微调")
simple("放大与修复",[("超分放大","ai upscale super resolution"),("Hires fix","hires fix"),("Tiled放大","tiled diffusion upscale"),("面部修复","face restoration gfpgan"),("ADetailer","adetailer auto detail"),("局部重绘","inpaint"),("手部修复","hand refiner"),("Ultimate SD放大","ultimate sd upscale")],"AI;放大修复")
simple("工作流与自动化",[("ComfyUI节点","comfyui node workflow"),("工作流编排","generation pipeline"),("批处理","batch generation"),("API调用","generation api"),("参数矩阵","xyz plot"),("WebUI","stable diffusion webui"),("提示词模板库","prompt library"),("工作流分享","workflow sharing")],"AI;工作流")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
