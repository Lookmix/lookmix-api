import json
from os.path import join, dirname, realpath, split
from jsonschema import validate, RefResolver
from app.repositories import user_repository


def load_json_schema(filename):
	relative_path = join('../models', filename)
	absolute_path = join(dirname(__file__), relative_path)
	with open(absolute_path) as schema_file:
		schema = json.loads(schema_file.read())
		return schema


def assert_valid_schema(data, schema_file):
	schema = load_json_schema(schema_file)
	dir = split(dirname(realpath(__file__)))[0] + '/models'
	resolver = RefResolver(referrer=schema, base_uri='file://' + dir + '/')
	return validate(data, schema, resolver=resolver)


