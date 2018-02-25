import pytest
import hypothesis.strategies as st
from hypothesis import given, assume

from collections import deque

from pytom.libs.bjorklund import bjorklund, to_binary, to_durations


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

    reference = reference_bjorklund(x, y)
    recursive = to_binary(bjorklund(x, y))

    # Check for equality up to rotation
    reference_deque = deque(reference)
    recursive_deque = deque(recursive)
    reference_rotations = (reference_deque.rotate(i) for i in range(len(reference)))
    recursive_rotations = (recursive_deque.rotate(i) for i in range(len(recursive)))

    assert any((a == b for a, b in zip(reference_rotations, recursive_rotations)))


@given(st.lists(st.integers(min_value=-16, max_value=16), max_size=32))
def test_to_binary(xs):
    if any(x <= 0 for x in xs):
        with pytest.raises(ValueError):
            to_binary(xs)
        return

    binary = to_binary(xs)
    durations = to_durations(binary)

    assert durations == xs


@given(st.lists(st.integers(min_value=-16, max_value=16), max_size=32))
def test_to_durations(xs):
    assume(not all(x == 1 or x == 0 for x in xs))
    with pytest.raises(ValueError):
        to_durations(xs)


@given(st.lists(st.integers(min_value=0, max_value=1), max_size=32))
def test_to_durations_2(xs):
    if xs and xs[0] == 0:
        with pytest.raises(ValueError):
            to_durations(xs)
        return

    durations = to_durations(xs)
    binary = to_binary(durations)

    assert binary == xs
