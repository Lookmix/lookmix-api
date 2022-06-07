from app.utils import validation
from app.repositories import enum_repository
from app.exceptions.error import DuplicatedOccasionException


def save_occasion(data):
	try:
		if not is_occasion_unique(data):
			raise DuplicatedOccasionException()

		enum_repository.add_occasion(data)
	except Exception as e:
		raise e


def get_occasions():
    try:
        occasions = enum_repository.get_occasions()

        return occasions
    except Exception as e:
        raise e


def get_seasons():
    try:
        seasons = enum_repository.get_seasons()

        return seasons
    except Exception as e:
        raise e


def is_occasion_unique(occasion):
    occasions = enum_repository.get_occasions()

    result = True

    if occasion in occasions:
        result = False
    return result
