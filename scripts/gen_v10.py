# -*- coding: utf-8 -*-
"""V10 建筑、室内与空间设计（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V10"; rows=[]
def block(cat,items,suf,tags):
    for zh,en,defs in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",en+(" "+suf if suf else ""),"",zh,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("建筑风格",[
("古典主义","classical architecture columns","强调柱式比例与秩序的古典建筑风格"),
("哥特","gothic architecture","以尖拱飞扶壁和彩窗见长的高耸建筑风格"),
("罗马式","romanesque architecture","厚墙圆拱与沉稳体量构成的中世纪建筑"),
("巴洛克","baroque architecture","以曲线动势和戏剧装饰塑造宏伟感的建筑"),
("洛可可","rococo architecture","轻盈繁复曲线与贝壳纹装饰的宫廷风格"),
("新古典","neoclassical architecture","复兴古希腊罗马秩序的简洁庄重建筑"),
("现代主义","modernist architecture","强调功能结构与简洁体块的现代建筑"),
("包豪斯","bauhaus architecture","功能主义与几何简洁结合的现代设计体系"),
("国际主义","international style architecture","玻璃钢框与无装饰立面的全球化现代建筑"),
("极简","minimalist architecture","以少量材料和纯净线条构成的克制建筑"),
("解构主义","deconstructivist architecture","打破正交秩序形成碎片化张力的建筑"),
("粗野主义","brutalist concrete architecture","裸露混凝土和厚重体块主导的建筑风格"),
("新中式","new chinese architecture","传统中式意象与现代空间结构结合的建筑"),
("徽派","huizhou chinese architecture","白墙黛瓦马头墙构成的江南地域建筑"),
("日式侘寂","japanese wabi-sabi architecture","朴素材料与残缺静寂气质的日式空间"),
("和风神社","japanese shrine architecture","木构屋顶与鸟居意象形成的神社建筑"),
("工业风","industrial architecture","裸露管线金属砖墙营造的粗粝工业空间"),
("未来主义","futuristic architecture","流线形体与科技材料构成的前瞻建筑"),
("有机建筑","organic flowing architecture","建筑形体与自然地形环境融合的设计"),
("仿生建筑","biomimetic architecture","借鉴生物结构与形态的建筑设计"),
("地中海","mediterranean architecture","白墙拱廊陶瓦与海岸暖光的建筑风格"),
("北欧","nordic architecture","自然材料与明亮简洁空间构成的北欧风格"),
("热带","tropical architecture","适应湿热气候的遮阳通风开放建筑"),
("阿拉伯","islamic arabic architecture","拱券穹顶与几何纹样构成的伊斯兰建筑")],"architecture","建筑;风格")

block("建筑空间",[
("中庭","atrium","建筑内部贯通多层的开放共享空间"),
("玻璃幕墙","glass curtain wall","以玻璃板覆盖外立面的轻质围护系统"),
("悬挑结构","cantilever","一端固定一端伸出的无支撑结构形式"),
("开放平面","open floor plan","减少隔墙形成连续灵活的室内平面"),
("螺旋楼梯","spiral staircase","围绕中心轴旋转上升的节省空间楼梯"),
("拱廊","arcade arches","连续拱形开口形成的步行廊道空间"),
("穹顶","dome","半球或曲面覆盖的大跨度屋顶结构"),
("通高","double-height space","跨越两层以上高度的开阔室内空间"),
("天井","light court","引入采光通风的竖向内院空间"),
("廊道","corridor gallery","连接房间或展区的线性通行空间"),
("中庭花园","atrium garden","在室内中庭布置绿植景观的共享空间"),
("挑空客厅","double-height living room","客厅上方取消楼板形成的双层高空间"),
("落地窗","floor-to-ceiling windows","从地面延伸至顶面的通透窗面"),
("天窗","skylight","屋顶开设用于采光的窗洞或玻璃面")],"interior space","建筑;空间")

block("室内设计",[
("北欧风","scandinavian interior","明亮木色与简洁软装构成的舒适室内风格"),
("极简室内","minimalist interior","少装饰和清晰收纳塑造的纯净室内"),
("工业风室内","industrial loft interior","裸砖金属管线和开放层高形成的室内风格"),
("日式原木","japandi interior","原木材质与留白秩序营造的温和日式空间"),
("奶油风","cream cozy interior","米白暖色与柔软材质构成的轻柔室内"),
("法式复古","french vintage interior","石膏线拱门与复古家具营造的优雅室内"),
("中古风","mid-century modern interior","中世纪家具和暖木色主导的复古现代空间"),
("侘寂室内","wabi-sabi interior","粗粝材质与不完美肌理营造的静寂空间"),
("赛博朋克室内","cyberpunk neon interior","霓虹光源与高科技材质形成的未来室内"),
("美式乡村","american country interior","木作布艺和质朴家具构成的乡村室内"),
("地中海风","mediterranean interior","蓝白色调拱形与陶土材质的海岸室内"),
("新中式室内","new chinese interior","中式格栅器物与现代布局结合的室内"),
("轻奢风","light luxury interior","金属石材与克制装饰构成的精致室内"),
("ins风","instagram aesthetic interior","适合社交媒体拍摄的清爽装饰风格"),
("复古怀旧","retro vintage interior","旧家具暖灯与年代元素营造的怀旧空间"),
("禅意","zen minimalist interior","留白低矮家具与自然材质形成的静心空间"),
("孟菲斯室内","memphis interior","鲜艳色块与几何图案构成的玩味室内")],"interior","建筑;室内")

block("家具与陈设",[
("北欧家具","scandinavian furniture","线条简洁木质温润的功能主义家具"),
("中古家具","mid-century furniture","细腿木作与流畅曲线构成的中世纪家具"),
("巴洛克家具","baroque furniture","雕花曲腿和金色装饰浓重的古典家具"),
("软装陈设","soft furnishing decor","用布艺摆件灯具完善空间氛围的配置"),
("绿植装饰","indoor plants decor","用室内植物增加自然感和空间层次"),
("艺术挂画","wall art decor","墙面艺术作品用于强化风格和视觉焦点"),
("地毯","rug decor","铺设地面以划分区域并增加柔软质感的织物"),
("吊灯","pendant lighting","从顶部悬挂形成重点照明和装饰的灯具"),
("落地灯","floor lamp","可移动的立式灯具用于局部照明和氛围")],"furniture","建筑;家具")

block("景观与氛围",[
("城市天际线","city skyline","建筑轮廓在地平线上形成的城市剪影"),
("园林景观","classical garden landscape","以植物水石路径组织的观赏性户外空间"),
("现代景观","modern landscape","简洁铺装植物与几何结构结合的景观设计"),
("中庭光井","light well glow","竖向采光井带来的内部自然光氛围"),
("空间光影","spatial light shadow","光线穿过结构在空间中形成的明暗层次"),
("黄昏暖光室内","golden hour interior light","落日暖光进入室内形成的柔和氛围"),
("晨光室内","morning light interior","清晨低角度自然光带来的清透室内感"),
("夜景灯光","night architectural lighting","夜间人工照明强化建筑轮廓与层次"),
("雾景建筑","foggy atmospheric architecture","雾气弱化边界并增强建筑空间纵深")],"landscape mood","建筑;景观氛围")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
