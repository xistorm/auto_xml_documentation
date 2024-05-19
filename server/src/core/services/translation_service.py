import torch

from translate import Translator


class TranslationService:
    _translator = Translator(from_lang='en', to_lang='ru')

    @staticmethod
    def translate_natural_language(text: str) -> str:
        translated = TranslationService._translator.translate(text.strip())

        return translated
