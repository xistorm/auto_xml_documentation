from concurrent.futures.thread import ThreadPoolExecutor

from src.utils import split_camel_case

from src.models.entities import Entity, VariableEntity, FunctionEntity, ClassEntity
from src.models.xml_documentations import XmlDocumentation, VariableXmlDocumentation, FunctionXmlDocumentation, ClassXmlDocumentation

from .summarization_service import SummarizationService
from .translation_service import TranslationService
from .cache_service import CacheService


class DocumentationService:
    thread_pool = ThreadPoolExecutor()
    language: str = 'en'

    @staticmethod
    def build_documented_entity(entity: Entity) -> Entity:
        cache_available = CacheService.ping()

        if cache_available and CacheService.has(entity, DocumentationService.language):
            documentation_text = CacheService.get(entity, DocumentationService.language)
            entity.add_xml_documentation_text(documentation_text)
        else:
            documentation = DocumentationService._build_xml_documentation(entity)
            documentation_text = entity.add_xml_documentation(documentation)
            if cache_available:
                CacheService.add(entity, documentation_text, DocumentationService.language)

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
        meta = VariableXmlDocumentation.get_meta(entity)
        summary = DocumentationService._build_summary_documentation(entity.text, meta)
        documentation = VariableXmlDocumentation(entity, summary)

        return documentation

    @staticmethod
    def _build_function_xml_documentation(entity: FunctionEntity) -> FunctionXmlDocumentation:
        meta = FunctionXmlDocumentation.get_meta(entity)
        summary = DocumentationService._build_summary_documentation(entity.text, meta)

        arguments = dict()
        for argument in entity.arguments:
            parsed_name = split_camel_case(argument.name)
            argument_summary = DocumentationService._build_summary_documentation(parsed_name)
            arguments[argument.name] = argument_summary

        documentation = FunctionXmlDocumentation(entity, summary=summary, arguments=arguments)

        return documentation

    @staticmethod
    def _build_class_xml_documentation(entity: ClassEntity) -> ClassXmlDocumentation:
        meta = ClassXmlDocumentation.get_meta(entity)
        summary = DocumentationService._build_summary_documentation(entity.text, meta)
        documentation = ClassXmlDocumentation(entity, summary)

        documented_entities = list(DocumentationService.thread_pool.map(DocumentationService.build_documented_entity, entity.entities()))
        for entity in entity.entities():
            xml_documentation_text = next(documented_entity.documentation for documented_entity in documented_entities if documented_entity.id == entity.id)
            entity.add_xml_documentation_text(xml_documentation_text)

        return documentation

    @staticmethod
    def _build_summary_documentation(code_text: str, meta: str | None = None) -> str:
        base_summary = SummarizationService.summarize_code(code_text)
        extended_summary = XmlDocumentation.enrich_summary(base_summary, meta) if meta else base_summary
        summary = TranslationService.translate(extended_summary, dest=DocumentationService.language)

        return summary

