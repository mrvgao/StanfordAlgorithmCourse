def __cmp__(x):
    if '__iter__' in dir(x):
        return [len(x), x[0]]
    else:
        return [1, x]


def sorted_list_with_tuple(L, reverse=False):
    return sorted(L, key=__cmp__, reverse=reverse)
