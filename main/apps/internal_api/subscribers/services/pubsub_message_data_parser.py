import base64
from typing import Type, TypeVar

import msgspec


T = TypeVar("T", bound=msgspec.Struct)


class PubSubMessageDataParser:
    def parse_data(self, data: str, message_type: Type[T]) -> T:
        raw_bytes_data = base64.b64decode(data)
        return msgspec.json.decode(raw_bytes_data, type=message_type)
