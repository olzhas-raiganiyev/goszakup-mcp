import random

import pytest

from goszakup_mcp import bin_iin


def make_valid(prefix: str) -> str:
    digit = bin_iin.check_digit(prefix)
    assert digit is not None
    return prefix + str(digit)


def valid_samples(n: int = 50, seed: int = 7) -> list[str]:
    rng = random.Random(seed)
    out: list[str] = []
    while len(out) < n:
        prefix = "".join(rng.choice("0123456789") for _ in range(11))
        if bin_iin.check_digit(prefix) is not None:
            out.append(make_valid(prefix))
    return out


@pytest.mark.parametrize("value", valid_samples())
def test_generated_numbers_are_valid(value: str) -> None:
    assert bin_iin.check(value).valid


def _detection_rate(pos: int, samples: list[str]) -> float:
    caught = total = 0
    for value in samples:
        for d in "0123456789":
            if d == value[pos]:
                continue
            total += 1
            caught += not bin_iin.check(value[:pos] + d + value[pos + 1 :]).valid
    return caught / total


def test_check_digit_change_is_always_detected() -> None:
    assert _detection_rate(11, valid_samples(200, seed=11)) == 1.0


@pytest.mark.parametrize("pos", range(10))
def test_typos_in_first_ten_digits_are_mostly_detected(pos: int) -> None:
    # The fallback weight pass lets a few typos through; ~98% are caught.
    assert _detection_rate(pos, valid_samples(200, seed=11)) > 0.95


def test_eleventh_digit_is_weakly_protected() -> None:
    """Known property of the checksum: digit 11 has weight 11 = 0 (mod 11) in the
    first pass, so most typos there pass validation. check_bin cannot catch them."""
    assert _detection_rate(10, valid_samples(200, seed=11)) < 0.5


def test_whitespace_is_trimmed() -> None:
    value = valid_samples(1)[0]
    assert bin_iin.check(f"  {value}\n").valid


@pytest.mark.parametrize(
    ("value", "fragment"),
    [
        ("12345", "exactly 12 digits"),
        ("1234567890123", "exactly 12 digits"),
        ("12345678901a", "digits only"),
        ("", "digits only"),
    ],
)
def test_bad_format_explains_reason(value: str, fragment: str) -> None:
    result = bin_iin.check(value)
    assert not result.valid
    assert result.reason is not None and fragment in result.reason


def test_wrong_check_digit_names_expected_digit() -> None:
    value = valid_samples(1)[0]
    wrong = value[:-1] + str((int(value[-1]) + 1) % 10)
    result = bin_iin.check(wrong)
    assert not result.valid
    assert result.reason is not None and f"expected {value[-1]}" in result.reason


def test_prefix_without_any_check_digit_is_invalid() -> None:
    rng = random.Random(3)
    for _ in range(100_000):
        prefix = "".join(rng.choice("0123456789") for _ in range(11))
        if bin_iin.check_digit(prefix) is None:
            result = bin_iin.check(prefix + "0")
            assert not result.valid
            assert result.reason is not None and "no valid check digit" in result.reason
            return
    pytest.fail("no prefix without a check digit found")


def test_check_digit_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        bin_iin.check_digit("123")
