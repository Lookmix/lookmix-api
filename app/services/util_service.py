from app.repositories import enum_repository


def get_seasons():
    try:
        seasons = enum_repository.get_seasons()
        return seasons
    except Exception as e:
        raise e

def get_by_index(array, index):
    try:
        return array[index]
    except IndexError as e:
        return False