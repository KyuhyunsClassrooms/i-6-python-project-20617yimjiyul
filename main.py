import random

# ==========================
# 기본 함수
# ==========================

def bar(cur, maxv, length=20):
    filled = int(cur / maxv * length)
    return "█" * filled + "░" * (length - filled)

def pause():
    input("\n엔터를 누르세요...")

# ==========================
# 플레이어
# ==========================

name = input("플레이어 이름: ")

player = {
    "name": name,
    "job": "전사",
    "level": 1,
    "exp": 0,
    "hp": 100,
    "max_hp": 100,
    "atk": 10,
    "crit": 10,
    "potions": 3,
    "skills": [
        ("연속 베기",150),
        ("강타",200),
        ("흡혈격",180)
    ]
}

weapon = {
    "name": "녹슨 철검",
    "level": 1,
    "exp": 0,
    "atk": 5,
    "skill_name": "강철 베기",
    "skill_damage": 250
}
weapon_pool = [

    {
        "name": "강철검",
        "atk": 15,
        "skill_name": "강철 난무",
        "skill_damage": 350
    },

    {
        "name": "기사검",
        "atk": 30,
        "skill_name": "기사의 맹세",
        "skill_damage": 450
    },

    {
        "name": "백은 성검",
        "atk": 60,
        "skill_name": "성광참",
        "skill_damage": 650
    },

    {
        "name": "붉은 달의 검",
        "atk": 150,
        "skill_name": "월광참",
        "skill_damage": 1000
    },

    {
        "name": "화염 일륜도",
        "atk": 250,
        "skill_name": "화염의 호흡",
        "skill_damage": 1500
    },

    {
        "name": "수류 일륜도",
        "atk": 260,
        "skill_name": "물의 호흡",
        "skill_damage": 1600
    },

    {
        "name": "뇌광 일륜도",
        "atk": 280,
        "skill_name": "번개의 호흡",
        "skill_damage": 1800
    },

    {
        "name": "천멸신검",
        "atk": 500,
        "skill_name": "천멸섬",
        "skill_damage": 3000
    }
]

floor = 1
checkpoint = 1

# ==========================
# 몬스터
# ==========================

titles = [
    "지각한",
    "숙제 안 한",
    "급식 기다리는",
    "수행평가에 쫓기는",
    "벼락치기하는",
    "내신이 걱정되는"
]

monster_data = {
    (1,9): ["슬라임","고블린","늑대"],
    (11,19): ["하피","리자드맨","오크"],
    (21,29): ["트롤","해골","좀비"],
    (31,39): ["리치","미믹","골렘"],
    (41,49): ["미노타우루스","가고일","그리폰"],
    (51,59): ["사이클롭스","네크로맨서","와이번"],
    (61,69): ["데몬","헬하운드","암흑기사"],
    (71,79): ["타락한 소드마스터","타락한 대마법사","마신"],
    (81,89): ["고대룡","심연의 기사","파멸의 군주"],
    (91,99): ["공허룡","종말의 사도","멸망의 화신"]
}
bosses = {

    10: "고블린 킹 그록",
    20: "오크 대장 로칸",
    30: "언데드 군주 모르테",
    40: "미믹 제왕 데보어",
    50: "황소왕 아스테론",
    60: "외눈의 군주 사이클론",
    70: "죽음의 기사왕 아르가스",
    80: "흑룡 제왕 카르자크",
    90: "심연의 신 리바노스",
    100: "탑의 지배자 제로스"
}
# ==========================
# 상태창
# ==========================

def show_status():

    need_exp = player["level"] ** 2 * 20
    need_weapon = weapon["level"] ** 2 * 10

    print("\n" + "="*50)

    print(f"{player['name']} ({player['job']})")
    print(f"현재 층 : {floor}")

    print()

    print(f"LV {player['level']}")

    print(
        f"HP [{bar(player['hp'], player['max_hp'])}] "
        f"{player['hp']}/{player['max_hp']}"
    )

    print(
        f"EXP [{bar(player['exp'], need_exp)}] "
        f"{player['exp']}/{need_exp}"
    )

    print()

    print(
        f"검 : {weapon['name']} "
        f"(LV {weapon['level']})"
    )

    print(
        f"검 EXP [{bar(weapon['exp'], need_weapon)}] "
        f"{weapon['exp']}/{need_weapon}"
    )

    print(f"포션 : {player['potions']}")

    print("="*50)

# ==========================
# 스킬
# ==========================

def get_skills():

    lv = player["level"]

    if lv < 10:
        s1 = ("연속 베기",150)
    elif lv < 20:
        s1 = ("폭풍 베기",300)
    else:
        s1 = ("천공참",500)

    if lv < 10:
        s2 = ("강타",200)
    elif lv < 20:
        s2 = ("대지 강타",350)
    else:
        s2 = ("지진 붕괴",600)

    if lv < 10:
        s3 = ("흡혈격",180)
    elif lv < 20:
        s3 = ("생명 흡수",300)
    else:
        s3 = ("영혼 포식",500)

    return s1,s2,s3

# ==========================
# 레벨업
# ==========================

def level_up():

    while True:

        need = player["level"] ** 2 * 20

        if player["exp"] < need:
            break

        player["exp"] -= need
        player["level"] += 1

        player["max_hp"] += 20
        player["hp"] = player["max_hp"]

        player["atk"] += 5

        print(f"\n🎉 LV {player['level']} 달성!")

def weapon_level_up():

    while True:

        need = weapon["level"] ** 2 * 10

        if weapon["exp"] < need:
            break

        weapon["exp"] -= need
        weapon["level"] += 1   
        if weapon["level"] == 100:
         evolve_weapon()
        print(
            f"\n⚔️ {weapon['name']} "
            f"LV {weapon['level']}!"
        )

# ==========================
# 몬스터 생성
# ==========================

def create_monster():

    for r, monsters in monster_data.items():

        if r[0] <= floor <= r[1]:

            return {
                "name":
                random.choice(titles)
                + " "
                + random.choice(monsters),

                "hp":
                50 + floor * 20,

                "max_hp":
                50 + floor * 20,

                "atk":
                5 + floor * 3
            }

    return {
    "name":
    random.choice(titles)
    + " "
    + random.choice(monsters),

    "hp":
    50 + floor * 20,

    "max_hp":
    50 + floor * 20,

    "atk":
    5 + floor * 3,

    "boss": False
}
def create_boss():

    boss_name = bosses[floor]

    if floor == 100:

        hp = 50000
        atk = 3000

    else:

        hp = floor * 250
        atk = floor * 10

    return {

        "name": boss_name,

        "hp": hp,
        "max_hp": hp,

        "atk": atk,

        "boss": True
    }
# ==========================
# 포션
# ==========================

def use_potion():
    

    if player["potions"] <= 0:

        print("포션 없음!")
        return

    heal = player["max_hp"] // 2

    player["hp"] = min(
        player["max_hp"],
        player["hp"] + heal
    )

    player["potions"] -= 1

    print(f"{heal} 회복!")
    
def get_weapon_pool():

    if floor <= 20:

        return [
            "강철검",
            "기사검",
            "백은 성검"
        ]

    elif floor <= 40:

        return [
            "백은 성검",
            "붉은 달의 검",
            "그림자 절단검"
        ]

    elif floor <= 60:

        return [
            "화염 일륜도",
            "수류 일륜도",
            "뇌광 일륜도"
        ]

    elif floor <= 80:

        return [
            "흑룡참마검",
            "천멸신검",
            "창세신검 아르카디아"
        ]

    else:

        weapons = [
            "공허의 검 오블리비언",
            "무한의 검 에테르노바",
            "신살검 카오스브링어"
        ]

        if random.randint(1, 100) == 1:
            weapons.append("절대신검 엑스칼리온")

        return weapons
     
def choose_weapon_reward():

    global weapon

    print("\n" + "=" * 50)
    print("⚔️ 검 보상")
    print("=" * 50)

    rewards = []

    available_names = get_weapon_pool()

    possible_weapons = []

    for w in weapon_pool:

        if w["name"] in available_names:

            possible_weapons.append(w)

    rewards = random.sample(
        possible_weapons,
        min(3, len(possible_weapons))
    )

    for i, w in enumerate(rewards, start=1):

        print()

        print(
            f"{i}. {w['name']}"
        )

        print(
            f"ATK +{w['atk']}"
        )

        print(
            f"스킬 : "
            f"{w['skill_name']}"
        )

    print()
    print("0. 현재 검 유지")

    while True:

        choice = input(
            "\n선택 : "
        )

        if choice == "0":
            return

        if choice in [
            "1",
            "2",
            "3"
        ]:

            selected = rewards[
                int(choice)-1
            ]

            old_level = weapon["level"]
            old_exp = weapon["exp"]

            weapon = {

                "name":
                selected["name"],

                "level":
                old_level,

                "exp":
                old_exp,

                "atk":
                selected["atk"],

                "skill_name":
                selected["skill_name"],

                "skill_damage":
                selected["skill_damage"]
            }

            print(
                f"\n⚔️ "
                f"{selected['name']}"
                f" 장착!"
            )

            pause()

            return
# ==========================
# 전투
# ==========================

def battle(monster):

     while monster["hp"] > 0 and player["hp"] > 0:

        print("\n" + "=" * 50)
        print(monster["name"])

        print(
            f"몬스터 HP [{bar(monster['hp'], monster['max_hp'])}] "
            f"{monster['hp']}/{monster['max_hp']}"
        )

        print(
            f"내 HP [{bar(player['hp'], player['max_hp'])}] "
            f"{player['hp']}/{player['max_hp']}"
        )

        print()

        s1, s2, s3 = get_skills()
        print("0 기본공격")
        print(f"1 {s1[0]}")
        print(f"2 {s2[0]}")
        print(f"3 {s3[0]}")
        print(f"4 {weapon['skill_name']}")
        print("5 포션")

        choice = input("\n선택 : ")

        if choice == "5":
            use_potion()
            continue

        atk = player["atk"] + weapon["atk"]
        dmg = atk

        if choice == "1":
            dmg = atk * s1[1] // 100

        elif choice == "2":
            dmg = atk * s2[1] // 100

        elif choice == "3":

            dmg = atk * s3[1] // 100

            heal = dmg // 3

            player["hp"] = min(
                player["max_hp"],
                player["hp"] + heal
            )

        elif choice == "4":

            dmg = (
                atk *
                weapon["skill_damage"]
                // 100
            )

        # 크리티컬
        if random.randint(1, 100) <= player["crit"]:

            dmg *= 2

            print("🔥 크리티컬!")

        monster["hp"] -= dmg

        print(f"{dmg} 피해!")

        # 몬스터 처치
        if monster["hp"] <= 0:

            exp = floor * 15
            wexp = floor * 10

            if monster.get("boss", False):

                exp *= 3
                wexp *= 3

            print(
                f"\n{monster['name']} 처치!"
            )

            print(f"EXP +{exp}")
            print(f"검 EXP +{wexp}")

            player["exp"] += exp
            weapon["exp"] += wexp

            level_up()
            weapon_level_up()

            # 검 진화 체크
            if weapon["level"] >= 100:
                evolve_weapon()

            # 보스 드랍
            if monster.get("boss", False):
                boss_drop()

            return True

        # 몬스터 턴
        mdmg = monster["atk"]

        player["hp"] -= mdmg

        print(
            f"{monster['name']}의 공격!"
        )

        print(f"{mdmg} 피해!")

        if player["hp"] <= 0:

            return False
def evolve_weapon():

    evolutions = {

        "화염 일륜도":
        {
            "name": "홍련 일륜도",
            "atk": 500,
            "skill_name": "홍련멸화",
            "skill_damage": 3000
        },

        "수류 일륜도":
        {
            "name": "해신 일륜도",
            "atk": 550,
            "skill_name": "해신난무",
            "skill_damage": 3200
        },

        "뇌광 일륜도":
        {
            "name": "신뢰 일륜도",
            "atk": 600,
            "skill_name": "신뢰섬",
            "skill_damage": 3500
        },

        "창세신검 아르카디아":
        {
            "name": "창세신검 아르카디아 EX",
            "atk": 5000,
            "skill_name": "창세멸망",
            "skill_damage": 15000
        }
    }

    if weapon["name"] in evolutions:

        evo = evolutions[weapon["name"]]

        weapon["name"] = evo["name"]
        weapon["atk"] = evo["atk"]
        weapon["skill_name"] = evo["skill_name"]
        weapon["skill_damage"] = evo["skill_damage"]

        print("\n🌟 검 진화!")
        print(f"{weapon['name']} 획득!")
        return True

    mdmg = monster["atk"]

    player["hp"] -= mdmg

    print(
            f"{monster['name']}의 공격!"
        )

    print(f"{mdmg} 피해!")

    if player["hp"] <= 0:
            return False
def floor_reward():

    print("\n" + "=" * 50)

    print("층 클리어 보상")

    print("=" * 50)

    print("1. HP 완전 회복")
    print("2. 포션 +1")
    print("3. 검 선택")

    choice = input("\n선택 : ")

    if choice == "1":
        player["hp"] = player["max_hp"]

    elif choice == "2":
        player["potions"] += 1

    elif choice == "3":
        choose_weapon_reward()

    pause()
# ==========================
# 메인 루프
# ==========================

while True:

    show_status()

    if floor in bosses:

        monster = create_boss()

        print("\n" + "=" * 50)
        print(f"⚠️ {floor}층 보스 등장!")
        print(monster["name"])
        print("=" * 50)

    else:

        monster = create_monster()

    win = battle(monster)

    if win:
        floor += 1

        if floor % 10 == 1:
            checkpoint = floor

        print(
            f"\n{floor-1}층 클리어!"
        )
        floor_reward()
        if floor >= 100:
            print("\n🎉 GAME CLEAR 🎉")
            break

        pause()

    else:

        print("\n사망!")

        floor = checkpoint

        player["hp"] = player["max_hp"]

        print(
            f"{checkpoint}층에서 부활!"
        )

        pause()
       