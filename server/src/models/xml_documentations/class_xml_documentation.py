from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import ClassEntity

from . import XmlDocumentation


class ClassXmlDocumentation(XmlDocumentation):
    def __init__(self, entity: ClassEntity, summary: str):
        modifiers = [str(modifier) for modifier in entity.modifiers]
        fields = [field.name for field in entity.fields]
        methods = [method.name for method in entity.methods]
        additional_line = f'{" ".join(modifiers)} class which contains {", ".join(fields)} fields and {", ".join(methods)} methods'

        extended_summary = XmlDocumentation._enrich_summary(summary, additional_line)

        super().__init__(entity, extended_summary)
