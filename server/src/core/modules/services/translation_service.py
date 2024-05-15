import torch

from translate import Translator


class TranslationService:
    _natural_translator = Translator(from_lang='en', to_lang='ru')

    @staticmethod
    def translate_natural_language(text: str) -> str:
        translated = TranslationService._natural_translator.translate(text.strip())

        return translated
