"""
Count the inverse pairs in an array. Such as: 4, 2, 1, 3 

we get (4, 2), (4, 1), (4, 3), (2, 1) four inverse pairs.
"""


def inverse_count(array):
    if len(array) == 1: return array, 0
    else:
        sorted_left, inverse_left = inverse_count(array[:len(array)//2])
        sorted_right, inverse_right = inverse_count(array[len(array)//2:])
        merged_sort, inverse_split = merge(sorted_left, sorted_right)
        return merged_sort, inverse_left + inverse_right + inverse_split


def merge(array_1, array_2):
    """
     Merges two sorted arrays into one sorted array and return the inverse number 
     of array1 and array1
    :param array_1: sorted_array
    :param array_2: sorted_array
    :return: sorted_array, inverse_number concated array_1, array_2
    """
    i, j = 0, 0,
    sorted_result = []
    inverse_num = 0

    while i < len(array_1) or j < len(array_2):
        if i >= len(array_1): sorted_result.append(array_2[j]); j += 1; continue
        if j >= len(array_2): sorted_result.append(array_1[i]); i += 1; continue

        if array_1[i] <= array_2[j]: sorted_result.append(array_1[i]); i += 1
        else: sorted_result.append(array_2[j]); inverse_num += (len(array_1) - i); j += 1

    return sorted_result, inverse_num


if __name__ == '__main__':
    assert merge([1, 2], [3, 4]) == ([1, 2, 3, 4], 0)
    assert merge([3, 4], [1, 2]) == ([1, 2, 3, 4], 4)
    assert merge([1], [2]) == ([1, 2], 0)
    assert merge([3], [2]) == ([2, 3], 1)
    assert merge([1, 2, 3], [2]) == ([1, 2, 2, 3], 1)

    assert inverse_count([1, 2, 3, 4])[1] == 0
    assert inverse_count([2, 3, 4, 1])[1] == 3
    assert inverse_count([4, 3, 2, 1])[1] == 6
    assert inverse_count([1, 4, 5, 3, 2])[1] == 5

    print('test done!')
