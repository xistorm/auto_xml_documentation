from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import VariableEntity

from . import XmlDocumentation


class VariableXmlDocumentation(XmlDocumentation):
    def __init__(self, entity: VariableEntity, summary: str):
        modifiers = [str(modifier) for modifier in entity.modifiers]
        additional_line = f'{" ".join(modifiers)} variable of {entity.value_type} type'

        extended_summary = XmlDocumentation._enrich_summary(summary, additional_line)

        super().__init__(entity, extended_summary)
