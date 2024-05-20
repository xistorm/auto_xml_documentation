import torch
import re

from typing import Tuple, List
from googletrans import Translator


class TranslationService:
    _translator = Translator()
    _tokens_placeholder = '<<< {} >>>'
    _static_part_pattern = r'\[[^\]]+\]'

    @staticmethod
    def _replace_static_parts(text: str) -> Tuple[str, List[str]]:
        tokens = re.findall(TranslationService._static_part_pattern, text)
        for i, token in enumerate(tokens):
            text = text.replace(token, TranslationService._tokens_placeholder.format(i))

        return text, tokens

    @staticmethod
    def _replace_placeholders_with_tokens(text: str, tokens: List[str]) -> str:
        for i, token in enumerate(tokens):
            text = text.replace(TranslationService._tokens_placeholder.format(i), token)

        return text


    @staticmethod
    def translate(text: str, src: str = 'en', dest: str = 'en') -> str:
        if src == dest:
            return text

        processed_text, tokens = TranslationService._replace_static_parts(text.strip())
        translated = TranslationService._translator.translate(processed_text, src=src, dest=dest)
        translated_text = f"{translated.text.replace('.', '. ')}."
        processed_translated_text = TranslationService._replace_placeholders_with_tokens(translated_text, tokens)

        return processed_translated_text
