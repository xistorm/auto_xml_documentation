from ..types import EntityType
from ..xml_documentations import XmlDocumentation


class Entity:
    def __init__(self, path: str, text: str, entity_type: EntityType):
        self.type = entity_type
        self.text = text
        self.path = path

    def add_xml_documentation(self, xml_documentation: XmlDocumentation) -> None:
        xml_documentation_text = xml_documentation.build_documentation_text()

        self.text = f'''
            {xml_documentation_text}
            {self.text}
        '''

    @staticmethod
    def _build_path(parent_path: str, name: str) -> str:
        path_chunks = [parent_path, name]
        filtered_path_chunks = [chunk for chunk in path_chunks if chunk]
        return '.'.join(filtered_path_chunks)
