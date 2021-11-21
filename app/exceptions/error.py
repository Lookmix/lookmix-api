class BadCredentialsException(Exception):
   pass


class DuplicatedUsernameException(Exception):
   pass


class DuplicatedPhoneException(Exception):
   pass


class PhoneNotFoundException(Exception):
   pass


class FailToGenerateVerifyCodeException(Exception):
   pass


class AttemptsExceedException(Exception):
   pass