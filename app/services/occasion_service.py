from app.repositories import occasion_repository
from app.exceptions.error import DuplicatedOccasionException


def save_occasion(data):
    try:
        id = data._id
        if not is_occasion_unique(id):
            raise DuplicatedOccasionException()
        occasion_repository.save(data)
    except Exception as e:
        raise e

def get_occasions():
    try:
        occasions = occasion_repository.get_occasions()
        return occasions
    except Exception as e:
        raise e

def get_by_id(id):
    try:
        occasion = occasion_repository.get_by_id(id)
        return occasion
    except Exception as e:
        raise e

def delete_occasion(ids):
    try:
        result = occasion_repository.delete_by_ids(ids)
        return result.deleted_count
    except Exception as e:
        raise e

def update_occasion(occasions):
    try:
        modified_count = 0
        for occasion in occasions:
            id = occasion["_id"]
            result = occasion_repository.update_by_id(id, occasion)
            modified_count += result.modified_count
        return modified_count
    except Exception as e:
        raise e

def is_occasion_unique(id):
    occasion = occasion_repository.get_by_id(id)
    result = True
    if occasion:
        result = False
    return result
