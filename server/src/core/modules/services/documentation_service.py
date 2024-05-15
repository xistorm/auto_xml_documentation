from src.models.entities import Entity, VariableEntity, FunctionEntity, ClassEntity
from src.models.xml_documentations import XmlDocumentation, VariableXmlDocumentation, FunctionXmlDocumentation, ClassXmlDocumentation

from .ai_model_service import AIModelService


class DocumentationService:
    @staticmethod
    def build_documented_entity(entity: Entity) -> Entity:
        documentation = DocumentationService._build_xml_documentation(entity)
        entity.add_xml_documentation(documentation)

        return entity

    @staticmethod
    def _build_xml_documentation(entity: Entity) -> XmlDocumentation:
        if isinstance(entity, VariableEntity):
            return DocumentationService._build_variable_xml_documentation(entity)
        if isinstance(entity, FunctionEntity):
            return DocumentationService._build_function_xml_documentation(entity)
        if isinstance(entity, ClassEntity):
            return DocumentationService._build_class_xml_documentation(entity)

    @staticmethod
    def _build_variable_xml_documentation(entity: VariableEntity) -> VariableXmlDocumentation:
        summary = AIModelService.summarize_code_block(entity.text)
        documentation = VariableXmlDocumentation(entity.id, summary)

        return documentation

    @staticmethod
    def _build_function_xml_documentation(entity: FunctionEntity) -> FunctionXmlDocumentation:
        summary = AIModelService.summarize_code_block(entity.body)
        returns = AIModelService.summarize_code_block(entity.text)
        arguments = dict()
        for argument in entity.arguments:
            arguments[argument.name] = AIModelService.summarize_code_block(argument.text)

        documentation = FunctionXmlDocumentation(entity.id, summary, returns, arguments)

        return documentation

    @staticmethod
    def _build_class_xml_documentation(entity: ClassEntity) -> ClassXmlDocumentation:
        summary = AIModelService.summarize_code_block(entity.text)
        documentation = ClassXmlDocumentation(entity.id, summary)

        for field in entity.entities():
            DocumentationService.build_documented_entity(field)

        return documentation
