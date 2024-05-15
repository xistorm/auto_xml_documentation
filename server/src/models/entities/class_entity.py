import re

from src.utils.code import read_code_block
from src.models.types import EntityType, AccessModifiers, Modifiers

from . import Entity, VariableEntity, FunctionEntity


class ClassEntity(Entity):
    _pattern = fr"""
        (?P<access_modifier>{AccessModifiers.union('|')})?\s*
        (?P<modifiers>({Modifiers.union()})*)
        class\s+(?P<name>[\w<>]+)\s*
        (?:\:\s*(?P<inheritance>[^{{]+))?
        ({{(?P<body>.*)}})?
    """

    def __init__(self, text: str):
        tokens = self._extract_tokens(text)

        self.inheritance = tokens['inheritance']
        self.body = tokens['body']
        self.fields = tokens['fields']
        self.methods = tokens['methods']

        super().__init__(EntityType.CLASS, tokens['name'], tokens['text'], tokens['access_modifier'], tokens['modifiers'])

    def __repr__(self):
        return f'''{{
            'access_modifier': {self.access_modifier},
            'modifiers': {self.modifiers},
            'name': {self.name},
            'fields': {self.fields},
            'methods': {self.methods},
        }}'''

    def entities(self):
        return self.fields + self.methods

    def build_text(self):
        lines = self.text.split('\n')
        processed_lines = []
        for line in lines:
            entity_link = Entity.extract_entity_link(line)
            if entity_link is not None:
                entity = next(entity for entity in self.entities() if entity.id == entity_link)
                processed_lines.append(entity.text)

                continue

            processed_lines.append(line)

        processed_text = '\n'.join(processed_lines)

        return processed_text

    def _extract_tokens(self, text: str) -> dict:
        match = re.search(self._pattern, text, re.VERBOSE | re.DOTALL)

        tokens = match.groupdict()
        tokens['modifiers'] = [modifier for modifier in tokens['modifiers'].split(' ') if modifier]
        tokens['inheritance'] = re.sub(r'\s|\n', '', tokens['inheritance']).split(',') if tokens['inheritance'] else []
        tokens['fields'] = []
        tokens['methods'] = []

        lines = [line for line in text.split('\n') if line]
        lines_amount = len(lines)
        index = -1
        processed_lines = []
        while index + 1 < lines_amount:
            index += 1
            line = lines[index]

            if FunctionEntity.is_function_text(line):
                function_text, steps = read_code_block(lines, index)
                function_entity = FunctionEntity(function_text)
                function_entity_link = function_entity.link_entity()

                processed_lines.append(function_entity_link)
                tokens['methods'].append(function_entity)

                index += steps
                continue

            if VariableEntity.is_variable_text(line):
                field_entity = VariableEntity(line)
                field_entity_link = field_entity.link_entity()

                processed_lines.append(field_entity_link)
                tokens['fields'].append(field_entity)

                continue

            processed_lines.append(line)

        processed_text = '\n'.join(processed_lines)
        tokens['text'] = processed_text

        return tokens

    @staticmethod
    def is_class_text(text: str) -> bool:
        return re.search(ClassEntity._pattern, text, re.VERBOSE | re.DOTALL) is not None
