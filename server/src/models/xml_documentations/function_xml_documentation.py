from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import FunctionEntity

from . import XmlDocumentation


class FunctionXmlDocumentation(XmlDocumentation):
    def __init__(self, entity: FunctionEntity, summary: str, returns: str | None = None, arguments: dict | None = None):
        super().__init__(entity, summary)

        self.returns = returns
        self.arguments = arguments

    @staticmethod
    def get_meta(entity: FunctionEntity) -> str:
        modifiers = " ".join([str(modifier) for modifier in entity.modifiers])
        arguments_names = ", ".join([argument.name for argument in entity.arguments])
        meta = f'[{modifiers}] function that processes [({arguments_names})] to get value of type [{entity.return_value_type}]'

        return meta

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
