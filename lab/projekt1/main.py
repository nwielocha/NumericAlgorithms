import scipy.interpolate as ip
import numpy as np
from numpy.polynomial.polynomial import Polynomial
import math
from itertools import compress, product, combinations
from sympy import Symbol


def sub_lists(a):
    if len(a) == 0:
        return [[]]
    cs = []
    for c in sub_lists(a[1:]):
        cs += [c, c + [a[0]]]
    return cs


def create_lx(tabelka, i):
    n = len(tabelka)
    wielomian = 1
    x = Symbol('x')
    for k in range(0, n):
        if i != k:
            wielomian = wielomian * (
                        (x - tabelka[k][0]) / (tabelka[i][0] - tabelka[k][0]))
    return wielomian


def create_polynomial(tabelka):
    result = 0
    for i in range(0, len(tabelka)):
        result += tabelka[i][1] * create_lx(tabelka, i)
    return result


# def return_polynomials(sub_arrays, data):
#     result = []
#     for array in sub_arrays:
#         result.append([ip.lagrange(array, [data[key] for key in array]),array])
#     return result


if __name__ == '__main__':
    constant = math.log(22, 2)

    tabelka = [(2 ** i, i) for i in range(0, 12)]
    all_index_subsequences = sub_lists([x for x in range(0, 12)])
    polynomial = create_polynomial(tabelka[3:7])
    print(polynomial)
    print(polynomial.subs(Symbol('x'), 22))

    # keys = [key for key, value in x_y.items()]
    # values = [value for key, value in x_y.items()]
    # subsequences_x = sub_lists(keys)
    # array_polynomial = return_polynomials(subsequences_x, x_y)
    # polynomials = [i[0] for i in array_polynomial]

    # best_result = min(array_polynomial,key=lambda x: np.abs(constant - x[0](22)))
    # best_subsequence = best_result[1]
    # best_subsequence_polynomial = best_result[0]
    # print(f"Najlepiej estymująca grupa węzłów : \n\n{best_subsequence}\n\nWyliczony dla niej wielomian:\n\n{best_subsequence_polynomial}\n\n"
    #       f"Log22 = {constant} \nF(22) dla obliczonego wielomianu:{best_subsequence_polynomial(22)}")
