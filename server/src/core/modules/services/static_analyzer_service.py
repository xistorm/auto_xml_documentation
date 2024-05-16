from typing import List, Tuple
from concurrent.futures.thread import ThreadPoolExecutor

from src.utils.code import read_code_block
from src.models.entities import Entity, ClassEntity, FunctionEntity, VariableEntity
from src.models.xml_documentations import XmlDocumentation

from .documentation_service import DocumentationService


class StaticAnalyzerService:
    thread_pool = ThreadPoolExecutor()

    @staticmethod
    def add_xml_documentation(code: str) -> str:
        processed_code, entities = StaticAnalyzerService.__destruct_code(code)
        documented_entities = list(StaticAnalyzerService.thread_pool.map(DocumentationService.build_documented_entity, entities))
        documented_code = StaticAnalyzerService.__struct_code(processed_code, documented_entities)

        return documented_code

    @staticmethod
    def __struct_code(code: str, entities: List[Entity]) -> str:
        lines = code.split("\n")

        processed_lines = []
        for line in lines:
            entity_link = Entity.extract_entity_link(line)
            if entity_link is not None:
                entity = next(entity for entity in entities if entity.id == entity_link)
                processed_lines.append(entity.build_text())
                continue

            if not XmlDocumentation.is_documentation_text(line):
                processed_lines.append(line)

        processed_code = '\n'.join(processed_lines)
        return processed_code

    @staticmethod
    def __destruct_code(code: str) -> Tuple[str, List[Entity]]:
        lines = [line for line in code.split('\n') if line]
        lines_amount = len(lines)

        processed_lines = []
        entities = []
        index = -1
        while index + 1 < lines_amount:
            index += 1
            line = lines[index]

            if ClassEntity.is_class_text(line):
                class_text, steps = read_code_block(lines, index)
                class_entity = ClassEntity(class_text)
                entities.append(class_entity)

                entity_link = class_entity.link_entity()
                processed_lines.append(entity_link)

                index += steps
                continue

            if FunctionEntity.is_function_text(line):
                function_text, steps = read_code_block(lines, index)
                function_entity = FunctionEntity(function_text)
                entities.append(function_entity)

                entity_link = function_entity.link_entity()
                processed_lines.append(entity_link)

                index += steps
                continue

            if VariableEntity.is_variable_text(line):
                variable_entity = VariableEntity(line)
                entities.append(variable_entity)

                entity_link = variable_entity.link_entity()
                processed_lines.append(entity_link)

                continue

            processed_lines.append(line)

        processed_code = '\n'.join(processed_lines)
        return processed_code, entities
