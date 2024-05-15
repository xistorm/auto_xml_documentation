from ..types import EntityType
from . import XmlDocumentation


class ClassXmlDocumentation(XmlDocumentation):
    def __init__(self, entity_id: str, summary: str):
        super().__init__(entity_id, EntityType.CLASS, summary)
