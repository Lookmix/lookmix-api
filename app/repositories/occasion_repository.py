from app.application import db
from app.exceptions.error import FailToInitOccasions
from bson.objectid import ObjectId


OCCASION_COLLECTION = "occasion"
OCCASIONS_KEY = "occasions"
TAGS_KEY = "tags"
TYPE_KEY = "type"
ID_KEY = "_id"
SET_KEY = "$set"
PUSH_KEY = "$push"
EACH_KEY = "$each"
IN_KEY = "$in"

def save(occasion):
    id = db[OCCASION_COLLECTION].insert_one(occasion).inserted_id
    return id

def get_occasions():
    occasions = list(db[OCCASION_COLLECTION].find({}))
    occasions_lenght = len(occasions)
    if occasions_lenght > 0:
        for occasion in occasions:
            occasion["_id"] = str(occasion["_id"])
        return occasions
    init_occasions()
    return get_occasions()

def get_occasions_count():
    result = db[OCCASION_COLLECTION].count_documents({})
    if result:
        return result
    return 0

def get_by_id(id):
    occasion = db[OCCASION_COLLECTION].find_one({ID_KEY: ObjectId(id)})
    if occasion:
        occasion[ID_KEY] = str(occasion[ID_KEY])
    return occasion

def save_many_occasions(occasions):
    ids = db[OCCASION_COLLECTION].insert_many(occasions).inserted_ids
    return ids

def update(id, data):
    db[OCCASION_COLLECTION].update_one(
        {ID_KEY: id},
        {SET_KEY: data}, upsert=False
    )

def delete_by_ids (ids):
    ids = [ObjectId(id) for id in ids]
    result = db[OCCASION_COLLECTION].delete_many({
        ID_KEY: { IN_KEY: ids }
    })
    return result

def init_occasions():
    print("INIT OCCASIONS")
    occasions = [
        {
    		"name": "básico/comum",
            "card_look_title": "Look básico/comum",
            "type": "rotina",
            "tags": [
                "básico", 
                "básica",
                "comum", 
                "basic", 
                "limpa",
                "lisa",
                "limpo",
                "liso",
                "neutro",
                "neutra"
            ]
        },
        {
            "name": "dia",
            "tags": ["day"],
            "type": "period",
        },
        {
            "name": "noite",
            "tags": ["night"],
            "type": "period"
        },
        {
            "name": "trabalho",
            "card_look_title": "Look para o trabalho",
            "type": "rotina",
            "tags": [
                "trabalho",
                "formal",
                "dress code",
                "uniforme"
            ]
        },
        {
            "name": "curso/faculdade",
            "card_look_title": "Look para curso/faculdade",
            "type": "rotina",
            "tags": [
                "curso",
                "faculdade",
                "escola",
                "universidade",
                "universitário",
                "universitária",
                "estudante",
                "colegial",
                "cursinho",
                "uniforme",
                "farda"
            ]
        },
        {
            "name": "festa/evento",
            "card_look_title": "Look para festa/evento",
            "type": "eventual",
            "tags": [
                "show",
                "música",
                "comemoração",
                "festa",
                "balada",
                "evento",
                "aniversário",
                "festival",
                "atração",
                "diversão"
            ]
        },
        {
            "name": "restaurante", # restaurante/bar
            "card_look_title": "Look para restaurante/bar",
            "type": "eventual",
            "tags": [
                "restaurante",
                "bar",
                "barzinho",
                "buteco",
                "gastronomia"
            ]
        },
        {
            "name": "shopping", # shopping/compras
            "card_look_title": "Look para shopping/compras",
            "type": "eventual",
            "tags": [
                "shopping",
                "compras"
            ]
        },
        {
            "name": "viagem",
            "card_look_title": "Look para viagem",
            "type": "eventual",
            "tags": [
                "viagem",
                "férias"
            ]
        },
        {
            "name": "praia", # praia/piscina
            "card_look_title": "Look para praia/piscina",
            "type": "eventual",
            "tags": [
                "praia",
                "piscina",
                "verão",
                "sol",
                "roupa de banho"
            ]
        },
        {
            "name": "atividade física",
            "card_look_title": "Look para atividade física",
            "type": "rotina",
            "tags": [
                "exercício",
                "academia",
                "musculação",
                "esporte",
                "futebol",
                "corrida",
                "caminhada",
                "bicicleta",
                "esportivo",
                "malhar",
                "treino"
            ]
        },
        {
            "name": "natureza",
            "card_look_title": "Look para natureza",
            "type": "eventual",
            "tags": [
                "sítio",
                "chácara",
                "natureza",
                "parque",
                "trilha",
                "jardim",
                "praça",
                "acampamento"
            ]
        },
        {
            "name": "entretenimento urbano",
            "card_look_title": "Look para entretenimento urbano",
            "type": "eventual",
            "tags": [
                "cinema",
                "teatro",
                "estádio de futebol",
                "museu",
                "cultura",
                "arte"
            ]
        },
        {
            "name": "encontro/date",
            "card_look_title": "Look para encontro/date",
            "type": "eventual",
            "tags": [
                "encontro",
                "date"
            ]
        },
        {
            "name": "prática religiosa",
            "card_look_title": "Look para prática religiosa",
            "type": "rotina",
            "tags": [
                "templo religioso",
                "religiso",
                "religisa",
            ]
        }
	]
    save_many_occasions(occasions)
    count = get_occasions_count()
    if count != len(occasions):
        raise FailToInitOccasions()

def get_day():
    occasion = db[OCCASION_COLLECTION].find_one(
        { TAGS_KEY: { IN_KEY: [ "day" ] } }
    )
    if occasion:
        occasion[ID_KEY] = str(occasion[ID_KEY])
    return occasion

def get_night():
    occasion = db[OCCASION_COLLECTION].find_one(
        { TAGS_KEY: { IN_KEY: [ "night" ] } }
    )
    if occasion:
        occasion[ID_KEY] = str(occasion[ID_KEY])
    return occasion

def get_periods():
    occasions = db[OCCASION_COLLECTION].find(
        { TYPE_KEY: "period" }
    )
    occasions = list(occasions)
    if len(occasions) > 0:
        for occasion in occasions:
            occasion[ID_KEY] = str(occasion[ID_KEY])
    return occasions