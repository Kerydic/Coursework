from numpy import *

# 矫正增量系数
c = 1


# 函数类，使用矩阵来存储函数信息，class_num为函数判定的类别
class NormalFunc:
    class_num = 0

    def __init__(self, num, omega1, omega2, omega3):
        self.class_num = num
        self.W = mat([omega1, omega2, omega3], dtype=float64)

    def add_x(self, xi):
        self.W += xi * c

    def minus_x(self, xi):
        self.W -= xi * c

    def answer(self, xi):
        return self.W * xi.T


# 点类，使用矩阵存储函数信息，class_num为点的类别
class Point:
    class_num = 0

    def __init__(self, num, coordinate1, coordinate2):
        self.class_num = num
        self.X = mat([coordinate1, coordinate2, 1])


# 获取高斯分布的点，接受分类中心、点的类别、点的数目，返回点类对象的list
def get_data(center, class_num, nums):
    original_data_x = random.normal(center[0], 0.5, nums)
    original_data_y = random.normal(center[1], 0.5, nums)
    data_n = []
    for i in range(0, nums):
        x = original_data_x[i]
        y = original_data_y[i]
        point_x = Point(class_num, x, y)
        data_n.append(point_x)
    return data_n


# 使用感知器算法完成训练，分类时采用wi/wi分类、wi/wj两分法特例
# 使用wi/wi分类法的感知器算法，接受类的数目、训练集、测试集，打印分类函数和准确率
def perception_1(class_number, points, judge_points):
    functions = []

    # 迭代次数
    times = 0

    # 获取初始权向量
    for i in range(0, class_number):
        functions.append(NormalFunc(i, 0, 0, 0))

    for i in range(0, class_number):
        # 迭代中是否全部正确
        all_right = False
        while not all_right:
            all_right = True
            for point in points:
                point_x = Point(point.class_num, point.X[0, 0], point.X[0, 1])
                # 如果该点不在要求的分类函数类中，将其乘以-1
                if point_x.class_num != i:
                    point_x.X *= -1
                if functions[i].answer(point_x.X) <= 0:
                    functions[i].add_x(point_x.X)
                    all_right = False
                times += 1

    # 使用测试集获得正确率
    wrongs = 0
    amount = len(judge_points)
    for point in points:
        num_p = point.class_num
        for func_n in functions:
            num_f = func_n.class_num
            if (func_n.answer(point.X) <= 0 and num_p == num_f) or (func_n.answer(point.X) > 0 and num_p != num_f):
                wrongs += 1
                break

    print("-------------------------------------- Perception_1 --------------------------------------")
    print("Discriminant function:\n")
    for func in functions:
        omega1 = str(func.W[0, 0])
        omega2 = str(func.W[0, 1])
        omega3 = str(func.W[0, 2])
        print("d" + str(func.class_num) + "(x) = " + omega1 + " * x1 + " + omega2 + " * x2 + " + omega3)
    print("\nThe correct rate of perception algorithm is " + str(100 * (1 - wrongs / amount)) + "%")
    print("------------------------------------------------------------------------------------------\n\n")


# 使用wi/wj分类法特例的感知器算法，接受类的数目、训练集、测试集，打印分类函数和准确率
def perception_2(class_number, points, judge_points):
    functions = []

    # 迭代次数
    times = 0

    for i in range(0, class_number):
        functions.append(NormalFunc(i, 0, 0, 0))

    # 迭代中是否全部正确
    all_right = False
    while not all_right:
        all_right = True
        for point in points:
            right = True
            class_num = point.class_num
            function_i = functions[class_num]
            # 对每个函数进行赏罚
            for function_j in functions:
                if function_j.class_num != class_num:
                    if function_j.answer(point.X) >= function_i.answer(point.X):
                        function_j.minus_x(point.X)
                        all_right = False
                        right = False
            if not right:
                functions[class_num].add_x(point.X)
            times += 1

    # 获取正确率
    wrongs = 0
    amount = len(judge_points)
    for point in judge_points:
        class_num = point.class_num
        function_i = functions[class_num]
        for function_j in functions:
            if function_j.class_num != class_num:
                if function_j.answer(point.X) >= function_i.answer(point.X):
                    wrongs += 1
                    break

    print("-------------------------------------- Perception_2 --------------------------------------")
    print("Discriminant function:\n")
    for func in functions:
        omega1 = str(func.W[0, 0])
        omega2 = str(func.W[0, 1])
        omega3 = str(func.W[0, 2])
        print("d" + str(func.class_num) + "(x) = " + omega1 + " * x1 + " + omega2 + " * x2 + " + omega3)
    print("\nThe correct rate of perception algorithm is " + str(100 * (1 - wrongs / amount)) + "%")
    print("------------------------------------------------------------------------------------------\n\n")


if __name__ == '__main__':
    # 训练集
    data = []
    data += get_data([5, 8], 0, 10)
    data += get_data([0, 5], 1, 10)
    data += get_data([10, 5], 2, 10)
    data += get_data([2.5, 0], 3, 10)
    data += get_data([7.5, 0], 4, 10)

    # 测试集
    judges = []
    judges += get_data([5, 8], 0, 5)
    judges += get_data([0, 5], 1, 5)
    judges += get_data([10, 5], 2, 5)
    judges += get_data([2.5, 0], 3, 5)
    judges += get_data([7.5, 0], 4, 5)

    perception_1(5, data, judges)
    perception_2(5, data, judges)
