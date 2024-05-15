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

    def __init__(self, text: str, path: str = None):
        tokens = self._extract_tokens(text)

        self.access_modifier = tokens['access_modifier']
        self.modifiers = tokens['modifiers']
        self.return_value_type = tokens['return_value_type']
        self.name = tokens['name']
        self.arguments = tokens['arguments']
        self.body = tokens['body']

        super().__init__(text, EntityType.FUNCTION)

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
