from ..types import EntityType
from . import XmlDocumentation


class VariableXmlDocumentation(XmlDocumentation):
    def __init__(self, summary: str, path: str):
        super().__init__(summary, path, EntityType.VARIABLE)
