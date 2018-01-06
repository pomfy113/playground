

def collinear(a, b, c):
# [ Ax * (By - Cy) + Bx * (Cy - Ay) + Cx * (Ay - By) ] / 2
    print(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))


a = (164.583,275.0)
b = (179.166,150.0)
c = (196.666,0.0)
collinear(a, b, c)

# ('Origin, laser, guard', (164.583, 275.0), (179.166, 150), (185, 100))
# 196.666, 0.0
