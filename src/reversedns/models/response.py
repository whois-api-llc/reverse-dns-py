import copy

from .base import BaseModel
import sys

if sys.version_info < (3, 9):
    import typing


def _string_value(values: dict, key: str) -> str:
    if key in values and values[key]:
        return str(values[key])
    return ''


def _int_value(values: dict, key: str) -> int:
    if key in values and values[key]:
        return int(values[key])
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _list_of_objects(values: dict, key: str, classname: str) -> list:
    r = []
    if key in values and type(values[key]) is list:
        r = [globals()[classname](x) for x in values[key]]
    return r


class Record(BaseModel):
    value: str
    name: str
    first_seen: str
    last_visit: str

    def __init__(self, values):
        super().__init__()
        self.value = ''
        self.name = ''
        self.first_seen = ''
        self.last_visit = ''

        if values is not None:
            self.value = _string_value(values, 'value')
            self.name = _string_value(values, 'name')
            self.first_seen = _string_value(values, 'first_seen')
            self.last_visit = _string_value(values, 'last_visit')


class Response(BaseModel):
    size: int

    if sys.version_info < (3, 9):
        result: typing.List[Record]
    else:
        result: [Record]

    def __init__(self, values):
        super().__init__()

        self.result = []
        self.size = 0

        if values is not None:
            self.result = _list_of_objects(values, 'result', 'Record')
            self.size = _int_value(values, 'size')


class ErrorMessage(BaseModel):
    code: int
    message: str

    def __init__(self, values):
        super().__init__()

        self.int = 0
        self.message = ''

        if values is not None:
            self.code = _int_value(values, 'code')
            self.message = _string_value(values, 'messages')
