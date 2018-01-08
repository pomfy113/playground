from fractions import gcd
import itertools
#
#
# # def collinear(a, b, c):
# # # [ Ax * (By - Cy) + Bx * (Cy - Ay) + Cx * (Ay - By) ] / 2
# #     print(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
#
# def collinear(p0, p1, p2):
#     x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
#     x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
#     print(x1 * y2 - x2 * y1)
#     return x1 * y2 - x2 * y1 <= 0.01
#
# # a = (164.583,275.0)
# # b = (179.166,150.0)
# # c = (196.666,0.0)
# a = (0,0)
# b = (1,100)
# c = (2,201)
# print(collinear(a, b, c))
#
#
# # ('Origin, laser, guard', (164.583, 275.0), (179.166, 150), (185, 100))
# # 196.666, 0.0

a = [1, 2, 3, 4, 5]
b = [6, 7, 8, 9, 10]

for i in itertools.product(a, b):
    print(i)
