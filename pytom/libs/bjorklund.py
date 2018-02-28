from pytom.libs.utils import reduce_with, foldr


def add_beats(xs, ys):
    return [x + y for x, y in zip(xs, durations_to_pulses(ys))]


def bjorklund_non_recursive(steps, pulses):
    """ Calculates optimal distribution of a number of pulses over a number of discrete steps.
    :param steps: number of steps (ex: divisions of a measure)
    :param pulses: number of pulses (ex: hits of a drum)
    :return: duration of each pulse (ex: bjorklund(8,2) => [3, 3, 2]

    Non-recursive version of the Bjorklund algorithm.

    >>> bjorklund(8, 4)
    [2, 2, 2, 2]

    >>> bjorklund(12, 5)
    [3, 2, 2, 3, 2]
    """
    if pulses <= 0 or steps <= 0 or pulses > steps:
        raise ValueError

    beats = []
    remainder = 1
    while remainder > 0:
        quotient, remainder = divmod(steps, pulses)
        beats.append([quotient] * pulses)
        steps, pulses = pulses, remainder

    result = foldr(add_beats, beats)
    return result


def bjorklund(steps, pulses):
    """ Calculates optimal distribution of a number of pulses over a number of discrete steps.
    :param steps: number of steps (ex: divisions of a measure)
    :param pulses: number of pulses (ex: hits of a drum)
    :return: duration of each pulse (ex: bjorklund(8,2) => [3, 3, 2]

    Divide steps into pulses.
    If the remainder is 0, pulses divide the steps equally and result of the division is the duration of each pulse.

    >>> bjorklund(8, 4)
    [2, 2, 2, 2]

    Otherwise recursively get the optimal distribution of the remainder over the pulses.
    Convert that into a binary representation. ex: [3, 2] => [1, 0, 0, 1, 0]
    Add the evenly distributed remainder to the equal division of steps.
    ex: bjorklund(12, 5) => [2, 2, 2, 2, 2] + [1, 0, 0, 1, 0] = [3, 2, 2, 3, 2]

    >>> bjorklund(12, 5)
    [3, 2, 2, 3, 2]
    """
    if pulses <= 0 or steps <= 0 or pulses > steps:
        raise ValueError
    quotient, remainder = divmod(steps, pulses)

    if remainder == 0:
        return [quotient] * pulses

    return add_beats([quotient] * pulses, bjorklund(pulses, remainder))


def durations_to_pulses(xs):
    """ Convert a list of durations into a list of pulses.
    :param xs: list of durations
    :return: list of pulses

    >>> durations_to_pulses([3, 3, 2])
    [1, 0, 0, 1, 0, 0, 1, 0]
    """
    if any([x <= 0 for x in xs]):
        raise ValueError
    return sum([[1] + [0] * (x - 1) for x in xs], [])


@reduce_with(init=[])
def pulses_to_durations(x, y):
    """ Convert a list of binary pulses into a list of durations.
        :param xs: list of pulses
        :return: list of durations

        >>> pulses_to_durations([1, 0, 0, 1, 0, 0, 1, 0])
        [3, 3, 2]
        """
    if not x:
        if y != 1:
            raise ValueError
        return [y]
    if y == 0:
        return x[:-1] + [x[-1] + 1]
    if y == 1:
        return x + [y]

    raise ValueError
