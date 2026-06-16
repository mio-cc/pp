# -*- coding: utf-8 -*-
"""V04 游戏原画与概念设计（穷举）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V04"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))

block("角色设计 / 职业定位",[
("骑士","Knight","重甲骑士","armored knight character concept","骑士, 重甲"),
("法师","Mage","法袍法师","robed mage wizard character","法师, 法袍"),
("刺客","Assassin","暗影刺客","hooded assassin character","刺客, 暗影"),
("战士","Warrior","重武器战士","heavy weapon warrior character","战士"),
("游侠","Ranger","弓箭游侠","archer ranger character","游侠, 弓箭"),
("机甲驾驶员","Mech Pilot","驾驶服飞行员","mech pilot suit character","机甲驾驶员"),
("赛博黑客","Cyber Hacker","赛博朋克黑客","cyberpunk hacker character","赛博黑客")],"游戏;角色")
block("角色设计 / 种族体型",[
("精灵","Elf","尖耳优雅精灵","elegant elf, pointed ears","精灵"),
("兽人","Orc","壮硕兽人","muscular orc","兽人"),
("矮人","Dwarf","矮壮大胡子","stout bearded dwarf","矮人"),
("龙人","Dragonborn","龙鳞人形","dragonborn scaled humanoid","龙人, 鳞甲"),
("巨人体型","Giant Build","庞大体型","giant massive build","巨人体型"),
("娇小体型","Petite Build","娇小灵巧","petite agile build","娇小体型")],"游戏;种族")
block("角色设计 / 表现",[
("角色三视图","Character Turnaround","正侧背三视","character turnaround three views","三视图"),
("姿态设计","Pose Design","动态姿态","dynamic action pose","姿态设计"),
("表情设计","Expression Sheet","表情合集","expression sheet","表情设计"),
("角色配色","Color Scheme","配色方案","character color scheme","角色配色")],"游戏;角色表现")
block("场景与世界观",[
("奇幻森林","Fantasy Forest","魔法森林环境","fantasy magical forest environment","奇幻森林"),
("赛博都市","Cyberpunk City","霓虹未来都市","cyberpunk neon megacity","赛博都市"),
("末世废土","Post-Apocalyptic","荒废废土","post-apocalyptic wasteland","末世废土"),
("蒸汽朋克城","Steampunk City","齿轮蒸汽","steampunk city, gears steam","蒸汽朋克"),
("太空站","Space Station","科幻太空站","sci-fi space station interior","太空站"),
("古代遗迹","Ancient Ruins","失落遗迹","ancient lost ruins","古代遗迹"),
("浮空岛","Floating Islands","空中浮岛","floating sky islands fantasy","浮空岛"),
("地下城","Dungeon","幽暗地牢","dark dungeon interior","地下城")],"游戏;场景")
block("道具与装备",[
("奇幻长剑","Fantasy Sword","符文长剑","ornate fantasy sword, runes","奇幻长剑"),
("法杖","Magic Staff","水晶法杖","crystal magic staff","法杖"),
("枪械设计","Sci-Fi Gun","科幻枪械","sci-fi futuristic gun design","枪械设计"),
("机甲","Mecha","巨型机甲","giant mecha robot design","机甲"),
("载具设计","Vehicle Design","未来载具","futuristic vehicle concept","载具设计"),
("护甲套装","Armor Set","全套护甲","full armor set design","护甲套装"),
("魔法道具","Magic Artifact","发光神器","glowing magic artifact","魔法道具")],"游戏;道具")
block("生物设计",[
("巨龙","Dragon","奇幻巨龙","fantasy dragon creature","巨龙"),
("怪物","Monster","原创怪物","original monster creature design","怪物"),
("机械兽","Mech Beast","机械生物","mechanical beast creature","机械兽"),
("异形生物","Alien Creature","外星生物","alien creature concept","异形生物"),
("精怪","Spirit Creature","灵兽精怪","spirit fae creature","精怪")],"游戏;生物")
block("UI与图标",[
("HUD界面","HUD","游戏抬头显示","game HUD interface","HUD界面"),
("技能图标","Skill Icon","技能图标","game skill icon set","技能图标"),
("界面框架","UI Frame","奇幻界面边框","fantasy UI frame ornate","界面框架"),
("血条法力条","Health/Mana Bar","状态条","health mana bar UI","血条法力条"),
("地图界面","Map UI","游戏地图","game map interface","地图界面")],"游戏;UI")
block("概念流程与风格",[
("剪影设计","Silhouette","剪影探索","silhouette thumbnail exploration","剪影设计"),
("色彩脚本","Color Script","色彩氛围脚本","color script mood","色彩脚本"),
("设定图","Concept Sheet","设定集","concept design sheet","设定图"),
("厚涂风格","Painterly","厚涂概念","painterly digital concept art","厚涂风格"),
("赛璐璐风格","Cel Shading","卡通平涂","cel-shaded anime style","赛璐璐, 卡通平涂"),
("写实CG","Realistic CG","写实渲染","realistic CG render","写实CG"),
("像素风","Pixel Art","复古像素","retro pixel art","像素风"),
("吉卜力风","Ghibli Style","治愈动画感","ghibli anime style","吉卜力风")],"游戏;风格")

existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V}: {len(rows)} | total: {len(allrows)}")
