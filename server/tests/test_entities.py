from src.models.entities import Entity
from src.models.xml_documentations import XmlDocumentation
from .stubs import lorem_ipsum, variable_entity, function_entity, class_entity, variable_xml_documentation, function_xml_documentation, class_xml_documentation


def test_entity_link():
    link = variable_entity.link_entity()
    assert link is not None

    words = lorem_ipsum.split(' ')
    words.insert(3, link)
    text_with_link = ' '.join(words)
    link_from_text = Entity.extract_entity_link(text_with_link)
    assert link_from_text == variable_entity.id


def test_entity_documentation():
    def assert_entity_documentation(entity: Entity, documentation: XmlDocumentation) -> None:
        entity.add_xml_documentation(documentation)
        documentation_text = documentation.build_documentation_text()
        documented_text = entity.build_text()

        assert entity.name in documented_text
        assert documentation_text in documented_text

    assert_entity_documentation(variable_entity, variable_xml_documentation)
    assert_entity_documentation(function_entity, function_xml_documentation)
    assert_entity_documentation(class_entity, class_xml_documentation)
