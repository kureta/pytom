from collections import deque

from pytom.libs.utils import reduce_with, lcm


# TODO: Write docstrings
class Bjorklund:
    @classmethod
    def from_n_steps_n_beats(cls, n_steps, n_beats):
        """
        Generate an Euclidean with given number of steps and number of beats.

        Parameters
        ----------
        n_steps : int
            Number of steps
        n_beats : int
            Number of beats

        Returns
        -------
        rhythm : Bjorklund
            Generated Bjorklund rhythm object.

        Examples
        --------
        >>> Bjorklund.from_n_steps_n_beats(8, 3)
        <3 2 3>

        """
        instance = bjorklund(n_steps, n_beats)
        return instance

    @classmethod
    def from_steps(cls, steps):
        """
        Create a Bjorklund rhythm object by explicitly providing each step

        Parameters
        ----------
        steps : list
            List of steps. `1` for a beat, `0` for a rest.
            ex: [1, 0, 0, 0, 1, 0, 1, 0, 1]

        Returns
        -------
        rhythm : Bjorklund
            Generated Bjorklund rhythm object.

        Examples
        --------
        >>> Bjorklund.from_steps([1, 0, 0, 0, 1, 0, 1, 0, 1])
        <4 2 2 1>

        """
        instance = cls([])
        instance.steps = steps
        return instance

    @classmethod
    def from_indices_and_n_steps(cls, indices, n_steps):
        """
        Create a Bjorklund rhythm object by explicitly providing each step

        Parameters
        ----------
        indices : list
            List of indices of beats.
            ex: [1, 3, 6, 7]
        n_steps : int
            Number of total steps.

        Returns
        -------
        rhythm : Bjorklund
            Generated Bjorklund rhythm object.

        Examples
        --------
        >>> Bjorklund.from_indices_and_n_steps([1, 3, 6, 7], 8)
        <2 3 1 2> (offset: 1)

        """
        instance = cls([])
        instance.steps = indices_and_n_steps_to_steps(indices, n_steps)
        return instance

    def __init__(self, durations, offset=0):
        """
        Default initialization method for the Bjorklund object.

        Parameters
        ----------
        durations : list
            List of durations of beats.
            ex: [2, 2, 2, 3]
        offset : int
            Offset of the first beat (number of silent beats before the start).

        Returns
        -------
        rhythm : Bjorklund
            Generated Bjorklund rhythm object.

        Examples
        --------
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

    def rotate_steps(self, n):
        """
        Rotate rhythm stepwise.

        Parameters
        ----------
        n : int
            Number of rotations. Rotate right if n is negative. It is the same
            as the `rotate` method of `collections.deque`

        Examples
        --------
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

        Parameters
        ----------
        n : int
            Number of rotations. Rotate right if n is negative. It is the same
            as the `rotate` method of `collections.deque`

        Examples
        --------
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

    @property
    def durations(self):
        """
        List of durations

        Returns
        -------
        durations : list

        Examples
        --------
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

        Returns
        -------
        offset : int

        Examples
        --------
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
            # print(f"Not enough empty steps at the end!\nSetting offset to the maximum allowed valueof {max_offset}.")
            offset = max_offset
        current_offset = self.offset
        steps = deque(self.steps)
        steps.rotate(offset - current_offset)
        self.steps = list(steps)

    @property
    def steps(self):
        """
        List of steps

        Returns
        -------
        steps : list

        Examples
        --------
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

        Returns
        -------
        indices : list

        Examples
        --------
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

        Returns
        -------
        n_steps : int

        Examples
        --------
        >>> x = Bjorklund([3, 2, 2])
        >>> print(x.n_steps)
        7
        """
        return len(self.steps)

    @property
    def n_beats(self):
        """
        Number of beats.

        Returns
        -------
        n_beats : int

        Examples
        --------
        >>> x = Bjorklund([3, 2, 2])
        >>> print(x.n_beats)
        3
        """
        return len(self.durations)

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


def steps_to_durations(steps):
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


def durations_to_steps(durations):
    if any([x <= 0 for x in durations]):
        raise ValueError("Negative or zero length durations do not make sense in this context!")

    return sum([[1] + [0] * (x - 1) for x in durations], [])


def steps_to_indices(steps):
    return [index for index, value in enumerate(steps) if value == 1]


def indices_and_n_steps_to_steps(indices, n_steps):
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
