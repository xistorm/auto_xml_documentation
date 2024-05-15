import re
import uuid

from typing import List

from ..types import EntityType, AccessModifiers
from ..xml_documentations import XmlDocumentation


class Entity:
    def __init__(self, entity_type: EntityType, name: str, text: str, access_modifier: str | None, modifiers: List[str] | None):
        self.type = entity_type
        self.access_modifier = access_modifier if access_modifier is not None else AccessModifiers.PRIVATE.value
        self.modifiers = modifiers if modifiers is not None else []
        self.name = name
        self.text = text
        self.id = str(uuid.uuid4())

    def add_xml_documentation(self, xml_documentation: XmlDocumentation) -> None:
        first_line = self.text.split('\n')[0]
        text_pad = len(first_line) - len(first_line.lstrip())
        xml_documentation_text = xml_documentation.build_documentation_text(text_pad)

        documented_text = '\n'.join(['', xml_documentation_text, self.text])
        self.text = documented_text

    def build_text(self):
        return self.text

    @staticmethod
    def extract_entity_link(text: str) -> str | None:
        entity_link = re.search(r'<entity>([\w-]+)</entity>', text)
        return entity_link.group(1) if entity_link is not None else None

    def link_entity(self) -> str:
        return f'<entity>{self.id}</entity>'
