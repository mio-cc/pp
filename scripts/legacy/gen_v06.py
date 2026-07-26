# -*- coding: utf-8 -*-
"""V06 灯光与色彩科学（穷举级：色相×深浅浓淡系统化 + 命名色 + 色温/模型/搭配/管理）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V06"; rows=[]
def enrich_def(cat, defs):
    if len(defs.strip() + "。") >= 8:
        return defs
    if cat.startswith("色彩体系 /"):
        return defs.strip().rstrip("。.；;，, ") + "色调"
    return defs

def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        defs = enrich_def(cat, defs)
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))

# ===== 色温整档 =====
block("光度与照度 / 色温",[
("1800K","1800K Color Temp","极低色温暖黄如烛光的成色","candlelight warm 1800K color temperature","1800K 色温, 烛光极暖"),
("2200K","2200K Color Temp","低色温日落暖橙的成色氛围","sunset warm 2200K color temperature","2200K 色温, 落日暖橙"),
("2700K","2700K Color Temp","白炽灯暖白偏黄的居家色温","warm white 2700K color temperature","2700K 色温, 暖白居家"),
("3200K","3200K Color Temp","钨丝灯标准暖调色温","tungsten 3200K warm color temperature","3200K 色温, 钨丝灯暖"),
("4000K","4000K Color Temp","日光灯中性偏暖白的成色","neutral warm 4000K color temperature","4000K 色温, 中性暖白"),
("5000K","5000K Color Temp","接近正午日光的中性白","standard white 5000K color temperature","5000K 色温, 标准白"),
("5500K","5500K Color Temp","正午日光平衡白的标准色温","daylight 5500K color temperature","5500K 色温, 正午日光"),
("6500K","6500K Color Temp","阴天偏冷的标准白成色","cool daylight 6500K color temperature","6500K 色温, 标准冷白"),
("7500K","7500K Color Temp","阴天蓝天偏冷的成色色调","shade blue 7500K color temperature","7500K 色温, 阴天蓝"),
("10000K","10000K Color Temp","极高色温下深蓝偏紫的冷调","deep blue 10000K cold color temperature","10000K 色温, 极冷蓝调")],"色彩;色温")

# ===== 颜色体系：色相族 × 变体 系统化穷举 =====
block("色彩体系 / 红色系",[
("红色","Pure Red","标准正红、纯度最高的红","pure vivid red color","红色"),
("深红色","Deep Red","暗沉浓烈的红","deep dark red color","深红色"),
("浅红色","Light Red","明快偏粉的浅红","light pale red color","浅红色"),
("暗红色","Dark Red","低明度深沉的红","dark muted red color","暗红色"),
("亮红色","Bright Red","高亮鲜艳的红","bright vivid red color","亮红色"),
("柔红色","Soft Red","低饱和柔和的红","soft pastel red color","柔红色"),
("浓红色","Rich Red","高饱和浓重的红","rich saturated red color","浓红色"),
("灰红色","Muted Red","灰调低纯度的红","muted grayish red color","灰红色"),
("淡红色","Pale Red","极浅近乎白的红","pale washed red color","淡红色")],"色彩;颜色")
block("色彩体系 / 橙色系",[
("橙色","Pure Orange","标准正橙、活力暖色","pure vivid orange color","橙色"),
("深橙色","Deep Orange","暗沉浓烈的橙","deep dark orange color","深橙色"),
("浅橙色","Light Orange","明快偏淡的橙","light pale orange color","浅橙色"),
("暗橙色","Dark Orange","低明度深沉的橙","dark muted orange color","暗橙色"),
("亮橙色","Bright Orange","高亮鲜艳的橙","bright vivid orange color","亮橙色"),
("柔橙色","Soft Orange","低饱和柔和的橙","soft pastel orange color","柔橙色"),
("浓橙色","Rich Orange","高饱和浓重的橙","rich saturated orange color","浓橙色"),
("灰橙色","Muted Orange","灰调低纯度的橙","muted grayish orange color","灰橙色"),
("淡橙色","Pale Orange","极浅近乎白的橙","pale washed orange color","淡橙色")],"色彩;颜色")
block("色彩体系 / 黄色系",[
("黄色","Pure Yellow","标准正黄、明快亮色","pure vivid yellow color","黄色"),
("深黄色","Deep Yellow","暗沉偏橙的黄","deep dark yellow color","深黄色"),
("浅黄色","Light Yellow","明快偏白的黄","light pale yellow color","浅黄色"),
("暗黄色","Dark Yellow","低明度土感的黄","dark muted yellow color","暗黄色"),
("亮黄色","Bright Yellow","高亮鲜明的黄","bright vivid yellow color","亮黄色"),
("柔黄色","Soft Yellow","低饱和柔和的黄","soft pastel yellow color","柔黄色"),
("浓黄色","Rich Yellow","高饱和浓重的黄","rich saturated yellow color","浓黄色"),
("灰黄色","Muted Yellow","灰调低纯度的黄","muted grayish yellow color","灰黄色"),
("淡黄色","Pale Yellow","极浅近乎白的黄","pale washed yellow color","淡黄色")],"色彩;颜色")
block("色彩体系 / 黄绿系",[
("黄绿色","Pure Chartreuse","黄绿之间的高亮混合色","pure vivid chartreuse color","黄绿色"),
("深黄绿色","Deep Chartreuse","暗沉偏绿的黄绿","deep dark chartreuse color","深黄绿色"),
("浅黄绿色","Light Chartreuse","明快偏淡的黄绿","light pale chartreuse color","浅黄绿色"),
("暗黄绿色","Dark Chartreuse","低明度深沉的黄绿","dark muted chartreuse color","暗黄绿色"),
("亮黄绿色","Bright Chartreuse","高亮鲜活的黄绿","bright vivid chartreuse color","亮黄绿色"),
("柔黄绿色","Soft Chartreuse","低饱和柔和的黄绿","soft pastel chartreuse color","柔黄绿色"),
("浓黄绿色","Rich Chartreuse","高饱和浓重的黄绿","rich saturated chartreuse color","浓黄绿色"),
("灰黄绿色","Muted Chartreuse","灰调低纯度的黄绿","muted grayish chartreuse color","灰黄绿色"),
("淡黄绿色","Pale Chartreuse","极浅近乎白的黄绿","pale washed chartreuse color","淡黄绿色")],"色彩;颜色")
block("色彩体系 / 绿色系",[
("绿色","Pure Green","标准正绿、自然色","pure vivid green color","绿色"),
("深绿色","Deep Green","暗沉浓密的绿","deep dark green color","深绿色"),
("浅绿色","Light Green","明快偏淡的绿","light pale green color","浅绿色"),
("暗绿色","Dark Green","低明度深沉的绿","dark muted green color","暗绿色"),
("亮绿色","Bright Green","高亮鲜活的绿","bright vivid green color","亮绿色"),
("柔绿色","Soft Green","低饱和柔和的绿","soft pastel green color","柔绿色"),
("浓绿色","Rich Green","高饱和浓重的绿","rich saturated green color","浓绿色"),
("灰绿色","Muted Green","灰调低纯度的绿","muted grayish green color","灰绿色"),
("淡绿色","Pale Green","极浅近乎白的绿","pale washed green color","淡绿色")],"色彩;颜色")
block("色彩体系 / 青绿系",[
("青绿色","Pure Teal","蓝绿之间的沉稳色调","pure vivid teal color","青绿色"),
("深青绿色","Deep Teal","暗沉浓烈的青绿","deep dark teal color","深青绿色"),
("浅青绿色","Light Teal","明快偏淡的青绿","light pale teal color","浅青绿色"),
("暗青绿色","Dark Teal","低明度深沉的青绿","dark muted teal color","暗青绿色"),
("亮青绿色","Bright Teal","高亮鲜活的青绿","bright vivid teal color","亮青绿色"),
("柔青绿色","Soft Teal","低饱和柔和的青绿","soft pastel teal color","柔青绿色"),
("浓青绿色","Rich Teal","高饱和浓重的青绿","rich saturated teal color","浓青绿色"),
("灰青绿色","Muted Teal","灰调低纯度的青绿","muted grayish teal color","灰青绿色"),
("淡青绿色","Pale Teal","极浅近乎白的青绿","pale washed teal color","淡青绿色")],"色彩;颜色")
block("色彩体系 / 青色系",[
("青色","Pure Cyan","标准正青、鲜亮的蓝绿","pure vivid cyan color","青色"),
("深青色","Deep Cyan","暗沉浓烈的青","deep dark cyan color","深青色"),
("浅青色","Light Cyan","明快偏白的青","light pale cyan color","浅青色"),
("暗青色","Dark Cyan","低明度深沉的青","dark muted cyan color","暗青色"),
("亮青色","Bright Cyan","高亮鲜活的青","bright vivid cyan color","亮青色"),
("柔青色","Soft Cyan","低饱和柔和的青","soft pastel cyan color","柔青色"),
("浓青色","Rich Cyan","高饱和浓重的青","rich saturated cyan color","浓青色"),
("灰青色","Muted Cyan","灰调低纯度的青","muted grayish cyan color","灰青色"),
("淡青色","Pale Cyan","极浅近乎白的青","pale washed cyan color","淡青色")],"色彩;颜色")
block("色彩体系 / 蓝色系",[
("蓝色","Pure Blue","标准正蓝、平静深远","pure vivid blue color","蓝色"),
("深蓝色","Deep Blue","暗沉浓密的蓝","deep dark blue color","深蓝色"),
("浅蓝色","Light Blue","明快偏淡的天蓝","light pale blue color","浅蓝色"),
("暗蓝色","Dark Blue","低明度深沉的蓝","dark muted blue color","暗蓝色"),
("亮蓝色","Bright Blue","高亮鲜活的蓝","bright vivid blue color","亮蓝色"),
("柔蓝色","Soft Blue","低饱和柔和的蓝","soft pastel blue color","柔蓝色"),
("浓蓝色","Rich Blue","高饱和浓重的蓝","rich saturated blue color","浓蓝色"),
("灰蓝色","Muted Blue","灰调低纯度的蓝","muted grayish blue color","灰蓝色"),
("淡蓝色","Pale Blue","极浅近乎白的蓝","pale washed blue color","淡蓝色")],"色彩;颜色")
block("色彩体系 / 靛蓝系",[
("靛蓝色","Pure Indigo","蓝紫之间的深沉靛色","pure vivid indigo color","靛蓝色"),
("深靛蓝色","Deep Indigo","暗沉极深的靛蓝","deep dark indigo color","深靛蓝色"),
("浅靛蓝色","Light Indigo","明快偏淡的靛蓝","light pale indigo color","浅靛蓝色"),
("暗靛蓝色","Dark Indigo","低明度近黑的靛蓝","dark muted indigo color","暗靛蓝色"),
("亮靛蓝色","Bright Indigo","高亮鲜活的靛蓝","bright vivid indigo color","亮靛蓝色"),
("柔靛蓝色","Soft Indigo","低饱和柔和的靛蓝","soft pastel indigo color","柔靛蓝色"),
("浓靛蓝色","Rich Indigo","高饱和浓重的靛蓝","rich saturated indigo color","浓靛蓝色"),
("灰靛蓝色","Muted Indigo","灰调低纯度的靛蓝","muted grayish indigo color","灰靛蓝色"),
("淡靛蓝色","Pale Indigo","极浅近乎白的靛蓝","pale washed indigo color","淡靛蓝色")],"色彩;颜色")
block("色彩体系 / 紫色系",[
("紫色","Pure Purple","标准正紫、神秘优雅","pure vivid purple color","紫色"),
("深紫色","Deep Purple","暗沉浓烈的紫","deep dark purple color","深紫色"),
("浅紫色","Light Purple","明快偏粉的紫","light pale purple color","浅紫色"),
("暗紫色","Dark Purple","低明度深沉的紫","dark muted purple color","暗紫色"),
("亮紫色","Bright Purple","高亮鲜活的紫","bright vivid purple color","亮紫色"),
("柔紫色","Soft Purple","低饱和柔和的紫","soft pastel purple color","柔紫色"),
("浓紫色","Rich Purple","高饱和浓重的紫","rich saturated purple color","浓紫色"),
("灰紫色","Muted Purple","灰调低纯度的紫","muted grayish purple color","灰紫色"),
("淡紫色","Pale Purple","极浅近乎白的紫","pale washed purple color","淡紫色")],"色彩;颜色")
block("色彩体系 / 品红系",[
("品红色","Pure Magenta","标准正品红、高饱和蓝红","pure vivid magenta color","品红色"),
("深品红色","Deep Magenta","暗沉浓烈的品红","deep dark magenta color","深品红色"),
("浅品红色","Light Magenta","明快偏粉的品红","light pale magenta color","浅品红色"),
("暗品红色","Dark Magenta","低明度深沉的品红","dark muted magenta color","暗品红色"),
("亮品红色","Bright Magenta","高亮鲜活的品红","bright vivid magenta color","亮品红色"),
("柔品红色","Soft Magenta","低饱和柔和的品红","soft pastel magenta color","柔品红色"),
("浓品红色","Rich Magenta","高饱和浓重的品红","rich saturated magenta color","浓品红色"),
("灰品红色","Muted Magenta","灰调低纯度的品红","muted grayish magenta color","灰品红色"),
("淡品红色","Pale Magenta","极浅近乎白的品红","pale washed magenta color","淡品红色")],"色彩;颜色")
block("色彩体系 / 粉色系",[
("粉色","Pure Pink","标准正粉、甜美柔和","pure vivid pink color","粉色"),
("深粉色","Deep Pink","暗沉浓烈的粉","deep dark pink color","深粉色"),
("浅粉色","Light Pink","明快偏白的粉","light pale pink color","浅粉色"),
("暗粉色","Dark Pink","低明度深沉的粉","dark muted pink color","暗粉色"),
("亮粉色","Bright Pink","高亮鲜活的粉","bright vivid pink color","亮粉色"),
("柔粉色","Soft Pink","低饱和柔和的粉","soft pastel pink color","柔粉色"),
("浓粉色","Rich Pink","高饱和浓重的粉","rich saturated pink color","浓粉色"),
("灰粉色","Muted Pink","灰调低纯度的粉","muted grayish pink color","灰粉色"),
("淡粉色","Pale Pink","极浅近乎白的粉","pale washed pink color","淡粉色")],"色彩;颜色")
block("色彩体系 / 棕色系",[
("棕色","Pure Brown","标准正棕、大地暖色","pure vivid brown color","棕色"),
("深棕色","Deep Brown","暗沉浓重的棕","deep dark brown color","深棕色"),
("浅棕色","Light Brown","明快偏淡的棕","light pale brown color","浅棕色"),
("暗棕色","Dark Brown","低明度近黑的棕","dark muted brown color","暗棕色"),
("亮棕色","Bright Brown","高亮鲜活的棕","bright vivid brown color","亮棕色"),
("柔棕色","Soft Brown","低饱和柔和的棕","soft pastel brown color","柔棕色"),
("浓棕色","Rich Brown","高饱和浓重的棕","rich saturated brown color","浓棕色"),
("灰棕色","Muted Brown","灰调低纯度的棕","muted grayish brown color","灰棕色"),
("淡棕色","Pale Brown","极浅近乎白的棕","pale washed brown color","淡棕色")],"色彩;颜色")
block("色彩体系 / 灰中性系",[
("灰色","Pure Gray","标准中性灰、无彩","pure neutral gray color","灰色"),
("深灰色","Deep Gray","暗沉近黑的灰","deep dark gray color","深灰色"),
("浅灰色","Light Gray","明快偏白的灰","light pale gray color","浅灰色"),
("暗灰色","Dark Gray","低明度深沉的灰","dark muted gray color","暗灰色"),
("亮灰色","Bright Gray","高亮中性的灰","bright neutral gray color","亮灰色"),
("柔灰色","Soft Gray","低饱和柔和的灰","soft pastel gray color","柔灰色"),
("浓灰色","Rich Gray","高对比的中性灰","rich saturated gray color","浓灰色"),
("灰灰色","Muted Gray","灰调低纯度的灰","muted grayish neutral color","灰灰色"),
("淡灰色","Pale Gray","极浅近乎白的灰","pale washed gray color","淡灰色")],"色彩;颜色")

# ===== 命名特色色 =====
block("色彩体系 / 命名色",[
("克莱因蓝","Klein Blue","专利高纯度深钴蓝、极致纯净","intense international klein blue","克莱因蓝"),
("蒂芙尼蓝","Tiffany Blue","知更鸟蛋壳般柔亮的天蓝","tiffany robin egg blue","蒂芙尼蓝"),
("普鲁士蓝","Prussian Blue","沉静深邃的含铁深蓝","dark prussian blue","普鲁士蓝"),
("孔雀蓝","Peacock Blue","如孔雀羽毛般的青蓝光泽","peacock blue-green iridescent","孔雀蓝"),
("藏青","Navy","深邃沉稳的深海军蓝","deep navy blue","藏青"),
("湖蓝","Lake Blue","清澈如湖面的明亮浅蓝","clear lake blue","湖蓝"),
("酒红","Burgundy","如红酒般深邃的暗紫红","wine burgundy deep red","酒红"),
("绯红","Scarlet","高饱和鲜亮夺目的红","bright vivid scarlet","绯红"),
("胭脂红","Carmine","传统胭脂般浓烈的深红","carmine crimson red","胭脂红"),
("珊瑚粉","Coral","温暖如珊瑚般的柔粉橙","warm coral pink","珊瑚粉"),
("藕荷色","Dusty Lilac","灰调偏紫的淡雅藕荷色","muted dusty lilac","藕荷色"),
("薰衣草紫","Lavender","薰衣草花般的柔和浅紫","soft lavender purple","薰衣草紫"),
("丁香紫","Lilac","丁香花般轻柔的浅淡紫","light lilac","丁香紫"),
("莫兰迪灰粉","Morandi Pink","莫兰迪式低饱和灰粉","morandi muted gray pink","莫兰迪灰粉"),
("祖母绿","Emerald","高饱和翠绿如祖母绿宝石","rich emerald green","祖母绿"),
("墨绿","Pine Green","深沉如墨的浓绿","deep pine green","墨绿"),
("橄榄绿","Olive","偏灰黄的橄榄果实色","muted olive green","橄榄绿"),
("薄荷绿","Mint","清凉薄荷般的新鲜浅绿","fresh mint green","薄荷绿"),
("抹茶绿","Matcha","日式抹茶粉般的柔灰绿","soft matcha green","抹茶绿"),
("芥末黄","Mustard","如芥末般复古的浓暗黄","retro mustard yellow","芥末黄"),
("姜黄","Turmeric","姜根般温暖明亮的黄","warm turmeric yellow","姜黄"),
("土黄赭石","Ochre","大地赭黄土般的暖黄","earthy ochre","土黄赭石"),
("驼色","Camel","骆驼毛般温暖的中性棕","warm camel tan","驼色"),
("焦糖色","Caramel","焦糖般浓暖的棕橙色","caramel brown","焦糖色"),
("巧克力棕","Chocolate","巧克力般深沉的棕","dark chocolate brown","巧克力棕"),
("米白","Off White","略带暖调的乳白","warm off-white cream","米白"),
("象牙白","Ivory","象牙般温润的柔白","soft ivory white","象牙白"),
("炭黑","Charcoal","介于黑与灰之间的深炭色","dark charcoal","炭黑"),
("银灰","Silver Gray","金属银光泽的中性灰","metallic silver gray","银灰"),
("玫瑰金","Rose Gold","金铜合金般的暖粉金属色","rose gold","玫瑰金"),
("香槟金","Champagne","香槟酒般的柔金光泽","champagne gold","香槟金")],"色彩;命名色")

# ===== 模型/空间 =====
block("色彩科学 / 色彩模型与空间",[
("RGB加色","RGB Additive","红绿蓝三原光叠加混合的成色模型","RGB additive color mixing model","RGB加色"),
("CMYK减色","CMYK Subtractive","青品黄黑四色油墨减色混合的印刷模型","CMYK subtractive print model","CMYK减色"),
("HSL","HSL Model","色相饱和明度三维圆柱的色彩模型","HSL hue saturation lightness model","HSL"),
("Lab","Lab Color","设备无关的感知均匀色彩空间","Lab device-independent color space","Lab"),
("色相","Hue","区分颜色种类的光谱属性","hue color family property","色相"),
("饱和度","Saturation","色彩鲜艳纯度的高低","saturation intensity","饱和度"),
("明度","Value","色彩的明暗深浅程度","brightness value lightness","明度"),
("sRGB","sRGB","网络显示通用的标准色域空间","sRGB standard web color gamut","sRGB"),
("Adobe RGB","Adobe RGB","覆盖更多绿色域的印刷标准色域","Adobe RGB wide gamut","Adobe RGB"),
("DCI-P3","DCI-P3","电影工业数字投影的宽色域","DCI-P3 cinema color gamut","DCI-P3"),
("Rec.2020","Rec.2020","超高清广播的极限宽色域","Rec.2020 ultra wide HDR gamut","Rec.2020")],"色彩;模型空间")

# ===== 搭配 =====
block("色彩搭配",[
("互补色","Complementary","色轮对角180度的冷暖撞色搭配","complementary color contrast pairing","互补色"),
("邻近色","Analogous","色轮相邻两三色的和谐柔和搭配","analogous harmony adjacent colors","邻近色"),
("三角配色","Triadic","色轮等距三色的平衡活泼搭配","triadic three-way color scheme","三角配色"),
("分裂互补","Split-Complementary","一色加其互补两侧色的柔和对比搭配","split complementary pairing","分裂互补"),
("四角配色","Tetradic","两组互补色矩形的丰富搭配","tetradic double-complementary scheme","四角配色"),
("单色系","Monochromatic","同色相不同明暗深浅的统一搭配","monochromatic single-hue shades","单色系"),
("同类色","Tonal","同色域微调明暗饱和的和谐搭配","tonal palette similar hues","同类色"),
("无彩色","Achromatic","纯黑白灰的无彩搭配","achromatic black white gray","无彩色")],"色彩;搭配")

# ===== 色调氛围 =====
block("色调与氛围",[
("暖色调","Warm Tone","以橙红黄为主体的温暖成色倾向","warm tone orange red dominant","暖色调"),
("冷色调","Cool Tone","以蓝青为主体的冷清成色倾向","cool tone blue cyan dominant","冷色调"),
("高饱和活力","High Saturation","色彩鲜艳纯度高、视觉冲击力强的成色","high saturation vivid lively","高饱和"),
("低饱和高级","Muted Desaturated","色彩纯度降低、灰调含蓄高级的成色","muted desaturated sophisticated tone","低饱和"),
("莫兰迪色","Morandi","低灰度柔和如莫兰迪画的高级灰调","morandi muted gray palette","莫兰迪色"),
("马卡龙色","Macaron","粉嫩甜美的柔和浅色糖果调","macaron pastel sweet tones","马卡龙色"),
("复古胶片色","Retro Film","怀旧褪色偏暖的胶片感成色","retro faded film color tone","复古胶片色"),
("赛博霓虹色","Cyber Neon","紫粉青霓虹高亮的赛博朋克成色","cyberpunk neon high-key palette","赛博霓虹色"),
("撞色","Color Blocking","高对比色块拼搭的醒目效果","bold color blocking contrast","撞色"),
("黑金奢华","Black Gold","黑底配金色的高奢质感成色","black and gold luxury palette","黑金奢华"),
("大地色系","Earth Tone","棕绿赭等自然的大地色组合","earth tone natural palette","大地色系"),
("糖果色","Candy Color","明亮快活如糖果的色彩组合","bright candy color palette","糖果色")],"色彩;色调")

# ===== 光质 + 管理感知 =====
block("光度与照度 / 光的属性",[
("高显色CRI","High CRI","光源还原物体真实色彩的准确度","high CRI accurate color rendering","高显色"),
("硬光","Hard Light","小光源产生的锐利阴影与高反差","hard light crisp sharp shadows","硬光"),
("柔光","Soft Light","大光源散射产生的柔和低反差","soft diffused gentle light","柔光"),
("体积光","Volumetric Light","丁达尔效应下的可见光束","volumetric god rays light beams","体积光"),
("逆光","Backlight","光源在主体背后产生轮廓发光","backlight rim glow silhouette","逆光"),
("散射光","Diffused","经介质散射后均匀柔和无方向的光","diffused even omnidirectional light","散射光")],"色彩;光质")
block("色彩管理与感知",[
("白平衡","White Balance","校准画面偏色使白色准确的调节","white balance color correction","白平衡"),
("色调映射","Tone Mapping","将HDR高动态压缩到显示范围的映射","HDR tone mapping compression","色调映射"),
("色彩对比","Color Contrast","冷暖明暗等色彩属性的差异感","color contrast visual difference","色彩对比"),
("同时对比","Simultaneous Contrast","相邻色彩因视觉互影响产生偏移","simultaneous contrast effect","同时对比"),
("HDR","HDR","高动态范围保留亮暗全部细节","high dynamic range","HDR"),
("色彩恒常","Color Constancy","人脑在不同光下仍认出同一色彩","color constancy perception","色彩恒常")],"色彩;管理感知")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
