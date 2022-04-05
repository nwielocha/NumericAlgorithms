import scipy.interpolate as ip
import numpy as np
from numpy.polynomial.polynomial import Polynomial
import math


def sub_lists (l):
    lists = []
    for i in range(len(l) + 1):
        for j in range(i):
            lists.append(l[j: i])
    return lists


def return_polynomials(sub_arrays, data):
    result = []
    for array in sub_arrays:
        result.append([ip.lagrange(array, [data[key] for key in array]),array])
    return result


if __name__ == '__main__':
    constant = math.log(22, 2)
    x_y = {2**i: i for i in range(0, 12)}
    keys = [key for key, value in x_y.items()]
    values = [value for key, value in x_y.items()]
    subsequences_x = sub_lists(keys)

    array_polynomial = return_polynomials(subsequences_x, x_y)
    polynomials = [i[0] for i in array_polynomial]

    best_result = min(array_polynomial,key=lambda x: np.abs(constant - x[0](22)))
    best_subsequence = best_result[1]
    best_subsequence_polynomial = best_result[0]
    print(f"Najlepiej estymująca grupa węzłów : \n\n{best_subsequence}\n\nWyliczony dla niej wielomian:\n\n{best_subsequence_polynomial}")
