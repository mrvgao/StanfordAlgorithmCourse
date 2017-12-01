from utils.utils import replace_element_quickly
from utils.profiler import get_running_time
import random
import copy


running_time = 10000


@get_running_time(running_time=running_time)
def original_replace_way(L, old_e, new_e):
    new_L = []
    for i in L:
        if i == old_e: new_L.append(new_e)
        else: new_L.append(i)
    return new_L


@get_running_time(running_time=running_time)
def replace_by_list_comprehension(L, old_e, new_e):
    return [new_e if e == old_e else e for e in L]


@get_running_time(running_time=running_time)
def replace_by_map(L, old_e, new_e):
    return list(map(lambda x: new_e if x == old_e else x, L))


replace_element_quickly = get_running_time(running_time=running_time)(replace_element_quickly)

LIST = [random.randrange(10) for _ in range(100)]
LIST = original_replace_way(LIST, 2, 3)
LIST = replace_by_list_comprehension(LIST, 2, 3)
LIST = replace_by_map(LIST, 2, 3)
assert 2 not in LIST

LIST = [random.randrange(10) for _ in range(100)]

assert 2 in LIST
list1 = replace_element_quickly(LIST[:], 2, 3)
list2 = original_replace_way(LIST, 2, 3)

assert 2 not in list1
assert len(list1) == 100, len(list1)
assert sorted(list1) == sorted(list2)

L = [1, 2, 2, 31, 42, 12, 13, 2, 1, 2, 32, 1]
print(replace_element_quickly(L[:], 2, 0))
print(L)
