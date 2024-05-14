from ..types import EntityType
from . import XmlDocumentation


class ClassXmlDocumentation(XmlDocumentation):
    def __init__(self, summary: str, path: str):
        super().__init__(summary, path, EntityType.CLASS)
