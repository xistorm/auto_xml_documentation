from .extended_enum import ExtendedEnum


class AccessModifiers(ExtendedEnum):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    INTERNAL = 'internal'

    @staticmethod
    def get_permission(modifier) -> str:
        match modifier:
            case AccessModifiers.PUBLIC.value: return 'Everyone'
            case AccessModifiers.PRIVATE.value: return 'Only it\'s class'
            case AccessModifiers.PROTECTED.value: return 'It\'s class and his children'
            case AccessModifiers.INTERNAL.value: return 'It\'s build'
