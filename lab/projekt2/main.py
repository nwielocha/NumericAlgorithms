from sympy import *

class NewtonMethod:


    def __init__(self,equation1, equation2, x_point=None,y_point=None):
        self.equation_1 = equation1
        self.equation_2 = equation2
        self.point = Point(x_point, y_point)

    def create_derivative_matrix(self):
        """
        Creates matrix out of two equations passed through constructor.
        Matrix contains two derivatives of each passed equation - calculated by x and y variable
        :return: Matrix of passed equations derivatives
        """
        self.matrix = Matrix([[self.equation_1.diff(Symbol('x')),
                       self.equation_1.diff(Symbol('y'))],
                      [self.equation_2.diff(Symbol('x')),
                       self.equation_2.diff(Symbol('y'))]])
        return self.matrix

    def sub_variables_for_values(self):
        pass

    def core_calculation(self,point: Point):
        first_component = Matrix([[point.x],[point.y]])
        second_component = self.create_derivative_matrix()
        third_component = Matrix([[self.equation_1.subs(Symbol('x'),point.x).subs(Symbol('y'),point.y)],
                                  [self.equation_2.subs(Symbol('x'),point.x).subs(Symbol('y'),point.y)]])
        return first_component - second_component * third_component


if __name__ == '__main__':
    x,y = Symbol('x y')
    NewtonProcessor = NewtonMethod(4*x**2 + 9*y**2 - 16,
                                   2*y**2 + 4*y - x + 2,
                                   x_point=2,y_point=2)

    p = NewtonProcessor.create_derivative_matrix()
    for x in p.values():
        print(x)


