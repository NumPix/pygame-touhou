import numpy as np


class Spline:
    """
    basic class for cubic uniform splines;
    """

    def __init__(self, characteristic_matrix: np.ndarray):
        self.characteristic_matrix = characteristic_matrix

    def curve(self, points: [np.ndarray, ...], u):

        points = [2 * points[0] - points[1]] + points + [2 * points[-1] - points[-2]]

        if u % 1 == 0:
            t = 1
            n = int(u) - 1
        else:
            t = u % 1
            n = int(u)


        p_matrix_x = np.array([
            [points[0 + n][0]],
            [points[1 + n][0]],
            [points[2 + n][0]],
            [points[3 + n][0]]
        ])

        p_matrix_y = np.array([
            [points[0 + n][1]],
            [points[1 + n][1]],
            [points[2 + n][1]],
            [points[3 + n][1]]
        ])

        t_matrix = np.array([1, t, t * t, t * t * t])

        coefficient_matrix_x = np.matmul(self.characteristic_matrix, p_matrix_x)
        coefficient_matrix_y = np.matmul(self.characteristic_matrix, p_matrix_y)

        part_x = np.matmul(np.rot90(coefficient_matrix_x), t_matrix)[0]
        part_y = np.matmul(np.rot90(coefficient_matrix_y), t_matrix)[0]

        return np.array([part_x, part_y])


class BasisSpline(Spline):
    def __init__(self):
        characteristic_matrix = np.array([
            [1 / 6, 2 / 3, 1 / 6, 0],
            [-.5, 0, .5, 0],
            [.5, -1, .5, 0],
            [-1 / 6, .5, -.5, 1 / 6]
        ])
        super().__init__(characteristic_matrix)
