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
    bits = []
    pre = 0
    for n in str(number_sequence)[::-1]:
        r, pre = one_bit_multiply(int(number), int(n), pre)
        bits.append(r)
    bits.append(pre)
    bits.reverse() # 123 * 3 ==> 9, 6, 3 ==> 3, 6, 9

    return int(''.join(map(str, bits))+ "0"*index)


def one_bit_multiply(a, b, pre=0):
    assert len(str(a)) == len(str(b)) == 1
    assert 0 <= int(pre) <= 9
    result = int(a) * int(b) + pre
    return result % 10, result // 10


def merge_inter_results(passes_results):
    return sum(passes_results)


def multiply(number1, number2):
    shorter, longer = (number1, number2) if len(str(number1)) < len(str(number2)) else (number2, number1)
    return merge_inter_results([record_pass(num, longer, index) for index, num in enumerate(str(shorter)[::-1])])


def tenth_power(power):
    return '0' * power


def multiply_tenth_power(number, power):
    return int(str(number) + tenth_power(power))


def kra_multiply(number1, number2) -> int:
    number1, number2 = str(number1), str(number2)

    if len(number1) == 1 and len(number2) == 1:
        return int(number1) * int(number2)
    else:
        # number1 => ab
        # number2 => cd
        width = len(number1) if len(number1) > len(number2) else len(number2)
        a, b = split_number_to_two_parts(number1, width=width)
        c, d = split_number_to_two_parts(number2, width=width)

        ac = kra_multiply(a, c)
        bd = kra_multiply(b, d)
        a_plus_b = int(a) + int(b)
        c_plus_d = int(c) + int(d)

        a_plus_b_by_c_plus_d = kra_multiply(a_plus_b, c_plus_d)

        ad_plus_bc = a_plus_b_by_c_plus_d - ac - bd

        result = multiply_tenth_power(ac, power=len(b) + len(d)) + multiply_tenth_power(ad_plus_bc, power=len(b)) + bd

        return result


def split_number_to_two_parts(number, width=None):
    width = width or len(number)
    number = str(number)
    if len(number) < width: number = '0' * (width - len(number)) + str(number)
    assert len(number) > 0
    mid = len(number) // 2
    return number[:mid], number[mid:]


def build_by_two_parts(part1, part2):
    # 123, 45 => 12300, 45, which could build 12345 by addition op.
    return str(part1) + len(part2) * '0', part2


if __name__ == '__main__':
    assert one_bit_multiply(1, 1) == (1, 0)
    assert one_bit_multiply(1, 1, 2) == (3, 0)
    assert one_bit_multiply(8, 9, 2) == (4, 7)
    assert one_bit_multiply('1', '1') == (1, 0)

    assert record_pass(0, '123', 0) == 0
    assert record_pass(1, '123', 0) == 123
    assert record_pass(1, '123', 2) == 12300
    assert merge_inter_results([0, 120, 12300]) == 0 + 120 + 12300
    assert multiply(1, 1) == 1 * 1
    assert multiply(11, 11) == 11 * 11
    assert multiply(123123, 11) == 123123 * 11
    assert multiply('123123', '11') == 123123 * 11

    assert split_number_to_two_parts('123') == ('1', '23')
    assert split_number_to_two_parts('1') == ('', '1')
    assert split_number_to_two_parts('1234') == ('12', '34')
    assert split_number_to_two_parts('12345678') == ('1234', '5678')

    assert split_number_to_two_parts('1', width=2) == ('0', '1')
    assert split_number_to_two_parts('11', width=3) == ('0', '11')
    assert split_number_to_two_parts('111', width=6) == ('000', '111')

    assert build_by_two_parts('123', '45') == ('12300', '45')
    assert build_by_two_parts('', '1') == ('0', '1')

    assert tenth_power(1) == '0'
    assert tenth_power(2) == '00'

    assert multiply_tenth_power(1, 1) == 10
    assert multiply_tenth_power(1, 0) == 1
    assert multiply_tenth_power(1, 10) == 10000000000

    assert kra_multiply('1', '2') == 2
    assert kra_multiply('11', '11') == 121
    r = kra_multiply('121', '121')
    assert r == 121 * 121
    assert kra_multiply('1111', '1111') == 1111 * 1111
    assert kra_multiply('123456789', '234567890') == 123456789 * 234567890

    print('test done!')

    print(multiply('3141592653589793238462643383279502884197169399375105820974944592',
                   '2718281828459045235360287471352662497757247093699959574966967627'))

    print(kra_multiply('3141592653589793238462643383279502884197169399375105820974944592',
                       '2718281828459045235360287471352662497757247093699959574966967627'))


