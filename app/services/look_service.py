from app.utils import validation
from app.repositories import look_repository
from app.repositories import occasion_repository
from app.exceptions.error import DuplicatedDayOfWeekException
from app.exceptions.error import DuplicatedPeriodException
from app.exceptions.error import PeriodEmptyException
from app.exceptions.error import PeriodTooLongException
from app.exceptions.error import DuplicatedOccasionException
from app.exceptions.error import DuplicatedSortException
from app.services import category_service
from app.services import clothe_service
from app.services import closet_service
from app.services import util_service
from functools import reduce
from threading import Thread
from queue import Queue
import json
from datetime import datetime
from datetime import date


def update_daily_look_setup(user_id, data):
    __validate_before_save(data)
    result = look_repository.update_daily_look_setup(user_id, data)
    return result


def get_daily_look_setup_by_user_id(id):
    result = look_repository.get_daily_look_setup_by_user_id(id)
    return result


CASUAL = "casual"
SOCIAL = "social"

def __validate_before_save(data):
    global CASUAL
    global SOCIAL
    validation.assert_valid_schema(data, "daily_look_setup.json")
    days_of_week = data["days_of_week"]
    __is_day_of_week_duplicated(days_of_week)
    __is_occasion_duplicated(days_of_week)
    __is_sort_duplicated(days_of_week)
    # occasions_of_the_days = [ day["occasions"] for day in days_of_week ]
    for day_of_week in days_of_week: # iterate days
        occasions_of_the_day = day_of_week["occasions"]
        for occasion in occasions_of_the_day: # iterate occasions
            casual_list = occasion[CASUAL]
            __is_period_duplicated(casual_list)
            social_list = occasion[SOCIAL]
            __is_period_duplicated(social_list)
            casual_list_length = len(casual_list)
            social_list_length = len(social_list)
            lists_length_sum = casual_list_length + social_list_length
            __check_occasion_arrays_length(lists_length_sum)


def __is_day_of_week_duplicated(days_of_week):
    days = [ day["day_of_week"] for day in days_of_week ]
    set_of_days = set()
    for day in days:
        if day in set_of_days:
            raise DuplicatedDayOfWeekException()
        set_of_days.add(day)


def __is_period_duplicated(period_list):
    set_of_period = set()
    for period in period_list:
        if period in set_of_period:
            raise DuplicatedPeriodException()
        set_of_period.add(period)


def __check_occasion_arrays_length(lists_length_sum):
    if lists_length_sum < 1:
        raise PeriodEmptyException()
    if lists_length_sum > 2:
        raise PeriodTooLongException()


def __is_occasion_duplicated(days_of_week):
    occasions_list = [ day["occasions"] for day in days_of_week ]
    for item in occasions_list:
        set_of_ids = set()
        occasion_ids = [ occasion["occasion_id"] for occasion in item ]
        for id in occasion_ids:
            if id in set_of_ids:
                raise DuplicatedOccasionException()
            set_of_ids.add(id)


def __is_sort_duplicated(days_of_week):
    order_list = [ day["sort"] for day in days_of_week ]
    set_of_order = set()
    for order in order_list:
        if order in set_of_order:
            raise DuplicatedSortException()
        set_of_order.add(order)


def get_looks(
    user_id, 
    type=None, 
    timestamp=None,
	occasion=None,
	season=None,
	period=None
):
    result = look_repository.get_lookset(user_id)
    if result:
        # set days_count from created_at to today
        created_at = result.get("created_at")
        year, month, day = created_at.split(" ")[0].split("-")
        created_at = date(int(year), int(month), int(day))
        today = date.today()
        delta = today - created_at
        result["days_count"] = delta.days
        return result
    return -1


def __save_lookset(user_id, looks):
    total_days = 0
    for look in looks:
        ranking = look.get("sort")
        # if ranking is not None and ranking > total_days:
        if ranking > total_days:
            total_days = ranking
    lookset = {
        "user_id": user_id,
        "looks": looks,
        "created_at": str(datetime.now()),
        "total_days": total_days
    }
    validation.assert_valid_schema(lookset, "lookset.json")
    result = look_repository.save_lookset(lookset, user_id)
    return result


# Consumer
def generate_lookset(queue, user_id):
    print('Consumer: Running')
    global CASUAL
    global SOCIAL
    while True:
        queue.get()
        queue.task_done()
        # __save_lookset(user_id, []) # reset lookset
        daily_look_setup = get_daily_look_setup_by_user_id(user_id)
        days_of_week = daily_look_setup.get("days_of_week")
        # sorting to use today as the first day of week
        today = int(datetime.now().date().strftime("%w")) # https://pynative.com/python-get-the-day-of-week/
        days_of_week = days_of_week[today:] + days_of_week[0:today]
        categories = category_service.get_categories()
        seasons = util_service.get_seasons()
        periods = __get_periods()
        casual_clothes = __get_casual_clothes(user_id)
        casual_looks, casual_looks_without_match = __generate_looks_by_type_and_season(days_of_week, casual_clothes, CASUAL, categories, seasons, periods)
        social_clothes = __get_social_clothes(user_id)
        social_looks, social_looks_without_match = __generate_looks_by_type_and_season(days_of_week, social_clothes, SOCIAL, categories, seasons, periods)
        looks = casual_looks + social_looks
        # https://stackoverflow.com/a/73050
        looks = sorted(looks, key=lambda look: look["sort"]) 
        looks = looks + casual_looks_without_match + social_looks_without_match
        result = __save_lookset(user_id, looks)
        print(f"updated: {result}")
        break
    print("exit")


# Producer
def dispatch_look_generation(user_id):
    # create the shared queue
    queue = Queue(maxsize=5)
    # start the consumer
    consumer = Thread(
        target=generate_lookset, 
        args=(queue, user_id), 
        daemon=True
    )
    consumer.start()
    queue.put(True)
    # wait for all threads to finish
    queue.join()


def __generate_looks_by_type_and_season(days_of_week, clothes, look_type, categories, seasons, periods):
    looks = []
    occasion_ids = __get_occasions_from_daily_look_setup(days_of_week)
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
                result = __generate_looks(
                    categories=categories,
                    fetch_clothes=clothes_by_season,
                    look_type=look_type,
                    occasion_id=occasion_id
                    ,period=period.get("_id")
                )
                for look in result:
                    if __clothe_combination_already_exists(looks, look):
                        continue
                    looks.append(look)
    looks, looks_without_match = __set_looks_ranking(looks, days_of_week, look_type)
    return looks, looks_without_match


def __get_occasions_from_daily_look_setup(days_of_week):
    day_of_week_occasions = list(map(lambda day: day.get("occasions"), days_of_week))
    occasion_ids_map = list(map(lambda occasions: (
        list(map(lambda occasion: occasion.get("occasion_id"), occasions))), day_of_week_occasions))
    occasion_ids = reduce(lambda prev, curr: list(
        prev) + list(curr), occasion_ids_map, [])
    occasion_ids = set(occasion_ids)
    return occasion_ids


def __clothe_combination_already_exists(looks, look):
    lookset_stringfy = json.dumps(looks)
    look_stringfy = json.dumps(look)
    if look_stringfy in lookset_stringfy:
        return True
    return False


def __generate_clothe_combinations_metadata(looks, look, look_type, occasion_id, period):
    if __clothe_combination_already_exists(looks, look):
        return
    category_ids = list(look)
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
        "type": look_type, # casual/social
        "repeat_count": 0
    }
    return result


# recursive
def __generate_clothe_combinations(
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
        next_clothes_by_category = util_service.get_by_index(clothes_by_category, category_count+1)
        if next_clothes_by_category and next_clothes_by_category.get("total_clothes") > 0: # se a próxima categoria tiver peças
            looks = __generate_clothe_combinations(
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
        data = __generate_clothe_combinations_metadata(looks, look, look_type, occasion_id, period)
        if data is not None:
            looks.append(data)
        continue
    return looks


def __generate_looks(categories, fetch_clothes, look_type, occasion_id, period):
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
    category_ids = list(map(lambda category: category.get("_id"), categories))
    look_template = {}
    clothes = []
    for category_id in category_ids:
        look_template[category_id] = None
        clothes.append(None)
    looks = __generate_clothe_combinations(
        clothes_by_category,
        occasion_id,
        [], # looks
        look_template,
        look_type,
        period,
        clothes
    )
    return looks


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


def __set_looks_ranking(looks, days_of_week, look_type):
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
    looks_without_match = []
    for name in day_of_week_names:
        looks_by_day_of_week[name] = []
    looks_length = len(looks)
    i = 0
    while (looks_length > i):
        match = False
        for day_of_week in days_of_week:
            day_of_week_name = day_of_week.get("day_of_week")
            for daily_look in day_of_week.get("looks"):
                if i >= looks_length:
                    continue
                look = looks[i]
                match_occasion = look.get("occasion") == daily_look.get("occasion")
                match_closet = look.get("type") == daily_look.get("type")
                match_period = look.get("period") == daily_look.get("period")
                # match_season = daily_look.get("season") in look.get("season")
                if match_occasion and match_closet and match_period: # and match_season:
                    looks_by_day_of_week[day_of_week_name].append(look)
                    i = i + 1
                    match = True
        if not match:
            unmatch_look = looks[i]
            unmatch_look["sort"] = -1
            looks_without_match.append(unmatch_look)
            i = i + 1
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
    return result, looks_without_match


def __callback_set_looks_ranking_social(day):
    global SOCIAL
    return __callback_set_looks_ranking(day, SOCIAL)


def __callback_set_looks_ranking_casual(day):
    global CASUAL
    return __callback_set_looks_ranking(day, CASUAL)


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


# TODO: PERMITIR REPETIÇÃO DE LOOKS QUE COMPARTILHAM MAIS DE UMA OCASIÃO
# TODO: LEVAR EM CONTA SE O LOOK É PARA O DIA OU PARA A NOITE

def __get_casual_clothes(user_id):
    closet_id = __get_closet_id(user_id)
    casual_clothes = clothe_service.get_casual_clothes_by_closet_id(closet_id)
    return casual_clothes


def __get_social_clothes(user_id):
    closet_id = __get_closet_id(user_id)
    social_clothes = clothe_service.get_social_clothes_by_closet_id(closet_id)
    return social_clothes


def __get_closet_id(user_id):
    closet_id = 0
    closet = closet_service.get_closet_by_user_id(user_id)
    if closet:
        closet_id = closet.get("_id")
    return closet_id


def __get_periods():
    result = occasion_repository.get_periods()
    return result


def __get_day_occasion():
    result = occasion_repository.get_day()
    return result


def __get_night_occasion():
    result = occasion_repository.get_night()
    return result


def getlooksetrecursive():
    return look_repository.get_lookset_recursive()


def getlooksetprocedure():
    return look_repository.get_lookset_procedure()
