import hypothesis.strategies as st
import pytest
from hypothesis import given

from pytom.libs.bjorklund import Bjorklund


def reference_bjorklund(steps, pulses):
    if pulses <= 0 or steps <= 0 or pulses > steps:
        raise ValueError
    pattern = []
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    while remainders[level] > 1:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level += 1

    counts.append(divisor)

    def build(level_):
        if level_ == -1:
            pattern.append(0)
        elif level_ == -2:
            pattern.append(1)
        else:
            for __ in range(0, counts[level_]):
                build(level_ - 1)
            if remainders[level_] != 0:
                build(level_ - 2)

    build(level)
    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]
    return pattern


@given(st.integers(min_value=-256, max_value=256), st.integers(min_value=-256, max_value=256))
def test_bjorklund(x, y):
    if y > x:
        with pytest.raises(ValueError):
            Bjorklund.from_n_steps_n_beats(x, y)
        with pytest.raises(ValueError):
            reference_bjorklund(x, y)
        return

    if y <= 0:
        with pytest.raises(ValueError):
            Bjorklund.from_n_steps_n_beats(x, y)
        with pytest.raises(ValueError):
            reference_bjorklund(x, y)
        return

    reference = Bjorklund.from_steps(reference_bjorklund(x, y))
    recursive = Bjorklund.from_n_steps_n_beats(x, y)

    assert reference == recursive
