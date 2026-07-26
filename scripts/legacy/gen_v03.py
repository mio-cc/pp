# -*- coding: utf-8 -*-
"""V03 绘画与艺术流派（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V03"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("绘画媒介",[
("油画","Oil Painting","以亚麻仁油调颜料的厚涂慢干媒介","oil painting, rich thick medium","油画"),
("水彩","Watercolor","水溶性透明颜料在水彩纸上晕染","watercolor, transparent wash","水彩"),
("丙烯","Acrylic Painting","快干合成树脂颜料、可厚可薄的媒介","acrylic painting, fast drying","丙烯"),
("水粉","Gouache","不透明水溶性颜料、色块平实","gouache, opaque matte","水粉"),
("坦培拉","Egg Tempera","蛋黄调和颜料的古典坦培拉媒介","egg tempera, ancient medium","坦培拉"),
("壁画","Fresco Mural","湿灰泥墙面上矿物颜料作画","fresco mural, wall painting","壁画"),
("水墨","Chinese Ink Wash","水墨在宣纸上渗化晕染的东方媒介","chinese ink wash, sumi-e","水墨"),
("工笔","Gongbi Fine Brush","细笔勾线层层渲染的工整画法","gongbi fine brush, detailed line","工笔"),
("写意水墨","Xieyi Ink","大笔挥洒不求形似的写意画法","xieyi ink, expressive freehand","写意水墨"),
("粉彩","Soft Pastel","粉质条状颜料直接涂抹的柔和媒介","soft pastel, powdery blend","粉彩"),
("油性彩铅","Colored Pencil","油性彩色铅笔叠加细腻的媒介","colored pencil, layered detail","油性彩铅"),
("马克笔","Marker Illustration","酒精/水性马克笔平涂速绘媒介","marker illustration, flat marker","马克笔"),
("铅笔素描","Pencil Sketch","石墨铅笔排线塑形的素描媒介","pencil sketch, graphite shading","铅笔素描"),
("炭笔","Charcoal Drawing","炭条炭笔深黑松散的素描媒介","charcoal drawing, deep black","炭笔"),
("钢笔淡彩","Pen and Wash","钢笔勾线加水彩淡彩的混合媒介","pen and wash, ink line watercolor","钢笔淡彩"),
("木刻版画","Woodcut Print","木板刻去留阳线压印的版种","woodcut print, relief block","木刻版画"),
("铜版蚀刻","Etching","酸腐蚀金属凹版印刷的版种","etching, intaglio copper plate","铜版蚀刻"),
("丝网版画","Silkscreen Print","丝网漏孔套色的孔版版种","silkscreen print, screen stencil","丝网版画"),
("石版画","Lithograph","油水相斥在石版上平版印刷","lithograph, flat stone print","石版画"),
("数字绘画","Digital Painting","数位板与绘画软件的电脑媒介","digital painting, tablet software","数字绘画"),
("拼贴","Collage","剪贴现成物组合的混合媒介","collage, mixed media cutout","拼贴"),
("蛋彩坦培拉","Tempera","蛋乳化颜料薄涂的古典媒介","tempera, egg emulsion paint","蛋彩坦培拉"),
("水彩淡墨","Ink and Wash","水墨与水彩交融的写意淡彩","ink and wash, soft wash blend","水彩淡墨")],"绘画;媒介")
block("艺术流派与时代",[
("文艺复兴","Renaissance","14-16世纪以人为本、复兴古典的人文艺术","renaissance, classical humanism","文艺复兴"),
("矫饰主义","Mannerism","文艺复兴后期拉长扭曲造型的风格","mannerism, elongated stylized","矫饰主义"),
("巴洛克","Baroque","17世纪戏剧光影与动态夸张的风格","baroque, dramatic chiaroscuro","巴洛克"),
("洛可可","Rococo","18世纪宫廷轻盈繁复的装饰风格","rococo, ornate pastel","洛可可"),
("新古典主义","Neoclassical","回归希腊罗马理性的庄重风格","neoclassical, grand rational","新古典主义"),
("浪漫主义","Romanticism","崇尚情感自然与个人激情的风格","romanticism, emotional sublime","浪漫主义"),
("写实主义","Realism","如实描绘平民日常的现实风格","realism, everyday truth","写实主义"),
("印象派","Impressionism","捕捉光色瞬间外光写生的流派","impressionism, light color moment","印象派"),
("后印象派","Post-Impressionism","强调主观结构与情感的延伸流派","post-impressionism, subjective form","后印象派"),
("点彩派","Pointillism","以纯色点并置混色的分色流派","pointillism, dot color mixing","点彩派"),
("野兽派","Fauvism","大胆纯色平涂的激进色彩流派","fauvism, bold pure color","野兽派"),
("表现主义","Expressionism","扭曲变形宣泄内心焦虑的流派","expressionism, distorted emotion","表现主义"),
("立体主义","Cubism","多视角同时解构重组的流派","cubism, multi-angle fragmentation","立体主义"),
("未来主义","Futurism","歌颂速度机械与动态的流派","futurism, speed machine motion","未来主义"),
("达达主义","Dada","反艺术反理性的虚无颠覆流派","dada, anti-art absurd","达达主义"),
("超现实主义","Surrealism","梦境潜意识荒诞并置的流派","surrealism, dream unconscious","超现实主义"),
("抽象表现主义","Abstract Expressionism","情感泼洒与色场的美国抽象流派","abstract expressionism, action painting","抽象表现主义"),
("色域绘画","Color Field Painting","大片平涂色彩营造氛围的抽象","color field painting, flat hue","色域绘画"),
("波普艺术","Pop Art","挪用大众图像商业符号的流派","pop art, mass media imagery","波普艺术"),
("欧普艺术","Op Art","几何视错觉欺骗眼睛的光效流派","op art, optical illusion","欧普艺术"),
("极简主义","Minimalism","极简几何重复去除多余的流派","minimalism, geometric reduction","极简主义"),
("构成主义","Constructivism","工业材料服务于社会的俄国流派","constructivism, industrial geometry","构成主义"),
("至上主义","Suprematism","纯几何与至上情感的俄国抽象","suprematism, pure geometric","至上主义"),
("风格派","De Stijl","红黄蓝三原色直线的荷兰几何派","de stijl, primary color grid","风格派"),
("象征主义","Symbolism","以象征隐喻暗示神秘意涵的流派","symbolism, mystical metaphor","象征主义"),
("纳比派","Les Nabis","强调装饰性与主观色彩的法国流派","les nabis, decorative subjective","纳比派"),
("分离派","Vienna Secession","维也纳脱离学院的新艺术分支","vienna secession, ornamental line","分离派"),
("新艺术运动","Art Nouveau","曲线藤蔓有机线条的装饰运动","art nouveau, organic curve","新艺术运动"),
("装饰艺术","Art Deco","几何对称机械美感的装饰风格","art deco, geometric glamour","装饰艺术"),
("超写实主义","Photorealism","极致逼真超越照片的写实流派","photorealism, hyper detailed","超写实主义"),
("新表现主义","Neo-Expression","80年代回归具象粗放的流派","neo-expressionism, raw figurative","新表现主义"),
("涂鸦街头艺术","Graffiti Street Art","街头喷漆即兴的城市亚文化","graffiti street art, urban spray","涂鸦街头艺术"),
("低眉艺术","Lowbrow Pop Surrealism","怪诞卡通融合波普的地下艺术","lowbrow pop surrealism, weird cartoon","低眉艺术"),
("浮世绘","Ukiyo-e","江户木版多色套印的日本风俗画","ukiyo-e japanese woodblock","浮世绘"),
("拜占庭圣像","Byzantine Icon","金色背景平面金箔的宗教圣像","byzantine icon, gold background","拜占庭圣像"),
("哥特","Gothic","尖拱细长向上的中世纪宗教风格","gothic, pointed arch","哥特"),
("中国山水","Chinese Shanshui","以山川林泉写意境的山水画","chinese shanshui ink landscape","中国山水"),
("文人画","Chinese Literati Painting","诗书画印一体的士大夫绘画","chinese literati painting","文人画"),
("敦煌壁画","Dunhuang Mural","丝路石窟矿物彩绘的佛教壁画","dunhuang mural, mineral pigment","敦煌壁画")],"绘画;流派")
block("笔触与肌理",[
("厚涂","Impasto","厚颜料堆叠形成凸起肌理","impasto thick textured","厚涂"),
("罩染","Glazing","透明色层叠加调整明暗色相","glazing transparent layers","罩染"),
("干笔飞白","Drybrush","笔墨偏干留下断续飞白纹理","drybrush scratchy","干笔飞白"),
("湿画法","Wet-on-Wet","湿底上作画产生柔边融合效果","wet on wet soft","湿画法"),
("平涂","Flat","均匀铺色形成平整色块","flat color blocking","平涂"),
("可见笔触","Visible Strokes","保留笔刷方向和力度痕迹","visible brushstrokes","可见笔触"),
("刮刀","Palette Knife","以刮刀推抹形成厚重块面","palette knife","刮刀"),
("泼墨","Splashed Ink","泼洒墨色形成偶发流动痕迹","splashed ink","泼墨"),
("皴法","Texture Stroke","以皴笔表现山石纹理结构","cun texture strokes","皴法"),
("晕染","Gradation","色墨渐次扩散形成柔和过渡","graded wash","晕染"),
("点描","Stippling","密集点状笔触构成明暗色面","stippling dots","点描"),
("拓印","Frottage","压印物体表面纹理形成图案","frottage texture rubbing","拓印"),
("刮擦","Sgraffito","刮开表层露出底色或纹理","sgraffito scratch","刮擦")],"绘画;笔触")
block("造型与理论",[
("一点透视","One-Point","以单一灭点组织空间深度","one point perspective","一点透视"),
("两点透视","Two-Point","以两个灭点表现转角空间","two point perspective","两点透视"),
("三点透视","Three-Point","加入垂直灭点强化仰俯视角","three point perspective","三点透视"),
("空气透视","Atmospheric","以远处淡化表现空间距离","atmospheric perspective haze","空气透视"),
("散点透视","Multi-Point","多视点游移组织画面空间","multi-point scattered perspective","散点透视"),
("明暗五调","Tonal Values","用五级明暗概括体积转折","five tonal values","明暗五调"),
("素描关系","Form Modeling","用明暗结构塑造物体体积","form modeling shading","素描关系"),
("人体解剖","Anatomy","以骨骼肌肉关系支撑造型","anatomy structure","人体解剖"),
("黄金分割","Golden Ratio","以黄金比例安排画面关系","golden ratio","黄金分割"),
("色彩和谐","Color Harmony","让色相明度纯度形成协调","color harmony","色彩和谐"),
("明暗对照法","Chiaroscuro","用强烈光暗反差制造戏剧性","chiaroscuro","明暗对照法"),
("薄涂法","Scumbling","以半透明薄层叠加色彩变化","scumbling","薄涂法")],"绘画;造型理论")
block("代表性风格 / 名家",[
("达芬奇风格","Leonardo da Vinci Style","晕涂朦胧、科学严谨的文艺复兴大师风","leonardo da vinci style sfumato","达芬奇风格"),
("米开朗基罗风格","Michelangelo Style","雄健肌肉、宏大史诗的雕塑感画风","michelangelo style","米开朗基罗风格"),
("拉斐尔风格","Raphael Style","和谐均衡、古典完美的圣母画风","raphael style","拉斐尔风格"),
("卡拉瓦乔风格","Caravaggio Style","强光暗对比的戏剧性明暗法","caravaggio tenebrism style","卡拉瓦乔风格"),
("维米尔风格","Vermeer Style","静谧室内与珍珠光的荷兰风俗画","vermeer style","维米尔风格"),
("伦勃朗风格","Rembrandt Style","金光三角光与笔触厚重的肖像风","rembrandt chiaroscuro style","伦勃朗风格"),
("透纳风格","Turner Style","光雾朦胧的浪漫主义风景风","turner atmospheric style","透纳风格"),
("梵高风格","Van Gogh Style","旋涡笔触与浓烈色彩的后期印象","van gogh swirling impasto style","梵高风格"),
("莫奈风格","Monet Style","捕捉光色瞬间变化的印象派风","monet impressionist style","莫奈风格"),
("德加风格","Degas Style","捕捉芭蕾舞者动态的印象派风","degas style","德加风格"),
("塞尚风格","Cezanne Style","几何色块建构的现代主义之父","cezanne style","塞尚风格"),
("高更风格","Gauguin Style","平涂纯色的原始主义热带画风","gauguin style","高更风格"),
("修拉风格","Seurat Style","科学并置色点的点彩派风","seurat pointillist style","修拉风格"),
("蒙克风格","Munch Style","扭曲线条宣泄焦虑的表现主义风","munch expressionist style","蒙克风格"),
("克林姆特风格","Klimt Style","金箔装饰与情欲象征的维也纳风","klimt gold ornament style","克林姆特风格"),
("席勒风格","Egon Schiele Style","骨感扭曲轮廓的表现主义肖像","egon schiele style","席勒风格"),
("毕加索风格","Picasso Style","多面切割重组的立体主义风","picasso cubist style","毕加索风格"),
("达利风格","Dali Style","超现实荒诞并置的梦境画风","dali surreal style","达利风格"),
("马格利特风格","Magritte Style","日常物错置的超现实智性画","magritte surreal style","马格利特风格"),
("埃舍尔风格","Escher Style","不可能几何与视错觉的理性画","escher impossible geometry style","埃舍尔风格"),
("波洛克风格","Jackson Pollock Style","滴洒泼颜料的抽象表现主义","jackson pollock drip style","波洛克风格"),
("罗斯科风格","Rothko Style","色块边缘晕染的色域绘画","rothko color field style","罗斯科风格"),
("沃霍尔风格","Andy Warhol Style","丝网重复与商业图像的波普","andy warhol pop art style","沃霍尔风格"),
("蒙德里安风格","Mondrian Style","红黄蓝直线格子的风格派","mondrian primary grid style","蒙德里安风格"),
("莫兰迪风格","Morandi Style","低饱和灰调静物的克制画风","morandi muted still life style","莫兰迪风格"),
("葛饰北斋风格","Hokusai Style","大胆构图与线条的浮世绘","hokusai ukiyo-e style","葛饰北斋风格"),
("歌川广重风格","Hiroshige Style","抒情风景与渐变天空的浮世绘","hiroshige ukiyo-e style","歌川广重风格"),
("齐白石风格","Qi Baishi Style","工写结合的花鸟虫鱼水墨","qi baishi ink style","齐白石风格"),
("张大千风格","Zhang Daqian Style","泼墨泼彩的现代山水风","zhang daqian splashed ink style","张大千风格"),
("徐悲鸿风格","Xu Beihong Style","中西融合的写意奔马水墨","xu beihong ink horse style","徐悲鸿风格")],"绘画;名家风格")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
