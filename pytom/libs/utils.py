from functools import reduce, wraps


def reduce_with(init):
    def reduce_with_(f_):
        @wraps(f_)
        def wrapper(xs):
            return reduce(f_, xs, init)

        return wrapper

    return reduce_with_
