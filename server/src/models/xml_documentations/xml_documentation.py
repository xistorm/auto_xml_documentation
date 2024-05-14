from ..types import EntityType


class XmlDocumentation:
    def __init__(self, summary: str, path: str, entity_type: EntityType):
        self.summary = summary
        self.path = path
        self.type = entity_type

    @staticmethod
    def _build_summary(summary: str) -> str:
        return f'''
            /// <summary>
            /// {summary}
            /// </summary>
        '''

    @staticmethod
    def _build_arguments(arguments: dict) -> str:
        arguments = [f'/// <param name="{name}">{summary}</param>' for name, summary in arguments.items()]

        return "\n".join(arguments)

    @staticmethod
    def _build_return_type(summary: str) -> str:
        return f'/// <returns>{summary}</returns>'

    def build_documentation_text(self):
        return XmlDocumentation._build_summary(self.summary)
