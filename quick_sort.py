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
        return array

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

    left_partition = quick_sort(array[:i], pivot_policy)
    right_partition = quick_sort(array[i+1:], pivot_policy)

    return left_partition + [pivot] + right_partition


def choose_pivot(array, policy='random'):
    pivot_chosen = {
        'random': random.choices(range(len(array)))[0],
        'first': 0,
        'last': 1
    }

    if policy in pivot_chosen: return pivot_chosen[policy]
    else: raise TypeError('pivot choose policy not supported')


if __name__ == '__main__':
    t_array = [1, 2]
    assert swap(t_array[:], 0, 1) == [2, 1]
    assert swap(t_array[:], 0, 0) == [1, 2]

    assert choose_pivot(t_array, 'first') == 0
    assert choose_pivot(t_array, 'last') == 1
    random_index = choose_pivot(t_array, 'random')
    assert random_index in [0, 1], random_index

    L = [1, 2]

    assert quick_sort(L) == [1, 2]

    L = [2, 1]
    assert quick_sort(L) == [1, 2]

    L = [2, 1, 3, 4]

    assert quick_sort(L) == [1, 2, 3, 4]

    L = list(range(100))
    random.shuffle(L)

    assert quick_sort(L) == sorted(L)

    print('test done!')


