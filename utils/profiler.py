from functools import wraps
import time


def get_running_time(running_time=1000):
    def decorate(func):
        @wraps(func)
        def __wrap(*args, **kwargs):
            start = time.time()
            for i in range(running_time): value = func(*args, **kwargs)
            print('used time: {}'.format(time.time() - start))
            return value
        return __wrap
    return decorate


