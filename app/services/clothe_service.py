from app.utils import validation 
from app.repositories import clothe_repository


def create(data):
  try:
    validation.assert_valid_schema(data, "clothe.json")
    closet_id = clothe_repository.save(data)
    return closet_id
  except Exception as e:
    raise e


def get_clothe_by_id(id):
	try:
		clothe = clothe_repository.get_by_id(id)

		return clothe
	except Exception as e:
		raise e


def get_clothe_by_user_id(user_id):
	try:
		clothe = clothe_repository.get_by_user_id(user_id)

		return clothe
	except Exception as e:
		raise e