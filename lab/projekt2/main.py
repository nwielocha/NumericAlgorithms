from sympy import *

class NewtonMethod:


    def __init__(self,equation1, equation2, x_point=None,y_point=None):
        self.equation_1 = equation1
        self.equation_2 = equation2
        self.point = Point(x_point, y_point)

    def calculate_derivative(self,equation,x:Symbol):
        return equation.diff(x)

    def create_derivative_matrix(self):
        return Matrix([[self.calculate_derivative(self.equation_1,Symbol('x')),
                       self.calculate_derivative(self.equation_1,Symbol('y'))],
                      [self.calculate_derivative(self.equation_2,Symbol('x')),
                       self.calculate_derivative(self.equation_2,Symbol('y'))]])

    def sub_variables_for_values(self):
        pass

    def core_calculation(self,point: Point,equation):
        first_component = Matrix([point.x,point.y])
        second_component = self.create_derivative_matrix()
        third_component = equation.subs(Symbol('x'),5).subs(Symbol('y'),5)
        return first_component - second_component * third_component

if __name__ == '__main__':
    x,y = Symbol('x y')
    NewtonProcessor = NewtonMethod(4*x**2 + 9*y**2 - 16,
                                   2*y**2 + 4*y - x + 2,
                                   x_point=2,y_point=2)

    p = NewtonProcessor.create_derivative_matrix()
    for x in p.values():
        print(x)


