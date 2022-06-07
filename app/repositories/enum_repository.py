from app import db
from app.exceptions.error import FailToInitOccasions
from app.exceptions.error import FailToInitSeasons


ENUM_DOC = "enum"
SEASONS_KEY = "seasons"
OCCASIONS_KEY = "occasions"
ID_KEY = "_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
EACH_KEY = "$each"
ID_ENUM = "9b05ef6d-18e8-49d7-9a94-8e1f59fbb2f8"

def save(enum):
    id = db[ENUM_DOC].insert_one(enum).inserted_id
    return id


def get_occasions():
    occasions = db[ENUM_DOC].find_one(
        { ID_KEY: ID_ENUM },
        { OCCASIONS_KEY: 1 }
    )
    if occasions and len(occasions) > 0:
        return occasions
    init_occasions()
    return get_occasions()


def get_occasions_count():
    result = db[ENUM_DOC].find_one(
        { ID_KEY: ID_ENUM },
        { OCCASIONS_KEY: 1 }
    )
    occasions = None
    if result:
        occasions = result.get(OCCASIONS_KEY, None)
    if occasions:
        count = len(occasions)
        return count
    return 0


def get_seasons():
    seasons = db[ENUM_DOC].find_one(
        { ID_KEY: ID_ENUM },
        { SEASONS_KEY: 1 }
    )
    if seasons and len(seasons) > 0:
        return seasons
    init_seasons()
    return get_seasons()


def get_seasons_count():
    result = db[ENUM_DOC].find_one(
        { ID_KEY: ID_ENUM },
        { SEASONS_KEY: 1 }
    )
    seasons = None
    if result:
        seasons = result.get(SEASONS_KEY, None)
    if seasons:
        count = len(seasons)
        return count
    return 0


def add_occasion(occasion):
    result = db[ENUM_DOC].update_one(
        { ID_KEY: ID_ENUM },
        { PUSH_KEY: { OCCASIONS_KEY: occasion } }
    )
    return result.modified_count


def save_many_occasions(occasions):
    result = db[ENUM_DOC].update_one(
        { ID_KEY: ID_ENUM },
        { PUSH_KEY: { OCCASIONS_KEY: { EACH_KEY: occasions } } }, upsert=True
    )
    return result.matched_count


def add_season(season):
    result = db[ENUM_DOC].update_one(
        { ID_KEY: ID_ENUM },
        { PUSH_KEY: { SEASONS_KEY: season } }
    )
    return result.modified_count


def save_many_seasons(seasons):
    result = db[ENUM_DOC].update_one(
        { ID_KEY: ID_ENUM },
        { PUSH_KEY: { SEASONS_KEY: { EACH_KEY: seasons } } }, upsert=True
    )
    return result.matched_count


def init_occasions():
    print("INIT OCCASIONS")
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
    save_many_occasions(occasions)
    count = get_occasions_count()
    if count != len(occasions):
        raise FailToInitOccasions()


def init_seasons():
    print("INIT SEASONS")
    seasons = [
		"Primavera",
		"Verão",
		"Outono",
		"Inverno"
	]
    save_many_seasons(seasons)
    count = get_seasons_count()
    if count != len(seasons):
        raise FailToInitSeasons()


