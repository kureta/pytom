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
        instance.steps = steps
        return instance

    def __init__(self, durations):
        self.__durations = None
        self.__steps = None
        self.__indices = None
        self.__offset = None
        self.__n_steps = None
        self.__n_beats = None

        self.durations = durations


    @property
    def durations(self):
        return self.__durations

    @durations.setter
    def durations(self, durations):
        if any([x <= 0 for x in durations]):
            raise ValueError("Negative or zero length durations do not make sense in this context!")

        self.__durations = durations
        self.__steps = sum([[1] + [0] * (x - 1) for x in durations], [])
        self.__indices = [index for index, value in enumerate(self.steps) if value == 1]
        self.__n_beats = len(self.durations)
        self.__n_steps = len(self.steps)

    @property
    def steps(self):
        return self.__steps

    # TODO: Pulses may start with a rest. What are we going to do with durations then?
    # Maybe replace duration with beat indices for generation. Use delta function to get cyclic durations.
    @steps.setter
    def steps(self, steps):
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

        self.__steps = steps
        self.__durations = deque(to_durations(steps))
        self.__indices = [index for index, value in enumerate(steps) if value == 1]
        self.__n_beats = len(self.durations)
        self.__n_steps = len(self.steps)

    # TODO: indices setter
    @property
    def indices(self):
        return self.__indices

    @property
    def n_steps(self):
        return self.__n_steps

    @property
    def n_beats(self):
        return self.__n_beats

    def delta(self, j, i):
        return (self.indices[(i + j) % self.n_beats] - self.indices[i]) % self.n_steps

    def delta_bar(self, i):
        result = 0
        for j in range(1, self.n_beats):
            result += self.delta(j, i)
        return result / (self.n_beats - 1)

    def uglyness(self, i):
        result = 0
        for j in range(1, self.n_beats):
            result += (self.delta(j, i) - self.delta_bar(i)) ** 2
        return result / (self.n_beats - 1)

    def total_uglyness(self):
        result = 0
        for j in range(1, self.n_beats // 2 + 1):
            for i in range(0, self.n_beats):
                result += (self.delta(j, i) - (j * self.n_steps) / self.n_beats) ** 2
        return 2 * result / self.n_beats

    def is_bjorklund(self):
        bjork = Bjorklund.from_n_steps_n_beats(self.n_steps, self.n_beats)
        return self == bjork

    def __len__(self):
        return self.n_steps

    def __add__(self, other):
        multiple = lcm(self.n_beats, other.n_steps)
        a = multiple // self.n_beats
        b = multiple // other.n_steps
        return Bjorklund([x + y for x, y in zip(self.durations * a, other.steps * b)])

    def __eq__(self, other):
        d_rotations = deque(self.durations)
        other_durations = deque(other.durations)

        for i in range(self.n_beats):
            if other_durations == d_rotations:
                return True
            d_rotations.rotate()
        return False

    def __repr__(self):
        return f"<{' '.join([str(i) for i in self.durations])}>"

    def __str__(self):
        return f"<{' '.join([str(i) for i in self.durations])}>"


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
