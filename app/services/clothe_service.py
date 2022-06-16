from app.utils import validation
from app.repositories import clothe_repository


def create(data, closet_id):
    try:
        del data["id"]
        data["closet_id"] = closet_id
        validation.assert_valid_schema(data, "clothe.json")
        clothe_id = clothe_repository.save(data)
        return clothe_id
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


def get_clothes_by_closet_id(id):
    try:
        clothes = clothe_repository.get_clothes_by_closet_id(id)
        return clothes
    except Exception as e:
        raise e


def get_social_clothes_by_closet_id(id):
    try:
        clothes = clothe_repository.get_social_clothes_by_closet_id(id)
        return clothes
    except Exception as e:
        raise e


def get_casual_clothes_by_closet_id(id):
    try:
        clothes = clothe_repository.get_casual_clothes_by_closet_id(id)
        return clothes
    except Exception as e:
        raise e