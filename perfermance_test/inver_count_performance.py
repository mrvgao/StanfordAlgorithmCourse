from InverseCount import inverse_count
from utils.profiler import get_running_time
import random


def generate_random_sequence(length):
    L = list(range(length))
    random.shuffle(L)
    return L


if __name__ == '__main__':
    assert isinstance(generate_random_sequence(10), list)
    assert len(generate_random_sequence(10)) == 10

    print('test done!')

