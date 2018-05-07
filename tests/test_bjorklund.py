import unittest

import hypothesis.strategies as st
from hypothesis import given, assume, reproduce_failure

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
        if n_steps < n_beats:
            self.assertRaises(ValueError, Bjorklund.from_n_steps_n_beats, n_steps, n_beats)
        elif n_steps <= 0 or n_beats <= 0:
            self.assertRaises(ValueError, Bjorklund.from_n_steps_n_beats, n_steps, n_beats)
        else:
            implementation = Bjorklund.from_n_steps_n_beats(n_steps, n_beats)
            reference = Bjorklund.from_steps(reference_bjorklund(n_steps, n_beats))
            self.assertEqual(implementation, reference)

    @given(st.lists(st.integers(), max_size=256))
    def test_from_steps(self, steps):
        if not steps:
            self.assertEqual(Bjorklund.from_steps(steps), Bjorklund([]))
        elif not all(s == 0 or s == 1 for s in steps):
            self.assertRaises(ValueError, Bjorklund.from_steps, steps)
        elif 1 not in steps:
            self.assertRaises(ValueError, Bjorklund.from_steps, steps)
        else:
            b1 = Bjorklund.from_steps(steps)
            self.assertEqual(b1.steps, steps)

    @given(st.lists(st.integers(min_value=0, max_value=256), max_size=256, unique=True),
           st.integers(min_value=0, max_value=8))
    def test_from_indices_and_n_steps(self, indices, tail):
        assume(indices)
        indices = sorted(list(set(indices)))
        n_steps = max([max(indices) + 1, len(indices)]) + tail
        b1 = Bjorklund.from_indices_and_n_steps(indices, n_steps)
        self.assertEqual((b1.indices, b1.n_steps), (indices, n_steps))

    @given(st.lists(st.integers(min_value=-256, max_value=256), max_size=256),
           st.integers(min_value=-256, max_value=256))
    @reproduce_failure('3.47.0', b'AAEAAAABAAAAAAAAAg==')
    def test_from_indices_and_n_steps_exceptions(self, indices, n_steps):
        indices = sorted(list(set(indices)))
        if not indices:
            if n_steps == 0:
                self.assertEqual(Bjorklund.from_indices_and_n_steps(indices, n_steps), Bjorklund([]))
            else:
                self.assertRaises(ValueError, Bjorklund.from_indices_and_n_steps, indices, n_steps)
        elif n_steps < max([max(indices) + 1, len(indices)]):
            self.assertRaises(ValueError, Bjorklund.from_indices_and_n_steps, indices, n_steps)
        elif any(x < 0 for x in indices):
            self.assertRaises(ValueError, Bjorklund.from_indices_and_n_steps, indices, n_steps)
        else:
            b1 = Bjorklund.from_indices_and_n_steps(indices, n_steps)
            self.assertEqual((b1.indices, b1.n_steps), (indices, n_steps))
    #
    # @given(st.lists(st.integers(min_value=1, max_value=128), max_size=128), st.integers(min_value=0, max_value=128))
    # def test___init__(self, durations, offset_):
    #     assume(durations)
    #     offset = min(offset_, durations[-1] - 1)
    #
    #     self.assertIsInstance(Bjorklund(durations, offset), Bjorklund)

    # @given(st.lists(st.integers(min_value=-128, max_value=128), max_size=128), st.integers(min_value=-128, max_value=128))
    # def test___init__exceptions(self, durations, offset):
    #     if any(x <= 0 for x in durations):
    #         self.assertRaises(ValueError, Bjorklund, durations, offset)
    #     else:
    #         b1 = Bjorklund(durations, offset)
    #         self.assertIsInstance(b1, Bjorklund)
    #         self.assertEqual((b1.durations, b1.offset) == (durations, offset))
