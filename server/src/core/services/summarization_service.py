import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.utils import capitalize


class SummarizationService:
    _model_name = 'Salesforce/codet5-base-multi-sum'
    _tokenizer = AutoTokenizer.from_pretrained(_model_name)
    _model = AutoModelForSeq2SeqLM.from_pretrained(_model_name)

    _words_black_list = [' ', 'Returns']

    @staticmethod
    def summarize_code(text: str, max_length: int = 50) -> str:
        inputs = SummarizationService._tokenizer(text.strip(), return_tensors='pt', max_length=512, truncation=True, padding='max_length')
        outputs = SummarizationService._model.generate(inputs['input_ids'], length_penalty=20.0, max_length=max_length, num_beams=4, early_stopping=True)
        translated = SummarizationService._tokenizer.decode(outputs[0], skip_special_tokens=True).strip('- ')
        translated = capitalize(translated.strip(' '.join(SummarizationService._words_black_list)))

        return translated
