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
    def test_from_n_steps_n_beats(self, n_steps, n_beats):
        assume(n_steps > n_beats)

        implementation = Bjorklund.from_n_steps_n_beats(n_steps, n_beats)
        reference = Bjorklund.from_steps(reference_bjorklund(n_steps, n_beats))

        self.assertEqual(implementation, reference)

    @given(st.integers(min_value=-128, max_value=128), st.integers(min_value=-128, max_value=128))
    def test_from_n_steps_n_beats_exceptions(self, n_steps, n_beats):
        if n_steps < n_beats or n_steps <= 0 or n_beats <= 0:
            self.assertRaises(ValueError, Bjorklund.from_n_steps_n_beats, n_steps, n_beats)
        else:
            self.assertIsInstance(Bjorklund.from_n_steps_n_beats(n_steps, n_beats), Bjorklund)

    @given(st.lists(st.integers(min_value=0, max_value=1), max_size=256))
    def test_from_steps(self, steps):
        assume(1 in steps)
        b1 = Bjorklund.from_steps(steps)

        self.assertEqual(b1, Bjorklund(b1.durations, b1.offset))

    @given(st.lists(st.integers(), max_size=256))
    def test_from_steps_exceptions(self, steps):
        if not steps:
            self.assertEqual(Bjorklund.from_steps(steps), Bjorklund([]))
        elif not all([s == 0 or s == 1 for s in steps]):
            self.assertRaises(ValueError, Bjorklund.from_steps, steps)
        elif 1 not in steps:
            self.assertRaises(ValueError, Bjorklund.from_steps, steps)
        else:
            self.assertIsInstance(Bjorklund.from_steps(steps), Bjorklund)
