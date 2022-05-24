from sympy import Matrix, Symbol, Float, solve_poly_system


class Point:

    def __init__(self, x_cord: Float, y_cord: Float):
        self.x = x_cord
        self.y = y_cord

    def __eq__(self, other):
        if other.x == self.x and other.y == self.y:
            return True
        return False
    

class Crossing:

    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2


class Response:

    def __init__(self, point, value=False):
        self.point = point
        self.value = value


class NewtonMethod:

    def __init__(self, equation1, equation2, x_point=None, y_point=None):
        self.equation_1 = equation1
        self.equation_2 = equation2
        self.point = Point(x_point, y_point)
        self.cross_point1 = Point(2, 0)
        self.cross_point2 = Point(0.2122922239929, -1.3258007243645)
        self.derivative_matrix = self.create_inverted_derivative_matrix()
        self.equations_matrix = Matrix([[self.equation_1],
                                        [self.equation_2]])

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
        return self.matrix ** -1

    def sub_variables_for_values(self, point: Point, matrix: Matrix) -> Matrix:
        """
        Substitute variables x,y with given Point coordinates
        :param point: Point object
        :param matrix: Matrix of equations which each element is going to be substituted with given values
        :return: Matrix of values
        """
        for i in range(0, len(matrix)):
            matrix[i] = Float(matrix[i].subs(Symbol('x'), point.x).subs(Symbol('y'), point.y), 4)
        return matrix

    def core_calculation(self, point: Point) -> Matrix:
        """
        Function creates 3 components needed to calculate  next iteration point.
        1st component - Matrix of x and y
        2nd component - Matrix of equations derivatives substituted with x'y from given point
        3rd component - Matrix of equations substituted with x'y from given component
        :param point: Point which is used to perform calculation
        :return: Point object used to calculate next values
        """
        first_component = Matrix([[point.x], [point.y]])
        second_component = self.sub_variables_for_values(point, self.derivative_matrix)
        third_component = self.sub_variables_for_values(point, self.equations_matrix)
        return first_component - (second_component * third_component)

    def loop_calculations(self, point, limit):
        for i in range(0, 10):
            matrix = self.core_calculation(point)
            point = Point(matrix[0], matrix[1])
            if abs(self.cross_point1.x - point.x) <= limit:
                if abs(self.cross_point1.y - point.y) <= limit:
                    return 1
            if abs(self.cross_point2.x - point.x) <= limit:
                if abs(self.cross_point2.x - point.x) <= limit:
                    return 2
        return 0

if __name__ == '__main__':
    pass