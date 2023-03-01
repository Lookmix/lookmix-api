from app import db
from bson.objectid import ObjectId

DAILY_LOOK_SETUP_COLLECTION = "daily_look_setup"
LOOKSET_COLLECTION = "lookset"
ID_KEY = "_id"
USER_ID_KEY = "user_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
IN_KEY = "$in"
MATCH_KEY = "$match"
PROJECT_KEY = "$project"
FILTER_KEY = "$filter"
EQUAL_KEY = "$eq"
INPUT_KEY = "input"
AS_KEY = "as"
CONDITION_KEY = "cond"
AND_KEY = "$and"

def update_daily_look_setup(user_id, data):
	result = db[DAILY_LOOK_SETUP_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: data },
		upsert=True
	).modified_count
	return result

def get_daily_look_setup_by_id(id):
    daily_look_setup = db[DAILY_LOOK_SETUP_COLLECTION].find_one(
		{ ID_KEY: ObjectId(id) }
	)
    if daily_look_setup:
        daily_look_setup[ID_KEY] = str(daily_look_setup[ID_KEY])
    return daily_look_setup

def get_daily_look_setup_by_user_id(id):
	daily_look_setup = db[DAILY_LOOK_SETUP_COLLECTION].find_one(
		{ USER_ID_KEY: id }
	)
	if daily_look_setup:
		daily_look_setup[ID_KEY] = str(daily_look_setup[ID_KEY])
	return daily_look_setup

def save_look(data):
    id = db[LOOKSET_COLLECTION].insert_one(data).inserted_id
    return id

def save_lookset(data, user_id):
    ids = db[LOOKSET_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: data },
		upsert=True
	).modified_count
    return ids

def get_lookset(
	user_id, 
	type=None,
	timestamp=None, 
	occasion=None, 
	season=None,
	period=None
):
	filters = []
	type_filter = { EQUAL_KEY: [ "$$item.type", type ] }
	timestamp_filter = { EQUAL_KEY: [ "$$item.timestamp", timestamp ] }
	occasion_filter = { EQUAL_KEY: [ "$$item.occasion", occasion ] }
	season_filter = { EQUAL_KEY: [ "$$item.season", season ] }
	period_filter = { EQUAL_KEY: [ "$$item.period", period ] }
	if type is not None:
		filters.append(type_filter)
	if timestamp is not None:
		filters.append(timestamp_filter)
	if occasion is not None:
		filters.append(occasion_filter)
	if season is not None:
		filters.append(season_filter)
	if period is not None:
		filters.append(period_filter)
	lookset = db[LOOKSET_COLLECTION].aggregate([
		{ MATCH_KEY: { USER_ID_KEY: user_id } },
		{
			PROJECT_KEY: {
				"user_id": 1,
				"created_at": 1,
				"days_count": 1,
				"total_days": 1,
				"looks": {
					FILTER_KEY: {
						INPUT_KEY: "$looks",
						AS_KEY: "item",
						CONDITION_KEY: { AND_KEY: filters }
					}
				}
			}
		}
	])
	lookset = list(lookset)
	if len(lookset) == 1:
		lookset = lookset[0]
		lookset[ID_KEY] = str(lookset[ID_KEY])
		return lookset
	return 0

def update_lookset_casual(user_id, data):
	result = db[LOOKSET_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: { "casual": data } }
	).modified_count
	return result

def update_lookset_social(user_id, data):
	result = db[LOOKSET_COLLECTION].update_one(
		{ USER_ID_KEY: user_id },
		{ SET_KEY: { "social": data } }
	).modified_count
	return result

def get_lookset_recursive():
	# lookset = db["lookset_recursive"].aggregate([
	# 	{ MATCH_KEY: { USER_ID_KEY: "63857a4cd8e4a56a37cfa115" } },
	# 	{
	# 		PROJECT_KEY: {
	# 			"user_id": 1,
	# 			"looks": {
	# 				FILTER_KEY: {
	# 					INPUT_KEY: "$looks",
	# 					AS_KEY: "item",
	# 					CONDITION_KEY: { AND_KEY: [
	# 						{ EQUAL_KEY: [ "$$item.type", "casual" ] }
	# 					] }
	# 				}
	# 			}
	# 		}
	# 	}
	# ])
	# lookset = list(lookset)
	# if len(lookset) == 1:
	# 	lookset = lookset[0]
	# 	lookset[ID_KEY] = str(lookset[ID_KEY])
	# return lookset
	lookset = db["lookset_recursive"].find_one(
		{ USER_ID_KEY: "6298301fed1909971532ca92" }
	)
	if lookset:
		lookset[ID_KEY] = str(lookset[ID_KEY])
	return lookset

def get_lookset_procedure():
	# lookset = db["lookset_procedural"].aggregate([
	# 	{ MATCH_KEY: { USER_ID_KEY: "63857a4cd8e4a56a37cfa115" } },
	# 	{
	# 		PROJECT_KEY: {
	# 			"user_id": 1,
	# 			"looks": {
	# 				FILTER_KEY: {
	# 					INPUT_KEY: "$looks",
	# 					AS_KEY: "item",
	# 					CONDITION_KEY: { AND_KEY: [
	# 						{ EQUAL_KEY: [ "$$item.type", "casual" ] }
	# 					] }
	# 				}
	# 			}
	# 		}
	# 	}
	# ])
	# lookset = list(lookset)
	# if len(lookset) == 1:
	# 	lookset = lookset[0]
	# 	lookset[ID_KEY] = str(lookset[ID_KEY])
	# return lookset
	lookset = db["lookset_procedural"].find_one(
		{ USER_ID_KEY: "6298301fed1909971532ca92" }
	)
	if lookset:
		lookset[ID_KEY] = str(lookset[ID_KEY])
	return lookset
