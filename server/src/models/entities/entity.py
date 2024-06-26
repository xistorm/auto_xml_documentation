import re
import uuid

from typing import List
from threading import Lock

from ..types import EntityType, AccessModifiers
from ..xml_documentations import XmlDocumentation


class Entity:
    def __init__(self, entity_type: EntityType, name: str, text: str, access_modifier: str | None, modifiers: List[str] | None):
        self._lock = Lock()

        self.id = str(uuid.uuid4())
        self.documentation = ''

        self.type = entity_type
        self.access_modifier = access_modifier if access_modifier is not None else AccessModifiers.PRIVATE.value
        self.modifiers = modifiers if modifiers is not None else []
        self.name = name
        self.text = text

    def add_xml_documentation(self, xml_documentation: XmlDocumentation) -> str:
        first_line = self.text.split('\n')[0]
        text_pad = len(first_line) - len(first_line.lstrip())

        xml_documentation_text = xml_documentation.build_documentation_text(text_pad)
        self.add_xml_documentation_text(xml_documentation_text)

        return xml_documentation_text

    def add_xml_documentation_text(self, xml_documentation_text: str) -> None:
        with self._lock:
            self.documentation = xml_documentation_text

    def get_documented_text(self) -> str:
        documented_text = '\n'.join(['', self.documentation, self.text])
        return documented_text

    def build_text(self) -> str:
        return self.get_documented_text()

    @staticmethod
    def extract_entity_link(text: str) -> str | None:
        entity_link = re.search(r'<entity>([\w-]+)</entity>', text)
        return entity_link.group(1) if entity_link is not None else None

    def link_entity(self) -> str:
        return f'<entity>{self.id}</entity>'
