from ..types import EntityType


class XmlDocumentation:
    def __init__(self, entity_id: str, entity_type: EntityType, summary: str):
        self.summary = summary
        self.entity_id = entity_id
        self.entity_type = entity_type

    @staticmethod
    def _build_xml_tag(tag: str, content: str, attributes: dict = None, pad: int = 0, extended: bool = True):
        prefix = f'{" " * pad}/// '
        parsed_attributes = [f'{name}="{value}"' for name, value in attributes.items()] if attributes is not None else []
        processed_attributes = " ".join(parsed_attributes)
        lines = [
            f'<{tag} {processed_attributes}>',
            content,
            f'</{tag}>',
        ]

        if not extended:
            return f'{prefix}{"".join(lines)}'

        processed_lines = [f'{prefix}{line}' for line in lines]
        return '\n'.join(processed_lines)

    @staticmethod
    def _build_summary(summary: str, pad: int = 0) -> str:
        return XmlDocumentation._build_xml_tag('summary', summary, pad=pad)

    @staticmethod
    def _build_arguments(arguments: dict, pad: int = 0) -> str:
        arguments_documentation = []
        for name, summary in arguments.items():
            documentation = XmlDocumentation._build_xml_tag('param', summary, {'name': name}, pad, False)
            arguments_documentation.append(documentation)

        return "\n".join(arguments_documentation)

    @staticmethod
    def _build_return_type(summary: str, pad: int = 0) -> str:
        return XmlDocumentation._build_xml_tag('returns', summary, pad=pad, extended=False)

    def build_documentation_text(self, pad: int = 0) -> str:
        return XmlDocumentation._build_summary(self.summary, pad)
