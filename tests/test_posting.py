import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def posting_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="posting", rule="posting", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "Assets 10 USD",
        "Assets -10 USD",
        "Assets:Bank -10.0 USD",
        "Assets:Bank -10.0 TWD",
        "Assets:Bank -10.0 TWD ; this is a comment",
        "Assets:Bank -10.0 TWD; this is a comment",
        "Assets:Bank -10.0 TWD @ 2.56 USD",
        "Assets:Bank -10.0 TWD @  2.56  USD",
        "Assets:Bank -10.0 TWD @@ 2.56 USD",
        "Assets:Bank -10.0 TWD {100.56 USD}",
        "Assets:Bank -10.0 TWD { 100.56 USD }",
        "Assets:Bank -10.0 TWD {{100.56 USD}}",
        "Assets:Bank -10.0 TWD {{ 100.56  USD}}",
        "Assets:Bank -10.0 TWD {100.56 # 12.34 USD}",
        "Assets:Bank -10.0 TWD { 100.56  #  12.34 USD }",
        "Assets:Bank -10.0 TWD {100.56 # 3.45 CAD }",
        "Assets:Bank -10.0 TWD {100.56 USD, 2021-06-07}",
        "Assets:Bank -10.0 TWD {100.56 USD  , 2021-06-07}",
        "Assets:Bank -10.0 TWD { 100.56 USD , 2021-06-07 }",
        "! Assets:Bank -10.0 TWD",
        "* Assets:Bank -10.0 TWD",
    ],
)
def test_parse_posting(posting_parser: Lark, text: str):
    posting_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "Assets 10",
        "A -10 USD",
        "@ Assets:Bank -10.0 TWD",
    ],
)
def test_parse_bad_posting(posting_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        posting_parser.parse(text)
