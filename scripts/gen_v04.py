# -*- coding: utf-8 -*-
"""V04 游戏原画与概念设计（穷举级）。合并模式。"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V04"; rows=[]
def simple(cat,items,suf,tags):
    for zh,en in items: rows.append(dict(zip(FIELDS,["",zh,en.title(),"",V,cat,zh+"。","","","",en+" "+suf,"",zh,"","","","",tags,"整理","published","V1.0"])))
simple("角色设计 / 职业定位",[("骑士","armored knight"),("法师","robed mage wizard"),("刺客","hooded assassin"),("战士","heavy warrior"),("游侠","archer ranger"),("牧师","cleric priest"),("盗贼","rogue thief"),("德鲁伊","druid"),("武僧","monk"),("死灵法师","necromancer"),("圣骑士","paladin"),("枪手","gunslinger"),("机甲驾驶员","mech pilot"),("赛博黑客","cyberpunk hacker"),("赏金猎人","bounty hunter"),("海盗","pirate"),("武士","samurai"),("忍者","ninja")],"character concept","游戏;职业")
simple("角色设计 / 种族体型",[("精灵","elegant elf"),("兽人","muscular orc"),("矮人","stout bearded dwarf"),("龙人","dragonborn scaled"),("亡灵","undead skeleton"),("恶魔","demon"),("天使","angel winged"),("半兽人","beastman"),("机器人","robot android"),("巨人","giant"),("哥布林","goblin"),("吸血鬼","vampire"),("狼人","werewolf"),("人鱼","mermaid"),("妖精","fairy sprite")],"character concept","游戏;种族")
simple("角色设计 / 表现",[("角色三视图","character turnaround three views"),("动态姿态","dynamic action pose"),("表情设计","expression sheet"),("角色配色","color scheme"),("立绘","character splash art"),("半身像","character bust portrait"),("Q版","chibi cute style"),("装备拆解","equipment breakdown")],"character","游戏;角色表现")
simple("场景与世界观",[("奇幻森林","fantasy magical forest"),("赛博都市","cyberpunk neon city"),("末世废土","post-apocalyptic wasteland"),("蒸汽朋克城","steampunk city"),("太空站","sci-fi space station"),("古代遗迹","ancient ruins"),("浮空岛","floating sky islands"),("地下城","dark dungeon"),("雪山","snowy mountains"),("沙漠绿洲","desert oasis"),("水下城市","underwater city"),("火山熔岩","volcanic lava"),("天空之城","sky castle"),("幽暗沼泽","dark swamp"),("东方仙境","oriental fairyland"),("机械都市","mechanical metropolis"),("废弃工厂","abandoned factory"),("魔法学院","magic academy")],"environment concept","游戏;场景")
simple("道具与装备",[("奇幻长剑","ornate fantasy sword"),("法杖","crystal magic staff"),("弓箭","fantasy bow"),("巨斧","battle axe"),("科幻枪","sci-fi gun"),("能量剑","energy sword"),("机甲","giant mecha"),("载具","futuristic vehicle"),("飞船","spaceship"),("护甲套装","armor set"),("头盔","helmet design"),("盾牌","shield"),("魔法道具","magic artifact"),("药水瓶","potion bottle"),("宝箱","treasure chest"),("机械臂","cybernetic arm")],"prop concept","游戏;道具")
simple("生物设计",[("巨龙","fantasy dragon"),("怪物","original monster"),("机械兽","mechanical beast"),("异形","alien creature"),("精怪","spirit fae creature"),("巨兽","giant kaiju"),("史莱姆","slime"),("元素生物","elemental creature"),("不死生物","undead creature"),("混合兽","chimera hybrid"),("昆虫怪","insect creature"),("深海怪","deep sea monster")],"creature concept","游戏;生物")
simple("UI与图标",[("HUD界面","game HUD"),("技能图标","skill icon set"),("界面框架","fantasy UI frame"),("血条法力条","health mana bar"),("地图界面","map interface"),("背包界面","inventory UI"),("技能树","skill tree UI"),("对话框","dialogue box UI"),("成就图标","achievement icon")],"game UI","游戏;UI")
simple("概念流程与风格",[("剪影设计","silhouette thumbnail"),("色彩脚本","color script mood"),("设定图","concept design sheet"),("厚涂风格","painterly concept art"),("赛璐璐","cel-shaded anime"),("写实CG","realistic CG render"),("像素风","pixel art"),("吉卜力风","ghibli anime style"),("美漫风","american comic style"),("国风","chinese ink game style"),("暗黑风","dark fantasy grimdark"),("卡通渲染","toon shading"),("低多边形","low poly stylized"),("黏土风","clay render style")],"concept style","游戏;风格")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
