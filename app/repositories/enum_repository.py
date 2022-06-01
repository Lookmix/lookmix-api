from app import db
from exceptions.error import FailToInitOccasions
from exceptions.error import FailToInitSeasons


ENUM_DOC = "enum"
SEASONS_KEY = "seasons"
OCCASIONS_KEY = "occasions"
ID_KEY = "_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
EACH_KEY = "$each"

def save(enum):
    id = db[ENUM_DOC].insert_one(enum).inserted_id
    return id


def get_occasions():
    occasions = db[ENUM_DOC].find_one(
        { },
        { OCCASIONS_KEY: 1 }
    )
    return occasions


def get_occasions_count():
    occasions = db[ENUM_DOC].find_one(
        { },
        { OCCASIONS_KEY: 1 }
    )
    count = len(occasions)
    return count


def get_seasons():
	seasons = db[ENUM_DOC].find_one(
        { },
        { SEASONS_KEY: 1 }
    )
	return seasons


def get_seasons_count():
    seasons = db[ENUM_DOC].find_one(
        { },
        { SEASONS_KEY: 1 }
    )
    count = len(seasons)
    return count


def add_occasion(occasion):
    result = db[ENUM_DOC].update_one(
        { },
        { PUSH_KEY: { OCCASIONS_KEY: occasion } }
    )
    return result.modified_count


def save_many_occasions(occasions):
    result = db[ENUM_DOC].update_one(
        { },
        { PUSH_KEY: { OCCASIONS_KEY: { EACH_KEY: occasions } } }
    )
    return result.modified_count


def add_season(season):
    result = db[ENUM_DOC].update_one(
        { },
        { PUSH_KEY: { SEASONS_KEY: season } }
    )
    return result.modified_count


def save_many_seasons(seasons):
    result = db[ENUM_DOC].update_one(
        { },
        { PUSH_KEY: { SEASONS_KEY: { EACH_KEY: seasons } } }
    )
    return result.modified_count


def __init_occassions():
    print("Init occasions")
    occasions = [
		"Básico/comum",
		"Dia",
		"Noite",
		"Trabalho",
		"Curso/Faculdade",
		"Festa/evento",
		"Restaurante",
		"Shopping",
		"Viagem",
		"Praia",
		"Atividade física",
		"Natureza"
	]
    count = get_occasions_count()
    result = []
    if count < 1:
        result = save_many_occasions(occasions)
    if len(result) == len(occasions):
        return result
    raise FailToInitOccasions()


def __init_seasons():
    print("Init seasons")
    seasons = [
		"primavera",
		"verão",
		"outono",
		"inverno"
	]
    count = get_seasons()
    result = []
    if count < 1:
        result = save_many_seasons(seasons)
    if len(result) == len(seasons):
        return result
    raise FailToInitSeasons()


__init_occassions()
__init_seasons()
