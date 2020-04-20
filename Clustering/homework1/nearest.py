import random
import math

x_list = [[0, 0], [3, 18], [2, 2], [1, 1], [15, 3], [4, 18], [16, 3], [15, 4], [16, 4], [17, 5], [20, 20]]


def nearest(t, x):
    # 聚类list
    z_list = []

    # 随机的初始聚类中心
    k = random.randint(0, len(x) - 1)
    z_list.append([k])

    index = 0
    while index < len(x):
        if index == k:
            index += 1
            continue

        # 未归入聚类的模式样本
        x_1 = x[index]
        # 最小的index在z_list中的位置
        index_of_min_in_zlist = 0
        distence_1 = float("Inf")

        for index_n in z_list:
            # 聚类中心
            x_2 = x[index_n[0]]

            distence_2 = math.sqrt((x_1[0] - x_2[0]) ** 2 + (x_1[1] - x_2[1]) ** 2)
            if distence_2 < distence_1:
                distence_1 = distence_2
                index_of_min_in_zlist = z_list.index(index_n)

        if distence_1 < t:
            z_list[index_of_min_in_zlist].append(index)
        else:
            z_list.append([index])

        index += 1

    return z_list


if __name__ == '__main__':
    print(nearest(3, x_list[:]))
