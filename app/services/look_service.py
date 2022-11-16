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
from functools import reduce
from threading import Thread
from queue import Queue
import json


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


def get_looks(user_id, type):
    result = look_repository.get_look_set(user_id, type=type)
    return result


# Consumer
def look_generation_callback(queue, user_id):
    print('Consumer: Running')
    while True:
        queue.get()
        queue.task_done()
        categories = category_service.get_categories()
        daily_look_setup = get_daily_look_setup_by_user_id(user_id)
        casual_looks = __generate_casual_looks(user_id, categories, daily_look_setup)
        social_looks = __generate_social_looks(user_id, categories, daily_look_setup)
        looks = casual_looks + social_looks
        lookset = {
            "user_id": user_id,
            "looks": looks
        }
        result = look_repository.save_lookset(lookset, user_id)
        print(f"updated: {result}")


# Producer
def dispatch_look_generation(user_id):
    # create the shared queue
    queue = Queue(maxsize=100)
    # start the consumer
    consumer = Thread(
        target=look_generation_callback, 
        args=(queue, user_id), 
        daemon=True
    )
    consumer.start()
    queue.put(True)
    # wait for all threads to finish
    queue.join()


def __generate_casual_looks(user_id, categories, daily_look_setup):
    casual_clothes = __get_casual_clothes(user_id)
    casual_looks = __generate_looks(
        categories, casual_clothes, daily_look_setup, "casual")
    return casual_looks


def __generate_social_looks(user_id, categories, daily_look_setup):
    social_clothes = __get_social_clothes(user_id)
    social_looks = __generate_looks(
        categories, social_clothes, daily_look_setup, "social")
    return social_looks


def __generate_looks(categories, fetch_clothes, daily_look_setup, type):
    looks = []
    if len(categories) < 1 or len(fetch_clothes) < 1:
        return
    days_of_week = daily_look_setup.get("days_of_week")
    day_of_week_occasions = map(lambda day: day.get("occasions"), days_of_week)
    occasion_ids_map = map(lambda occasions: (
        map(lambda occasion: occasion.get("occasion_id"), occasions)), day_of_week_occasions)
    occasion_ids = reduce(lambda prev, curr: list(prev) + list(curr), occasion_ids_map, [])
    occasion_ids = set(occasion_ids)
    result = []
    for category in categories:
        category_id = category.get("_id")
        clothes = filter(lambda clothe: clothe.get("category_id") ==
                         category_id, fetch_clothes)
        clothes = list(clothes)
        total_clothes = len(clothes)
        result.append({
            "category_id": category_id,
            "category": category.get("name"),
            "total_clothes": total_clothes,
            "clothes": clothes
        })
    result.sort(key=(lambda clothe: clothe["total_clothes"]), reverse=True)
    if result[0].get("total_clothes") == 0:
        return
    category_ids = map(lambda category: category.get("_id"), categories)
    look_template = {}
    for category_id in category_ids:
        look_template[category_id] = None
    for a in result[0].get("clothes"):  # para cada peça na categoria 0 faça
        if result[1].get("total_clothes") == 0:  # se categoria 1 não tiver peças
            for occasion_id in occasion_ids:  # para cada ocasião cadastrada na rotina semanal
                look = json.loads(json.dumps(look_template))
                if occasion_id in a["occasions"]:
                    look[result[0]["category_id"]] = a
                looks_string = json.dumps(looks)
                look_string = json.dumps(look)
                if look_string not in looks_string:
                    key_values = look.keys()
                    key_values = filter(lambda x: x[1] != None, key_values)
                    if len(list(key_values)) > 0:
                        look = {
                            "data": look,
                            "occasion": occasion_id,
                            "period": None,
                            "timestamp": None,
                            "season": None,
                            "type": type
                        }
                        looks.append(look)
            continue
        for b in result[1].get("clothes"):
            if result[2].get("total_clothes") == 0:
                for occasion_id in occasion_ids:
                    look = json.loads(json.dumps(look_template))
                    if occasion_id in a["occasions"]:
                        look[result[0]["category_id"]] = a
                    if occasion_id in b["occasions"]:
                        look[result[1]["category_id"]] = b
                    looks_string = json.dumps(looks)
                    look_string = json.dumps(look)
                    if look_string not in looks_string:
                        key_values = look.keys()
                        key_values = filter(lambda x: x[1] != None, key_values)
                        if (len(list(key_values)) > 0):
                            look = {
                                "data": look,
                                "occasion": occasion_id,
                                "period": None,
                                "timestamp": None,
                                "season": None,
                                "type": type
                            }
                            looks.append(look)
                continue
            for c in result[2].get("clothes"):
                if result[3].get("total_clothes") == 0:
                    for occasion_id in occasion_ids:
                        look = json.loads(json.dumps(look_template))
                        if occasion_id in a["occasions"]:
                            look[result[0]["category_id"]] = a
                        if occasion_id in b["occasions"]:
                            look[result[1]["category_id"]] = b
                        if occasion_id in c["occasions"]:
                            look[result[2]["category_id"]] = c
                        looks_string = json.dumps(looks)
                        look_string = json.dumps(look)
                        if look_string not in looks_string:
                            key_values = look.keys()
                            key_values = filter(
                                lambda x: x[1] != None, key_values)
                            if len(key_values) > 0:
                                look = {
                                    "data": look,
                                    "occasion": occasion_id,
                                    "period": None,
                                    "timestamp": None,
                                    "season": None,
                                    "type": type
                                }
                                looks.append(look)
                    continue
                for d in result[3].get("clothes"):
                    if result[4].get("total_clothes") == 0:
                        for occasion_id in occasion_ids:
                            look = json.loads(json.dumps(look_template))
                            if occasion_id in a["occasions"]:
                                look[result[0]["category_id"]] = a
                            if occasion_id in b["occasions"]:
                                look[result[1]["category_id"]] = b
                            if occasion_id in c["occasions"]:
                                look[result[2]["category_id"]] = c
                            if occasion_id in d["occasions"]:
                                look[result[3]["category_id"]] = d
                            looks_string = json.dumps(looks)
                            look_string = json.dumps(look)
                            if (look_string not in looks_string):
                                key_values = look.keys()
                                key_values = filter(
                                    lambda x: x[1] != None, key_values)
                                if (len(list(key_values)) > 0):
                                    look = {
                                        "data": look,
                                        "occasion": occasion_id,
                                        "period": None,
                                        "timestamp": None,
                                        "season": None,
                                        "type": type
                                    }
                                    looks.append(look)
                        continue
                    for e in result[4].get("clothes"):
                        if result[5].get("total_clothes") == 0:
                            for occasion_id in occasion_ids:
                                look = json.loads(json.dumps(look_template))
                                if occasion_id in a["occasions"]:
                                    look[result[0]["category_id"]] = a
                                if occasion_id in b["occasions"]:
                                    look[result[1]["category_id"]] = b
                                if occasion_id in c["occasions"]:
                                    look[result[2]["category_id"]] = c
                                if occasion_id in d["occasions"]:
                                    look[result[3]["category_id"]] = d
                                if occasion_id in e["occasions"]:
                                    look[result[4]["category_id"]] = e
                                looks_string = json.dumps(looks)
                                look_string = json.dumps(look)
                                if (look_string not in looks_string):
                                    key_values = look.keys()
                                    key_values = filter(
                                        lambda x: x[1] != None, key_values)
                                    if (len(list(key_values)) > 0):
                                        look = {
                                            "data": look,
                                            "occasion": occasion_id,
                                            "period": None,
                                            "timestamp": None,
                                            "season": None,
                                            "type": type
                                        }
                                        looks.append(look)
                            continue
                        for f in result[5].get("clothes"):
                            if result[6].get("total_clothes") == 0:
                                for occasion_id in occasion_ids:
                                    look = json.loads(
                                        json.dumps(look_template))
                                    if occasion_id in a["occasions"]:
                                        look[result[0]["category_id"]] = a
                                    if occasion_id in b["occasions"]:
                                        look[result[1]["category_id"]] = b
                                    if occasion_id in c["occasions"]:
                                        look[result[2]["category_id"]] = c
                                    if occasion_id in d["occasions"]:
                                        look[result[3]["category_id"]] = d
                                    if occasion_id in e["occasions"]:
                                        look[result[4]["category_id"]] = e
                                    if occasion_id in f["occasions"]:
                                        look[result[5]["category_id"]] = f
                                    looks_string = json.dumps(looks)
                                    look_string = json.dumps(look)
                                    if (look_string not in looks_string):
                                        key_values = look.keys()
                                        key_values = filter(
                                            lambda x: x[1] != None, key_values)
                                        if (len(list(key_values)) > 0):
                                            look = {
                                                "data": look,
                                                "occasion": occasion_id,
                                                "period": None,
                                                "timestamp": None,
                                                "season": None,
                                                "type": type
                                            }
                                            looks.append(look)
                                continue
                            for g in result[6].get("clothes"):
                                if result[7].get("total_clothes") == 0:
                                    for occasion_id in occasion_ids:
                                        look = json.loads(
                                            json.dumps(look_template))
                                        if occasion_id in a["occasions"]:
                                            look[result[0]["category_id"]] = a
                                        if occasion_id in b["occasions"]:
                                            look[result[1]["category_id"]] = b
                                        if occasion_id in c["occasions"]:
                                            look[result[2]["category_id"]] = c
                                        if occasion_id in d["occasions"]:
                                            look[result[3]["category_id"]] = d
                                        if occasion_id in e["occasions"]:
                                            look[result[4]["category_id"]] = e
                                        if occasion_id in f["occasions"]:
                                            look[result[5]["category_id"]] = f
                                        if occasion_id in g["occasions"]:
                                            look[result[6]["category_id"]] = g
                                        looks_string = json.dumps(looks)
                                        look_string = json.dumps(look)
                                        if (look_string not in looks_string):
                                            key_values = look.keys()
                                            key_values = filter(
                                                lambda x: x[1] != None, key_values)
                                            if (len(list(key_values)) > 0):
                                                look = {
                                                    "data": look,
                                                    "occasion": occasion_id,
                                                    "period": None,
                                                    "timestamp": None,
                                                    "season": None,
                                                    "type": type
                                                }
                                                looks.append(look)
                                    continue
                                for h in result[7].get("clothes"):
                                    if result[8].get("total_clothes") == 0:
                                        for occasion_id in occasion_ids:
                                            look = json.loads(
                                                json.dumps(look_template))
                                            if occasion_id in a["occasions"]:
                                                look[result[0]
                                                     ["category_id"]] = a
                                            if occasion_id in b["occasions"]:
                                                look[result[1]
                                                     ["category_id"]] = b
                                            if occasion_id in c["occasions"]:
                                                look[result[2]
                                                     ["category_id"]] = c
                                            if occasion_id in d["occasions"]:
                                                look[result[3]
                                                     ["category_id"]] = d
                                            if occasion_id in e["occasions"]:
                                                look[result[4]
                                                     ["category_id"]] = e
                                            if occasion_id in f["occasions"]:
                                                look[result[5]
                                                     ["category_id"]] = f
                                            if occasion_id in g["occasions"]:
                                                look[result[6]
                                                     ["category_id"]] = g
                                            if occasion_id in h["occasions"]:
                                                look[result[7]
                                                     ["category_id"]] = h
                                            looks_string = json.dumps(looks)
                                            look_string = json.dumps(look)
                                            if (look_string not in looks_string):
                                                key_values = look.keys()
                                                key_values = filter(
                                                    lambda x: x[1] != None, key_values)
                                                if (len(list(key_values)) > 0):
                                                    look = {
                                                        "data": look,
                                                        "occasion": occasion_id,
                                                        "period": None,
                                                        "timestamp": None,
                                                        "season": None,
                                                        "type": type
                                                    }
                                                    looks.append(look)
                                        continue
                                    for i in result[8].get("clothes"):
                                        for occasion_id in occasion_ids:
                                            look = json.loads(
                                                json.dumps(look_template))
                                            if occasion_id in a["occasions"]:
                                                look[result[0]
                                                     ["category_id"]] = a
                                            if occasion_id in b["occasions"]:
                                                look[result[1]
                                                     ["category_id"]] = b
                                            if occasion_id in c["occasions"]:
                                                look[result[2]
                                                     ["category_id"]] = c
                                            if occasion_id in d["occasions"]:
                                                look[result[3]
                                                     ["category_id"]] = d
                                            if occasion_id in e["occasions"]:
                                                look[result[4]
                                                     ["category_id"]] = e
                                            if occasion_id in f["occasions"]:
                                                look[result[5]
                                                     ["category_id"]] = f
                                            if occasion_id in g["occasions"]:
                                                look[result[6]
                                                     ["category_id"]] = g
                                            if occasion_id in h["occasions"]:
                                                look[result[7]
                                                     ["category_id"]] = h
                                            if occasion_id in i["occasions"]:
                                                look[result[8]
                                                     ["category_id"]] = i
                                            looks_string = json.dumps(looks)
                                            look_string = json.dumps(look)
                                            if (look_string not in looks_string):
                                                key_values = look.keys()
                                                key_values = filter(
                                                    lambda x: x[1] != None, key_values)
                                                if (len(list(key_values)) > 0):
                                                    look = {
                                                        "data": look,
                                                        "occasion": occasion_id,
                                                        "period": None,
                                                        "timestamp": None,
                                                        "season": None,
                                                        "type": type
                                                    }
                                                    looks.append(look)
    return looks


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
