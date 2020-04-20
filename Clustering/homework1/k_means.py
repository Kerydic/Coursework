import math
import random
from functools import reduce

x_list = [[0, 0], [3, 18], [2, 2], [1, 1], [15, 3], [4, 18], [16, 3], [15, 4], [16, 4], [17, 5], [20, 20]]


def z_constructor(k):
    z_list = []
    i = 0
    while i < k:
        z = random.randint(0, len(x_list) - 1)
        if [z] in z_list:
            continue
        z_list.append([z])
        i += 1
    return z_list


def z_values_constructor(z_list, xlist):
    z_values = []
    for indexs in z_list:
        z_value = []
        for index in indexs:
            z_value.append(xlist[index])
        sum = reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], z_value)
        z_values.append( [sum[0]/len(z_value),sum[1]/len(z_value)])
    return z_values


def inZlist(index, zlist):
    for indexs in zlist:
        for index_n in indexs:
            if index == index_n:
                return True
    return False


def step(k, xlist, z_list, z_values):
    pre_z_list = z_list
    index = 0
    while index < len(xlist):
        if inZlist(index, z_list):
            index += 1
            continue

        x_1 = xlist[index]
        min_index = -1
        distence_1 = float("Inf")
        for i in range(0, k):
            x_2 = z_values[i]
            distence_2 = math.sqrt((x_1[0] - x_2[0]) ** 2 + (x_1[1] - x_2[1]) ** 2)
            if distence_2 < distence_1:
                distence_1 = distence_2
                min_index = i

        z_list[min_index].append(index)
        index += 1
    if z_list != pre_z_list:
        step(k, xlist, z_list, z_values)

    return z_list


def k_means(k, xlist):
    z_list = z_constructor(k)
    z_values = z_values_constructor(z_list, x_list)
    return step(k, xlist, z_list, z_values)


if __name__ == '__main__':
    print(k_means(4, x_list))
