import math
import random
from functools import reduce

# x_list = [[0, 0], [1, 1], [2, 2], [4, 3], [5, 3], [4, 4], [5, 4], [6, 5]]
x_list = [[0, 0], [3, 18], [2, 2], [1, 1], [15, 3], [4, 18], [16, 3], [15, 4], [16, 4], [17, 5], [20, 20]]


# make the original list of cluster center and its value
def z_constructor(nc, xlist):
    z_list = []
    z_values = []
    i = 0
    while i < nc:
        z = random.randint(0, len(x_list) - 1)
        if [z] in z_list:
            continue
        z_list.append([z])
        z_values.append(xlist[z])
        i += 1
    return z_values


# calc the distence of two point
def dist(x_a, x_b):
    return math.sqrt((x_a[0] - x_b[0]) ** 2 + (x_a[1] - x_b[1]) ** 2)


# merge two cluster center
def merge(x_a, nj_a, x_b, nj_b):
    return [(x_a[0] * nj_a + x_b[0] * nj_b) / (nj_a + nj_b), (x_a[1] * nj_a + x_b[1] * nj_b) / (nj_a + nj_b)]


# the main algorithm
def isodata(xlist, k, theta_n, theta_s, theta_c, l, I):
    # step 1, set original list
    nc = 1
    z_list = []
    z_values = z_constructor(nc, xlist)

    # times of iterations
    times = 0
    while times < I:
        # step 2， put every x into proper cluster
        del z_list[:]
        for i in range(len(z_values)):
            z_list.append([-1])
        for x in xlist:
            distence_1 = float("Inf")
            z_min = 0
            for i in range(len(z_values)):
                distence_2 = dist(x, z_values[i])
                if distence_2 < distence_1:
                    distence_1 = distence_2
                    z_min = i
            z_list[z_min].append(xlist.index(x))
        for z in z_list:
            del z[0]

        # step 3, if the number of a cluster is smaller than theta_n ,delete it
        for z in z_list:
            if len(z) < theta_n:
                z_list.remove(z)
                nc -= 1
                continue

        # step 4 to 6
        average_dist = 0
        z_dist_list = []
        del z_values[:]
        for indexs in z_list:
            z_value = []
            for index in indexs:
                z_value.append(xlist[index])
            sum = reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], z_value)
            # the center of each cluster
            z_values.append([sum[0] / len(z_value), sum[1] / len(z_value)])

            dist_sum = 0
            for i in range(len(indexs)):
                dist_sum += dist(z_value[i], z_values[z_list.index(indexs)])
            z_dist_list.append(dist_sum / len(indexs))

            average_dist = reduce(lambda x, y: x + y, z_dist_list) / len(z_dist_list)

        # step 7
        flag = 0
        if times >= I:
            theta_n = 0
        elif nc <= k / 2:
            flag = 1
        elif times % 2 == 0 or theta_c >= 2 * k:
            flag = 0
        else:
            flag = 1

        # if flag equals 1, will run step 8 to 10
        if flag == 1:
            # step 8 and 9
            segma = []
            for indexs in z_list:
                z_value = z_values[z_list.index(indexs)]
                sum = reduce(lambda x, y: [x[0]+y[0],x[1]+y[1]],map(lambda x: [(x_list[x][0] - z_value[0])**2, (x_list[x][1] - z_value[1])**2], indexs))
                if math.sqrt(sum[0] / len(indexs)) >= math.sqrt(sum[1] / len(indexs)):
                    segma.append([math.sqrt(sum[0] / len(indexs)), 0])
                else:
                    segma.append([math.sqrt(sum[1] / len(indexs)), 1])

            # step 10
            z_values_tocalc = z_values[:]
            flag_10 = 0
            for segma_j in segma:
                if segma_j[0] <= theta_s:
                    continue
                index = segma.index(segma_j)
                z_dist = z_dist_list[index]
                number = len(z_list[index])
                if (z_dist > average_dist and number > 2*(theta_n + 1)) or nc <= k/2:
                    nc += 1
                    p = 0.5
                    z_j_add = z_values[index][:]
                    z_j_minus = z_values[index][:]
                    z_j_add[segma_j[1]] += p * segma_j[0]
                    z_j_minus[segma_j[1]] -= p * segma_j[0]
                    z_values_tocalc.append(z_j_add)
                    z_values_tocalc.append(z_j_minus)
                    del z_values_tocalc[z_values_tocalc.index(z_values[index])]
                    flag_10 = 1
            z_values = z_values_tocalc[:]
            if flag_10 == 1:
                times += 1
                continue

        # step 11 and 12
        dist_of_centers = []
        for i in range(len(z_values)):
            for j in range(i + 1, len(z_values)):
                dist_of_centers.append([[i, j], dist(z_values[i], z_values[j])])
        lower_dist = sorted(filter(lambda x_n: x_n[1] <= theta_c, dist_of_centers))

        # step 13, merge clusters whose distance to others is smaller than theta_c
        z_list_tocalc = z_list[:]
        z_values_tocalc = z_values[:]
        merge_times = 0
        for lower in lower_dist:
            index_1 = lower[0][0]
            index_2 = lower[0][1]
            if not (z_list[index_1] in z_list_tocalc and z_list[index_2] in z_list_tocalc):
                continue
            nj1, nj2 = len(z_list[index_1]), len(z_list[index_2])
            z_list_tocalc[z_list_tocalc.index(z_list[index_1])] += z_list[index_2]
            del z_list_tocalc[z_list_tocalc.index(z_list[index_2])]
            z_values_tocalc[z_values_tocalc.index(z_values[index_1])] = \
                merge(z_values[index_1], nj1, z_values[index_2], nj2)
            del z_values_tocalc[z_values_tocalc.index(z_values[index_2])]
            nc -= 1
            merge_times += 1
            if merge_times >= l:
                break
        z_list = z_list_tocalc[:]
        z_values = z_values_tocalc[:]

        times += 1

    return z_list


# isodata(xlist, k, theta_n, theta_s, theta_c, l, i):
if __name__ == '__main__':
    print(isodata(x_list, 4, 1, 1, 4, 0, 4))
