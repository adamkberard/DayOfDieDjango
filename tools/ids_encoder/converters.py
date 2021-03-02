from django.conf import settings
from hashids import Hashids


class HashidsConverter():
    regex = '[0-9a-zA-Z]+'

    def to_python(self, value: str) -> int:
        hashids = Hashids(settings.HASHIDS_SALT, min_length=8)
        decoded_values = hashids.decode(value)
        # output of hashids.decode is always a tuple
        if len(decoded_values) != 1:
            raise ValueError
        return decoded_values[0]

    def to_url(self, value: int) -> str:
        hashids = Hashids(settings.HASHIDS_SALT, min_length=8)
        return hashids.encode(value)
