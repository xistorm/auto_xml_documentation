from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import FunctionEntity

from . import XmlDocumentation


class FunctionXmlDocumentation(XmlDocumentation):
    def __init__(self, entity: FunctionEntity, summary: str, returns: str | None = None, arguments: dict | None = None):
        modifiers = [str(modifier) for modifier in entity.modifiers]
        arguments_names = [argument.name for argument in entity.arguments] if len(entity.arguments) > 0 else []
        additional_line = f'{" ".join(modifiers)} function which processing {", ".join(arguments_names)} to get {entity.return_value_type} value'

        extended_summary = XmlDocumentation._enrich_summary(summary, additional_line)

        super().__init__(entity, extended_summary)

        self.returns = returns
        self.arguments = arguments

    def build_documentation_text(self, pad: int = 0) -> str:
        documentations = [
            XmlDocumentation._build_permission(self.permission, pad),
            XmlDocumentation._build_modifiers(self.modifiers, pad),
            XmlDocumentation._build_summary(self.summary, pad),
            XmlDocumentation._build_arguments(self.arguments, pad) if self.arguments is not None else None,
            XmlDocumentation._build_return_type(self.returns, pad) if self.returns is not None else None,
        ]
        filtered_documentations = [documentation for documentation in documentations if documentation is not None]

        return "\n".join(filtered_documentations)
