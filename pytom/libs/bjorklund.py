from collections import deque
from operator import add

from pytom.libs.utils import reduce_with, foldr


class Bjorklund:
    @classmethod
    def from_steps_and_durations(cls, n_steps, n_pulses):
        instance = bjorklund(n_steps, n_pulses)
        return instance

    @classmethod
    def from_pulses(cls, pulses):
        instance = cls([])
        instance.pulses = pulses
        return instance

    def __init__(self, durations):
        self.durations = deque(durations)

    def check_bjorkness(self):
        bjork = Bjorklund.from_steps_and_durations(len(self.pulses), len(self.durations))
        return self == bjork

    @property
    def pulses(self):
        if any([x <= 0 for x in self.durations]):
            raise ValueError("Negative or zero length durations do not make sense in this context!")
        return sum([[1] + [0] * (x - 1) for x in self.durations], [])

    # TODO: Pulses may start with a rest. What are we going to do with durations then?
    # Maybe replace duration with pulse indices for generation. Use delta function to get cyclic durations.
    @pulses.setter
    def pulses(self, value):
        @reduce_with(init=[])
        def to_durations(x, y):
            if not x:
                if y != 1:
                    raise NotImplemented("Patterns cannot start with rests just yet. Sorry.")
                return [y]
            if y == 0:
                return x[:-1] + [x[-1] + 1]
            if y == 1:
                return x + [y]

        self.durations = deque(to_durations(value))

    @property
    def pulse_indices(self):
        return [index for index, value in enumerate(self.pulses) if value == 1]

    def delta(self, j, i):
        n_pulses = len(self.pulse_indices)
        n_steps = len(self.pulses)
        return (self.pulse_indices[(i + j) % n_pulses] - self.pulse_indices[i]) % n_steps

    def delta_bar(self, i):
        n_pulses = len(self.pulse_indices)
        result = 0
        for j in range(1, n_pulses):
            result += self.delta(j, i)
        return result / (n_pulses - 1)

    def uglyness(self, i):
        n_pulses = len(self.pulse_indices)
        result = 0
        for j in range(1, n_pulses):
            result += (self.delta(j, i) - self.delta_bar(i)) ** 2
        return result / (n_pulses - 1)

    def total_uglyness(self):
        n_pulses = len(self.pulse_indices)
        n_steps = len(self.pulses)
        result = 0
        for j in range(1, n_pulses // 2 + 1):
            for i in range(0, n_pulses):
                result += (self.delta(j, i) - (j * n_steps) / n_pulses) ** 2
        return 2 * result / n_pulses

    def __len__(self):
        return len(self.pulses)

    def __add__(self, other):
        return Bjorklund([x + y for x, y in zip(self.durations, other.pulses)])

    def __eq__(self, other):
        result = False
        for i in range(len(self.durations)):
            self.durations.rotate()
            if other.durations == self.durations:
                result = True
                break
        return result

    def __repr__(self):
        return f"<{' '.join([str(i) for i in self.durations])}>"

    def __str__(self):
        return f"<{' '.join([str(i) for i in self.durations])}>"


def bjorklund(n_steps, n_pulses):
    """ Calculates optimal distribution of a number of pulses over a number of discrete steps.
    :param n_steps: number of steps (ex: divisions of a measure)
    :param n_pulses: number of pulses (ex: hits of a drum)
    :return: duration of each pulse (ex: bjorklund(8,2) => [3, 3, 2]

    Divide steps into pulses.
    If the remainder is 0, pulses divide the steps equally and result of the division is the duration of each pulse.

    >>> bjorklund(8, 4)
    <2 2 2 2>

    Otherwise recursively get the optimal distribution of the remainder over the pulses.
    Convert that into a binary representation. ex: [3, 2] => [1, 0, 0, 1, 0]
    Add the evenly distributed remainder to the equal division of steps.
    ex: bjorklund(12, 5) => [2, 2, 2, 2, 2] + [1, 0, 0, 1, 0] = [3, 2, 2, 3, 2]

    >>> bjorklund(12, 5)
    <3 2 2 3 2>
    """
    if n_pulses <= 0 or n_steps <= 0 or n_pulses > n_steps:
        raise ValueError("Negative or zero number of steps or pulses do not make sense in this context!")
    quotient, remainder = divmod(n_steps, n_pulses)

    if remainder == 0:
        return Bjorklund([quotient] * n_pulses)

    return Bjorklund([quotient] * n_pulses) + bjorklund(n_pulses, remainder)


def bjorklund_non_recursive(n_steps, n_pulses):
    """ Calculates optimal distribution of a number of pulses over a number of discrete steps.
    :param n_steps: number of steps (ex: divisions of a measure)
    :param n_pulses: number of pulses (ex: hits of a drum)
    :return: duration of each pulse (ex: bjorklund(8,2) => [3, 3, 2]

    Non-recursive version of the Bjorklund algorithm.

    >>> bjorklund(8, 4)
    <2 2 2 2>

    >>> bjorklund(12, 5)
    <3 2 2 3 2>
    """
    if n_pulses <= 0 or n_steps <= 0 or n_pulses > n_steps:
        raise ValueError

    beats = []
    remainder = 1
    while remainder > 0:
        quotient, remainder = divmod(n_steps, n_pulses)
        beats.append(Bjorklund([quotient] * n_pulses))
        n_steps, n_pulses = n_pulses, remainder

    result = foldr(add, beats)
    return result
