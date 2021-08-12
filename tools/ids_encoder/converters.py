from . import decode_id, encode_id
from .utils import REGEX


class HashidsConverter():
    regex = REGEX

    def to_python(self, value: str) -> int:
        return decode_id(value)

    def to_url(self, value: int) -> str:
        return encode_id(value)
