class BadCredentialsException(Exception):
    pass


class DuplicatedUsernameException(Exception):
    pass


class DuplicatedPhoneException(Exception):
    pass


class PhoneNotFoundException(Exception):
    pass


class FailToGenerateOTPException(Exception):
    pass


class AttemptsExceedException(Exception):
    pass


class RequiredParamException(Exception):
    pass


class FailToInitCategories(Exception):
    pass


class FailToInitOccasions(Exception):
    pass


class FailToInitSeasons(Exception):
    pass


class DuplicatedCategoryException(Exception):
    pass


class DuplicatedOccasionException(Exception):
    pass