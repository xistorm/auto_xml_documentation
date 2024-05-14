import re

from typing import List, Tuple

from src.utils.code import read_code_block
from src.models.entities import Entity, ClassEntity, FunctionEntity, VariableEntity

from .documentation_service import DocumentationService


class StaticAnalyzerService:
    @staticmethod
    def add_xml_documentation(code: str) -> str:
        processed_code, entities = StaticAnalyzerService.__destruct_code(code)
        documented_entities = [DocumentationService.build_documented_entity(entity) for entity in entities]
        documented_code = StaticAnalyzerService.__struct_code(processed_code, documented_entities)

        return documented_code

    @staticmethod
    def __struct_code(code: str, entities: List[Entity]) -> str:
        lines = code.split("\n")

        processed_lines = []
        for line in lines:
            entity_path = StaticAnalyzerService.__extract_entity_link(line)
            if entity_path is not None:
                entity = next(entity for entity in entities if entity.path == entity_path)
                processed_lines.append(entity.text)
                continue

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

                entity_link = StaticAnalyzerService.__link_entity(class_entity)
                processed_lines.append(entity_link)

                index += steps
                continue

            if FunctionEntity.is_function_text(line):
                function_text, steps = read_code_block(lines, index)
                function_entity = FunctionEntity(function_text)
                entities.append(function_entity)

                entity_link = StaticAnalyzerService.__link_entity(function_entity)
                processed_lines.append(entity_link)

                index += steps
                continue

            if VariableEntity.is_variable_text(line):
                variable_entity = VariableEntity(line)
                entities.append(variable_entity)

                entity_link = StaticAnalyzerService.__link_entity(variable_entity)
                processed_lines.append(entity_link)

                continue

            processed_lines.append(line)

        processed_code = '\n'.join(processed_lines)
        return processed_code, entities

    @staticmethod
    def __extract_entity_link(text: str) -> str | None:
        entity_link = re.search(r'<entity>([\w.]+)</entity>', text)
        return entity_link.group(1) if entity_link is not None else None

    @staticmethod
    def __link_entity(entity: Entity) -> str:
        return f'<entity>{entity.path}</entity>'
