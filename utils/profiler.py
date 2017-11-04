from functools import wraps
import time


def get_running_time(func, passes=1):
    @wraps(func)
    def _warp(*args, **kwargs):
        begin = time.time()
        [func(*args, **kwargs) for _ in range(passes)]
        end = time.time()
        return end - begin
    return _warp


if __name__ == '__main__':
    def f(n): time.sleep(n); print(n)
    print(type(get_running_time(f)))
    assert abs(get_running_time(f)(1) - 1) < 0.1
    assert abs(get_running_time(f)(2) - 2) < 0.1
    assert abs(get_running_time(f, passes=2)(2) - 4) < 0.1
    print('test done!')



