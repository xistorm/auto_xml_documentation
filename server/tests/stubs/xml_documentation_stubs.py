from src.models.xml_documentations import VariableXmlDocumentation, FunctionXmlDocumentation, ClassXmlDocumentation
from .entity_stubs import variable_entity, function_entity, class_entity


summary = 'some summary'
arguments = {'arg1': 'arg1 summary', 'arg2': 'arg2 summary'}
returns = 'function returns value'

variable_xml_documentation = VariableXmlDocumentation(variable_entity, summary)
function_xml_documentation = FunctionXmlDocumentation(function_entity, summary, returns, arguments)
class_xml_documentation = ClassXmlDocumentation(class_entity, summary)
