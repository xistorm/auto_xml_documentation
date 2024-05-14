from ..types import EntityType
from . import XmlDocumentation


class FunctionXmlDocumentation(XmlDocumentation):
    def __init__(self, summary: str, returns: str, arguments: dict, path: str):
        super().__init__(summary, path, EntityType.FUNCTION)

        self.returns = returns
        self.arguments = arguments

    def build_documentation_text(self, pad: int = 0) -> str:
        documentations = [
            XmlDocumentation._build_summary(self.summary, pad),
            XmlDocumentation._build_arguments(self.arguments, pad),
            XmlDocumentation._build_return_type(self.returns, pad),
        ]
        filtered_documentations = [documentation for documentation in documentations if documentation]

        return "\n".join(filtered_documentations)
