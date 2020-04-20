import math

x_list = [[0, 0], [3, 18], [2, 2], [1, 1], [15, 3], [4, 18], [16, 3], [15, 4], [16, 4], [17, 5], [20, 20]]


def hierarchical(t, x):
    z_list = []

    # 初始化聚类中心list
    index = 0
    while index < len(x_list):
        z_list.append([index])
        index += 1
    step(t, x, z_list)

    return z_list


def step(t, x, zlist):
    min_list = []
    distence_1 = float("Inf")
    for index_1 in range(len(x)):
        x_1 = x[index_1]
        for index_2 in range(index_1 + 1, len(x)):
            x_2 = x[index_2]
            distence_2 = math.sqrt((x_1[0] - x_2[0]) ** 2 + (x_1[1] - x_2[1]) ** 2)

            if distence_2 < distence_1:
                min_list = [[x[index_1], x[index_2]]]
                distence_1 = distence_2
            elif distence_2 == distence_1:
                min_list.append([x[index_1], x[index_2]])

    for d_n in min_list:
        if d_n[0] in x and d_n[1] in x:
            index_1 = x.index(d_n[0])
            index_2 = x.index(d_n[1])
            x.append([(d_n[0][0] + d_n[1][0]) / 2, (d_n[0][1] + d_n[1][1]) / 2])
            zlist.append(zlist[index_1] + zlist[index_2])
            del x[index_1]
            del x[index_2 - 1]
            del zlist[index_1]
            del zlist[index_2 - 1]

    if distence_1 < t:
        step(t, x, zlist)


if __name__ == '__main__':
    print(hierarchical(2, x_list[:]))
