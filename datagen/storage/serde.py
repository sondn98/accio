from typing import Any, Protocol


class Serializable(Protocol):
    def serialize(self, *args, **kwargs) -> bytes: ...

    @classmethod
    def deserialize(cls, *args, **kwargs) -> Any: ...
