from functools import reduce, wraps


def reduce_with(init):
    def reduce_with_(f_):
        @wraps(f_)
        def wrapper(xs):
            if init is not None:
                return reduce(f_, xs, init)
            else:
                return reduce(f_, xs)

        return wrapper

    return reduce_with_


def flip(func):
    @wraps(func)
    def newfunc(x, y):
        return func(y, x)

    return newfunc


def foldr(func, xs, init=None):
    if init is not None:
        return reduce(flip(func), reversed(xs), init)
    else:
        return reduce(flip(func), reversed(xs))
