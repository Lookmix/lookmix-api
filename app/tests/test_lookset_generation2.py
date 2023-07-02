from functools import reduce
from threading import Thread
from queue import Queue
import json
from datetime import datetime
from datetime import date
import time

# Consumer
def generate_lookset(): # (queue, flag):
    print('Consumer: Running')
    global CASUAL
    global SOCIAL
    while True:
        # queue.get()
        # queue.task_done()
        # save_lookset(user_id, []) # reset lookset
        daily_look_setup = get_daily_look_setup_by_user_id()
        days_of_week = daily_look_setup.get("days_of_week")
        # sorting to use today as the first day of week
        today = int(datetime.now().date().strftime("%w")) # https://pynative.com/python-get-the-day-of-week/
        days_of_week = days_of_week[today:] + days_of_week[0:today]
        categories = get_categories()
        seasons = get_seasons()
        periods = get_periods()
        casual_clothes = get_casual_clothes()
        casual_looks = generate_looks_by_type_and_season(days_of_week, casual_clothes, CASUAL, categories, seasons, periods)
        social_clothes = get_social_clothes()
        social_looks = generate_looks_by_type_and_season(days_of_week, social_clothes, SOCIAL, categories, seasons, periods)
        looks = casual_looks + social_looks
        # https://stackoverflow.com/a/73050
        looks = sorted(looks, key=lambda look: look["sort"]) 
        # result = save_lookset(user_id, looks)
        write_json(looks)
        print(f"updated: {len(looks)}")
        break
    print("exit")


# Producer
def dispatch_look_generation():
    # create the shared queue
    queue = Queue(maxsize=5)
    # start the consumer
    consumer = Thread(
        target=generate_lookset, 
        args=(queue, True),
        daemon=True
    )
    consumer.start()
    queue.put(True)
    # wait for all threads to finish
    queue.join()


def generate_looks_by_type_and_season(days_of_week, clothes, look_type, categories, seasons, periods):
    looks = []
    occasion_ids = get_occasions_from_daily_look_setup(days_of_week)
    for occasion_id in occasion_ids:
        clothes_by_occasion = filter(
            lambda clothe: occasion_id in clothe.get("occasions"), 
        clothes)
        clothes_by_occasion = list(clothes_by_occasion)
        for period in periods:
            clothes_by_period = filter(
                lambda clothe: period.get("_id") in clothe.get("occasions"), 
            clothes_by_occasion)
            clothes_by_period = list(clothes_by_period)
            if len(clothes_by_period) < 1:
                continue
            for season in seasons:
                clothes_by_season = filter(
                    lambda clothe: season.lower() in clothe.get("seasons"), 
                clothes_by_period)
                clothes_by_season = list(clothes_by_season)
                result = generate_looks(
                    categories=categories,
                    fetch_clothes=clothes_by_season,
                    look_type=look_type,
                    occasion_id=occasion_id
                    ,period=period.get("_id")
                )
                for look in result:
                    if clothe_combination_already_exists(looks, look):
                        continue
                    looks.append(look)
    looks = set_looks_ranking(looks, days_of_week, look_type)
    return looks


def get_occasions_from_daily_look_setup(days_of_week):
    day_of_week_occasions = map(lambda day: day.get("occasions"), days_of_week)
    occasion_ids_map = map(lambda occasions: (
        map(lambda occasion: occasion.get("occasion_id"), occasions)), day_of_week_occasions)
    occasion_ids = reduce(lambda prev, curr: list(
        prev) + list(curr), occasion_ids_map, [])
    occasion_ids = set(occasion_ids)
    return occasion_ids


def clothe_combination_already_exists(looks, look):
    lookset_stringfy = json.dumps(looks)
    look_stringfy = json.dumps(look)
    if look_stringfy in lookset_stringfy:
        return True
    return False


def generate_clothe_combinations_metadata(looks, look, look_type, occasion_id, period):
    if clothe_combination_already_exists(looks, look):
        return
    category_ids = look.keys()
    category_ids = list(filter(lambda category_id: look[category_id] != None, category_ids))
    min_clothes = 2
    if len(category_ids) < min_clothes:
        return
    seasons = []
    for category_id in category_ids:
        look_seasons = look[category_id].get("seasons")
        if len(seasons) > 0 and len(seasons) < len(look_seasons):
            continue
        seasons = look_seasons
    result = {
        "data": look,
        "occasion": occasion_id,
        "period": period, # day/night
        "sort": None,
        "season": seasons,
        "type": look_type,
        "repeat_count": 0
    }
    return result


# recursive
def generate_clothe_combinations(
    clothes_by_category,
    occasion_id,
    looks, # array
    look_template,
    look_type,
    period,
    clothes=[],
    category_count=0 # zero-based index/counter
):
    for clothe in clothes_by_category[category_count].get("clothes"): # para cada peça na categoria atual faça
        clothes[category_count] = clothe
        next_clothes_by_category = get_by_index(clothes_by_category, category_count+1)
        if next_clothes_by_category and next_clothes_by_category.get("total_clothes") > 0: # se a próxima categoria tiver peças
            looks = generate_clothe_combinations(
                clothes_by_category,
                occasion_id,
                looks,
                look_template,
                look_type,
                period,
                clothes,
                category_count+1
            )
        look = json.loads(json.dumps(look_template))
        for previous_clothe_index, previous_clothe in enumerate(clothes):
            look[clothes_by_category[previous_clothe_index]["category_id"]] = previous_clothe
        data = generate_clothe_combinations_metadata(looks, look, look_type, occasion_id, period)
        if data is not None:
            looks.append(data)
        continue
    return looks


def generate_looks(categories, fetch_clothes, look_type, occasion_id, period):
    if len(categories) < 1 or len(fetch_clothes) < 1:
        return
    clothes_by_category = []
    for category in categories:
        category_id = category.get("_id")
        clothes = filter(lambda clothe: clothe.get(
            "category_id") == category_id, fetch_clothes)
        clothes = list(clothes)
        total_clothes = len(clothes)
        clothes_by_category.append({
            "category_id": category_id,
            "category": category.get("name"),
            "total_clothes": total_clothes,
            "clothes": clothes
        })
    clothes_by_category.sort(
        key=(lambda clothe: clothe["total_clothes"]), reverse=True)
    if clothes_by_category[0].get("total_clothes") == 0:
        return
    category_ids = map(lambda category: category.get("_id"), categories)
    look_template = {}
    clothes = []
    for category_id in category_ids:
        look_template[category_id] = None
        clothes.append(None)
    looks = generate_clothe_combinations(
        clothes_by_category,
        occasion_id,
        [], # looks
        look_template,
        look_type,
        period,
        clothes
    )
    return looks


def get_look_count_by_day_of_week(days_of_week, look_type):
    look_count_by_day_of_week = []
    for day in days_of_week:
        daily_look_count = 0
        occasion_ids = []
        for occasion in day["occasions"]:
            occasions_length = len(occasion[look_type])
            daily_look_count += occasions_length
            if occasions_length > 0:
                occasion_ids.append(occasion["occasion_id"])
        occasion_and_look_count_by_day_of_week = {
            "daily_look_count": daily_look_count,
            "occasion_ids": occasion_ids,
            "periods": []
            # { 
            # occasionid: [ idnoite, iddia ], 
            # occasionid: [ idnoite, iddia ],
            # }
        }
        # occasion_and_look_count_by_day_of_week["periods"].append(
        #     { map(lambda occasion: { occasion["occasion_id"]: occasion[type] }, day["occasions"]) }
        # )
        look_count_by_day_of_week.append(occasion_and_look_count_by_day_of_week)
    return look_count_by_day_of_week

# type: social, casual
def get_period_by_day_occasion(days_of_week, look_type):
    result = []
    for day_of_week in days_of_week:
        occasions = day_of_week.get("occasions")
        day_of_week_occasions = []
        for occasion in occasions:
            occasion_id = occasion.get("occasion_id")
            periods = occasion.get(look_type)
            occasions = map(lambda period: { occasion_id: period }, periods)
            day_of_week_occasions = day_of_week_occasions + list(occasions)
        result.append(day_of_week_occasions)
    return result
    # [
    #   [ # sunday
    #       { occasion_id1: day_id },
    #       { occasion_id1: night_id },
    #       { occasion_id2: night_id }
    #   ]
    # 
    # TODO: CORRIGIR PROBLEMA NA ORDENAÇÃO DOS LOOKS:
    # UM LOOK PARA O DIA ESTÁ SENDO ALOCADO PARA UMA 
    # OCASIÇÃO NOTURNA

def generate_look2():
    # FILTER CLOTHES BY OCCASION
    # FILTER CLOTHES BY TYPE (CASUAL/SOCIAL)
    # FILTER CLOTHES BY SEASON
    # FILTER CLOTHES BY PERIOD (DAY/NIGHT)
    # GENERATE LOOKS
    # SORT LOOKS BY DAY OF WEEK ACCORDING WITH OCCASION, TYPE, SEASON AND PERIOD
    pass


def __callback_set_looks_ranking(day, type):
    looks = []
    for occasion in day.get("occasions"):
        for period in occasion[type]:
            item = {
                "occasion": occasion.get("occasion_id"),
                "type": type,
                "period": period,
                "season": None
            }
            looks.append(item)
    return {
        "day_of_week": day.get("day_of_week"),
        "looks": looks
    }

CASUAL = "casual"
SOCIAL = "social"

def __callback_set_looks_ranking_social(day):
    global SOCIAL
    return __callback_set_looks_ranking(day, SOCIAL)

def __callback_set_looks_ranking_casual(day):
    global CASUAL
    return __callback_set_looks_ranking(day, CASUAL)

def set_looks_ranking(looks, days_of_week, look_type):
    global CASUAL
    if look_type == CASUAL:
        days_of_week = map(__callback_set_looks_ranking_casual, days_of_week)
    else:
        days_of_week = map(__callback_set_looks_ranking_social, days_of_week)
    days_of_week = list(days_of_week)
    day_of_week_names = map(lambda day: day.get("day_of_week"), days_of_week)
    day_of_week_names = list(day_of_week_names)
    # sorting, first day of week must be today
    today_day_of_week_index = int(datetime.now().date().strftime("%w"))
    day_of_week_names = day_of_week_names[today_day_of_week_index:] + day_of_week_names[:today_day_of_week_index]
    looks_by_day_of_week = {}
    for name in day_of_week_names:
        looks_by_day_of_week[name] = []
    looks_length = len(looks)
    for i in range(0, looks_length):
        look = looks[i]
        match = False
        for day_of_week in days_of_week:
            if match:
                continue
            day_of_week_name = day_of_week.get("day_of_week")
            for daily_look in day_of_week.get("looks"):
                if match:
                    continue
                match_occasion = look.get("occasion") == daily_look.get("occasion")
                match_closet = look.get("type") == daily_look.get("type")
                match_period = look.get("period") == daily_look.get("period")
                # match_season = daily_look.get("season") in look.get("season")
                if match_occasion and match_closet and match_period: # and match_season:
                    looks_by_day_of_week[day_of_week_name].append(look)
                    match = True
    result = []
    has_look = True
    sort = 0
    while has_look:
        for day_of_week in days_of_week:
            day_of_week_name = day_of_week.get("day_of_week")
            for look_setup in day_of_week.get("looks"):
                look_index = None
                for index in range(0, len(looks_by_day_of_week[day_of_week_name])):
                    if looks_by_day_of_week[day_of_week_name][index].get("occasion") == look_setup.get("occasion"):
                        look_index = index
                        break
                if look_index != None:
                    look = looks_by_day_of_week[day_of_week_name].pop(look_index)
                    look["sort"] = sort
                    result.append(look)
            sort = sort + 1
        # stop condition
        remaining_looks = []
        for day_of_week in days_of_week:
            day_of_week_name = day_of_week.get("day_of_week")
            remaining_looks = remaining_looks + looks_by_day_of_week[day_of_week_name]
        if len(remaining_looks) == 0:
            has_look = False
    json_object = json.dumps(result, indent=4)
    with open(f"looksbysdayofweek_{look_type}.json", "w") as outfile:
        outfile.write(json_object)
    return result

    '''
    days_of_week = [
        {
            day_of_week: "segunda",
            looks: [
                {
                    occasion: "trabalho",
                    closet: "casual"
                    period: "day",
                    season: "fall"
                },
                {
                    occasion: "academia",
                    closet: "casual"
                    period: "night",
                    season: "fall"
                }
            ]
        }
    ]
    '''
    # TODO: SORT BY WEATHER OF THE DAY

# TODO: PERMITIR REPETIÇÃO DE LOOKS QUE COMPARTILHAM MAIS DE UMA OCASIÃO
# TODO: LEVAR EM CONTA SE O LOOK É PARA O DIA OU PARA A NOITE

def get_daily_look_setup_by_user_id():
    result = {
        "_id": "63d708d10eea647190f3cb7f",
        "days_of_week": [
            {
                "day_of_week": "domingo",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035213"
                        ],
                        "occasion_id": "6315604bdaf4e3d095035220",
                        "social": [
                            "6315604bdaf4e3d095035214"
                        ]
                    }
                ],
                "sort": 0
            },
            {
                "day_of_week": "segunda",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035213"
                        ],
                        "occasion_id": "6315604bdaf4e3d095035215",
                        "social": []
                    }
                ],
                "sort": 1
            },
            {
                "day_of_week": "terça",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035214"
                        ],
                        "occasion_id": "6315604bdaf4e3d09503521c",
                        "social": []
                    }
                ],
                "sort": 2
            },
            {
                "day_of_week": "quarta",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035213"
                        ],
                        "occasion_id": "6315604bdaf4e3d095035212",
                        "social": []
                    },
                    {
                        "casual": [],
                        "occasion_id": "6315604bdaf4e3d095035215",
                        "social": [
                            "6315604bdaf4e3d095035214"
                        ]
                    }
                ],
                "sort": 3
            },
            {
                "day_of_week": "quinta",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035214"
                        ],
                        "occasion_id": "6315604bdaf4e3d095035215",
                        "social": []
                    }
                ],
                "sort": 4
            },
            {
                "day_of_week": "sexta",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035213"
                        ],
                        "occasion_id": "6315604bdaf4e3d095035215",
                        "social": []
                    }
                ],
                "sort": 5
            },
            {
                "day_of_week": "sábado",
                "occasions": [
                    {
                        "casual": [
                            "6315604bdaf4e3d095035213"
                        ],
                        "occasion_id": "6315604bdaf4e3d09503521c",
                        "social": []
                    }
                ],
                "sort": 6
            }
        ],
        "user_id": "6298301fed1909971532ca92"
    }
    return result

def get_casual_clothes():
    casual_clothes = [
        {
            "_id": "62a413f666724c5f403cf980",
            "category_id": "629d286bec74d540eb5fb0e9",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52137525213_e856c41ae9_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035212"
            ],
            "seasons": [
                "primavera",
                "verão",
                "outono"
            ],
            "type": "casual"
        },
        {
            "_id": "62a413f966724c5f403cf981",
            "category_id": "629d286bec74d540eb5fb0e9",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52137741934_a4a99fcabf_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a",
                "6315604bdaf4e3d09503521c"
            ],
            "seasons": [
                "primavera",
                "verão",
                "outono",
                "inverno"
            ],
            "type": "casual"
        },
        {
            "_id": "62a4140866724c5f403cf986",
            "category_id": "629d286bec74d540eb5fb0e8",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52137503691_33070fd125_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035212",
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "primavera",
                "verão",
                "outono",
                "inverno"
            ],
            "type": "casual"
        },
        {
            "_id": "62a4169a66724c5f403cf987",
            "category_id": "629d286bec74d540eb5fb0e8",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52137515811_b8022953f4_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "primavera",
                "verão",
                "outono",
                "inverno"
            ],
            "type": "casual"
        },
        {
            "_id": "62a7f1bf4ff9bba04173359a",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52145403355_86bf6d6cab_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "primavera"
            ],
            "type": "casual"
        },
        {
            "_id": "62c9d85bd168f9c20acb7950",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52205398840_b6e41d506c_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "primavera",
                "verão"
            ],
            "type": "casual"
        },
        {
            "_id": "62c9e3fbd168f9c20acb795a",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52205256934_2cfce4c495_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d09503521a",
                "6315604bdaf4e3d095035219"
            ],
            "seasons": [
                "primavera",
                "verão"
            ],
            "type": "casual"
        },
        {
            "_id": "62cce00abce9ce70a9a56914",
            "category_id": "629d286bec74d540eb5fb0e8",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52210782224_9c450ceac7_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "inverno",
                "outono"
            ],
            "type": "casual"
        },
        {
            "_id": "62cf902d501ba2742df1fa91",
            "category_id": "629d286bec74d540eb5fb0e9",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52215069973_f7bf69327f_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035212",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035214"
            ],
            "seasons": [
                "primavera",
                "outono"
            ],
            "type": "casual"
        },
        {
            "_id": "62cf9c58c973e41fdbfde779",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52215124508_6fab503a0f_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d09503521c",
                "6315604bdaf4e3d09503521d"
            ],
            "seasons": [
                "primavera",
                "verão"
            ],
            "type": "casual"
        },
        {
            "_id": "62d0d70867f3eaba19fd0b53",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52217114716_edc4eae397_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "outono"
            ],
            "type": "casual"
        },
        {
            "_id": "62e881a9d778ffcff674dace",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52257353078_592981c715_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035212",
                "6315604bdaf4e3d095035216"
            ],
            "seasons": [
                "Inverno",
                "Outono"
            ],
            "type": "casual"
        },
        {
            "_id": "62e8872913adc71d29f9a0f7",
            "category_id": "629d286bec74d540eb5fb0e9",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52257861670_1c20994936_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035216",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "primavera",
                "verão",
                "inverno",
                "outono"
            ],
            "type": "casual"
        },
        {
            "_id": "6316c43f9ae66942d36d846e",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52338066380_7dbb9a9274_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035212",
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035219",
                "6315604bdaf4e3d09503521a",
                "6315604bdaf4e3d09503521e"
            ],
            "seasons": [
                "primavera",
                "verão"
            ],
            "type": "casual"
        }
    ]
    return casual_clothes

def get_social_clothes():
    social_clothes = [
        {
            "_id": "62c9c91d336080751568ceae",
            "category_id": "629d286bec74d540eb5fb0e7",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52204773396_8dcc9479d5_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "inverno",
                "outono"
            ],
            "type": "social"
        },
        {
            "_id": "62fc629e98e43430688253f9",
            "category_id": "629d286bec74d540eb5fb0ee",
            "closet_id": "72177720299676310",
            "image": "https://live.staticflickr.com/65535/52291448274_69f0ca273c_n.jpg",
            "occasions": [
                "6315604bdaf4e3d095035214",
                "6315604bdaf4e3d095035213",
                "6315604bdaf4e3d095035215",
                "6315604bdaf4e3d095035217",
                "6315604bdaf4e3d095035218",
                "6315604bdaf4e3d09503521a"
            ],
            "seasons": [
                "primavera",
                "verão",
                "inverno",
                "outono"
            ],
            "type": "social"
        }
    ]
    return social_clothes

def get_periods():
    result = [
        {
            "_id": "6315604bdaf4e3d095035213",
            "name":"dia",
            "tags":["day"],
            "type":"period"
        },
        {
            "_id": "6315604bdaf4e3d095035214",
            "name":"noite",
            "tags":["night"],
            "type":"period"
        }
    ]
    return result

def get_categories():
    return [
        {
            "_id": "629d286bec74d540eb5fb0ea",
            "name": "Peças sobrepostas",
            "description": "Casacos, jaquetas, moletons ou sobretudos",
            "sort": 4
        },
        {
            "_id": "629d286bec74d540eb5fb0e9",
            "name": "Pés",
            "description": "Calçados ou meias",
            "sort": 3
        },
        {
            "_id": "629d286bec74d540eb5fb0e7",
            "name": "Roupas de cima",
            "description": "Camisas, camisetas, polos, blusas ou regatas",
            "sort": 1
        },
        {
            "_id": "629d286bec74d540eb5fb0eb",
            "name": "Peças únicas",
            "description": "Vestidos ou macacões",
            "sort": 5
        },
        {
            "_id": "629d286bec74d540eb5fb0ec",
            "name": "Acessórios de cabeça",
            "description": "Bonés, chapéus, óculos, brincos ou laços",
            "sort": 6
        },
        {
            "_id": "629d286bec74d540eb5fb0ed",
            "name": "Acessórios de pescoço",
            "description": "Colares, correntes, gravatas ou cachecóis",
            "sort": 7
        },
        {
            "_id": "629d286bec74d540eb5fb0ee",
            "name": "Acessórios de braços e mãos",
            "description": "Bolsas, pulseiras, relógios, anéis ou luvas",
            "sort": 8
        },
        {
            "_id": "629d286bec74d540eb5fb0ef",
            "name": "Cintura",
            "description": "Cintos ou laços",
            "sort": 9
        },
        {
            "_id": "629d286bec74d540eb5fb0e8",
            "name": "Pernas",
            "description": "Calças, shorts, saias ou bermudas",
            "sort": 2
        }
    ]

def get_seasons():
    return [
        "primavera",
        "verão",
        "outono",
        "inverno"
    ]

def get_by_index(array, index):
    try:
        return array[index]
    except IndexError as e:
        return False
    
def write_json(data):
    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to sample.json
    with open("recursive5.json", "w") as outfile:
    # with open("procedure4.json", "w") as outfile:
        outfile.write(json_object)
    print(len(data))

generate_lookset()