import json
from os.path import join, dirname, realpath, split
from jsonschema import (
	validate, 
	RefResolver, 
	ValidationError
)

def load_json_schema(filename):
	relative_path = join('./', filename)
	absolute_path = join(dirname(__file__), relative_path)
	with open(absolute_path) as schema_file:
		schema = json.loads(schema_file.read())
		return schema

def assert_valid_schema(data, schema_file):
	schema = load_json_schema(schema_file)
	dir = split(dirname(realpath(__file__)))[0] + '/tests'
	resolver = RefResolver(referrer=schema, base_uri='file://' + dir + '/')
	return validate(data, schema, resolver=resolver)

def validate_verify_token_schema():
	data = {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzbXNJZCI6IjQ5NDhkYWEyLThjYmQtNGEwMi1iNDk2LWQwZmNkNDFiNGY3MiIsImV4cCI6MTYzNzgwMzQ3MX0.vSShtyKIR_h3s68j91AMYwsNuAsoeOWtH8GOThtZVQw",
    "code": "195115",
    "id": "4948daa2-8cbd-4a02-b496-d0fcd41b4f72",
    "user": {
			"phone": "11951672083",
			"password": "vinicius",
			"timestamp": "06/03/2022 15:11"
    }
	}
	schema = "verify_token_test.json"
	assert_valid_schema(data, schema)

def validate_daily_look_setup_schema():
	data = {
		"_id": "abc123",
		"user_id": "f7gfd98gfd",
		"days_of_week": [
			{
				"day_of_week": "domingo",
				"occasions": [
					{
						"casual": [ "dia" ],
						"social": [],
						"occasion_id": "6315604bdaf4e3d09503521c"
					},
					{
						"casual": [ "dia" ],
						"social": [ "noite" ],
						"occasion_id": "6315604bdaf4e3d095035220"
					}
				],
				"sort": 0
			},
			{
				"day_of_week": "quinta",
				"occasions": [
					{
						"casual": [ "dia" ],
						"social": [],
						"occasion_id": "6315604bdaf4e3d09503521c"
					}
				],
				"sort": 1
			}
		]
	}
	# days_of_week_occasions = [ day["occasions"] for day in data["days_of_week"] ]
	# print(days_of_week_occasions)
	schema = "daily_look_setup_test.json"
	assert_valid_schema(data, schema)

try:
	validate_verify_token_schema()
	validate_daily_look_setup_schema()
except ValidationError as e:
	validator = e.validator
	customErrorMessage = e.schema.get("errorMessage", {}).get(validator)
	message = e.message
	if customErrorMessage is not None:
		message = customErrorMessage
	print(message)