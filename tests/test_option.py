import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def option_parser() -> Lark:
    return Lark(
        """
    start: option
    %import .option.option
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        'option "key" "value"',
        'option "key" "value" ; this is a comment',
    ],
)
def test_parse_option(plugin_parser, text: str):
    plugin_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        'option "key"',
        'option key "value"',
        "option 'key' 'value'",
    ],
)
def test_parse_bad_option(plugin_parser, text: str):
    with pytest.raises(UnexpectedInput):
        plugin_parser.parse(text)