from rest_framework.exceptions import APIException
from . import custom_status


class CustomAPIException(APIException):

    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        code_and_detail = custom_status.code_and_detail[status_code]
        code = code if code is not None else code_and_detail[0]
        detail = detail if detail is not None else code_and_detail[1]
        self.code = code
        self.detail = detail
