from app.utils import validation 
from app.repositories import look_repository
from app.exceptions.error import DuplicatedDayOfWeekException
from app.exceptions.error import DuplicatedPeriodException
from app.exceptions.error import PeriodEmptyException
from app.exceptions.error import PeriodTooLongException
from app.exceptions.error import DuplicatedOccasionException

def update_daily_look_setup(user_id, data):
	__validate_before_save(data)
	result = look_repository.update_daily_look_setup(user_id, data)
	return result

def get_daily_look_setup_by_user_id(id):
	result = look_repository.get_daily_look_setup_by_user_id(id)
	return result

def __validate_before_save(data):
	validation.assert_valid_schema(data, "daily_look_setup.json")
	days_of_week = data["days_of_week"]
	__is_day_of_week_duplicated(days_of_week)
	__is_occasion_duplicated(days_of_week)
	# occasions_of_the_days = [ day["occasions"] for day in days_of_week ]
	for day_of_week in days_of_week: # iterate days
		occasions_of_the_day = day_of_week["occasions"]
		for occasion in occasions_of_the_day: # iterate occasions
			casual_list = occasion["casual"]
			__is_period_duplicated(casual_list)
			social_list = occasion["social"]
			__is_period_duplicated(social_list)
			casual_list_length = len(casual_list)
			social_list_length = len(social_list)
			lists_length_sum = casual_list_length + social_list_length
			__check_occasion_arrays_length(lists_length_sum)

def __is_day_of_week_duplicated(days_of_week):
	days = [ day["day_of_week"] for day in days_of_week ]
	set_of_days = set()
	for day in days:
		if day in set_of_days:
			raise DuplicatedDayOfWeekException()
		set_of_days.add(day)

def __is_period_duplicated(period_list):
	set_of_period = set()
	for period in period_list:
		if period in set_of_period:
			raise DuplicatedPeriodException()
		set_of_period.add(period)

def __check_occasion_arrays_length(lists_length_sum):
	if lists_length_sum < 1:
		raise PeriodEmptyException()
	if lists_length_sum > 2:
		raise PeriodTooLongException()

def __is_occasion_duplicated(days_of_week):
	occasions_list = [ day["occasions"] for day in days_of_week ]
	for item in occasions_list:
		set_of_ids = set()
		occasion_ids = [ occasion["occasion_id"] for occasion in item ]
		for id in occasion_ids:
			if id in set_of_ids:
				raise DuplicatedOccasionException()
			set_of_ids.add(id)