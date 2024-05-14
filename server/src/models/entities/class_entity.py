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

        self.access_modifier = tokens['access_modifier']
        self.modifiers = tokens['modifiers']
        self.name = tokens['name']
        self.fields = tokens['fields']
        self.methods = tokens['methods']

        super().__init__(self.name, text, EntityType.CLASS)

    def __repr__(self):
        return f'''{{
            'access_modifier': {self.access_modifier},
            'modifiers': {self.modifiers},
            'name': {self.name},
            'fields': {self.fields},
            'methods': {self.methods},
        }}'''

    def _extract_tokens(self, text: str) -> dict:
        match = re.search(self._pattern, text, re.VERBOSE | re.DOTALL)

        tokens = match.groupdict()
        tokens['modifiers'] = [modifier for modifier in tokens['modifiers'].split(' ') if modifier]
        tokens['inheritance'] = re.sub(r'\s|\n', '', tokens['inheritance']).split(',') if tokens['inheritance'] else None
        tokens['fields'] = []
        tokens['methods'] = []

        body_lines = [line for line in tokens['body'].split('\n') if line]
        lines_amount = len(body_lines)
        index = -1
        while index + 1 < lines_amount:
            index += 1
            line = body_lines[index]

            if FunctionEntity.is_function_text(line):
                function_text, steps = read_code_block(body_lines, index)
                function_entity = FunctionEntity(function_text, tokens['name'])
                tokens['methods'].append(function_entity)

                index += steps
                continue

            if VariableEntity.is_variable_text(line):
                field_entity = VariableEntity(line, tokens['name'])
                tokens['fields'].append(field_entity)

                continue

        del tokens['body']

        return tokens

    @staticmethod
    def is_class_text(text: str) -> bool:
        return re.search(ClassEntity._pattern, text, re.VERBOSE | re.DOTALL) is not None
