# -*- coding: utf-8 -*-
"""V03 绘画与艺术流派（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V03"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("绘画媒介",[
("油画","Oil Painting","厚重层次、色彩浓郁luminous","oil painting, rich layered luminous color","油画, 浓郁层次"),
("水彩","Watercolor","透明水润晕染","watercolor, transparent luminous washes","水彩, 透明晕染"),
("丙烯","Acrylic","速干鲜艳","acrylic painting, fast-dry vivid","丙烯, 鲜艳"),
("水粉","Gouache","不透明哑光平涂","gouache, opaque matte flat color","水粉, 哑光平涂"),
("坦培拉","Tempera","蛋彩细腻古典","egg tempera, fine classical","坦培拉, 蛋彩古典"),
("壁画","Fresco","湿壁画矿物质感","fresco mural, mineral texture","壁画, 湿壁"),
("水墨","Ink Wash","东方水墨写意","chinese ink wash painting","水墨, 写意"),
("粉彩","Pastel","柔和粉质","soft pastel, powdery","粉彩, 柔和粉质"),
("彩铅","Colored Pencil","细腻彩铅","colored pencil drawing","彩铅"),
("马克笔","Marker","设计马克笔","marker illustration","马克笔, 设计"),
("铅笔素描","Pencil Sketch","铅笔线稿","pencil sketch, graphite","铅笔素描"),
("炭笔","Charcoal","炭笔浓黑明暗","charcoal drawing, bold tonal","炭笔, 浓黑明暗"),
("钢笔淡彩","Pen and Wash","钢笔线+淡彩","pen and ink wash","钢笔淡彩"),
("木刻版画","Woodcut","木刻黑白肌理","woodcut print, bold texture","木刻版画"),
("铜版画","Etching","蚀刻细线","etching, fine engraved lines","铜版画, 蚀刻"),
("丝网版画","Screen Print","波普平涂套色","silkscreen, pop flat color","丝网版画, 套色"),
("数字绘画","Digital Painting","数位板厚涂","digital painting, concept art","数字绘画")],"绘画;媒介")

block("艺术流派与时代",[
("文艺复兴","Renaissance","古典写实和谐","renaissance painting, classical realism","文艺复兴, 古典写实"),
("巴洛克","Baroque","戏剧明暗动感","baroque, dramatic chiaroscuro movement","巴洛克, 戏剧明暗"),
("洛可可","Rococo","华丽柔美装饰","rococo, ornate pastel elegance","洛可可, 华丽柔美"),
("新古典主义","Neoclassicism","庄重理性线条","neoclassical, ordered linear","新古典主义"),
("浪漫主义","Romanticism","情感壮丽自然","romanticism, dramatic emotional nature","浪漫主义"),
("写实主义","Realism","真实日常","realism, truthful everyday","写实主义"),
("印象派","Impressionism","光色瞬间笔触","impressionism, loose brushstrokes light","印象派, 光色笔触"),
("后印象派","Post-Impressionism","主观色彩结构","post-impressionism, expressive color","后印象派"),
("点彩派","Pointillism","色点并置","pointillism, dots of color","点彩派, 色点"),
("野兽派","Fauvism","狂野纯色","fauvism, wild vivid color","野兽派, 纯色"),
("表现主义","Expressionism","主观扭曲情绪","expressionism, distorted emotional","表现主义, 扭曲情绪"),
("立体主义","Cubism","几何多视点","cubism, fragmented geometric multiple viewpoints","立体主义, 几何多视点"),
("未来主义","Futurism","速度动感","futurism, motion speed","未来主义"),
("达达主义","Dada","拼贴反叛","dada, collage anti-art","达达, 拼贴"),
("超现实主义","Surrealism","梦境荒诞并置","surrealism, dreamlike bizarre juxtaposition","超现实主义, 梦境"),
("抽象表现主义","Abstract Expressionism","泼洒抽象","abstract expressionism, gestural","抽象表现主义"),
("波普艺术","Pop Art","大众文化鲜艳","pop art, bold commercial","波普艺术"),
("极简主义","Minimalism","极简几何","minimalism, geometric reduction","极简主义"),
("浮世绘","Ukiyo-e","日本木刻平面","ukiyo-e japanese woodblock flat","浮世绘"),
("拜占庭","Byzantine","金底圣像","byzantine, gold icon","拜占庭, 金底圣像"),
("哥特","Gothic","尖拱宗教","gothic, religious pointed","哥特"),
("中国山水","Chinese Landscape","水墨山水留白","chinese shanshui ink landscape","中国山水, 留白"),
("装饰艺术","Art Deco","几何奢华对称","art deco, geometric luxe symmetry","装饰艺术 Art Deco"),
("新艺术运动","Art Nouveau","有机曲线植物","art nouveau, organic flowing lines","新艺术, 有机曲线")],"绘画;流派")

block("笔触与肌理",[
("厚涂","Impasto","厚堆笔触立体","impasto, thick textured strokes","厚涂, 立体笔触"),
("罩染","Glazing","透明层叠通透","glazing, transparent layers luminous","罩染, 透明层叠"),
("干笔","Drybrush","干笔飞白","drybrush, scratchy texture","干笔, 飞白"),
("湿画法","Wet-on-Wet","湿融柔边","wet-on-wet, soft blended edges","湿画法, 柔边"),
("平涂","Flat Color","平整色块","flat color blocking","平涂, 色块"),
("可见笔触","Visible Brushstrokes","笔触明显","visible expressive brushstrokes","可见笔触"),
("刮刀","Palette Knife","刮刀块面","palette knife, bold planes","刮刀"),
("泼墨","Splashed Ink","泼洒水墨","splashed ink, spontaneous","泼墨"),
("皴法","Texture Strokes","山石皴法","texture strokes shanshui","皴法"),
("晕染","Gradation Wash","渐变晕染","graded wash gradation","晕染")],"绘画;笔触")

block("造型语言",[
("一点透视","One-Point Perspective","单灭点纵深","one-point perspective","一点透视"),
("两点透视","Two-Point Perspective","双灭点立体","two-point perspective","两点透视"),
("三点透视","Three-Point Perspective","俯仰三灭点","three-point perspective","三点透视"),
("空气透视","Atmospheric Perspective","远处淡蓝虚化","atmospheric perspective, distant haze","空气透视, 远处淡化"),
("明暗五调","Tonal Values","高光灰中调阴影反光","five tonal values, light to shadow","明暗五调"),
("素描关系","Form Modeling","体积塑造","form modeling, volume shading","素描关系, 体积"),
("人体解剖","Anatomy","骨骼肌肉结构","anatomy, skeletal muscle structure","人体解剖"),
("黄金分割","Golden Ratio","比例和谐","golden ratio proportion","黄金分割")],"绘画;造型")

block("代表性风格",[
("梵高风格","Van Gogh Style","漩涡厚涂笔触","in the style of Van Gogh, swirling impasto","梵高风格, 漩涡笔触"),
("莫奈风格","Monet Style","印象光色","in the style of Monet, impressionist light","莫奈风格"),
("达利风格","Dalí Style","超现实融化","in the style of Dali, surreal melting","达利风格, 超现实"),
("葛饰北斋风格","Hokusai Style","浮世绘波浪","in the style of Hokusai, ukiyo-e wave","北斋风格, 浮世绘"),
("克林姆特风格","Klimt Style","金箔装饰","in the style of Klimt, gold ornament","克林姆特, 金箔"),
("伦勃朗风格","Rembrandt Style","暗调明暗对照","in the style of Rembrandt, chiaroscuro","伦勃朗风格, 明暗"),
("莫兰迪风格","Morandi Style","灰调静物","in the style of Morandi, muted still life","莫兰迪, 灰调"),
("蒙德里安风格","Mondrian Style","红黄蓝格子","in the style of Mondrian, primary grid","蒙德里安, 格子")],"绘画;风格")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} generated: {len(rows)} | total: {len(allrows)}")
