import time
from sympy import diff, Matrix, Symbol, Float
import numpy as np


class Point:

    def __init__(self, x_cord: Float, y_cord: Float):
        self.x = x_cord
        self.y = y_cord


class Crossing:

    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2


class NewtonMethod:

    def __init__(self ,equation1, equation2, x_point=None, y_point=None):
        self.equation_1 = equation1
        self.equation_2 = equation2
        self.point = Point(x_point, y_point)

    def create_inverted_derivative_matrix(self) -> Matrix:
        """
        Creates matrix out of two equations passed through constructor.
        Matrix contains two derivatives of each passed equation - calculated by x and y variable
        :return: Matrix of passed equations derivatives
        """
        self.matrix = Matrix([[self.equation_1.diff(Symbol('x')),
                       self.equation_1.diff(Symbol('y'))],
                      [self.equation_2.diff(Symbol('x')),
                       self.equation_2.diff(Symbol('y'))]])
        return self.matrix**-1

    def sub_variables_for_values(self,point: Point,matrix: Matrix) -> Matrix:
        """
        Substitute variables x,y with given Point coordinates
        :param point: Point object
        :param matrix: Matrix of equations which each element is going to be substituted with given values
        :return: Matrix of values
        """
        for i in range (0,len(matrix)):
            matrix[i] = Float(matrix[i].subs(Symbol('x'), point.x).subs(Symbol('y'),point.y),4)
        return matrix

    def core_calculation(self,point: Point) -> Matrix:
        """
        Function creates 3 components needed to calculate  next iteration point.
        1st component - Matrix of x and y
        2nd component - Matrix of equations derivatives substituted with x'y from given point
        3rd component - Matrix of equations substituted with x'y from given component
        :param point: Point which is used to perform calculation
        :return: Point object used to calculate next values
        """
        first_component = Matrix([[point.x],[point.y]])
        second_component = self.sub_variables_for_values(point, self.create_inverted_derivative_matrix())
        third_component = Matrix([[self.equation_1],
                                  [self.equation_2]])
        third_component = self.sub_variables_for_values(point,third_component)

        return first_component - (second_component * third_component)

    def loop_calculations(self, point):
        for i in range(0, 100):
            matrix = self.core_calculation(point)
            point = Point(matrix[0], matrix[1])


if __name__ == '__main__':
    x = Symbol('x')
    y = Symbol('y')
    NewtonProcessor = NewtonMethod(4*x**2 + 9*y**2 - 16,
                                   2*y**2 + 4*y - x + 2,
                                   x_point=1, y_point=1)
    p = NewtonProcessor.create_inverted_derivative_matrix()
    print(NewtonProcessor.loop_calculations(Point(1,1)))

