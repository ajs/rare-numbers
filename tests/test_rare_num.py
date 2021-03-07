"""Tests for rare numbers"""


import itertools

import pytest

from rare_num import (
    rare_last_digit, py37_isqrt, is_perfect_square,
    digital_root, is_rare, rare_numbers, rare_second_digits
)


@pytest.mark.parametrize(
    'n, result', (
        (1, 1),
        (10, 3),
        (16, 4),
        (99999980000001, 9999999),
        (152415787532388367501905199875019052100, 12345678901234567890),
        (152415787532388367501905199875019052101, 12345678901234567890),
        (152415787532388367526596557677488187880, 12345678901234567890),
        (152415787532388367526596557677488187881, 12345678901234567891),
    )
)
def test_isqrt(n, result):
    assert py37_isqrt(n) == result, f"Expect isqrt({n}) == {result}"


@pytest.mark.parametrize(
    'n, result', (
        (1, True),
        (2, False),
        (4, True),
        (1002001, True),
        (1002002, False),
        (152415787532388367526596557677488187881, True),
        (152415787532388367526596557677488187882, False),
    )
)
def test_is_perfect_square(n, result):
    assert is_perfect_square(n) is result, f"Expect is_perfect_square({n}) is {result!r}"


@pytest.mark.parametrize(
    'n, result', (
        (1, 1),
        (10, 1),
        (19, 1),
        (38, 2),
        (12345678901234567890, 9),
    )
)
def test_digital_root(n, result):
    assert digital_root(n) == result, f"Expect digital_root({n}) == {result}"


@pytest.mark.parametrize(
    'n, result', (
        (1, False),
        (65, True),
        (66, False),
        (67, False),
        (621770, True),
        (22134434735752443122, True),
        (22134434535752443122, False),
        (61999171315484316965, True),
        (61999171315484316960, False),
        (65459144877856561700, True),
        (65459144877856561705, False),
    )
)
def test_is_rare(n, result):
    assert is_rare(n) is result, f"Expect is_rare({n}) is {result!r}"


def _digit_pairs(filter_func):
    """Generate pairs of digits that meet filter_func's metric"""

    for a, b in itertools.product(range(10), repeat=2):
        if filter_func(a, b):
            yield (a, b)


@pytest.mark.parametrize(
    'first, last, expect, desc', (
        (2, 2, [(n,n) for n in range(10)], "B = P"),
        (4, 0, _digit_pairs(lambda a, b: (a - b) % 2 == 0), "|B - P| = zero or Even"),
        (6, 0, _digit_pairs(lambda a, b: (a - b) % 2 == 1), "|B - P| = Odd"),
        (8, 2, _digit_pairs(lambda a, b: a + b == 9), "B + P = 9"),
        (8, 3, _digit_pairs(lambda a, b: (a - b == 7 or b - a == 3)), "B - P=7 or P - B = 3"),
        (8, 7, _digit_pairs(lambda a, b: (a + b == 11 or a + b == 1)), "B + P = 11 or B + P = 1"),
        (8, 8, [(n,n) for n in range(10)], "B = P"),
    )
)
def test_rare_second_digits(first, last, expect, desc):
    msg = f"{first}, {last}: {desc}"
    result = set(rare_second_digits(first, last))
    expect = set(expect)
    assert result == expect, msg


@pytest.mark.parametrize(
    'digits, result', (
        (2, [65]),
        (3, []),
        (4, []),
        (5, []),
        (6, [621770]),
    )
)
def test_rare_numbers(digits, result):
    """Check small ranges that can be completed fast"""

    assert list(rare_numbers(digits)) == result, f"Expect {result!r} for {digits} digits"
