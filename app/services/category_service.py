from app.utils import validation
from app.repositories import category_repository
from app.exceptions.error import DuplicatedCategoryException


def create(data):
	try:
		validation.assert_valid_schema(data, "category.json")

		name = data.get("name")

		if not is_category_unique(name):
			raise DuplicatedCategoryException()

		category_id = category_repository.save(data)

		return category_id
	except Exception as e:
		raise e


def get_category_by_id(id):
    try:
        category = category_repository.get_by_id(id)

        return category
    except Exception as e:
        raise e


def get_categories():
    try:
        categories = category_repository.get_all()
        for c in categories:
            c["_id"] = str(c["_id"])
        return categories
    except Exception as e:
        raise e


def is_category_unique(name):
    category = category_repository.get_by_name(name)

    result = True

    if category:
        result = False
    return result