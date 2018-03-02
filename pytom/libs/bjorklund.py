from typing import List
from collections import deque

from pytom.libs.utils import reduce_with, lcm


# TODO: Write docstrings
# TODO: use numpydoc or change docstring style
class Bjorklund:
    """
    Bjorklund(durations, offset=0)

    Stores different representation of a rhythmic pattern and keeps all of them up to
    date with respect to each other. Can calculate 'uglyness' of a pattern or a specific
    beat of a pattern as defined in Bjorklund (2003). Can be initiated with an Euclidean
    rhythm.

    It has different initialization methods:

    >>> Bjorklund(durations=[3, 2, 3], offset=0)
    <3 2 3>
    >>> Bjorklund.from_n_steps_n_beats(n_steps=8, n_beats=3)
    <3 2 3>
    >>> Bjorklund.from_steps(steps=[1, 0, 0, 1, 0, 1, 0, 0])
    <3 2 3>
    >>> Bjorklund.from_indices_and_n_steps(indices=[0, 3, 5], n_steps=8)
    <3 2 3>
    """
    @classmethod
    def from_n_steps_n_beats(cls, n_steps, n_beats):
        """
        Generate an Euclidean for given number of steps and number of beats.

        :param n_steps: Number of steps
        :param n_beats: Number of beats
        :return: Generated Bjorklund rhythm object.

        >>> Bjorklund.from_n_steps_n_beats(8, 3)
        <3 2 3>
        """
        instance = bjorklund(n_steps, n_beats)
        return instance

    @classmethod
    def from_steps(cls, steps):
        """
        Create a Bjorklund rhythm object by explicitly providing each step

        :param steps: Number of steps
        :return: Generated Bjorklund rhythm object.

        >>> Bjorklund.from_steps([1, 0, 0, 0, 1, 0, 1, 0, 1])
        <4 2 2 1>
        """
        instance = cls([])
        instance.steps = steps
        return instance

    @classmethod
    def from_indices_and_n_steps(cls, indices, n_steps):
        """
        Create a Bjorklund rhythm object from indices and number of steps.

        :param indices: List of indices of beats.
        :param n_steps: Number of steps.
        :return: Generated Bjorklund rhythm object.

        >>> Bjorklund.from_indices_and_n_steps([1, 3, 6, 7], 8)
        <2 3 1 2> (offset: 1)
        """
        instance = cls([])
        instance.steps = indices_and_n_steps_to_steps(indices, n_steps)
        return instance

    def __init__(self, durations, offset=0):
        """
        Default initialization method for the Bjorklund object.

        :param durations: List of durations of beats.
        :param offset: Offset of the first beat (number of silent beats before the start).
        :return: Generated Bjorklund rhythm object.

        >>> Bjorklund([2, 2, 2, 3])
        <2 2 2 3>
        >>> x = Bjorklund([3, 2, 3], 1)
        >>> print(x)
        <3 2 3> (offset: 1)
        >>> print(x.steps)
        [0, 1, 0, 0, 1, 0, 1, 0]
        """
        self.__durations = []
        self.__steps = []
        self.__indices = []

        self.durations = durations
        self.offset = offset

    @property
    def durations(self):
        """
        List of durations

        :return: list of durations

        >>> x = Bjorklund.from_n_steps_n_beats(9, 4)
        >>> print(x.durations)
        [3, 2, 2, 2]
        """
        return self.__durations

    @durations.setter
    def durations(self, durations):
        self.__durations = durations
        self.__steps = durations_to_steps(durations)
        self.__indices = steps_to_indices(self.steps)

    @property
    def offset(self):
        """
        Offset of the first beat from the beginning.

        :return: Offset

        >>> x = Bjorklund.from_steps([0, 0, 1, 0, 1, 1])
        >>> print(x.offset)
        2
        """
        try:
            return self.steps.index(1)
        except ValueError:
            return None

    @offset.setter
    def offset(self, offset):
        if self.offset is None:
            return
        max_offset = self.steps[::-1].index(1)
        if offset > max_offset:
            print(f"Not enough empty steps at the end!"
                  "setting offset to the maximum allowed valueof {max_offset}")
            offset = max_offset
        current_offset = self.offset
        steps = deque(self.steps)
        steps.rotate(offset - current_offset)
        self.steps = list(steps)

    @property
    def steps(self):
        """
        List of steps

        :return: list of steps

        >>> x = Bjorklund.from_n_steps_n_beats(9, 4)
        >>> print(x.steps)
        [1, 0, 0, 1, 0, 1, 0, 1, 0]
        """
        return self.__steps

    @steps.setter
    def steps(self, steps):
        self.__steps = steps
        self.__durations = steps_to_durations(steps)
        self.__indices = steps_to_indices(steps)

    @property
    def indices(self):
        """
        List of beat indices

        :return: list of indices

        >>> x = Bjorklund.from_n_steps_n_beats(9, 4)
        >>> print(x.indices)
        [0, 3, 5, 7]
        """
        return self.__indices

    @indices.setter
    def indices(self, indices):
        self.__indices = indices
        self.__steps = indices_and_n_steps_to_steps(indices, self.n_steps)
        self.durations = steps_to_durations(self.steps)

    @property
    def n_steps(self):
        """
        Number of steps.

        :return: number of steps

        >>> x = Bjorklund([3, 2, 2])
        >>> print(x.n_steps)
        7
        """
        return len(self.steps)

    @property
    def n_beats(self):
        """
        Number of beats.

        :return: number of beats

        >>> x = Bjorklund([3, 2, 2])
        >>> print(x.n_beats)
        3
        """
        return len(self.durations)

    def rotate_steps(self, n):
        """
        Rotate rhythm stepwise.

        :param n: Number of rotations. Rotate right if n is negative.
        It is the same as the `rotate` method of `collections.deque`

        >>> x = Bjorklund([3, 2, 3], 1)
        >>> print(x)
        <3 2 3> (offset: 1)
        >>> print(x.steps)
        [0, 1, 0, 0, 1, 0, 1, 0]
        >>> x.rotate_steps(-1)
        >>> print(x.steps)
        [1, 0, 0, 1, 0, 1, 0, 0]
        >>> print(x)
        <3 2 3>
        >>> x.rotate_steps(3)
        >>> print(x.steps)
        [1, 0, 0, 1, 0, 0, 1, 0]
        >>> print(x)
        <3 3 2>
        """
        steps = deque(self.steps)
        steps.rotate(n)
        self.steps = list(steps)

    def rotate_durations(self, n):
        """
        Rotate rhythm by durations. This does not effect the `offset` of the rhythm.

        :param n: Number of rotations. Rotate right if n is negative.
        It is the same as the `rotate` method of `collections.deque`

        >>> x = Bjorklund([3, 2, 3], 1)
        >>> print(x)
        <3 2 3> (offset: 1)
        >>> print(x.steps)
        [0, 1, 0, 0, 1, 0, 1, 0]
        >>> x.rotate_durations(-1)
        >>> print(x.steps)
        [0, 1, 0, 1, 0, 0, 1, 0]
        >>> print(x)
        <2 3 3> (offset: 1)
        >>> x.rotate_durations(2)
        >>> print(x.steps)
        [0, 1, 0, 0, 1, 0, 0, 1]
        >>> print(x)
        <3 3 2> (offset: 1)
        >>> y = Bjorklund([3, 2, 5, 4])
        >>> print(y)
        <3 2 5 4>
        >>> y.rotate_durations(1)
        >>> print(y)
        <4 3 2 5>
        """
        durations = deque(self.durations)
        durations.rotate(n)
        offset = self.offset
        self.durations = list(durations)
        self.offset = offset

    def __delta(self, j, i):
        """
        :math:`\delta_j(i)` as defined in Bjorklund (2003).

        Forward distance between pulse i and the jth pulse after i.

        Parameters
        ----------
        j : int
        i : int

        Returns
        -------
        delta : int
        """
        return (self.indices[(i + j) % self.n_beats] - self.indices[i]) % self.n_steps

    def __delta_bar(self, i):
        """
        :math:`\bar{\delta}_j(i)` as defined in Bjorklund (2003).

        Parameters
        ----------
        i : int

        Returns
        -------
        delta_bar : int
        """
        result = 0
        for j in range(1, self.n_beats):
            result += self.__delta(j, i)
        return result / (self.n_beats - 1)

    def uglyness(self, i):
        """
        Uglyness of a beat as defined in Bjorklund (2003).

        Parameters
        ----------
        i : int

        Returns
        -------
        uglyness : float

        Examples
        --------
        >>> x = Bjorklund.from_indices_and_n_steps([1, 2, 3, 5, 7], 8)
        >>> print(x)
        <1 1 2 2 2> (offset: 1)
        >>> print([f"{x.uglyness(i):.2f}" for i in range(x.n_beats)])
        ['3.69', '5.00', '3.69', '2.19', '2.19']
        """
        result = 0
        for j in range(1, self.n_beats):
            result += (self.__delta(j, i) - self.__delta_bar(i)) ** 2
        return result / (self.n_beats - 1)

    def total_uglyness(self):
        """
        Total uglyness of a pattern as defined in Bjorklund (2003).

        Returns
        -------
        total_uglyness : float

        Examples
        --------
        >>> x = Bjorklund.from_indices_and_n_steps([1, 2, 3, 5, 7], 8)
        >>> print(x)
        <1 1 2 2 2> (offset: 1)
        >>> print(f"{x.total_uglyness():.2f}")
        1.60
        >>> y = Bjorklund.from_n_steps_n_beats(8, 4)
        >>> print(y)
        <2 2 2 2>
        >>> print(f"{y.total_uglyness():.2f}")
        0.00
        """
        result = 0
        for j in range(1, self.n_beats // 2 + 1):
            for i in range(0, self.n_beats):
                result += (self.__delta(j, i) - (j * self.n_steps) / self.n_beats) ** 2
        return 2 * result / self.n_beats

    def is_bjorklund(self):
        """
        Is the rhythm an evenly distributed Euclidean rhythm?

        Returns
        -------
        is_bjorklund : bool

        Examples
        --------
        >>> x = Bjorklund([3, 3, 2])
        >>> x.is_bjorklund()
        True
        >>> y = Bjorklund([1, 3, 3])
        >>> y.is_bjorklund()
        False

        Notes
        -----
        Rotations of the same pattern are equivalent.
        """
        bjork = Bjorklund.from_n_steps_n_beats(self.n_steps, self.n_beats)
        return self == bjork

    def __len__(self):
        return self.n_steps

    def __add__(self, other):
        # TODO: Maybe don't
        multiple = lcm(self.n_beats, other.n_steps)
        a = multiple // self.n_beats
        b = multiple // other.n_steps
        return Bjorklund([x + y for x, y in zip(self.durations * a, other.steps * b)])

    def __eq__(self, other):
        my_durations = deque(self.durations)
        other_durations = deque(other.durations)

        for i in range(self.n_beats):
            if other_durations == my_durations:
                return True
            my_durations.rotate()
        return False

    def __repr__(self):
        dur_reps = f"<{' '.join([str(i) for i in self.durations])}>"
        if self.offset == 0:
            return dur_reps
        return f"{dur_reps} (offset: {self.offset})"

    def __str__(self):
        dur_reps = f"<{' '.join([str(i) for i in self.durations])}>"
        if self.offset == 0:
            return dur_reps
        return f"{dur_reps} (offset: {self.offset})"


def steps_to_durations(steps: List[int]) -> List[int]:
    """
    Convert `steps` representation of a Bjorklund into `durations` representation

    >>> steps_to_durations([1, 0, 1, 0])
    [2, 2]

    :param steps: list of steps. 1 where there is a beat 0 where there is silence
    :return: list of durations.
    """
    @reduce_with(init=[])
    def s_to_d(x, y):
        if y == 0:
            return x[:-1] + [x[-1] + 1]
        if y == 1:
            return x + [y]
        raise ValueError("Steps can contain only beats (1) or rests (0)!")

    if not steps:
        return []

    index = steps.index(1)
    return s_to_d(steps[index:] + steps[:index])


def durations_to_steps(durations: List[int]) -> List[int]:
    """
    Convert `durations` representation of a Bjorklund into `steps` representation

    >>> durations_to_steps([3, 2, 1])
    [1, 0, 0, 1, 0, 1]

    :param durations: list of durations
    :return: list of steps. 1 where there is a beat 0 where there is silence
    """
    if any([x <= 0 for x in durations]):
        raise ValueError("Negative or zero length durations do not make sense in this context!")

    return sum([[1] + [0] * (x - 1) for x in durations], [])


def steps_to_indices(steps: List[int]) -> List[int]:
    """
    Convert `steps` representation of a Bjorklund into `indices` representation

    >>> steps_to_indices([0, 1, 1, 0, 0, 1])
    [1, 2, 5]

    :param steps: list of steps. 1 where there is a beat 0 where there is silence
    :return: list of indices of beats (indices of 1s in steps).
    """
    return [index for index, value in enumerate(steps) if value == 1]


def indices_and_n_steps_to_steps(indices: List[int], n_steps: int) -> List[int]:
    """
    Convert `indices` representation of a Bjorklund into `steps` representation

    >>> indices_and_n_steps_to_steps([0, 2, 3], 8)
    [1, 0, 1, 1, 0, 0, 0, 0]

    :param indices: list of indices of beats (indices of 1s in steps).
    :param n_steps: number of steps
    :return: list of steps. 1 where there is a beat 0 where there is silence
    """
    steps = [0] * n_steps
    for index in indices:
        steps[index] = 1
    return steps


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
        raise ValueError("Negative or zero number of steps or beats do not make sense!")

    quotient, remainder = divmod(n_steps, n_beats)
    if remainder == 0:
        return Bjorklund([quotient] * n_beats)

    return Bjorklund([quotient] * n_beats) + bjorklund(n_beats, remainder)
