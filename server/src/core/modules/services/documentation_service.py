from src.models.entities import Entity, VariableEntity, FunctionEntity, ClassEntity
from src.models.xml_documentations import XmlDocumentation, VariableXmlDocumentation, FunctionXmlDocumentation, ClassXmlDocumentation


class DocumentationService:
    @staticmethod
    def build_documented_entity(entity: Entity) -> Entity:
        return entity

    @staticmethod
    def build_xml_documentation(entity: Entity) -> XmlDocumentation:
        pass

    @staticmethod
    def _build_variable_xml_documentation(entity: VariableEntity) -> VariableXmlDocumentation:
        pass

    @staticmethod
    def _build_function_xml_documentation(entity: FunctionEntity) -> FunctionXmlDocumentation:
        pass

    @staticmethod
    def _build_class_xml_documentation(entity: ClassEntity) -> ClassXmlDocumentation:
        pass
