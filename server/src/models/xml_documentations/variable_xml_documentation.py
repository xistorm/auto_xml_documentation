from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import VariableEntity

from . import XmlDocumentation


class VariableXmlDocumentation(XmlDocumentation):
    def __init__(self, entity: VariableEntity, summary: str):
        super().__init__(entity, summary)

    @staticmethod
    def get_meta(entity: VariableEntity) -> str:
        modifiers = " ".join([str(modifier) for modifier in entity.modifiers])
        meta = f'[{modifiers}] variable of type [{entity.value_type}]'

        return meta
