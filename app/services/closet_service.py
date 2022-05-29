from app.utils import validation 
from app.repositories import closet_repository


def create(closet_id, user_id):
	closet = {
		"_id": closet_id,
		"user_id": user_id,
		"clothe_ids": []
	}
	validation.assert_valid_schema(closet, "closet.json")
	closet_id = closet_repository.save(closet)
	return closet_id


def add_clothe_to_closet(closet_id, clothe_id):
	try:
		# if not closet:
		# 	closet_id = create(user_id)
		# 	flickr.create_photoset(closet_id)
		# 	closet = closet_repository.get_by_id(closet_id)
        # return flickr.(user_id)
		closet_repository.add_clothe_id(closet_id, clothe_id)
	except Exception as e:
		raise e


def get_closet_by_id(id):
	try:
		closet = closet_repository.get_by_id(id)

		return closet
	except Exception as e:
		raise e


def get_closet_by_user_id(user_id):
	try:
		closet = closet_repository.get_by_user_id(user_id)

		return closet
	except Exception as e:
		raise e