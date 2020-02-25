import jsonref
from app.repositories import user_repository
from os.path import join, dirname
from jsonschema import validate


def assert_valid_schema(data, schema_file):
    """ Checks whether the given data matches the schema """

    schema = _load_json_schema(schema_file)
    return validate(data, schema)


def _load_json_schema(filename):
    """ Loads the given schema file """

    relative_path = join('../models', filename)
    absolute_path = join(dirname(__file__), relative_path)

    base_path = dirname(absolute_path)
    base_uri = 'file://{}/'.format(base_path)

    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)


def is_unique_username(username):
    user = user_repository.get_by_username(username)
    
    if user:
        return False
    return True


def is_unique_phone(phone):
    user = user_repository.get_by_phone(phone)

    if user:
        return False
    return True

