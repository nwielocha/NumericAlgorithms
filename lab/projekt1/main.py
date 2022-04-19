import numpy as np
import math
from itertools import compress, product, combinations
from sympy import *


def sub_lists(a):
    if len(a) == 0:
        return [[]]
    cs = []
    for c in sub_lists(a[1:]):
        cs += [c, c + [a[0]]]
    return cs

class Estimation:

    def __init__(self, nodes,  polynomial, input_value):
        """
        Class which represents single composition of nodes, polynomial based on them and
        value calculated with substituting x with some arbitrary number
        :param nodes: List of nodes in a x - fx table
        :param polynomial: Polynomial interpolated with given nodes
        :param input_value: Value gained by using arbitrary number in polynomial
        """
        self.nodes = nodes
        self.polynomial = polynomial
        if input_value:
            self.estimated_value = Float(polynomial.subs(Symbol('x'),input_value),6)
        else:
            self.estimated_value = None

    def calculate_value(self,input_value):
        return Float(self.polynomial.subs(Symbol('x'),input_value),6)


class Lagrange:

    def __init__(self,table: dict):
        """
        Class made to provide data for GUI of application which implements LaGrange interpolation algorithm
        :param table: x - fx table  in dictionary form where keys are nodes and values are corresponding f(node) values
        """
        self.table = table
        self.subtables = sub_lists(list(table.keys()))

    def create_lx(self,nodes: list, i):
        """
        Creates lx coefficient used in lagrange formula
        :param nodes: list of nodes used to calculate lx
        :param i: number of iteration from parent-function create_polynomial
        :return: returns calculated polynomial in form of sympy object
        """
        lx_coeff = 1
        x = Symbol('x')
        for k in range(0, len(nodes)):
            if i != k:
                lx_coeff = lx_coeff * ((x - nodes[k]) / (nodes[i] - nodes[k]))
        return lx_coeff

    def create_empty_estimation(self, nodes):
        """
        Create polynomial out of given nodes
        Nodes must be contained in object's table property
        :param nodes: Nodes out of which polynomial is interpolated
        :return: interpolated polynomial
        """
        if set(nodes) - set(self.table.keys()):
            raise Exception('Wrong nodes input')
        result = 0
        for i in range(0,len(nodes)):
            result += self.table[nodes[i]] * self.create_lx(nodes, i)
        return Estimation(nodes, simplify(result, ratio=1), None)

    def best_estimation(self,input_value,value):
        """
        Creates Estimation object with best possible result
        :param input_value: Input to calculate polynomial value
        :param value: Value to compare with polynomial(input_value)
        :return: Estimation object containing polynomial / nodes which interpolated polynomial / value of polynomial(input)
        """
        results = []
        for sublist in self.subtables:
            if len(sublist) > 1:
                polynomial = self.create_empty_estimation(sublist).polynomial
                results.append(Estimation(sorted(sublist), polynomial, input_value))
        best_result = min(results, key=lambda x: np.abs(value - x.estimated_value))
        return best_result

    def worst_estimation(self, input_value, value):
        """
        Creates Estimation object with worst possible result
        :param input_value: Input to calculate polynomial value
        :param value: Value to compare with polynomial(input_value)
        :return: Estimation object containing polynomial / nodes which interpolated polynomial / value of polynomial(input)
        """
        results = []
        for sublist in self.subtables:
            if len(sublist) > 1:
                polynomial = self.create_empty_estimation(sublist).polynomial
                results.append(Estimation(sorted(sublist), polynomial, input_value))
        best_result = max(results, key=lambda x: np.abs(value - x.estimated_value))
        return best_result

    def estimation_by_value(self,input_value):
        """
        Estimates value of polynomial interpolated with usage of whole object's table with given input
        :param input_value: Input to calculate polynomial value
        :return: Estimation object
        """
        polynomial = self.create_empty_estimation(list(self.table.keys())).polynomial
        return Estimation(list(self.table.keys()),polynomial, input_value)

    def calculate_logarithm(self, base, value):
        """
        Calculates logarithm with given base,value with usage of math lib
        """
        return math.log(value, base)

if __name__ == '__main__':
    lagrange = Lagrange({2 ** i:i for i in range(0, 12)})
    wielomian = lagrange.create_empty_estimation([8,16,32])
    wartosc = wielomian.calculate_value(22)