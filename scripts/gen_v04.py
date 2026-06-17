# -*- coding: utf-8 -*-
"""V04 游戏原画与概念设计（穷举级）。合并模式。

范式说明：全部使用 block()，每条 item 必须给出真实 definition_short
（解释术语是什么/作用/视觉特征），严禁复读术语名。
"""
import csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; CSV=ROOT/"data"/"raw"/"terms_seed.csv"
FIELDS=["term_uid","zh_term","en_term","aliases","volume_code","category","definition_short","definition_long","visual_effect","prompt_usage","positive_prompt","negative_prompt","positive_prompt_cn","negative_prompt_cn","use_cases","related_terms","confused_with","tags","source_refs","status","version"]
V="V04"; rows=[]
def block(cat,items,tags):
    for zh,en,defs,pen,pcn in items:
        if defs.strip().rstrip("。.；;，, ")==zh.strip().rstrip("。.；;，, "):
            raise ValueError(f"definition_short 禁止复读术语名: {zh!r} -> {defs!r}")
        rows.append(dict(zip(FIELDS,["",zh,en,"",V,cat,defs+"。","","","",pen,"",pcn,"","","","",tags,"互联网研究整理","published","V1.0"])))
block("角色设计 / 职业定位",[
("骑士","Armored Knight","重甲持盾冲锋陷阵的近战职业","armored knight character concept","骑士"),
("法师","Robed Mage Wizard","身穿长袍以法术远程攻击的职业","robed mage wizard character concept","法师"),
("刺客","Hooded Assassin","暗影中潜行致命暗杀的敏捷职业","hooded assassin stealth character","刺客"),
("战士","Heavy Warrior","近身肉搏重武器的高体力职业","heavy warrior melee fighter","战士"),
("游侠","Archer Ranger","弓箭远程、擅长野外生存的职业","archer ranger ranged character","游侠"),
("牧师","Cleric Priest","信仰驱动的治愈与辅助职业","cleric priest healer support","牧师"),
("盗贼","Rogue Thief","开锁偷盗陷阱操作的敏捷职业","rogue thief stealthy rogue","盗贼"),
("德鲁伊","Druid","与自然沟通、可变形的半施法职业","druid nature shapeshifter","德鲁伊"),
("武僧","Monk","徒手格斗精神修行的高敏捷职业","monk martial artist character","武僧"),
("死灵法师","Necromancer","操控亡灵与暗黑魔法的禁忌职业","necromancer dark summoner","死灵法师"),
("圣骑士","Paladin","信仰与剑盾兼具的神圣战士职业","paladin holy knight","圣骑士"),
("枪手","Gunslinger","使用火器远程射击的职业","gunslinger gunfighter character","枪手"),
("机甲驾驶员","Mech Pilot","驾驶巨型战斗机甲的操控者","mech pilot robot operator","机甲驾驶员"),
("赛博黑客","Cyberpunk Hacker","虚拟空间入侵的黑客角色","cyberpunk hacker netrunner","赛博黑客"),
("赏金猎人","Bounty Hunter","接受悬赏追捕目标的独立佣兵","bounty hunter mercenary tracker","赏金猎人"),
("海盗","Pirate","航海掠夺自由不羁的海上冒险者","pirate sea raider","海盗"),
("武士","Samurai","忠义刀法精湛的东方剑士","samurai sword warrior","武士"),
("忍者","Ninja","隐遁暗杀精通忍术的谍战角色","ninja shadow stealth","忍者")],"游戏;职业")
block("角色设计 / 种族体型",[
("精灵","Elegant Elf","尖耳修长、亲近自然的长寿种族","elegant elf pointy-eared","精灵"),
("兽人","Muscular Orc","绿皮粗壮、崇尚力量的蛮族","muscular orc brutish","兽人"),
("矮人","Stout Bearded Dwarf","矮壮长须、精通锻造的矿洞种族","stout bearded dwarf smith","矮人"),
("龙人","Dragonborn Scaled","身上覆鳞、可吐息的龙血种族","dragonborn scaled draconic","龙人"),
("亡灵","Undead Skeleton","不死骸骨、被暗魔法驱动的存在","undead skeleton corpse","亡灵"),
("恶魔","Demon","来自深渊的邪恶超自然实体","demon infernal evil","恶魔"),
("天使","Angel Winged","背生双翼、圣洁光辉的天界存在","angel winged holy","天使"),
("半兽人","Beastman","人兽混合特征的中性种族","beastman hybrid anthropomorphic","半兽人"),
("机器人","Robot Android","机械结构、AI驱动的拟人角色","robot android machine","机器人"),
("巨人","Giant","体型数倍于常人的巨大种族","giant huge massive","巨人"),
("哥布林","Goblin","矮小狡诈的贪婪地精种族","goblin small cunning greedy","哥布林"),
("吸血鬼","Vampire","嗜血长生、惧阳光的暗夜种族","vampire blood immortal","吸血鬼"),
("狼人","Werewolf","满月变身为狼人的诅咒种族","werewolf lycanthrope","狼人"),
("人鱼","Mermaid","鱼尾人身的水下幻想种族","mermaid aquatic fish-tail","人鱼"),
("妖精","Fairy Sprite","微小透明翅膀的魔法精灵","fairy sprite tiny winged","妖精")],"游戏;种族")
block("角色设计 / 表现",[
("角色三视图","Character Turnaround","展示角色正面侧面背面的标准设计稿","character turnaround three views","角色三视图"),
("动态姿态","Dynamic Action Pose","表现角色动作张力的动态设计","dynamic action pose design","动态姿态"),
("表情设计","Expression Sheet","列出角色喜怒哀乐等表情的系列图","expression sheet emotions","表情设计"),
("角色配色","Color Scheme","定义角色主色辅色点缀的配色方案","color scheme palette design","角色配色"),
("立绘","Character Splash Art","全幅场景化的角色宣传展示图","character splash art illustration","立绘"),
("半身像","Character Bust Portrait","胸部以上的角色肖像特写","character bust portrait close-up","半身像"),
("Q版","Chibi Cute Style","大头小身的可爱夸张比例风格","chibi cute proportional style","Q版"),
("装备拆解","Equipment Breakdown","分解展示角色穿戴装备的分层图","equipment breakdown layers","装备拆解")],"游戏;角色表现")
block("场景与世界观",[
("奇幻森林","Fantasy Magical Forest","古树荧光蘑菇的魔法森林场景","fantasy magical forest scene","奇幻森林"),
("赛博都市","Cyberpunk Neon City","霓虹高楼雨夜的反乌托邦都市","cyberpunk neon city streets","赛博都市"),
("末世废土","Post-Apocalyptic Wasteland","文明崩溃后荒芜废墟的荒原","post-apocalyptic wasteland ruins","末世废土"),
("蒸汽朋克城","Steampunk City","齿轮蒸汽管道的维多利亚机械城","steampunk city gears brass","蒸汽朋克城"),
("太空站","Sci-Fi Space Station","漂浮太空中的科幻空间站","sci-fi space station orbital","太空站"),
("古代遗迹","Ancient Ruins","被植被侵蚀的远古文明废墟","ancient ruins overgrown stone","古代遗迹"),
("浮空岛","Floating Sky Islands","悬浮云端的空中岛屿群","floating sky islands cloud","浮空岛"),
("地下城","Dark Dungeon","地下的黑暗迷宫式冒险空间","dark dungeon labyrinth","地下城"),
("雪山","Snowy Mountains","终年积雪的壮观高山场景","snowy mountains blizzard","雪山"),
("沙漠绿洲","Desert Oasis","荒漠中泉水环绕的生机之地","desert oasis water palm","沙漠绿洲"),
("水下城市","Underwater City","海底的奇幻城市建筑场景","underwater city submerged","水下城市"),
("火山熔岩","Volcanic Lava","岩浆流淌的火山口危险场景","volcanic lava eruption","火山熔岩"),
("天空之城","Sky Castle","云端之上的宏伟城堡群落","sky castle floating above clouds","天空之城"),
("幽暗沼泽","Dark Swamp","浓雾弥漫的阴森湿地场景","dark swamp foggy murky","幽暗沼泽"),
("东方仙境","Oriental Fairyland","仙山云海的中国风奇幻仙境","oriental fairyland chinese myth","东方仙境"),
("机械都市","Mechanical Metropolis","全机械齿轮构成的工业都市","mechanical metropolis industrial","机械都市"),
("废弃工厂","Abandoned Factory","锈蚀机器荒废的工业建筑","abandoned factory rusted","废弃工厂"),
("魔法学院","Magic Academy","培养魔法师的古堡学院场景","magic academy castle school","魔法学院")],"游戏;场景")
block("道具与装备",[
("奇幻长剑","Ornate Fantasy Sword","华丽装饰的中世纪风格长剑","ornate fantasy sword weapon","奇幻长剑"),
("法杖","Crystal Magic Staff","顶端镶嵌宝石施法用杖","crystal magic staff wizard","法杖"),
("弓箭","Fantasy Bow","精美弓身配箭袋的远程武器","fantasy bow arrow ranged","弓箭"),
("巨斧","Battle Axe","重型双刃劈砍的暴力武器","battle axe heavy cleaving","巨斧"),
("科幻枪","Sci-Fi Gun","未来科技造型的能量火器","sci-fi gun energy weapon","科幻枪"),
("能量剑","Energy Sword","发光等离子刃的未来近战武器","energy sword plasma blade","能量剑"),
("机甲","Giant Mecha","巨大人形战斗机器人","giant mecha robot suit","机甲"),
("载具","Futuristic Vehicle","未来风格的交通载具","futuristic vehicle transport","载具"),
("飞船","Spaceship","星际航行的宇宙飞船","spaceship starship craft","飞船"),
("护甲套装","Armor Set","全身防护的战甲组合套装","armor set full plate","护甲套装"),
("头盔","Helmet Design","保护头部的穿戴式护具","helmet head protection","头盔"),
("盾牌","Shield","手持格挡的防御装备","shield defense blocking","盾牌"),
("魔法道具","Magic Artifact","蕴含魔法力量的神秘器物","magic artifact enchanted","魔法道具"),
("药水瓶","Potion Bottle","盛装魔法药剂的玻璃瓶","potion bottle flask magical","药水瓶"),
("宝箱","Treasure Chest","藏有宝物的装饰性箱匣","treasure chest loot reward","宝箱"),
("机械臂","Cybernetic Arm","替代天然肢体的高科技义肢","cybernetic arm prosthetic","机械臂")],"游戏;道具")
block("生物设计",[
("巨龙","Fantasy Dragon","喷火飞行的巨型有鳞爬行类","fantasy dragon fire-breathing","巨龙"),
("怪物","Original Monster","原创设计的非自然生物","original monster creature","怪物"),
("机械兽","Mechanical Beast","齿轮电机驱动的仿生机械生物","mechanical beast robot","机械兽"),
("异形","Alien Creature","外星世界的原创异种生物","alien creature xenomorph","异形"),
("精怪","Spirit Fae Creature","自然精灵或元素化身的微小型生物","spirit fae nature creature","精怪"),
("巨兽","Giant Kaiju","体型如山般的破坏性巨大怪物","giant kaiju enormous","巨兽"),
("史莱姆","Slime","果冻状可变形的低级奇幻生物","slime gelatinous blob","史莱姆"),
("元素生物","Elemental Creature","由火水风土等元素凝聚而成的生物","elemental creature fire water","元素生物"),
("不死生物","Undead Creature","被魔法复活持续活动的不死体","undead creature corpse reanimated","不死生物"),
("混合兽","Chimera Hybrid","多物种拼接的混血神话生物","chimera hybrid multi-part","混合兽"),
("昆虫怪","Insect Creature","放大化的恐怖昆虫型怪物","insect creature giant bug","昆虫怪"),
("深海怪","Deep Sea Monster","栖息深海的巨大未知生物","deep sea monster leviathan","深海怪")],"游戏;生物")
block("UI与图标",[
("HUD界面","Game HUD","叠加在游戏画面上的信息界面","game HUD heads-up display","HUD界面"),
("技能图标","Skill Icon Set","表示技能效果的方形小图标","skill icon set ability","技能图标"),
("界面框架","Fantasy UI Frame","包裹功能面板的装饰性边框","fantasy UI frame ornamental","界面框架"),
("血条法力条","Health Mana Bar","显示生命值与法力值的条形指示器","health mana bar indicator","血条法力条"),
("地图界面","Map Interface","展示游戏世界地理的小地图","map interface minimap world","地图界面"),
("背包界面","Inventory UI","管理角色道具物品的网格界面","inventory UI item grid","背包界面"),
("技能树","Skill Tree UI","分支解锁技能的树状界面","skill tree UI branch unlock","技能树"),
("对话框","Dialogue Box UI","展示NPC对话的文字气泡或面板","dialogue box UI conversation","对话框"),
("成就图标","Achievement Icon","解锁成就时的奖章风格图标","achievement icon badge","成就图标")],"游戏;UI")
block("概念流程与风格",[
("剪影设计","Silhouette Thumbnail","用纯黑剪影确认角色识别度","silhouette thumbnail recognition","剪影设计"),
("色彩脚本","Color Script Mood","按镜头排列的色彩情绪序列图","color script mood per shot","色彩脚本"),
("设定图","Concept Design Sheet","多视图+细节注释的综合设计稿","concept design sheet annotated","设定图"),
("厚涂风格","Painterly Concept Art","笔触明显的数字厚涂概念画风格","painterly concept art brushy","厚涂风格"),
("赛璐璐","Cel-Shaded Anime","平涂阴影的日式动画渲染风格","cel-shaded anime flat","赛璐璐"),
("写实CG","Realistic CG Render","照片级光影的3D写实渲染风格","realistic CG render photoreal","写实CG"),
("像素风","Pixel Art","复古8/16位像素点阵风格","pixel art retro 8bit 16bit","像素风"),
("吉卜力风","Ghibli Anime Style","吉卜力工作室水彩温暖动画风","ghibli anime warm watercolor","吉卜力风"),
("美漫风","American Comic Style","粗线高对比的美国漫画分格风","american comic style bold ink","美漫风"),
("国风","Chinese Ink Game Style","水墨线条配传统色的中式游戏画风","chinese ink game style","国风"),
("暗黑风","Dark Fantasy Grimdark","低饱和阴暗血腥的暗黑奇幻风","dark fantasy grimdark gloomy","暗黑风"),
("卡通渲染","Toon Shading","边缘描线+平涂色的卡通渲染","toon shading outline flat","卡通渲染"),
("低多边形","Low Poly Stylized","面数极少的几何简约3D风格","low poly stylized geometric","低多边形"),
("黏土风","Clay Render Style","橡皮泥质感的光滑柔和渲染","clay render smooth soft","黏土风")],"游戏;风格")
existing=[]
if CSV.exists(): existing=[r for r in csv.DictReader(open(CSV,encoding="utf-8-sig")) if r["volume_code"]!=V]
for i,r in enumerate(rows,1): r["term_uid"]=f"{V}_T{i:04d}"
allrows=existing+rows
with open(CSV,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(allrows)
print(f"{V} 穷举: {len(rows)} | total: {len(allrows)}")
