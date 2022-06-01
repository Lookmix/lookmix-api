from app import db
from bson.objectid import ObjectId
from exceptions.error import FailToInitCategories


CATEGORY_DOC = "category"
ID_KEY = "_id"
SET_KEY = "$set"
PUSH_KEY ="$push"

def save(category):
    id = db[CATEGORY_DOC].insert_one(category)
    return id


def save_many(categories):
    ids = db[CATEGORY_DOC].insert_many(categories).inserted_ids
    return ids


def get_by_id(id):
    category = db[CATEGORY_DOC].find_one(
		{ ID_KEY: ObjectId(id) }
	)
    if category:
        category[ID_KEY] = str(category[ID_KEY])
    return category


def get_all():
    categories = db[CATEGORY_DOC].find(
        { },
        { CATEGORY_DOC: 1 }
    )
    return categories


def get_categories_count():
	count = db[CATEGORY_DOC].count_documents()
	return count


def update(id, data):
    db[CATEGORY_DOC].update_one(
        { ID_KEY: id },
        { SET_KEY: data }, upsert=False
    )


def delete(id):
    pass


def __init_categories():
    print("Init categories")
    categories = [
		{
			"name": "Roupas de cima",
			"description": "Camisas, camisetas, polos, blusas ou regatas",
		},
		{
			"name": "Pernas",
			"description": "Calças, shorts, saias ou bermudas"
		},
		{
			"name": "Pés",
			"description": "Calçados ou meias"
		},
		{
			"name": "Peças sobrepostas",
			"description": "Casacos, jaquetas, moletons ou sobretudos",
		},
		{
			"name": "Peças únicas",
			"description": "Vestidos ou macacões"
		},
		{
			"name": "Acessórios de cabeça",
			"description": "Bonés, chapéus, óculos, brincos ou laços"
		},
		{
			"name": "Acessórios de pescoço",
			"description": "Colares, correntes, gravatas ou cachecóis",
		},
		{
			"name": "Acessórios de braços e mãos",
			"description": "Bolsas, pulseiras, relógios, anéis ou luvas"
		},
		{
            "name": "Cintura",
            "description": "Cintos ou laços"
        }
	]
    count = get_categories_count()
    result = []
    if count < 1:
        result = save_many(categories)
    if len(result) == len(categories):
        return result
    raise FailToInitCategories()


__init_categories()
