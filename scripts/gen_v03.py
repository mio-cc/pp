# -*- coding: utf-8 -*-
"""V03 绘画与艺术流派（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V03"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
def simple(cat,items,suf,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en.title(),"",V,cat,zh+"。","","","",en+" "+suf,"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("绘画媒介",[("油画","oil painting"),("水彩","watercolor"),("丙烯","acrylic painting"),("水粉","gouache"),("坦培拉","egg tempera"),("壁画","fresco mural"),("水墨","chinese ink wash"),("工笔","gongbi fine brush"),("写意水墨","xieyi ink"),("粉彩","soft pastel"),("油性彩铅","colored pencil"),("马克笔","marker illustration"),("铅笔素描","pencil sketch"),("炭笔","charcoal drawing"),("钢笔淡彩","pen and wash"),("木刻版画","woodcut print"),("铜版蚀刻","etching"),("丝网版画","silkscreen print"),("石版画","lithograph"),("数字绘画","digital painting"),("拼贴","collage"),("蛋彩坦培拉","tempera"),("水彩淡墨","ink and wash")],"art medium","绘画;媒介")
simple("艺术流派与时代",[("文艺复兴","renaissance"),("矫饰主义","mannerism"),("巴洛克","baroque"),("洛可可","rococo"),("新古典主义","neoclassical"),("浪漫主义","romanticism"),("写实主义","realism"),("印象派","impressionism"),("后印象派","post-impressionism"),("点彩派","pointillism"),("野兽派","fauvism"),("表现主义","expressionism"),("立体主义","cubism"),("未来主义","futurism"),("达达主义","dada"),("超现实主义","surrealism"),("抽象表现主义","abstract expressionism"),("色域绘画","color field painting"),("波普艺术","pop art"),("欧普艺术","op art"),("极简主义","minimalism"),("构成主义","constructivism"),("至上主义","suprematism"),("风格派","de stijl"),("象征主义","symbolism"),("纳比派","les nabis"),("分离派","vienna secession"),("新艺术运动","art nouveau"),("装饰艺术","art deco"),("超写实主义","photorealism"),("新表现主义","neo-expressionism"),("涂鸦街头艺术","graffiti street art"),("低眉艺术","lowbrow pop surrealism"),("浮世绘","ukiyo-e japanese woodblock"),("拜占庭圣像","byzantine icon"),("哥特","gothic"),("中国山水","chinese shanshui ink landscape"),("文人画","chinese literati painting"),("敦煌壁画","dunhuang mural")],"art movement","绘画;流派")
block("笔触与肌理",[
("厚涂","Impasto","厚堆立体","impasto thick textured","厚涂"),
("罩染","Glazing","透明层叠","glazing transparent layers","罩染"),
("干笔飞白","Drybrush","干笔","drybrush scratchy","干笔"),
("湿画法","Wet-on-Wet","湿融柔边","wet on wet soft","湿画法"),
("平涂","Flat","平整色块","flat color blocking","平涂"),
("可见笔触","Visible Strokes","笔触明显","visible brushstrokes","可见笔触"),
("刮刀","Palette Knife","刮刀块面","palette knife","刮刀"),
("泼墨","Splashed Ink","泼洒","splashed ink","泼墨"),
("皴法","Texture Stroke","山石皴","cun texture strokes","皴法"),
("晕染","Gradation","渐变晕","graded wash","晕染"),
("点描","Stippling","点状","stippling dots","点描"),
("拓印","Frottage","纹理拓印","frottage texture rubbing","拓印"),
("刮擦","Sgraffito","刮出底色","sgraffito scratch","刮擦")],"绘画;笔触")
block("造型与理论",[
("一点透视","One-Point","单灭点","one point perspective","一点透视"),
("两点透视","Two-Point","双灭点","two point perspective","两点透视"),
("三点透视","Three-Point","三灭点","three point perspective","三点透视"),
("空气透视","Atmospheric","远处淡化","atmospheric perspective haze","空气透视"),
("散点透视","Multi-Point","中国散点","multi-point scattered perspective","散点透视"),
("明暗五调","Tonal Values","明暗调子","five tonal values","明暗五调"),
("素描关系","Form Modeling","体积塑造","form modeling shading","素描关系"),
("人体解剖","Anatomy","骨骼肌肉","anatomy structure","人体解剖"),
("黄金分割","Golden Ratio","比例和谐","golden ratio","黄金分割"),
("色彩和谐","Color Harmony","色彩协调","color harmony","色彩和谐"),
("明暗对照法","Chiaroscuro","强光暗","chiaroscuro","明暗对照法"),
("薄涂法","Scumbling","半透明罩","scumbling","薄涂法")],"绘画;造型理论")
simple("代表性风格 / 名家",[("达芬奇风格","leonardo da vinci style sfumato"),("米开朗基罗风格","michelangelo style"),("拉斐尔风格","raphael style"),("卡拉瓦乔风格","caravaggio tenebrism style"),("维米尔风格","vermeer style"),("伦勃朗风格","rembrandt chiaroscuro style"),("透纳风格","turner atmospheric style"),("梵高风格","van gogh swirling impasto style"),("莫奈风格","monet impressionist style"),("德加风格","degas style"),("塞尚风格","cezanne style"),("高更风格","gauguin style"),("修拉风格","seurat pointillist style"),("蒙克风格","munch expressionist style"),("克林姆特风格","klimt gold ornament style"),("席勒风格","egon schiele style"),("毕加索风格","picasso cubist style"),("达利风格","dali surreal style"),("马格利特风格","magritte surreal style"),("埃舍尔风格","escher impossible geometry style"),("波洛克风格","jackson pollock drip style"),("罗斯科风格","rothko color field style"),("沃霍尔风格","andy warhol pop art style"),("蒙德里安风格","mondrian primary grid style"),("莫兰迪风格","morandi muted still life style"),("葛饰北斋风格","hokusai ukiyo-e style"),("歌川广重风格","hiroshige ukiyo-e style"),("齐白石风格","qi baishi ink style"),("张大千风格","zhang daqian splashed ink style"),("徐悲鸿风格","xu beihong ink horse style")],"art style","绘画;名家风格")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
