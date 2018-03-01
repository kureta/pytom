from collections import deque

from pytom.libs.utils import reduce_with, lcm


class Bjorklund:
    @classmethod
    def from_n_steps_n_beats(cls, n_steps, n_beats):
        instance = bjorklund(n_steps, n_beats)
        return instance

    @classmethod
    def from_steps(cls, steps):
        instance = cls([])
        instance._steps = steps
        return instance

    def __init__(self, durations):
        # deque of durations of each beat
        self._durations = deque(durations)
        # GETTER ONLY
        self._n_beats = len(self._durations)
        # GETTER ONLY
        self._n_steps = len(self._steps)
        # TODO: the following
        # GETTER AND SETTER
        # __offset
        # GETTER AND SETTER
        # __indices
        # GETTER AND SETTER
        # __steps

    def is_bjorklund(self):
        bjork = Bjorklund.from_n_steps_n_beats(len(self._steps), len(self._durations))
        return self == bjork

    @property
    def _steps(self):
        if any([x <= 0 for x in self._durations]):
            raise ValueError("Negative or zero length durations do not make sense in this context!")
        return sum([[1] + [0] * (x - 1) for x in self._durations], [])

    # TODO: Pulses may start with a rest. What are we going to do with durations then?
    # Maybe replace duration with beat indices for generation. Use delta function to get cyclic durations.
    @_steps.setter
    def _steps(self, value):
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

        self._durations = deque(to_durations(value))

    @property
    def __indices(self):
        return [index for index, value in enumerate(self._steps) if value == 1]

    def delta(self, j, i):
        return (self.__indices[(i + j) % self._n_beats] - self.__indices[i]) % self._n_steps

    def delta_bar(self, i):
        result = 0
        for j in range(1, self._n_beats):
            result += self.delta(j, i)
        return result / (self._n_beats - 1)

    def uglyness(self, i):
        result = 0
        for j in range(1, self._n_beats):
            result += (self.delta(j, i) - self.delta_bar(i)) ** 2
        return result / (self._n_beats - 1)

    def total_uglyness(self):
        result = 0
        for j in range(1, self._n_beats // 2 + 1):
            for i in range(0, self._n_beats):
                result += (self.delta(j, i) - (j * self._n_steps) / self._n_beats) ** 2
        return 2 * result / self._n_beats

    def __len__(self):
        return len(self._steps)

    # noinspection PyProtectedMember
    def __add__(self, other):
        multiple = lcm(len(self._durations), len(other._steps))
        a = multiple // len(self._durations)
        b = multiple // len(other._steps)
        return Bjorklund([x + y for x, y in zip(self._durations * a, other._steps * b)])

    # noinspection PyProtectedMember
    def __eq__(self, other):
        result = False
        for i in range(len(self._durations)):
            self._durations.rotate()
            if other._durations == self._durations:
                result = True
                break
        return result

    def __repr__(self):
        return f"<{' '.join([str(i) for i in self._durations])}>"

    def __str__(self):
        return f"<{' '.join([str(i) for i in self._durations])}>"


def bjorklund(n_steps, n_beats):
    """ Calculates optimal distribution of a number of beats over a number of discrete steps.
    :param n_steps: number of steps (ex: divisions of a measure)
    :param n_beats: number of beats (ex: hits of a drum)
    :return: duration of each beat (ex: bjorklund(8,2) => [3, 3, 2]

    Divide steps into beats.
    If the remainder is 0, beats divide the steps equally and result of the division is the duration of each beat.

    >>> bjorklund(8, 4)
    <2 2 2 2>

    Otherwise recursively get the optimal distribution of the remainder over the beats.
    Convert that into a binary representation. ex: [3, 2] => [1, 0, 0, 1, 0]
    Add the evenly distributed remainder to the equal division of steps.
    ex: bjorklund(12, 5) => [2, 2, 2, 2, 2] + [1, 0, 0, 1, 0] = [3, 2, 2, 3, 2]

    >>> bjorklund(12, 5)
    <3 2 2 3 2>
    """
    if n_beats <= 0 or n_steps <= 0 or n_beats > n_steps:
        raise ValueError("Negative or zero number of steps or beats do not make sense in this context!")

    quotient, remainder = divmod(n_steps, n_beats)
    if remainder == 0:
        return Bjorklund([quotient] * n_beats)

    return Bjorklund([quotient] * n_beats) + bjorklund(n_beats, remainder)
