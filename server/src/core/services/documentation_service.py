from src.utils import split_camel_case

from src.models.entities import Entity, VariableEntity, FunctionEntity, ClassEntity
from src.models.xml_documentations import XmlDocumentation, VariableXmlDocumentation, FunctionXmlDocumentation, ClassXmlDocumentation

from .summarization_service import SummarizationService
from .cache_service import CacheService


class DocumentationService:
    @staticmethod
    def build_documented_entity(entity: Entity) -> Entity:
        if CacheService.has(entity):
            documentation_text = CacheService.get(entity)
            entity.add_xml_documentation_text(documentation_text)
        else:
            documentation = DocumentationService._build_xml_documentation(entity)
            documentation_text = entity.add_xml_documentation(documentation)
            CacheService.add(entity, documentation_text)

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
        summary = SummarizationService.summarize_code(entity.text)
        documentation = VariableXmlDocumentation(entity, summary)

        return documentation

    @staticmethod
    def _build_function_xml_documentation(entity: FunctionEntity) -> FunctionXmlDocumentation:
        summary = SummarizationService.summarize_code(entity.text)
        arguments = dict()
        for argument in entity.arguments:
            parsed_name = split_camel_case(argument.name)
            arguments[argument.name] = SummarizationService.summarize_code(parsed_name)

        documentation = FunctionXmlDocumentation(entity, summary=summary, arguments=arguments)

        return documentation

    @staticmethod
    def _build_class_xml_documentation(entity: ClassEntity) -> ClassXmlDocumentation:
        summary = SummarizationService.summarize_code(entity.text)
        documentation = ClassXmlDocumentation(entity, summary)

        for field in entity.entities():
            DocumentationService.build_documented_entity(field)

        return documentation
