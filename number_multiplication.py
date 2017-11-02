""" Multiply two numbers. 

Input:  11
        11

Output: 11 * 11 = 121

Input:  111111....111
        222222....222

Output: the two number's result. 
"""

"""Analysis 

the inputs are 2 number sequence consist of n1, n2, .. nN ; m1, m2, m3, ,,,, mM

the result is shorter sequence is Sm, longer is Sn, Sm[-1] * Sn[-1]. 

There are |Sm| inter results records for each pass. 

inventory: 

    1. input_1, input_2
    2. inter results recorders. r1, r2, ... rN (n is the shorter length of two inputs).
    3. final result. 
    
function: 
    1. record_pass -> result_on_one_pass
    2. merge_inter_results
"""


def record_pass(number, number_sequence, index):
    """"
    :param number: if 111 * 345, in the first pass, 5 is the number, second pass, 4 is the number.
    :param number_sequence: 111 * 345, 111 is the number sequence.
    :param index: if 111 * 345, when 1st pass, index is 0, second pass, index is 1, etc. 
    :return: the multiply result of this pass. 111 * 345, first pass is 111 * 5, and the second pass is 111 * 4 = 444 
     and concate a 0. 4440
    """
    return int(str(int(number) * int(number_sequence)) + "0"*index)


def merge_inter_results(passes_results):
    return sum(passes_results)


def multiplication(number1, number2):
    shorter, longer = (number1, number2) if len(str(number1)) < len(str(number2)) else (number2, number1)
    return merge_inter_results([record_pass(num, longer, index) for index, num in enumerate(str(shorter)[::-1])])

assert record_pass(0, '123', 0) == 0
assert record_pass(1, '123', 0) == 123
assert record_pass(1, '123', 2) == 12300
assert merge_inter_results([0, 120, 12300]) == 0 + 120 + 12300
assert multiplication(1, 1) == 1 * 1
assert multiplication(11, 11) == 11 * 11
assert multiplication(123123, 11) == 123123 * 11
assert multiplication('123123', '11') == 123123 * 11

print('test done!')


