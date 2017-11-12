"""
Experiment of QuickSort of Week3 for Course1. 

Counting the Comparision time based on different pivot chosen methods. 

We could get the comparision time for length m just (m - 1) + total recursive comparision 
time. 

Author: Minchiuan
Date: 2017-Nov-12
"""
import random


def swap(array, i, j):
    array[i], array[j] = array[j], array[i]
    return array


def quick_sort(array, pivot_policy='random'):
    if len(array) <= 1:
        return array, 0

    pivot_index = choose_pivot(array, pivot_policy)
    pivot = array[pivot_index]

    array = swap(array, pivot_index, 0)

    i, j = 0, 0

    while j < len(array) - 1:
        j += 1  # j advance one step
        if array[j] <= pivot:
            i += 1
            swap(array, i, j)

    swap(array, 0, i)

    left_partition, comparision_time_left = quick_sort(array[:i], pivot_policy)
    right_partition, comparision_time_right = quick_sort(array[i+1:], pivot_policy)

    return left_partition + [pivot] + right_partition, comparision_time_left + comparision_time_right + len(array) - 1


def choose_pivot(array, policy='random'):
    pivot_chosen = {
        'random': random.randint(0, len(array) - 1),
        'first': 0,
        'last': -1,
        'median': median_of_three(array)
    }

    if policy in pivot_chosen: return pivot_chosen[policy]
    else: raise TypeError('pivot choose policy not supported')


def median_of_three(array):
    first_index = 0
    last_index = -1
    media_index = (len(array) + 1) // 2 - 1
    # 0, 1, 2, 3, 4    (5 + 1) // 2 - 1 == 2, median is 2
    # 0, 1, 2, 3   (4 + 1)//2 - 1 == 1, median is 1

    def is_media(a, b, c): return (array[b] - array[a]) * (array[c] - array[a]) < 0

    if is_media(first_index, last_index, media_index): return first_index
    elif is_media(last_index, first_index, media_index): return last_index
    else: return media_index


def sort_file_data(file, policy):
    numbers = [int(n) for n in open(file)]
    numbers, comparision_time = quick_sort(numbers, policy)
    return numbers, comparision_time

if __name__ == '__main__':
    t_array = [1, 2]
    assert swap(t_array[:], 0, 1) == [2, 1]
    assert swap(t_array[:], 0, 0) == [1, 2]

    assert choose_pivot(t_array, 'first') == 0
    assert choose_pivot(t_array, 'last') == -1
    random_index = choose_pivot(t_array, 'random')
    assert random_index in [0, 1], random_index

    L = [1, 2]

    assert quick_sort(L)[0] == [1, 2]

    L = [2, 1]
    assert quick_sort(L)[0] == [1, 2]

    L = [2, 1, 3, 4]

    assert quick_sort(L)[0] == [1, 2, 3, 4]

    L = list(range(100))
    random.shuffle(L)

    assert quick_sort(L, pivot_policy='random')[0] == sorted(L)

    L = list(range(100))
    random.shuffle(L)
    assert quick_sort(L, pivot_policy='last')[0] == sorted(L)

    L = list(range(100))
    random.shuffle(L)
    assert quick_sort(L, pivot_policy='first')[0] == sorted(L)

    L = list(range(100))
    random.shuffle(L)
    assert quick_sort(L, pivot_policy='median')[0] == sorted(L)

    print('test done!')

    print('running' + '#'*18)

    print(sort_file_data('data/QuickSort.txt', policy='random')[1])
    print(sort_file_data('data/QuickSort.txt', policy='first')[1])
    print(sort_file_data('data/QuickSort.txt', policy='last')[1])
    print(sort_file_data('data/QuickSort.txt', policy='median')[1])


