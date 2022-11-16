from app import db
from app.exceptions.error import FailToInitSeasons


ENUM_COLLECTION = "enum"
SEASONS_KEY = "seasons"
ID_KEY = "_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
EACH_KEY = "$each"
ID_ENUM = "9b05ef6d-18e8-49d7-9a94-8e1f59fbb2f8"

def save(enum):
    id = db[ENUM_COLLECTION].insert_one(enum).inserted_id
    return id


def get_seasons():
    seasons = db[ENUM_COLLECTION].find_one(
        { ID_KEY: ID_ENUM },
        { SEASONS_KEY: 1 }
    )
    if seasons and len(seasons) > 0:
        return seasons
    init_seasons()
    return get_seasons()


def get_seasons_count():
    result = db[ENUM_COLLECTION].find_one(
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


def add_season(season):
    result = db[ENUM_COLLECTION].update_one(
        { ID_KEY: ID_ENUM },
        { PUSH_KEY: { SEASONS_KEY: season } }
    )
    return result.modified_count


def save_many_seasons(seasons):
    result = db[ENUM_COLLECTION].update_one(
        { ID_KEY: ID_ENUM },
        { PUSH_KEY: { SEASONS_KEY: { EACH_KEY: seasons } } }, upsert=True
    )
    return result.matched_count


def init_seasons():
    print("INIT SEASONS")
    seasons = [
		"primavera",
		"verão",
		"outono",
		"inverno"
	]
    save_many_seasons(seasons)
    count = get_seasons_count()
    if count != len(seasons):
        raise FailToInitSeasons()


