from app.utils import validation
from app.repositories import clothe_repository
from datetime import datetime


def create(data, closet_id):
    try:
        del data["id"]
        data["closet_id"] = closet_id
        data["created_at"] = str(datetime.now())
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


def update_by_id(clothes):
    try:
        modified_count = 0
        for clothe in clothes:
            id = clothe["_id"]
            result = clothe_repository.update_by_id(id, clothe)
            modified_count += result.modified_count
        return modified_count
    except Exception as e:
        raise e


def delete_clothe_by_ids(ids):
    print("Deleting clothe from atlas - clothe_service")
    try:
        result = clothe_repository.delete_by_ids(ids)
        return result.deleted_count
    except Exception as e:
        raise e
    
def get_all(closet_id):
    try:
        return clothe_repository.get_all(closet_id=closet_id)
    except Exception as e:
        raise e