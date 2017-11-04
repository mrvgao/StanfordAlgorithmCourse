"""
in naive approach, the running time is |shorter| * |longer|, if we denote the 
longer's length is k * shorter's length, and consuming time is k * shorter * shorter. 
therefore, the time is O(n^2)

let's do a test.
"""
from number_multiplication import multiply
import random
from utils.profiler import get_running_time



def generate_random_number_by_length(length):
    assert length > 0
    return str(str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(length-1)]))


def get_running_time_by_lengthes(lengthes, passes=1):
    times = []
    for length in lengthes:
        print('length: {}'.format(length))
        g = generate_random_number_by_length
        t = get_running_time(multiply, passes=passes)(g(length), g(length))
        times.append(t)
    return times


def get_running_time_relation(lengthes):
    times = get_running_time_by_lengthes(lengthes, passes=1000)
    print('running times: {}'.format(times))
    print('time % n^2 == {}'.format([t / (l ** 2) for t, l in zip(times, lengthes)]))

if __name__ == '__main__':
    assert len(str(generate_random_number_by_length(1))) == 1
    assert len(str(generate_random_number_by_length(10))) == 10
    assert len(str(generate_random_number_by_length(100))) == 100

    test_lengthes = [10, 20, 50, 100, 500, 1000, 2000]
    times = get_running_time_by_lengthes(test_lengthes)
    assert isinstance(times, list)
    assert len(times) == len(test_lengthes)
    print('test done!')

    get_running_time_relation(test_lengthes)

