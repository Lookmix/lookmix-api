from app.utils import validation
from app.repositories import look_repository
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


def update_daily_look_setup(user_id, data):
    __validate_before_save(data)
    result = look_repository.update_daily_look_setup(user_id, data)
    return result


def get_daily_look_setup_by_user_id(id):
    result = look_repository.get_daily_look_setup_by_user_id(id)
    return result


def __validate_before_save(data):
    validation.assert_valid_schema(data, "daily_look_setup.json")
    days_of_week = data["days_of_week"]
    __is_day_of_week_duplicated(days_of_week)
    __is_occasion_duplicated(days_of_week)
    __is_sort_duplicated(days_of_week)
    # occasions_of_the_days = [ day["occasions"] for day in days_of_week ]
    for day_of_week in days_of_week: # iterate days
        occasions_of_the_day = day_of_week["occasions"]
        for occasion in occasions_of_the_day: # iterate occasions
            casual_list = occasion["casual"]
            __is_period_duplicated(casual_list)
            social_list = occasion["social"]
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
    type, 
    timestamp=None,
	occasion=None,
	season=None,
	period=None
):
    result = look_repository.get_lookset(user_id, type=type)
    if result: 
        return result
    # len(result.get("looks")) < 1: empty closet, no way to generate lookset
    return 0 # in progress lookset generate


# Consumer
def generate_lookset(queue, user_id):
    print('Consumer: Running')
    while True:
        queue.get()
        queue.task_done()
        daily_look_setup = get_daily_look_setup_by_user_id(user_id)
        days_of_week = daily_look_setup.get("days_of_week")
        casual_clothes = __get_casual_clothes(user_id)
        casual_looks = __generate_looks_by_type_and_season(days_of_week, casual_clothes, "casual")
        social_clothes = __get_social_clothes(user_id)
        social_looks = __generate_looks_by_type_and_season(days_of_week, social_clothes, "social")
        looks = casual_looks + social_looks
        total_days = looks[len(looks)-1].get("sort")
        lookset = {
            "user_id": user_id,
            "looks": looks,
            "created_at": datetime.now(),
            "days_count": 0,
            "total_days": total_days
        }
        validation.assert_valid_schema(lookset, "lookset.json")
        result = look_repository.save_lookset(lookset, user_id)
        print(f"updated: {result}")


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


def __generate_looks_by_type_and_season(days_of_week, clothes, type):
    categories = category_service.get_categories()
    seasons = util_service.get_seasons()
    looks = []
    occasion_ids = __get_occasions_from_daily_look_setup(days_of_week)
    for occasion_id in occasion_ids:
        clothes_by_occasion = filter(
            lambda clothe: occasion_id in clothe.get("occasions"), 
        clothes)
        clothes_by_occasion = list(clothes_by_occasion)
        if len(clothes_by_occasion) < 1:
            continue
        for season in seasons:
            clothes_by_season = filter(
                lambda clothe: season.lower() in clothe.get("seasons"), 
            clothes_by_occasion)
            clothes_by_season = list(clothes_by_season)
            result = __generate_looks(
                categories=categories,
                fetch_clothes=clothes_by_season,
                type=type,
                occasion_id=occasion_id
            )
            for look in result:
                if __clothe_combination_already_exists(looks, look):
                    continue
                looks.append(look)
    looks = __set_looks_ranking(looks, days_of_week, type)
    return looks


def __get_occasions_from_daily_look_setup(days_of_week):
    day_of_week_occasions = map(lambda day: day.get("occasions"), days_of_week)
    occasion_ids_map = map(lambda occasions: (
        map(lambda occasion: occasion.get("occasion_id"), occasions)), day_of_week_occasions)
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


def __generate_clothe_combinations_metadata(looks, look, type, occasion_id):
    if __clothe_combination_already_exists(looks, look):
        return
    category_ids = look.keys()
    category_ids = list(filter(lambda category_id: look[category_id] != None, category_ids))
    if len(category_ids) > 1:
        # TODO: REFACTOR SEASONS SELECT
        seasons = reduce(lambda prev, curr_category_id: 
            list(prev) + list(look[curr_category_id].get("seasons")), category_ids, []
        )
        result = {
            "data": look,
            "occasion": occasion_id,
            "period": "-", # day/night
            "sort": None,
            "season": seasons,
            "type": type
        }
        return result


# recursive
def __generate_clothe_combinations(
    clothes_by_category,
    occasion_id,
    looks, # array
    look_template,
    type,
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
                type,
                clothes,
                category_count+1
            )
        look = json.loads(json.dumps(look_template))
        for previous_clothe_index, previous_clothe in enumerate(clothes):
            look[clothes_by_category[previous_clothe_index]["category_id"]] = previous_clothe
        data = __generate_clothe_combinations_metadata(looks, look, type, occasion_id)
        if data is not None:
            looks.append(data)
        continue
    return looks


def __generate_looks(categories, fetch_clothes, type, occasion_id):
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
    looks = __generate_clothe_combinations(
        clothes_by_category,
        occasion_id,
        [], # looks
        look_template,
        type,
        clothes
    )
    return looks


def __get_look_count_by_day_of_week(days_of_week, type):
    look_count_by_day_of_week = []
    for day in days_of_week:
        daily_look_count = 0
        occasion_ids = []
        for occasion in day["occasions"]:
            daily_look_count += len(occasion[type])
            occasion_ids.append(occasion["occasion_id"])
        occasion_and_look_count_by_day_of_week = {
            "daily_look_count": daily_look_count,
            "occasion_ids": occasion_ids
        }
        look_count_by_day_of_week.append(occasion_and_look_count_by_day_of_week)
    return look_count_by_day_of_week


def __set_looks_ranking(looks, days_of_week, type):
    lookcount_by_day_of_week = __get_look_count_by_day_of_week(days_of_week, type)
    ranking = 0
    result = []
    occasions = map(lambda look: look.get("occasion"), looks)
    occasions = set(occasions)
    looks_by_occasion = {}
    for occasion_id in occasions:
        looks_by_occasion[occasion_id] = list(filter(
            lambda look: look.get("occasion") == occasion_id,
        looks))
    while len(result) < len(looks):
        for day_of_week in lookcount_by_day_of_week:
            for occasion_id in day_of_week.get("occasion_ids"):
                if occasion_id not in occasions:
                    continue
                if len(looks_by_occasion[occasion_id]) < 1:
                    continue
                look = looks_by_occasion[occasion_id].pop(0)
                look["sort"] = ranking
                result.append(look)
            ranking += 1
    # TODO: SORT BY WEATHER OF THE DAY
    return result


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




def getlooksetrecursive():
    return look_repository.get_lookset_recursive()


def getlooksetprocedure():
    return look_repository.get_lookset_procedure()
