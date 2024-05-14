from enum import Enum
from typing import List


class ExtendedEnum(Enum):
    @classmethod
    def values(cls) -> List[str]:
        return list(map(lambda x: x.value, cls))

    @classmethod
    def union(cls, sep=r'\s+|') -> str:
        return sep.join(cls.values())
