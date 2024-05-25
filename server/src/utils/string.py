import re


def split_camel_case(text: str) -> str:
    return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', text).lower()


def capitalize(text: str) -> str:
    if len(text) < 2:
        return text.upper()
    return text[0].upper() + text[1:]
