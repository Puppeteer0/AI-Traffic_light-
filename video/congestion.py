from numpy import *
def data_calculation(data):
    data_list = []
    for i in range(len(data)):
        data_list.append(data[i])
    tag1 = "person";
    plist = []
    tag2 = "car";
    clist = []
    tag3 = "bus";
    blist = []
    tag4 = "truck";
    tlist = []
    length = len(data_list)
    # print(length)
    for i in range(length):
        if tag1 in data_list[i]:
            plist.append(data_list[i][-1])
        if tag2 in data_list[i]:
            clist.append(data_list[i][-1])
        if tag3 in data_list[i]:
            blist.append(data_list[i][-1])
        if tag4 in data_list[i]:
            tlist.append(data_list[i][-1])

    def count_x(xlist, x1, x2):
        count1 = count2 = count3 = 0
        for i in range(len(xlist)):
            if int(xlist[i]) <= x1:
                count1 = count1 + 1
            if x1 < int(xlist[i]) <= x2:
                count2 = count2 + 1
            if int(xlist[i]) > x2:
                count3 = count3 + 1
        return count1, count2, count3

    a1, a2, a3 = count_x(plist, 1, 2)
    b1, b2, b3 = count_x(clist, 3, 7)
    c1, c2, c3 = count_x(blist, 2, 4)
    d1, d2, d3 = count_x(tlist, 1, 2)

    def shodvalue_calculate(xlist, ylist, zlist, ulist, x1, x2):
        count_1 = count_2 = count_3 = 0
        # print(len(xlist))
        for i in range(len(xlist)-1):
            # print(i)
            if int(xlist[i]) + int(ylist[i]) + int(zlist[i]) + int(ulist[i]) <= x1:
                count_1 = count_1 + 1
            if int(xlist[i]) + int(ylist[i]) + int(zlist[i]) + int(ulist[i]) > x1 and int(xlist[i]) + int(
                    ylist[i]) + int(zlist[i]) + int(ulist[i]) <= x2:
                count_2 = count_2 + 1
            if int(xlist[i]) + int(ylist[i]) + int(zlist[i]) + int(ulist[i]) > x2:
                count_3 = count_3 + 1
        return count_1, count_2, count_3

    x1, x2, x3 = shodvalue_calculate(plist, clist, blist, tlist, 15, 20)
    # print(x1, x2, x3)

    def light_span(xlist, ylist, zlist, ulist, x1, x2, time):
        lightspan = 0
        text = ""
        mini = min(len(xlist), len(ylist), len(zlist), len(ulist)) - 1
        if time > mini:
            time = mini+2
        threshold = int(xlist[time]) + int(ylist[time]) + int(zlist[time]) + int(ulist[time])

        if threshold <= x1:
            lightspan = 40
            text = "该路段通畅,设置红绿灯时间为:"
        if threshold > x1 and threshold <= x2:
            lightspan = 30
            text = "该路段正常,设置红绿灯时间为:"
        if threshold > x2:
            lightspan = 20
            text = "该路段拥堵,设置红绿灯时间为:"
        return text, lightspan

    text, lightspan = light_span(plist, clist, blist, tlist, 15, 20, 0)
    return text, lightspan
