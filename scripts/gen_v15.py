# -*- coding: utf-8 -*-
"""V15 视觉风格、审美标签与时代风格（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V15"; rows=[]
def block(cat,items,tags):
    for zh,en,defs in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",en+" aesthetic","",zh,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("类型与审美标签",[
("赛博朋克","cyberpunk neon dystopia","霓虹科技与低生活感并置的反乌托邦风格"),
("蒸汽朋克","steampunk victorian gears","维多利亚机械齿轮和蒸汽动力构成的复古科幻"),
("柴油朋克","dieselpunk interwar","两战时期工业机械和硬朗金属感的架空风格"),
("生物朋克","biopunk organic tech","有机组织与生物科技融合的怪异未来风格"),
("废土风","post-apocalyptic wasteland","末日荒漠、锈蚀装备和资源匮乏感的风格"),
("国潮","chinese guochao trendy","中国传统符号与当代潮流设计融合的风格"),
("侘寂","wabi-sabi rustic imperfect","接受残缺、粗粝和时间痕迹的朴素审美"),
("极简主义","minimalist","用少量元素、留白和秩序表达的克制风格"),
("孟菲斯","memphis bold geometric","鲜艳色块和几何图案构成的后现代玩味风格"),
("蒸汽波","vaporwave retro digital","复古电脑、粉紫渐变和消费符号的网络美学"),
("故障波","glitchcore","数字错位、噪声和失真构成的故障审美"),
("Y2K千禧","y2k metallic millennium","金属塑料、低腰和早期互联网未来感的风格"),
("暗黑哥特","dark gothic","尖拱黑色蕾丝和宗教阴影构成的暗黑风格"),
("治愈系","cozy healing","柔和色彩与温暖日常感带来的舒缓风格"),
("梦核","dreamcore surreal nostalgic","梦境般失真空间和怀旧碎片构成的超现实感"),
("怪核","weirdcore uncanny","低保真图像和不安符号形成的诡异网络美学"),
("阈限空间","liminal space eerie","空荡过渡场所带来熟悉又陌生的不安感"),
("故障艺术","glitch art","利用数字错误和信号断裂形成的视觉艺术"),
("低多边形","low poly","用少量多边形面构成的简化三维风格"),
("扁平化","flat design","去除拟真阴影并强调色块图形的设计风格"),
("拟物化","skeuomorphic","用真实材质和立体细节模拟实物的界面风格"),
("3D潮玩","3d blind box toy render","潮流玩具般圆润可爱的三维渲染风格"),
("黏土风","clay render claymation","模拟手捏黏土材质和柔软形体的风格"),
("赛博格","cyborg aesthetic","人体与机械电子部件融合的半机械审美"),
("国风水墨","chinese ink wash aesthetic","水墨笔触留白和东方意境构成的风格"),
("和风浮世","japanese ukiyo aesthetic","浮世绘线条色块和日本传统图案的风格"),
("克苏鲁","lovecraftian cosmic horror","触手古神和不可名状恐惧构成的宇宙恐怖"),
("暗黑奇幻","dark fantasy grimdark","魔法怪物与阴郁世界观结合的黑暗幻想"),
("童话梦幻","fairytale whimsical","柔和光色、奇幻生物和童话场景构成的风格"),
("未来主义","futuristic","流线科技材料和前瞻形态构成的未来感"),
("复古未来","retrofuturism","旧时代想象中的未来科技与复古造型结合"),
("故障朋克","glitchpunk","朋克反叛气质与数字故障效果结合的风格"),
("超扁平","superflat takashi style","日本流行文化与无景深平面图像结合的风格")],"风格;标签")

block("时代美学",[
("50年代","1950s retro aesthetic","战后家居广告、粉彩和圆润汽车线条的年代感"),
("60年代","1960s mod psychedelic","迷幻色彩、几何图案和太空时代的摩登风"),
("70年代","1970s funk disco","暖棕橙色、迪斯科和嬉皮元素的年代风格"),
("80年代","1980s neon synthwave","霓虹网格、合成器和录像带质感的复古未来"),
("90年代","1990s nostalgic","胶片颗粒、街头休闲和早期数码感的怀旧风"),
("千禧Y2K","y2k 2000s","银色塑料、网络图标和千禧未来感的审美"),
("世纪中期现代","mid-century modern","简洁木作、细腿家具和有机曲线的现代设计"),
("维多利亚","victorian era","繁复装饰、深色木作和古典礼仪感的时代风格"),
("装饰艺术时代","art deco era 1920s","几何对称、金属线条和奢华都会感的风格"),
("古典复兴","classical revival","重拾古希腊罗马比例柱式的庄重审美")],"风格;时代")

block("地域与网络美学",[
("日系","japanese clean aesthetic","清淡色彩、留白和精致日常感的日本风格"),
("韩系","korean soft aesthetic","柔光浅色和清爽时尚感构成的韩式风格"),
("欧美","western aesthetic","强调立体轮廓、自由感和强表达的西方风格"),
("中式","chinese aesthetic","传统纹样、器物和东方秩序构成的中国风格"),
("和风","traditional japanese","榻榻米、木构和日式纹样构成的传统日本风"),
("北欧","scandinavian aesthetic","明亮木色、功能简洁和自然舒适的北欧风"),
("地中海","mediterranean aesthetic","蓝白色、陶土和海岸阳光构成的地域风格"),
("热带","tropical aesthetic","棕榈植物、高饱和色和湿热阳光的风格"),
("cottagecore田园","cottagecore rural cozy","乡村花园、手作布艺和慢生活感的网络美学"),
("暗黑学院","dark academia","古书、深棕色和学院建筑构成的阴郁学术风"),
("浅色学院","light academia","米白书卷、阳光教室和温柔学术感的风格"),
("精灵核","fairycore","蘑菇花草、透明翅膀和童话森林的美学"),
("海洋核","oceancore","海浪贝壳、蓝绿色和水下意象构成的网络风格"),
("绿野核","goblincore","苔藓石头和野外小物构成的粗野自然审美"),
("城市废墟","urbex urban decay","废弃建筑、剥落墙面和探险感的城市审美"),
("赛博绿洲","solarpunk green utopia","绿色能源、植物建筑和乐观未来构成的风格")],"风格;地域网络")

block("品牌调性与媒介",[
("高级感","premium luxury","克制材质和精致留白形成的高价值感"),
("科技感","futuristic tech","冷色光效、精密线条和未来材料构成的调性"),
("年轻活力","youthful vibrant","鲜亮色彩和动态构图形成的青春能量感"),
("温暖治愈","warm healing","暖光柔色与亲近日常形成的舒缓调性"),
("简约高效","clean efficient","清晰层级和少干扰视觉形成的工作型调性"),
("奢华金属","luxury metallic","金银金属光泽与深色背景形成的高奢质感"),
("自然有机","natural organic","植物纹理和非规则形态构成的自然调性"),
("复古怀旧","retro nostalgic","旧物色彩和年代符号唤起的怀旧感"),
("拼贴混媒","mixed media collage","照片纸张纹理和图形叠加的混合媒介风格"),
("手绘+数字","hand-drawn digital hybrid","手绘线条与数字渲染结合的混合视觉"),
("3D+2D混合","3d 2d hybrid","三维体积与平面图形并置的复合表现"),
("实拍+CG","live action cg composite","真实摄影与计算机图形合成的影像风格")],"风格;品牌媒介")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
