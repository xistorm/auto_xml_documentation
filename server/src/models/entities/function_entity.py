import re

from ..types import EntityType, AccessModifiers, Modifiers
from . import Entity, VariableEntity


class FunctionEntity(Entity):
    _pattern = fr"""
        \s*
        (?P<access_modifier>{AccessModifiers.union('|')})?\s*
        (?P<modifiers>({Modifiers.union()})*)
        (?P<return_value_type>[\w<>\[\]]+)?\s+
        (?P<name>\w+)\s*
        (\((?P<arguments>[^)]*)\))
        (\n|\s)*
        (((?P<body>({{.*}})|(\s*=>\s*.*;))?))?
    """

    def __init__(self, text: str):
        tokens = self._extract_tokens(text)

        self.return_value_type = tokens['return_value_type']
        self.arguments = tokens['arguments']
        self.body = tokens['body']

        super().__init__(EntityType.FUNCTION, tokens['name'], text, tokens['access_modifier'], tokens['modifiers'])

    def __repr__(self):
        return f'''{{
            'access_modifier': {self.access_modifier},
            'modifiers': {self.modifiers},
            'return_value_type': {self.return_value_type},
            'name': {self.name},
            'arguments': {self.arguments},
            'body': {self.body},
        }}'''

    @staticmethod
    def _extract_tokens(text: str) -> dict:
        match = re.search(FunctionEntity._pattern, text, re.VERBOSE | re.DOTALL)

        tokens = match.groupdict()
        tokens['modifiers'] = [modifier for modifier in tokens['modifiers'].split(' ') if modifier]
        tokens['arguments'] = [VariableEntity(argument) for argument in tokens['arguments'].split(', ') if argument]

        return tokens

    @staticmethod
    def is_function_text(text: str) -> bool:
        return re.search(FunctionEntity._pattern, text, re.VERBOSE | re.DOTALL) is not None
