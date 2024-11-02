from rest_framework.exceptions import APIException


class CustomTokenError(APIException):
    status_code = 401
    default_detail = "Token etibarsızdır."
    default_code = "token_etibarsız"

    # default_detail = "Token is not valid."
    # default_code = "token_not_valid"

    def __init__(self, detail=None, code=None, *args, **kwargs):
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.code = code
        super().__init__(detail, code, *args, **kwargs)
