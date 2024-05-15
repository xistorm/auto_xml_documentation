from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import ClassEntity

from . import XmlDocumentation


class ClassXmlDocumentation(XmlDocumentation):
    def __init__(self, entity: ClassEntity, summary: str):
        modifiers = " ".join([str(modifier) for modifier in entity.modifiers])
        fields = ", ".join([field.name for field in entity.fields])
        methods = ", ".join([method.name for method in entity.methods])
        inheritance = ", ".join(entity.inheritance)
        additional_line = f'{modifiers} class {f"which inherits {inheritance} and" if inheritance else ""} contains {f"[{fields}] fields" if fields else ""}{" and " if methods and fields else ""}{f"[{methods}] methods" if methods else ""}'

        extended_summary = XmlDocumentation._enrich_summary(summary, additional_line)

        super().__init__(entity, extended_summary)
