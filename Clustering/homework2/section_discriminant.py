from numpy import *

# 请编写程序实现分段线性判别法进行数据分类。样本数据请自拟并不能少于30个数据样本，类别不少于3类，每类至少有2个以上子类
# 矫正增量系数
c = 1


# 函数类，使用矩阵来存储函数信息，class_num为函数判定的类别
class NormalFunc:
    class_num = 0
    child_num = 0

    def __init__(self, num, num2, omega1, omega2, omega3):
        self.class_num = num
        self.child_num = num2
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
    child_num = 0

    def __init__(self, num, num2, coordinate1, coordinate2):
        self.class_num = num
        self.child_num = num2
        self.X = mat([coordinate1, coordinate2, 1])


# 获取高斯分布的点，接受分类中心、点的类别、点的数目，返回点类对象的list
def get_data(center, class_num, child_num, nums):
    original_data_x = random.normal(center[0], 0.5, nums)
    original_data_y = random.normal(center[1], 0.5, nums)
    data_n = []
    for i in range(0, nums):
        x = original_data_x[i]
        y = original_data_y[i]
        point_x = Point(class_num, child_num, x, y)
        data_n.append(point_x)
    return data_n


def normal_section_discriminant(class_number, child_numbers, points, judge_points):
    functions = []

    # 迭代次数
    times = 0

    # 获取初始权向量
    for i in range(0, class_number):
        funcs_n = []
        for j in range(child_numbers[i]):
            funcs_n.append(NormalFunc(i, j, 0, 0, 0))
        functions.append(funcs_n)

    # 迭代中是否全部正确
    all_right = False
    while not all_right:
        all_right = True
        for point in points:
            right = True
            class_num = point.class_num
            child_num = point.child_num
            function_i = functions[class_num][child_num]
            # 对每个函数进行赏罚
            for functions_i in functions:
                for function_j in functions_i:
                    if function_j.child_num != child_num or function_j.class_num != class_num:
                        if function_j.answer(point.X) >= function_i.answer(point.X):
                            function_j.minus_x(point.X)
                            all_right = False
                            right = False
            if not right:
                functions[class_num][child_num].add_x(point.X)
            times += 1

    # 获取正确率
    wrongs = 0
    amount = len(judge_points)
    for point in judge_points:
        class_num = point.class_num
        max_answer = []
        for func_n in functions:
            max_answer.append(max(map(lambda x: x.answer(point.X), func_n)))

        for i in range(len(max_answer)):
            if i != class_num:
                if max_answer[i] >= max_answer[class_num]:
                    wrongs += 1
                    break

    print("---------------------------------------- Section -----------------------------------------")
    print("Discriminant function:\n")
    for funcs_n in functions:
        for func in funcs_n:
            omega1 = str(func.W[0, 0])
            omega2 = str(func.W[0, 1])
            omega3 = str(func.W[0, 2])
            print("d" + str(func.class_num) + str(func.child_num) +
                  "(x) = " + omega1 + " * x1 + " + omega2 + " * x2 + " + omega3)
    print("\nThe correct rate of perception algorithm is " + str(100 * (1 - wrongs / amount)) + "%")
    print("------------------------------------------------------------------------------------------\n\n")


if __name__ == '__main__':
    # 训练集
    data = []
    data += get_data([0, 5], 0, 0, 10)
    data += get_data([2.5, 0], 0, 1, 10)
    data += get_data([2.5, 10], 1, 0, 10)
    data += get_data([5, 5], 1, 1, 10)
    data += get_data([10, 5], 1, 2, 10)
    data += get_data([12.5, 0], 2, 0, 10)
    data += get_data([12.5, 10], 2, 1, 10)
    data += get_data([15, 5], 2, 2, 10)

    # 测试集
    judges = []
    judges += get_data([0, 5], 0, 0, 5)
    judges += get_data([2.5, 0], 0, 1, 5)
    judges += get_data([2.5, 10], 1, 0, 5)
    judges += get_data([5, 5], 1, 1, 5)
    judges += get_data([10, 5], 1, 2, 5)
    judges += get_data([12.5, 0], 2, 0, 5)
    judges += get_data([12.5, 10], 2, 1, 5)
    judges += get_data([15, 5], 2, 2, 5)

    normal_section_discriminant(3, [2, 3, 3], data, judges)

    # for point in data:
    #     plt.scatter(point.X[0, 0], point.X[0, 1], color="c", s=15)
    #
    # plt.show()
