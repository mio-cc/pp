# -*- coding: utf-8 -*-
"""V05 平面设计与版式（穷举级）。合并模式。

范式说明：本脚本只使用 block()，每个 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁用「术语名+。」的占位。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V05"; rows=[]
def block(cat,items,tags):
    # item = (zh, en, definition_short, positive_prompt_en, positive_prompt_cn)
    for zh,en,defs,pen,pcn in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("字体与排印 / 字体分类",[
("衬线体","Serif Typeface","笔画端部带装饰小脚的经典正文字体","serif typeface, classic typography","衬线体"),
("无衬线体","Sans-serif Typeface","无装饰脚、笔画均匀的现代字体","sans-serif typeface, modern clean","无衬线体"),
("板衬线","Slab Serif","衬线粗厚如板、强几何感的工业字体","slab serif typeface, bold geometric","板衬线"),
("手写体","Script Typeface","模仿手写连笔的装饰性字体","script typeface, handwritten elegant","手写体"),
("哥特黑体","Blackletter Gothic","中世纪尖笔书写、密集棱角的装饰字体","blackletter gothic typeface","哥特黑体"),
("等宽字体","Monospace Typeface","每字符等宽、用于代码与终端的字体","monospace typeface, code terminal","等宽字体"),
("展示体","Display Typeface","为大字号标题设计的夸张字体","display typeface, bold headline","展示体"),
("圆体","Rounded Typeface","笔画端部圆角、亲和圆润的字体","rounded typeface, friendly soft","圆体"),
("宋体","Song Serif Chinese","横细竖粗、带衬线的中文传统印刷体","song serif typeface, chinese classic","宋体"),
("黑体","Hei Sans Chinese","笔画均匀、无衬线的中文现代字体","hei sans typeface, chinese modern","黑体"),
("楷体","Kai Chinese","仿手写楷书、端庄正式的中文字体","kai typeface, chinese formal script","楷体"),
("书法字体","Calligraphy Type","仿毛笔书法、带笔锋韵味的字体","calligraphy typeface, brush stroke","书法字体"),
("像素字体","Pixel Bitmap Font","位图点阵风格、复古游戏感的字体","pixel bitmap font, retro 8bit","像素字体"),
("可变字体","Variable Font","单文件含多轴向可调的新型字体","variable font, dynamic weight axis","可变字体")],"平面;字体")
block("字体与排印 / 排印属性",[
("字重层级","Font Weight Hierarchy","用粗细对比建立信息主次层级","font weight hierarchy, bold emphasis","字重层级"),
("字距调整","Kerning Tracking","调整字符间距以改善视觉平衡","kerning tracking, letter spacing","字距调整"),
("行距","Leading Line Spacing","行与行之间的垂直间距控制","leading line spacing, readable","行距"),
("字号层级","Type Scale Hierarchy","用字号大小拉开标题到正文层级","type scale hierarchy, heading sizes","字号层级"),
("基线网格","Baseline Grid","所有文字对齐的统一基线系统","baseline grid, aligned typography","基线网格"),
("首字下沉","Drop Cap","段首首字放大数倍的装饰手法","drop cap, decorative initial","首字下沉"),
("对齐排版","Text Alignment","文本相对边界的排列方式","text alignment, ordered layout","对齐排版"),
("两端对齐","Justified Text","左右两端同时齐整的规整排版","justified text, flush both edges","两端对齐"),
("竖排","Vertical Typesetting","自上而下、自右向左的竖向排版","vertical typesetting, chinese style","竖排"),
("文字环绕","Text Wrap","文字沿图形边缘流动环绕","text wrap around image","文字环绕"),
("字偶距","Letter Spacing","字母之间的水平间距控制","letter spacing, tracking","字偶距")],"平面;排印")
block("版式与网格",[
("网格系统","Grid System Layout","用栅格对齐元素的版式骨架","grid system layout, structured","网格系统"),
("瑞士国际主义","Swiss International Style","网格+无衬线+留白的功能主义版式","swiss international typographic style","瑞士国际主义"),
("黄金比例版式","Golden Ratio Layout","按1:1.618比例分割的版面","golden ratio layout, balanced","黄金比例版式"),
("对齐","Alignment Ordered","元素沿统一参考线整齐排列","alignment, clean ordered layout","对齐"),
("留白","White Space Negative","刻意留出的呼吸空隙","white space, negative space, breathing","留白"),
("分栏","Multi-column Layout","文字纵向分多栏排布","multi-column layout, magazine","分栏"),
("对称布局","Symmetrical Layout","左右镜像的庄重版式","symmetrical layout, balanced mirror","对称布局"),
("非对称布局","Asymmetrical Dynamic Layout","不平衡但富有张力的动态版式","asymmetrical dynamic layout","非对称布局"),
("模块化版式","Modular Grid","按等大模块拼接的版式","modular grid layout, block based","模块化版式"),
("杂志版式","Editorial Magazine Layout","图文混排、节奏丰富的杂志版式","editorial magazine layout","杂志版式"),
("拼贴版式","Collage Layout","多元素层叠撕贴的拼贴感版式","collage layout, layered cutout","拼贴版式"),
("满版出血","Full Bleed Layout","图像铺满到页面裁切边缘","full bleed layout, edge to edge","满版出血"),
("网格破坏","Broken Grid","刻意打破网格的自由版式","broken grid, deconstructed layout","网格破坏"),
("黄金螺旋版式","Golden Spiral Layout","沿黄金螺旋引导视线的版式","golden spiral layout","黄金螺旋版式")],"平面;版式")
block("品牌视觉",[
("字标logo","Wordmark Logo","纯文字设计的标志","wordmark logo, typographic logo","字标logo"),
("图形标志","Abstract Logomark","抽象图形符号的标志","abstract logomark, symbol mark","图形标志"),
("徽章logo","Emblem Badge Logo","文字嵌于图形内的徽记标志","emblem badge logo","徽章logo"),
("组合标志","Combination Mark","文字与图形组合的标志","combination mark, logo lockup","组合标志"),
("字母标","Lettermark Monogram","首字母缩写设计的标志","lettermark monogram logo","字母标"),
("品牌主色","Brand Color Palette","品牌固定的核心色彩规范","brand color palette","品牌主色"),
("VI系统","Visual Identity System","统管品牌所有视觉的系统规范","visual identity system, VI","VI系统"),
("吉祥物","Brand Mascot","拟人化形象代言品牌","brand mascot, character mascot","吉祥物"),
("辅助图形","Brand Graphic Pattern","品牌延展用的辅助纹样","brand graphic pattern, supporting motif","辅助图形"),
("品牌字体","Brand Typeface","品牌专属或指定的字体","brand typeface, custom font","品牌字体")],"平面;品牌")
block("海报与广告",[
("极简海报","Minimalist Poster","大量留白、少元素的极简海报","minimalist poster, clean simple","极简海报"),
("瑞士海报","Swiss Grid Poster","网格严谨、字体主导的瑞士风海报","swiss grid poster, typographic","瑞士海报"),
("拼贴海报","Collage Poster","多素材层叠拼贴的海报","collage poster, layered mixed media","拼贴海报"),
("大字标题海报","Big Typographic Poster","巨型字体为视觉主体的海报","big typographic poster, oversized type","大字标题海报"),
("主视觉","Hero Key Visual","广告活动的核心主图","hero key visual, campaign main visual","主视觉"),
("复古海报","Vintage Retro Poster","怀旧质感与配色的旧式海报","vintage retro poster, aged look","复古海报"),
("电影海报","Movie Poster","突出影片明星与氛围的宣传海报","movie poster, cinematic teaser","电影海报"),
("音乐节海报","Music Festival Poster","强视觉冲击的演出海报","music festival poster, bold graphic","音乐节海报"),
("日式海报","Japanese Poster Design","留白与禅意并存的日式海报","japanese poster design, minimal zen","日式海报"),
("孟菲斯海报","Memphis Style Poster","几何撞色、活泼的孟菲斯风海报","memphis style poster, playful geometric","孟菲斯海报"),
("渐变海报","Gradient Poster","以渐变色彩为主体的海报","gradient poster, color blend","渐变海报"),
("故障海报","Glitch Poster","数字故障错位的破坏感海报","glitch poster, digital distortion","故障海报")],"平面;海报")
block("信息设计",[
("信息图","Infographic","图文结合可视化解释信息","infographic, visual explanation","信息图"),
("图表","Data Chart","用图形量化展示数据的图","data chart, quantitative graph","图表"),
("数据可视化","Data Visualization","把数据转为可视图形的表达","data visualization, chart based","数据可视化"),
("图标系统","Icon Set","风格统一的一套图标","icon set, consistent pictograms","图标系统"),
("标识系统","Wayfinding Signage","引导方向的空间标识系统","wayfinding signage, directional system","标识系统"),
("流程图","Flowchart","用符号与连线表示流程","flowchart, process diagram","流程图"),
("地图设计","Map Design","地理信息可视化的地图","map design, cartography","地图设计"),
("时间线","Timeline Graphic","按时间顺序排列事件的图","timeline graphic, chronological","时间线"),
("仪表盘","Dashboard UI","汇总关键指标的可视化面板","dashboard UI, metrics panel","仪表盘")],"平面;信息")
block("印刷工艺",[
("CMYK印刷","CMYK Print","青品黄黑四色减色叠加的印刷成色方式","CMYK print, four-color process","CMYK印刷"),
("专色印刷","Pantone Spot Color","用预设专色油墨精准还原特定色","pantone spot color print","专色印刷"),
("烫金","Gold Foil Stamping","加压烫覆金属箔的金属光泽工艺","gold foil stamping, metallic foil","烫金"),
("UV局部光油","Spot UV Gloss","局部涂UV光油的亮泽凸起工艺","spot UV gloss coating","UV局部光油"),
("压凹凸","Emboss Deboss","加压做出凹凸立体触感的工艺","emboss deboss, tactile relief","压凹凸"),
("特种纸","Textured Specialty Paper","带特殊纹理或质感的印刷用纸","textured specialty paper","特种纸"),
("出血","Print Bleed","图像超出裁切线避免露白的预留","print bleed, edge margin","出血"),
("Riso孔版","Risograph Print","油墨套色的孔版印刷质感","risograph print, soy ink overlay","Riso孔版"),
("丝网印刷","Screen Print","丝网漏印的平面印刷工艺","screen print, silkscreen","丝网印刷"),
("击凸","Embossing","从背面加压顶出凸起的工艺","embossing, raised relief","击凸"),
("镂空","Die Cut","模切出透空形状的工艺","die cut, cutout shape","镂空"),
("覆膜","Lamination","表面覆塑料薄膜的保护工艺","lamination, protective film","覆膜")],"平面;印刷")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
