import re
from typing import List

from src.models.xml_documentations.xml_documentation import XmlDocumentation
from .stubs.xml_documentation_stubs import variable_xml_documentation, function_xml_documentation, class_xml_documentation



def test_is_xml_documentation():
    assert XmlDocumentation.is_documentation_text('/// <summary>summary</summary>') == True
    assert XmlDocumentation.is_documentation_text('<tag>content</tag') == False
    assert XmlDocumentation.is_documentation_text('/// some comment') == False


def test_build_documentation_text():
    def assert_has_tags(documentation: XmlDocumentation, tags: List[str]) -> None:
        pattern = '.*'.join([f'/// <{tag}.*>.*</{tag}>' for tag in tags])
        assert re.match(pattern, documentation.build_documentation_text(), re.DOTALL) is not None

    assert_has_tags(variable_xml_documentation, ['permission', 'summary'])
    assert_has_tags(class_xml_documentation, ['permission', 'summary'])
    assert_has_tags(function_xml_documentation, ['permission', 'summary', 'param', 'returns'])
