from collections import Counter
from functools import reduce
import operator as op


def __cmp__(x):
    if '__iter__' in dir(x):
        return [len(x), x[0]]
    else:
        return [1, x]


def sorted_list_with_tuple(L, reverse=False):
    return sorted(L, key=__cmp__, reverse=reverse)


def __replace_element_quickly(L, element, new_element):
    if element in L:
        L[L.index(element)] = new_element
        return __replace_element_quickly(L, element, new_element)
    return L


def replace_element_quickly(L, element, new_element):
    return __replace_element_quickly(L, element, new_element)
