"""
in naive approach, the running time is |shorter| * |longer|, if we denote the 
longer's length is k * shorter's length, and consuming time is k * shorter * shorter. 
therefore, the time is O(n^2)

let's do a test.
"""
import random
from number_multiplication import multiply
from utils.profiler import get_running_time
from number_multiplication import kar_multiply


def generate_random_number_by_length(length):
    assert length > 0
    return str(str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(length-1)]))


def get_running_time_by_lengthes(func, lengthes, passes=1):
    times = []
    for length in lengthes:
        print('length: {}'.format(length))
        g = generate_random_number_by_length
        t = get_running_time(func, passes=passes)(g(length), g(length))
        times.append(t)
    return times


def get_running_time_relation(func, lengthes, relation_func):
    times = get_running_time_by_lengthes(func, lengthes, passes=1000)
    print('running times: {}'.format(times))
    print('time % n^2 == {}'.format([relation_func(t, n) for t, n in zip(times, lengthes)]))

if __name__ == '__main__':
    assert len(str(generate_random_number_by_length(1))) == 1
    assert len(str(generate_random_number_by_length(10))) == 10
    assert len(str(generate_random_number_by_length(100))) == 100

    test_lengths = [10, 20, 50, 100, 500, 1000, 2000]
    times = get_running_time_by_lengthes(multiply, test_lengths, passes=1)
    assert isinstance(times, list)
    assert len(times) == len(test_lengths)
    print('test done!')

    time_for_naive = get_running_time_by_lengthes(multiply, test_lengths, passes=1000)
    time_for_kar = get_running_time_by_lengthes(kar_multiply, test_lengths, passes=100)
    print(time_for_naive)
    print(time_for_kar)
    # get_running_time_relation(multiply, test_lengthes)
    # get_running_time_relation(kar_multiply, test_lengthes)

