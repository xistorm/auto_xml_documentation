from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities import Entity
import re

from ..types import AccessModifiers

from src.utils import capitalize


class XmlDocumentation:
    def __init__(self, entity: Entity, summary: str):
        self.entity_id = entity.id
        self.entity_type = entity.type
        self.permission = AccessModifiers.get_permission(entity.access_modifier)
        self.modifiers = ','.join([str(modifier) for modifier in entity.modifiers])
        self.summary = summary

    @staticmethod
    def _enrich_summary(summary: str, additional: str) -> str:
        separator = '. '
        extended_summary = separator.join([summary.strip(separator), additional])
        summary_lines = extended_summary.split(separator)
        processed_lines = [capitalize(re.sub(r'\s+', ' ', line.strip())) for line in summary_lines if line]
        formatted_summary = separator.join(processed_lines)

        return formatted_summary

    @staticmethod
    def _build_xml_tag(tag: str, content: str, attributes: dict = None, pad: int = 0, extended: bool = True) -> str:
        if content is None:
            print(content)
        prefix = f'{" " * pad}/// '
        parsed_attributes = [f'{name}="{value}"' for name, value in attributes.items()] if attributes is not None else []
        processed_attributes = " ".join(parsed_attributes)
        processed_content = content.replace('. ', '\n') if extended else content.replace('\n', '. ')
        content_lines = [line for line in processed_content.split('\n') if line]
        lines = [
            f'<{tag}{" " if processed_attributes else ""}{processed_attributes}>',
            *content_lines,
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

    @staticmethod
    def _build_permission(permission: str, pad: int = 0) -> str:
        return XmlDocumentation._build_xml_tag('permission', permission, pad=pad, extended=False)

    @staticmethod
    def _build_modifiers(modifiers: str, pad: int = 0) -> str:
        return XmlDocumentation._build_xml_tag('modifiers', modifiers, pad=pad, extended=False)

    def build_documentation_text(self, pad: int = 0) -> str:
        return '\n'.join([
            XmlDocumentation._build_permission(self.permission, pad),
            XmlDocumentation._build_summary(self.summary, pad),
        ])

    @staticmethod
    def is_documentation_text(text: str) -> bool:
        return re.search(r'\s*///.*', text, re.DOTALL) is not None
