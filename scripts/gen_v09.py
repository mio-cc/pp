# -*- coding: utf-8 -*-
"""V09 构图与视觉叙事（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V09"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("构图语法",[
("三分法","Rule of Thirds","画面横竖各两条三分线将主体放在交叉点上","rule of thirds composition","三分法"),
("黄金螺旋","Golden Spiral Fibonacci","沿黄金螺旋线安排主体的自然优美构图","golden spiral fibonacci composition","黄金螺旋"),
("黄金分割","Golden Ratio","按1:1.618比例分割画面的经典法则","golden ratio division composition","黄金分割"),
("中心对称","Central Symmetry","主体居中与两侧镜像对称的庄重构图","central symmetry composition","中心对称"),
("对角线","Diagonal Dynamic","沿对角线布局产生动感张力","diagonal dynamic composition","对角线"),
("引导线","Leading Lines","利用场景线条引导视线到主体的构图","leading lines composition","引导线"),
("框架式","Framing","用前景框遮形成画中画的包围构图","framing within frame composition","框架式"),
("三角构图","Triangular","三个主要元素构成三角形的稳定布局","triangular stable composition","三角构图"),
("S形曲线","S-Curve","S形曲线引导视线穿越画面的优美构图","s-curve flowing composition","S形曲线"),
("C形构图","C-Curve","C形弧线包围主体形成视觉包裹","c-curve wrapping composition","C形构图"),
("重复韵律","Repetition Rhythm","相同元素规律重复形成视觉韵律","repetition rhythm pattern","重复韵律"),
("放射构图","Radial","从中心向外发散的放射性线条布局","radial burst composition","放射构图"),
("水平线","Horizontal Calm","水平线条主导的宁静平稳构图","horizontal calm composition","水平线"),
("垂直线","Vertical","竖直线条营造的高度与庄严感","vertical height composition","垂直线"),
("曲线引导","Curved Lines","弯曲路径引导视线流动的柔和构图","curved lines flowing composition","曲线引导"),
("螺旋构图","Spiral","螺旋线旋入画面中心的运动感构图","spiral inward composition","螺旋构图"),
("井字构图","Grid Nine","九宫格四线交叉点的网格构图法","grid nine-square composition","井字构图"),
("L形构图","L-Shaped","L形线条框出主体形成拐角布局","l-shaped corner composition","L形构图"),
("满构图","Full Frame Fill","主体充满画面的压迫式密集构图","full frame fill composition","满构图"),
("极简构图","Minimalist","大量留白极少元素的高级简约构图","minimalist sparse composition","极简构图")],"构图;语法")
block("视觉层级与引导",[
("视觉重心","Visual Weight Focal","画面中吸引注意力的最突出位置","visual weight focal point","视觉重心"),
("主次层级","Visual Hierarchy","按重要性排列信息主次关系的层级系统","visual hierarchy priority","主次层级"),
("视线引导","Eye Flow Guidance","控制观者视线在画面中移动的路径","eye flow guidance path","视线引导"),
("对比强调","Contrast Emphasis","用明暗/色彩/大小差异突出主体","contrast emphasis highlight","对比强调"),
("前中后景","Foreground Midground Background Layers","画面纵深三层空间的信息层次","foreground midground background","前中后景"),
("留白呼吸","Negative Space","刻意的空白区域提供视觉休息","negative space breathing room","留白呼吸"),
("视觉焦点","Focal Point","画面中观者目光最先落下的中心","focal point attention center","视觉焦点"),
("景深层次","Depth Layering","利用虚实变化区分前后纵深层次","depth layering focus blur","景深层次"),
("大小对比","Scale Contrast","大小物体并置产生的尺度差异感","scale contrast size","大小对比"),
("明暗对比","Tonal Contrast","亮部暗部相邻产生的光影反差","tonal contrast light dark","明暗对比"),
("色彩引导","Color Guidance","用色彩纯度或暖冷引导视觉流向","color guidance saturation temperature","色彩引导")],"构图;层级")
block("叙事与张力",[
("视觉节奏","Visual Rhythm Pacing","画面元素重复或渐变形成的视觉韵律","visual rhythm pacing","视觉节奏"),
("画面张力","Compositional Tension","不平衡或冲突元素产生的紧张视觉感","compositional tension imbalance","画面张力"),
("叙事留白","Narrative Space","画面中未交代的暗示性空白引发想象","narrative space suggestion","叙事留白"),
("方向暗示","Implied Direction","通过视线或动态暗示画面外空间的存在","implied direction gaze motion","方向暗示"),
("呼应平衡","Visual Balance","左右或上下元素互相呼应的视觉平衡","visual balance correspondence","呼应平衡"),
("打破常规","Broken Symmetry","刻意打破对称产生意外与活力","broken symmetry disruption","打破常规"),
("对称平衡","Symmetrical Balance","两侧完全对称的庄重和谐构图","symmetrical balance mirror","对称平衡"),
("非对称平衡","Asymmetrical Balance","两侧不同但视觉重量相等的平衡","asymmetrical balance weighted","非对称平衡"),
("动态平衡","Dynamic Balance","运动中的不稳定但整体协调的张力平衡","dynamic balance motion","动态平衡"),
("视觉重量分布","Weight Distribution","元素大小明暗色彩决定画面沉重感分布","weight distribution visual mass","视觉重量分布"),
("故事性瞬间","Decisive Moment","卡蒂埃-布列松式的决定性叙事瞬间","decisive moment narrative","故事性瞬间")],"构图;叙事")
block("视角与画幅",[
("平视","Eye Level","与人眼等高的自然平直视角","eye level view","平视"),
("俯视","High Angle","从上方向下看的视角、主体显弱","high angle looking down","俯视"),
("仰视","Low Angle Heroic","从下方向上看的视角、主体显强","low angle looking up heroic","仰视"),
("鸟瞰","Top-Down Aerial","正上方垂直向下的鸟瞰俯视","top-down aerial view","鸟瞰"),
("虫视","Worm Eye View","贴近地面极低角度的仰视","worm eye ground-level view","虫视"),
("荷兰角","Dutch Tilt","地平线倾斜的不安动感视角","dutch tilt canted horizon","荷兰角"),
("正方形画幅","Square 1:1","等边正方形的1:1社交媒体画幅","square 1:1 format","正方形画幅"),
("竖幅","Vertical Portrait","竖向的肖像/手机竖屏画幅","vertical portrait format","竖幅"),
("横幅","Horizontal Landscape","横向的风光/电影宽屏画幅","horizontal landscape format","横幅"),
("宽幅全景","Panoramic","超宽的全景横幅画幅","panoramic wide format","宽幅全景"),
("超宽画幅","Ultrawide Cinematic","2.39:1等超宽电影级画幅","ultrawide cinematic format","超宽画幅")],"构图;视角画幅")
block("心理与格式塔",[
("接近原则","Gestalt Proximity","距离近的元素被感知为一组的倾向","gestalt proximity grouping","接近原则"),
("相似原则","Gestalt Similarity","外形相似的元素被归为一组的倾向","gestalt similarity grouping","相似原则"),
("闭合原则","Gestalt Closure","人脑自动补全不完整图形的倾向","gestalt closure completion","闭合原则"),
("连续原则","Gestalt Continuity","沿平滑曲线追踪的视觉连续倾向","gestalt continuity flow","连续原则"),
("图底关系","Figure-Ground","主体与背景之间的可逆视觉分离","figure-ground reversible","图底关系"),
("简化原则","Gestalt Pragnanz","大脑偏好最简单最规则形状的倾向","gestalt pragnanz simplicity","简化原则"),
("共同命运","Common Fate","同方向运动的元素被视为一组","common fate motion grouping","共同命运"),
("对称原则","Gestalt Symmetry","对称图形被感知为统一整体","gestalt symmetry unity","对称原则"),
("焦点引力","Focal Attraction","画面中最引人注目位置的吸引法则","focal attraction attention","焦点引力")],"构图;格式塔")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
