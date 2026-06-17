#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv

raise SystemExit(
    "scripts/gen_terms.py is deprecated because it writes placeholder definitions. "
    "Use scripts/gen_v01.py ... gen_v15.py merge generators with real definition_short values."
)

CSV_PATH = "data/raw/terms_seed.csv"

# Read existing CSV to find max UIDs
max_uid_per_volume = {}
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        term_uid = row['term_uid']
        volume_code = term_uid.split('_')[0]
        term_num = int(term_uid.split('_')[1][1:])
        if volume_code not in max_uid_per_volume:
            max_uid_per_volume[volume_code] = 0
        max_uid_per_volume[volume_code] = max(max_uid_per_volume[volume_code], term_num)

print(f"Current max UIDs per volume: {max_uid_per_volume}")

# Define new terms for all 15 volumes
new_terms = []

# V01 terms
v01_terms = [
    {"term_uid": "V01_T0010", "zh_term": "相机传感器", "en_term": "Camera Sensor", "aliases": "感光元件;CMOS;CCD", "volume_code": "V01", "category": "相机与感光", "definition_short": "捕捉光线转换为电信号的光电元件。", "definition_long": "相机传感器是数字摄影的核心，通过光电二极管将光子转换为电信号，尺寸影响进光量和噪点，常见CMOS和CCD两种类型。", "visual_effect": "传感器大进光量充足噪点低，小传感器光线不足易产生噪点。", "prompt_usage": "camera sensor size;full frame;aps-c sensor", "positive_prompt": "full frame camera, excellent noise handling, rich shadow detail, clean iso", "negative_prompt": "excessive noise;crushed shadows;low dynamic range", "use_cases": "专业摄影;微光夜拍;高感应用", "related_terms": "像素;ISO感光度;动态范围;信噪比", "confused_with": "镜头;光圈", "tags": "摄影;硬件;技术", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0011", "zh_term": "白平衡", "en_term": "White Balance", "aliases": "色温平衡;AWB;自动白平衡", "volume_code": "V01", "category": "曝光控制", "definition_short": "调整色温使中性灰显示为中性的拍摄参数。", "definition_long": "白平衡通过选择参考白色调整色温偏差，不同光源(晴天;阴天;白炽灯)色温差异大，正确白平衡保证色彩还原准确。", "visual_effect": "正确白平衡色彩还原自然，错误白平衡画面偏冷或偏暖。", "prompt_usage": "neutral white balance;color accurate;natural skin tone", "positive_prompt": "accurate white balance, neutral color, natural skin tones, color accurate", "negative_prompt": "color cast;yellow tint;blue tint;white balance error", "use_cases": "人像摄影;产品拍摄;色彩关键工作", "related_terms": "色温;自动曝光;测光模式", "confused_with": "曝光补偿;色彩饱和度", "tags": "摄影;色彩;参数", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0012", "zh_term": "动态范围", "en_term": "Dynamic Range", "aliases": "宽容度;DR值;动态范围值", "volume_code": "V01", "category": "相机与感光", "definition_short": "传感器能记录的最亮和最暗区域的比值。", "definition_long": "动态范围越大能保留的暗部和高光细节越多，现代全画幅相机动态范围约12-14档，受传感器设计和ISO影响。", "visual_effect": "宽动态范围天空和地面细节兼得，窄动态范围容易过曝或欠曝。", "prompt_usage": "high dynamic range;extended highlights;shadow detail", "positive_prompt": "extended dynamic range, rich highlight detail, visible shadow texture, balanced exposure", "negative_prompt": "clipped highlights;crushed blacks;low dynamic range", "use_cases": "风景摄影;高反差场景;HDR处理", "related_terms": "曝光;HDR;色调映射;对数配置", "confused_with": "对比度;饱和度", "tags": "摄影;技术;传感器", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0013", "zh_term": "焦距", "en_term": "Focal Length", "aliases": "镜头焦距;mm;毫米", "volume_code": "V01", "category": "镜头与景深", "definition_short": "镜头光学中心到感光元件的距离，决定视角范围。", "definition_long": "焦距越短视角越广(广角)，焦距越长视角越窄(长焦)，焦距也影响透视感和背景虚化程度。", "visual_effect": "广角呈现宽广透视；长焦压缩空间突出主体；标准焦距接近人眼视角。", "prompt_usage": "wide angle lens;telephoto lens;35mm equivalent", "positive_prompt": "85mm focal length, compressed background, flattering perspective, portrait focal length", "negative_prompt": "distorted perspective;wrong field of view", "use_cases": "广角风景;标准人像;长焦特写", "related_terms": "视角;景深;焦点;透视", "confused_with": "光圈;焦点", "tags": "摄影;镜头;光学", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0014", "zh_term": "测光模式", "en_term": "Metering Mode", "aliases": "曝光测光;测光;评价测光", "volume_code": "V01", "category": "曝光控制", "definition_short": "相机测量场景亮度并计算曝光量的方式。", "definition_long": "常见测光模式包括评价测光(全场景平均);中央重点(强调中心);点测光(单点精确)，不同模式适应不同场景亮度分布。", "visual_effect": "恰当的测光模式保证主体曝光，错误模式导致过曝或欠曝。", "prompt_usage": "spot metering;center weighted;matrix metering", "positive_prompt": "accurate metering, proper exposure for subject, well-balanced tones", "negative_prompt": "underexposed subject;overexposed highlights;incorrect metering", "use_cases": "逆光拍摄;高反差场景;精确曝光", "related_terms": "曝光;白平衡;曝光补偿;ISO", "confused_with": "对焦模式;曝光补偿", "tags": "摄影;曝光;参数", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0015", "zh_term": "镜头畸变", "en_term": "Lens Distortion", "aliases": "桶形畸变;枕形畸变;色差", "volume_code": "V01", "category": "镜头与景深", "definition_short": "镜头产生的直线弯曲变形现象。", "definition_long": "广角镜头易产生桶形畸变(中心鼓起)，长焦镜头产生枕形畸变(中心凹陷)，现代镜头和后期软件可修正。", "visual_effect": "明显的桶形或枕形弯曲变形，线条不直。", "prompt_usage": "distortion-free;corrected optics;straight lines", "positive_prompt": "minimal distortion, straight lines, corrected optics, clean perspective", "negative_prompt": "barrel distortion;pincushion distortion;curved lines", "use_cases": "建筑摄影;校正工作;极限广角", "related_terms": "焦距;视角;透视;色差", "confused_with": "透视变形;运动模糊", "tags": "摄影;镜头;光学", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0016", "zh_term": "对焦追踪", "en_term": "Autofocus Tracking", "aliases": "连续自动对焦;AF-C;动物眼睛识别", "volume_code": "V01", "category": "镜头与景深", "definition_short": "相机持续追踪移动被摄体并保持对焦的功能。", "definition_long": "对焦追踪使用相位对焦或对比度对焦持续更新焦点位置，现代相机加入AI识别能自动锁定人脸;眼睛或动物，大幅提升运动拍摄成功率。", "visual_effect": "快速移动的被摄体始终保持清晰对焦。", "prompt_usage": "sharp focus tracking;continuous af;subject remains sharp", "positive_prompt": "sharp moving subject, continuous autofocus, eye focus, subject locked, detailed", "negative_prompt": "blurry subject;lost focus;out of focus moving object", "use_cases": "运动摄影;野生动物摄影;动态人像", "related_terms": "自动对焦;焦点;对焦模式;景深", "confused_with": "快门速度;光圈", "tags": "摄影;焦点;技术", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0017", "zh_term": "曝光锁定", "en_term": "Exposure Lock", "aliases": "AE锁;曝光保持", "volume_code": "V01", "category": "曝光控制", "definition_short": "锁定当前测光结果防止随后重组合改变曝光的功能。", "definition_long": "曝光锁定在逆光或高反差场景中很实用，先对主体点测并锁定曝光，然后重组合拍摄，确保主体曝光准确。", "visual_effect": "锁定后无论怎样重组合曝光值保持一致。", "prompt_usage": "exposure locked;consistent exposure;ae lock maintained", "positive_prompt": "locked exposure, consistent brightness, subject properly exposed", "negative_prompt": "exposure varies;inconsistent exposure;automatic exposure fluctuation", "use_cases": "逆光摄影;构图调整;序列拍摄", "related_terms": "曝光补偿;测光模式;曝光", "confused_with": "焦点锁定;白平衡锁定", "tags": "摄影;曝光;功能", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0018", "zh_term": "光圈优先模式", "en_term": "Aperture Priority Mode", "aliases": "A档;Av档;光圈优先", "volume_code": "V01", "category": "曝光控制", "definition_short": "摄影师设定光圈相机自动调整快门的半自动曝光模式。", "definition_long": "光圈优先模式让摄影师控制景深，相机根据测光和ISO自动计算快门，适合对景深有要求的场景如人像或产品摄影。", "visual_effect": "景深按设定的光圈值呈现，整体曝光由相机维持。", "prompt_usage": "aperture priority, photographer controls depth of field", "positive_prompt": "aperture priority f1.8, controlled depth of field, proper exposure, creative", "negative_prompt": "wrong shutter speed;exposure error;unexpected depth", "use_cases": "人像摄影;产品摄影;创意景深控制", "related_terms": "光圈;快门速度;曝光;模式", "confused_with": "快门优先;手动模式", "tags": "摄影;曝光;模式", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
    {"term_uid": "V01_T0019", "zh_term": "高速同步闪光", "en_term": "High-speed Flash Sync", "aliases": "HSS;高速闪光;Hs模式", "volume_code": "V01", "category": "曝光控制", "definition_short": "在快门速度超过相机闪光同步速度时使用闪光灯的技术。", "definition_long": "普通闪光同步速度通常1/200秒，高速同步通过脉冲调制使闪光灯在高速快门下仍能工作，允许强光下使用大光圈和浅景深。", "visual_effect": "在阳光下能使用大光圈浅景深并用闪光灯补光。", "prompt_usage": "high-speed sync, daylight fill flash, shallow depth on bright day", "positive_prompt": "fill flash in daylight, shallow depth of field, bright sun, ambient fill, f1.8", "negative_prompt": "harsh midday shadow;deep shadows;small aperture forced", "use_cases": "日光补光;阳光人像;控制背景曝光", "related_terms": "闪光灯;快门速度;同步速度;光圈", "confused_with": "快门速度;闪光功率", "tags": "摄影;灯光;闪光", "source_refs": "AI生成", "status": "published", "version": "V1.0"},
]

new_terms.extend(v01_terms)

# Add remaining 140+ terms for V02-V15 (10 per volume)
vol_data = {
    'V02': [('景深雾化', 'Focus Breathing', '镜头景别'), ('摇臂运动', 'Crane Shot', '摄影机运动'), ('环形光', 'Ring Light', '灯光与影调'), ('对比光', 'Contrast Lighting', '灯光与影调'), ('色温调和', 'Color Temperature Harmony', '灯光与影调'), ('镜头语言叙事', 'Shot Language Narrative', '镜头语言'), ('DCI标准', 'DCI 4K Standard', '电影格式'), ('片场勤务', 'Set Department', '片场工作流'), ('镜头数据表', 'Camera Report Sheet', '片场工作流'), ('素材备份', 'Footage Backup', '片场工作流')],
    'V03': [('油画肌理', 'Oil Painting Texture', '笔触与肌理'), ('拜占庭艺术', 'Byzantine Art', '艺术流派与时代'), ('造型比例', 'Figure Proportions', '造型语言'), ('色彩和谐', 'Color Harmony', '艺术理论'), ('点彩派', 'Pointillism', '艺术流派与时代'), ('表现主义', 'Expressionism', '艺术流派与时代'), ('立体主义', 'Cubism', '艺术流派与时代'), ('抽象艺术', 'Abstract Art', '代表性风格'), ('版画技法', 'Printmaking', '绘画媒介'), ('素描基础', 'Drawing Fundamentals', '绘画媒介')],
    'V04': [('角色配色方案', 'Character Color Scheme', '角色设计'), ('场景植被设计', 'Vegetation Design', '场景与世界观'), ('UI图标风格', 'UI Icon Style', 'UI与图标'), ('界面交互设计', 'UI Interaction Design', 'UI与图标'), ('菜单系统设计', 'Menu System Design', 'UI与图标'), ('HUD设计', 'HUD Design', 'UI与图标'), ('道具功能表现', 'Prop Functionality', '道具与装备'), ('护甲设计', 'Armor Design', '道具与装备'), ('头部设计', 'Head Design', '生物设计'), ('姿态与表现', 'Posture and Expression', '角色设计')],
    'V05': [('排版美感', 'Typographic Beauty', '字体与排印'), ('栅格布局', 'Grid Layout', '版式与网格'), ('色彩心理', 'Color Psychology', '品牌视觉'), ('海报设计原则', 'Poster Design Principles', '海报与广告'), ('信息架构', 'Information Architecture', '信息设计'), ('纸张选择', 'Paper Selection', '印刷工艺'), ('字重应用', 'Font Weight Usage', '字体与排印'), ('间距设计', 'Spacing Design', '版式与网格'), ('焦点管理', 'Focal Point Management', '信息设计'), ('阅读流线', 'Reading Flow', '版式与网格')],
    'V06': [('光的质量', 'Light Quality', '光度与照度'), ('色彩空间', 'Color Space', '色彩科学'), ('显示器校准', 'Monitor Calibration', '色彩管理'), ('灯光比例', 'Lighting Ratio', '灯光布置'), ('曝光融合', 'Exposure Blending', 'HDR与动态范围'), ('色感适应', 'Color Adaptation', '视觉感知'), ('光学原理', 'Optical Principles', '光度与照度'), ('色调映射', 'Tone Mapping', 'HDR与动态范围'), ('亮度对比', 'Brightness Contrast', '色彩科学'), ('光的衍射', 'Light Diffraction', '光度与照度')],
    'V07': [('漫反射', 'Diffuse Reflection', 'PBR材质'), ('环境遮蔽', 'Ambient Occlusion', '贴图通道'), ('镜像反射', 'Specular Reflection', 'Shader与节点'), ('路径追踪', 'Path Tracing', '渲染算法'), ('皮肤着色', 'Skin Shading', '表面与质感'), ('布料模拟', 'Fabric Simulation', '表面与质感'), ('着色器编写', 'Shader Writing', 'Shader与节点'), ('纹理投影', 'Texture Projection', '贴图通道'), ('体积光', 'Volumetric Light', '渲染算法'), ('粒子系统', 'Particle System', '引擎与管线')],
    'V08': [('提示词顺序', 'Prompt Order', '提示词结构'), ('风格标签', 'Style Tags', '视觉修饰符'), ('质量标签', 'Quality Tags', '视觉修饰符'), ('艺术家参考', 'Artist Reference', '视觉修饰符'), ('负向权重', 'Negative Weighting', '负向与约束'), ('采样步数优化', 'Step Optimization', '参数与随机性'), ('指导强度', 'Guidance Strength', '参数与随机性'), ('提示词评估', 'Prompt Evaluation', '评估与迭代'), ('文本编码', 'Text Encoding', '多模态提示'), ('嵌入模型', 'Embedding Model', '多模态提示')],
    'V09': [('中轴线', 'Central Axis', '构图语法'), ('对角线构图', 'Diagonal Composition', '构图语法'), ('S形构图', 'S-curve Composition', '构图语法'), ('视觉流向', 'Visual Flow', '视觉层级'), ('节奏变化', 'Rhythm Variation', '叙事节奏'), ('低角度镜头', 'Low Angle Shot', '视角与主体'), ('高角度镜头', 'High Angle Shot', '视角与主体'), ('正方形画幅', 'Square Framing', '格式与画幅'), ('竖幅构图', 'Portrait Framing', '格式与画幅'), ('格式塔聚合', 'Gestalt Grouping', '心理与格式塔')],
    'V10': [('新古典主义', 'Neoclassicism', '建筑风格'), ('后现代建筑', 'Postmodern Architecture', '建筑风格'), ('开放式平面', 'Open Floor Plan', '建筑空间'), ('通高设计', 'Double Height Design', '建筑空间'), ('北欧室内', 'Scandinavian Interior', '室内设计'), ('工业风格', 'Industrial Style', '室内设计'), ('家具陈设', 'Furniture Arrangement', '家具与陈设'), ('园林景观', 'Garden Landscape', '景观与城市'), ('城市规划', 'Urban Planning', '景观与城市'), ('光影营造', 'Light and Shadow', '空间氛围')],
    'V11': [('西服剪裁', 'Tailoring', '服装结构'), ('双层面料', 'Double Knit', '面料与纹样'), ('蕾丝纹样', 'Lace Pattern', '面料与纹样'), ('A字裙廓', 'A-line Skirt', '廓形与剪裁'), ('泡泡袖', 'Puff Sleeves', '廓形与剪裁'), ('朋克风格', 'Punk Style', '时代与风格'), ('波西米亚', 'Bohemian', '时代与风格'), ('珠宝配饰', 'Jewelry Accessories', '配饰与道具'), ('帽饰设计', 'Hat Design', '配饰与道具'), ('妆容风格', 'Makeup Style', '发妆与造型')],
    'V12': [('计时与节拍', 'Timing and Spacing', '动画基础'), ('预期动作', 'Anticipation', '动画基础'), ('分镜表', 'Shot List', '分镜语言'), ('镜头时长', 'Shot Duration', '分镜语言'), ('场景时长', 'Scene Duration', '时间与节奏'), ('音效同步', 'Sound Sync', '时间与节奏'), ('逆向动力学', 'Inverse Kinematics', '角色绑定'), ('正向动力学', 'Forward Kinematics', '角色绑定'), ('粒子效果', 'Particle Effects', '特效与合成'), ('绿幕合成', 'Chroma Key Compositing', '特效与合成')],
    'V13': [('粗剪', 'Rough Cut', '剪辑基础'), ('精剪', 'Fine Cut', '剪辑基础'), ('皮肤修饰', 'Skin Retouching', '修图与润饰'), ('瑕疵移除', 'Blemish Removal', '修图与润饰'), ('色彩分离', 'Color Separation', '调色流程'), ('蒙版合成', 'Mask Compositing', '合成技术'), ('特效插件', 'Effects Plugins', '滤镜与效果'), ('字幕制作', 'Subtitle Creation', '输出与交付'), ('音频混音', 'Audio Mixing', '输出与交付'), ('归档交付', 'Archive and Delivery', '输出与交付')],
    'V14': [('Stable Diffusion', 'Stable Diffusion', '模型类型'), ('DALL-E模型', 'DALL-E Model', '模型类型'), ('Midjourney模型', 'Midjourney Model', '模型类型'), ('欧拉采样器', 'Euler Sampler', '采样与调度'), ('DPM采样器', 'DPM Sampler', '采样与调度'), ('深度图控制', 'Depth Control', '控制与条件生成'), ('姿态识别', 'Pose Recognition', '控制与条件生成'), ('人脸交换', 'Face Swap', 'LoRA与微调'), ('超分放大', 'Upscaling', '放大与修复'), ('工作流编辑', 'Workflow Editing', '节点与自动化')],
    'V15': [('极简美学', 'Minimalist Aesthetics', '类型与审美标签'), ('朋克美学', 'Punk Aesthetics', '类型与审美标签'), ('巴洛克', 'Baroque', '时代风格'), ('洛可可', 'Rococo', '时代风格'), ('中国古典', 'Chinese Classical', '地域风格'), ('日本和风', 'Japanese Aesthetic', '地域风格'), ('赛博美学', 'Cyber Aesthetics', '网络美学'), ('复古未来', 'Retro-futurism', '网络美学'), ('品牌调性', 'Brand Tone', '品牌语气'), ('混合风格', 'Hybrid Style', '混合媒介')],
}

for vol_code, terms_list in vol_data.items():
    for idx, (zh_term, en_term, category) in enumerate(terms_list, start=7):
        term = {
            "term_uid": f"{vol_code}_T{idx:04d}",
            "zh_term": zh_term,
            "en_term": en_term,
            "aliases": "别名1;别名2;别名3",
            "volume_code": vol_code,
            "category": category,
            "definition_short": f"{zh_term}的简短定义。",
            "definition_long": f"{zh_term}的详细解释，涵盖理论基础、应用场景和实践意义。",
            "visual_effect": f"{zh_term}的典型视觉表现特征。",
            "prompt_usage": f"与{zh_term}相关的提示词用法",
            "positive_prompt": f"{zh_term}, high quality, detailed, professional, well-executed, masterpiece",
            "negative_prompt": "low quality, poor execution, unprofessional, incomplete, blurry",
            "use_cases": "应用场景1;应用场景2;应用场景3",
            "related_terms": "相关术语1;相关术语2;相关术语3",
            "confused_with": "容易混淆的术语",
            "tags": f"{vol_code};{category};术语",
            "source_refs": "AI生成",
            "status": "published",
            "version": "V1.0"
        }
        new_terms.append(term)

print(f"Total new terms to add: {len(new_terms)}")

# Append using csv.writer
with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'term_uid', 'zh_term', 'en_term', 'aliases', 'volume_code', 'category',
        'definition_short', 'definition_long', 'visual_effect', 'prompt_usage',
        'positive_prompt', 'negative_prompt', 'use_cases', 'related_terms',
        'confused_with', 'tags', 'source_refs', 'status', 'version'
    ])
    for term in new_terms:
        writer.writerow(term)

print(f"Successfully appended {len(new_terms)} terms")
