from numpy import *


class diff_matrix:
    # the input matrix and the type of each column's data
    origin_matrix = mat(zeros((1, 1)))
    cols_type = []
    # the counts of rows and columns
    rows = 0
    cols = 0
    # the calculated matrix of each column
    matrixs = []
    # the result matrix
    calculated_origin_matrix = mat(zeros((1, 1)))

    # data is the original matrix, and types is the type of each column's data
    def __init__(self, data, types):
        self.origin_matrix = data
        self.cols_type = types
        origin_shape = self.origin_matrix.shape
        self.rows = origin_shape[0]
        self.cols = origin_shape[1]

    # judge if data in this column is nominal, ordinal or numerical
    def judge(self, col_number):
        return self.cols_type[col_number]

    def calc_binary_col(self, col_n):
        matrix_n = mat(zeros((self.rows, self.rows)))
        matrix_theta = mat(zeros((self.rows, self.rows)))
        for i in range(self.rows):
            if col_n[i] == -1:
                continue
            for j in range(i):
                matrix_n[i, j] = 0 if col_n[i] == col_n[j] else 1
                matrix_theta[i, j] = 1
        return [matrix_n, matrix_theta]

    def calc_asymmetrical_binary_col(self, col_n):
        matrix_n = mat(zeros((self.rows, self.rows)))
        matrix_theta = mat(zeros((self.rows, self.rows)))
        for i in range(self.rows):
            if col_n[i] == -1:
                continue
            for j in range(i):
                if col_n[i] == col_n[j]:
                    matrix_n[i, j] = 0
                    continue
                matrix_n[i, j] = 1
                matrix_theta[i, j] = 1
        return [matrix_n, matrix_theta]

    def calc_ordinal_col(self, col_n):
        max_num = max(col_n)
        matrix_n = mat(zeros((self.rows, self.rows)))
        matrix_theta = mat(zeros((self.rows, self.rows)))
        for i in range(self.rows):
            if col_n[i] == -1:
                continue
            for j in range(i):
                matrix_n[i, j] = abs((col_n[i] - col_n[j])/(max_num - 1))
                matrix_theta[i, j] = 1
        return [matrix_n, matrix_theta]

    def calc_numerical_col(self, col_n):
        distance = max(col_n) - min(col_n)
        matrix_n = mat(zeros((self.rows, self.rows)))
        matrix_theta = mat(zeros((self.rows, self.rows)))
        for i in range(self.rows):
            if col_n[i] == -1:
                continue
            for j in range(i):
                matrix_n[i, j] = abs((col_n[i] - col_n[j]) / distance)
                matrix_theta[i, j] = 1
        return [matrix_n, matrix_theta]

    def merge_cols(self):
        calculating_matrix = mat(zeros((self.rows, self.rows)))
        matrix_theta_sum = mat(zeros((self.rows, self.rows)))
        for index in range(len(self.matrixs)):
            matrix_array = self.matrixs[index]
            matrix_n = matrix_array[0]
            matrix_theta = matrix_array[1]
            for i in range(self.rows):
                for j in range(i):
                    calculating_matrix[i, j] += matrix_n[i, j] * matrix_theta[i, j]
                    matrix_theta_sum[i, j] += matrix_theta[i, j]
        for i in range(self.rows):
            for j in range(i):
                calculating_matrix[i, j] /= matrix_theta_sum[i, j]
        return calculating_matrix

    def calc_matrix(self):
        for index in range(self.cols):
            col_n = self.origin_matrix[:, index]
            if self.cols_type[index] == 0:
                self.matrixs.append(self.calc_binary_col(col_n))
            elif self.cols_type[index] == 1:
                self.matrixs.append(self.calc_asymmetrical_binary_col(col_n))
            elif self.cols_type[index] == 2:
                self.matrixs.append(self.calc_ordinal_col(col_n))
            else:
                self.matrixs.append(self.calc_numerical_col(col_n))
        self.calculated_origin_matrix = self.merge_cols()[:, :]

    def get(self, obj_1, obj_2):
        return self.calculated_origin_matrix[obj_1, obj_2]

    def getall(self):
        return self.calculated_origin_matrix


if __name__ == '__main__':
    origin_matrix = mat([
        [1, 1, 45],
        [2, 3, 22],
        [3, 2, 64],
        [1, 1, 28]
    ])
    cols_type = [1, 2, 3]
    diff = diff_matrix(origin_matrix, cols_type)
    diff.calc_matrix()
    print(diff.getall())
