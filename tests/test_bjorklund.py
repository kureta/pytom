import unittest
from hypothesis import given, assume
import hypothesis.strategies as st

from pytom.libs.bjorklund import Bjorklund


def reference_bjorklund(steps, beats):
    if beats <= 0 or steps <= 0 or beats > steps:
        raise ValueError
    pattern = []
    counts = []
    remainders = []
    divisor = steps - beats
    remainders.append(beats)
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


# TODO: Improve test coverage
class BjorklundTest(unittest.TestCase):

    @given(st.integers(min_value=1, max_value=128), st.integers(min_value=1, max_value=128))
    def test_from_n_steps_n_beats(self, x, y):
        assume(x > y)

        implementation = Bjorklund.from_n_steps_n_beats(x, y)
        reference = Bjorklund.from_steps(reference_bjorklund(x, y))

        self.assertEqual(implementation, reference)

    @given(st.integers(min_value=-128, max_value=128), st.integers(min_value=-128, max_value=128))
    def test_from_n_steps_n_beats_exceptions(self, x, y):
        if x < y or x <= 0 or y <= 0:
            self.assertRaises(ValueError, Bjorklund.from_n_steps_n_beats, x, y)
        else:
            self.assertIsInstance(Bjorklund.from_n_steps_n_beats(x, y), Bjorklund)
