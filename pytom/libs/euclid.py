from typing import List, Union
from math import gcd


def steps_from_beat_durations(durations: List[int]) -> List[int]:
    if any(x <= 0 for x in durations):
        raise ValueError("Negative or zero length durations do not make sense!")

    return sum([[1] + [0] * (x - 1) for x in durations], [])


def indices_from_steps(steps: List[int]) -> List[int]:
    return [index for index, value in enumerate(steps) if value == 1]


def distribute_remainder(duration: int, remainder: Union[int, List[int]]) -> List[int]:
    if isinstance(remainder, int):
        remainder = [remainder]
    remainder_steps = steps_from_beat_durations(remainder)

    durations = [duration] * len(remainder_steps)

    return [x + y for x, y in zip(durations, remainder_steps)]


def euclid(n_steps: int, n_beats: int) -> List[int]:
    if n_beats <= 0 or n_steps <= 0:
        raise ValueError("Negative or zero number of steps or beats do not make sense!")
    if n_beats > n_steps:
        raise ValueError("Number of beats cannot be more than the number of steps!")

    quotient, remainder = divmod(n_steps, n_beats)
    if remainder == 0:
        return [quotient] * n_beats

    return distribute_remainder(quotient, euclid(n_beats, remainder))


class Euclid:
    def __init__(self, n_steps: int, n_beats: int):
        n_gcd = gcd(n_steps, n_beats)

        self.n_steps = n_steps // n_gcd
        self.n_beats = n_beats // n_gcd
        self.beat_durations = euclid(self.n_steps, self.n_beats)
        self.steps = steps_from_beat_durations(self.beat_durations)
        self.indices = indices_from_steps(self.steps)

    def __delta(self, j: int, i: int) -> int:
        return (self.indices[(i + j) % self.n_beats] - self.indices[i]) % self.n_steps

    def __delta_bar(self, i) -> float:
        result = 0
        for j in range(1, self.n_beats):
            result += self.__delta(j, i)
        return result / (self.n_beats - 1)

    def uglyness(self, i: int) -> float:
        result = 0
        for j in range(1, self.n_beats):
            result += (self.__delta(j, i) - self.__delta_bar(i)) ** 2
        return result / (self.n_beats - 1)

    def total_uglyness(self) -> float:
        result = 0
        for j in range(1, self.n_beats // 2 + 1):
            for i in range(0, self.n_beats):
                result += (self.__delta(j, i) - (j * self.n_steps) / self.n_beats) ** 2
        return 2 * result / self.n_beats
