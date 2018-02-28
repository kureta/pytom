from collections import deque

import hypothesis.strategies as st
import pytest
from hypothesis import given, assume

from pytom.libs.bjorklund import Bjorklund, bjorklund, bjorklund_non_recursive


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
        level = level + 1

    counts.append(divisor)

    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)
        else:
            for i in range(0, counts[level]):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)

    build(level)
    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]
    return pattern


@given(st.integers(min_value=-256, max_value=256), st.integers(min_value=-256, max_value=256))
def test_bjorklund(x, y):
    if y > x:
        with pytest.raises(ValueError):
            bjorklund(x, y)
        with pytest.raises(ValueError):
            reference_bjorklund(x, y)
        return

    if y <= 0:
        with pytest.raises(ValueError):
            bjorklund(x, y)
        with pytest.raises(ValueError):
            reference_bjorklund(x, y)
        return

    reference = Bjorklund.from_pulses(reference_bjorklund(x, y))
    recursive = bjorklund(x, y)

    assert reference == recursive


@given(st.integers(min_value=-256, max_value=256), st.integers(min_value=-256, max_value=256))
def test_bjorklund_non_recursive(x, y):
    if y > x:
        with pytest.raises(ValueError):
            bjorklund_non_recursive(x, y)
        with pytest.raises(ValueError):
            reference_bjorklund(x, y)
        return

    if y <= 0:
        with pytest.raises(ValueError):
            bjorklund_non_recursive(x, y)
        with pytest.raises(ValueError):
            reference_bjorklund(x, y)
        return

    reference = Bjorklund.from_pulses(reference_bjorklund(x, y))
    recursive = bjorklund_non_recursive(x, y)

    assert reference == recursive
