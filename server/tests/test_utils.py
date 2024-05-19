from itertools import repeat

from src.utils import split_camel_case, capitalize, read_code_block
from .stubs import function_text, arrow_function_text, class_text, lorem_ipsum


def test_split_camel_case():
    assert split_camel_case('CamelCaseString') == 'camel case string'
    assert split_camel_case('smallCamelCaseString') == 'small camel case string'


def test_capitalize():
    assert capitalize('string') == 'String'
    assert capitalize('some text example') == 'Some text example'
    assert capitalize('some Text Example') == 'Some Text Example'


def test_read_code_block():
    start_index = 5
    lorem_ipsum_multiline = '\n'.join(repeat(lorem_ipsum, start_index))

    def assert_code_block(code_block):
        expected_steps = len(code_block.split('\n')) - 1
        formatted_code_block = f'{lorem_ipsum_multiline}\n{code_block}\n{lorem_ipsum_multiline}'.split('\n')
        new_code_block, steps = read_code_block(formatted_code_block, start_index)

        assert new_code_block == code_block
        assert steps == expected_steps

    assert_code_block(function_text)
    assert_code_block(arrow_function_text)
    assert_code_block(class_text)
