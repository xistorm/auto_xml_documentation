from .extended_enum import ExtendedEnum


class Modifiers(ExtendedEnum):
    STATIC = 'static'

    CONST = 'const'
    READONLY = 'readonly'
    VOLATILE = 'volatile'

    VIRTUAL = 'virtual'
    ABSTRACT = 'abstract'
    OVERRIDE = 'override'
    ASYNC = 'async'

    SEALED = 'sealed'
    PARTIAL = 'partial'
