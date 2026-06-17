# -*- coding: utf-8 -*-
"""V14 AI图像模型参数与工作流（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V14"; rows=[]
def block(cat,items,tags):
    for zh,en,defs in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",en,"",zh,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("模型类型",[
("SD1.5","stable diffusion 1.5","经典Stable Diffusion潜空间图像生成模型"),
("SD2.1","stable diffusion 2.1","改进文本编码和训练数据的SD二代模型"),
("SDXL","sdxl","更大网络和双编码器构成的高质量SD模型"),
("SD3","stable diffusion 3","融合扩散Transformer架构的新一代SD模型"),
("Flux","flux model","高提示词理解和写实能力的扩散生成模型"),
("Midjourney","midjourney","以审美风格化见长的在线图像生成系统"),
("DALL-E 3","dall-e 3","强调文本遵循和语义准确的图像生成模型"),
("Imagen","google imagen","Google研发的文本到图像扩散模型体系"),
("扩散模型","diffusion model","从噪声逐步去噪生成图像的模型类别"),
("GAN","gan generative adversarial","生成器与判别器对抗训练的生成模型"),
("VAE","vae variational autoencoder","把图像压缩到潜变量再重建的生成模型"),
("Latent扩散","latent diffusion","在压缩潜空间中去噪生成图像的方法"),
("一致性模型","consistency model","以少步采样快速生成的扩散替代模型"),
("级联扩散","cascade diffusion","多阶段由低到高分辨率生成的扩散系统")],"AI;模型")

block("采样与调度",[
("Euler采样","euler sampler","用欧拉法逐步去噪的基础采样器"),
("Euler a采样","euler a sampler","带随机性的欧拉祖先采样器，变化更丰富"),
("DPM++ 2M","dpm++ 2m karras","高质量稳定去噪的多步DPM采样器"),
("DPM++ SDE","dpm++ sde","引入随机微分方程的细腻采样器"),
("DDIM","ddim","可确定性快速采样的早期扩散采样方法"),
("UniPC","unipc","统一预测校正框架下的高效采样器"),
("LCM","lcm fast sampler","少步快速生成的一致性蒸馏采样方式"),
("Karras调度","karras scheduler","按Karras噪声曲线分配采样步长的调度"),
("采样步数","sampling steps","去噪迭代次数，影响细节质量和耗时"),
("CFG引导","cfg scale","控制提示词约束强弱的分类器自由引导"),
("种子","seed","决定随机噪声初始状态的可复现数值"),
("Clip跳过","clip skip","跳过CLIP末层以改变文本特征解释的参数")],"AI;采样")

block("控制与条件",[
("ControlNet","controlnet","用额外结构条件控制扩散生成的网络"),
("Canny边缘","controlnet canny","以边缘线稿约束画面轮廓的控制方式"),
("深度Depth","controlnet depth","用深度图约束空间前后关系的控制方式"),
("OpenPose姿态","controlnet openpose","用人体骨架点位约束角色姿态"),
("线稿Lineart","controlnet lineart","用清晰线稿控制图像结构和轮廓"),
("涂鸦Scribble","controlnet scribble","用粗略涂鸦草图引导生成构图"),
("法线Normal","controlnet normalmap","用表面法线约束三维凹凸朝向"),
("语义分割Seg","controlnet segmentation","用类别色块图控制物体区域分布"),
("软边缘HED","controlnet softedge hed","用柔和边缘图保留轮廓而减少硬线"),
("T2I-Adapter","t2i adapter","轻量条件适配器，用额外输入控制生成"),
("IP-Adapter","ip-adapter","用参考图特征控制人物、风格或构图"),
("区域控制","regional prompt control","给画面不同区域分配不同提示词条件"),
("Reference参考","controlnet reference","通过参考图传递风格、颜色或人物特征")],"AI;控制")

block("微调与定制",[
("LoRA","lora finetune","低秩适配权重，用小文件学习风格或角色"),
("LyCORIS","lycoris","扩展LoRA结构的轻量微调方法集合"),
("DreamBooth","dreambooth","用少量样本定制特定主体的微调方法"),
("文本反演","textual inversion embedding","学习新词向量以召回特定概念的技术"),
("Hypernetwork","hypernetwork","用外部小网络调制主模型特征的微调方式"),
("全量微调","full finetune","直接更新模型全部权重的深度训练方式"),
("DoRA","dora","分解权重方向和幅度的高效微调方法"),
("数据集准备","dataset captioning","整理图片和标注以支持模型训练的流程")],"AI;微调")

block("放大与修复",[
("超分放大","ai upscale super resolution","用AI提升图像分辨率和细节清晰度"),
("Hires fix","hires fix","先低分生成再高分重绘以增加细节"),
("Tiled放大","tiled diffusion upscale","分块扩散放大以处理超大分辨率图像"),
("面部修复","face restoration gfpgan","用专门模型修复人脸五官和清晰度"),
("ADetailer","adetailer auto detail","自动检测局部并二次重绘细节的工具"),
("局部重绘","inpaint","只在遮罩区域内重新生成或修复图像"),
("手部修复","hand refiner","针对手指结构错误进行局部修正的流程"),
("Ultimate SD放大","ultimate sd upscale","分块重绘放大并保留整体一致性的插件")],"AI;放大修复")

block("工作流与自动化",[
("ComfyUI节点","comfyui node workflow","用节点连接模型、参数和处理步骤的工作流"),
("工作流编排","generation pipeline","把生成、控制、修复和输出串联成流程"),
("批处理","batch generation","一次运行生成多张图或多组任务的方式"),
("API调用","generation api","通过接口提交提示词和参数生成图像"),
("参数矩阵","xyz plot","横纵轴批量比较参数组合效果的图表"),
("WebUI","stable diffusion webui","浏览器界面的本地图像生成操作平台"),
("提示词模板库","prompt library","复用常见风格和参数组合的提示词集合"),
("工作流分享","workflow sharing","导出节点图或参数以复现生成流程")],"AI;工作流")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
