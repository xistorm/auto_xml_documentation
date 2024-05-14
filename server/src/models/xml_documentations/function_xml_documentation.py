from ..types import EntityType
from . import XmlDocumentation


class FunctionXmlDocumentation(XmlDocumentation):
    def __init__(self, summary: str, path: str, returns: str, arguments: dict):
        super().__init__(summary, path, EntityType.FUNCTION)

        self.returns = returns
        self.arguments = arguments

    def build_documentation_text(self) -> str:
        summary = XmlDocumentation._build_summary(self.summary)
        arguments = XmlDocumentation._build_arguments(self.arguments)
        return_type = XmlDocumentation._build_return_type(self.returns)

        return "\n".join([summary, arguments, return_type])
