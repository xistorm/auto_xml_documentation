import re

from ..types import EntityType, AccessModifiers, Modifiers, ValueTypes
from . import Entity


class VariableEntity(Entity):
    _pattern = fr"""
        \s*
        (?P<access_modifier>{AccessModifiers.union('|')})?\s*
        (?P<modifiers>({Modifiers.union()})*)
        (?P<value_type>({ValueTypes.union('|')}|[A-Z]\w*)([\[\]]*|(<\w+>)))\s+
        (?P<name>\w+)\s*
        ((=\s*)(?P<init_value>([^;]*)))?\s*
    """

    def __init__(self, text: str, path: str = None):
        tokens = VariableEntity._extract_tokens(text)

        self.name = tokens['name']
        self.value_type = tokens['value_type']
        self.access_modifier = tokens['access_modifier']
        self.modifiers = tokens['modifiers']
        self.init_value = tokens['init_value']

        path = Entity._build_path(path, self.name)

        super().__init__(path, text, EntityType.VARIABLE)

    def __repr__(self):
        return f'''{{
            'access_modifier': {self.access_modifier},
            'modifiers': {self.modifiers},
            'value_type': {self.value_type},
            'name': {self.name},
            'init_value': {self.init_value},
        }}'''

    @staticmethod
    def _extract_tokens(text: str) -> dict:
        match = re.search(VariableEntity._pattern, text, re.VERBOSE)

        tokens = match.groupdict()
        tokens['modifiers'] = [modifier for modifier in tokens['modifiers'].split(' ') if modifier]

        return tokens

    @staticmethod
    def is_variable_text(text: str) -> bool:
        return re.search(VariableEntity._pattern, text, re.VERBOSE) is not None
