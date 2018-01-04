def is_on(a, b, c):
    "Return true iff point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    if a[0] != b[0]:
        is_within = within(a[0], c[0], b[0])
    else:
        is_within = within(a[1], c[1], b[1])
    return collinear(a, b, c) and is_within

def collinear(a, b, c):
    "Return true iff a, b, and c all lie on the same line."
    return round((b[0] - a[0]) * (c[1] - a[1]),2) == round((c[0] - a[0]) * (b[1] - a[1]),2)


def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p


print(is_on((0,0), (4,1), (1,0.25)))

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False


L1 = line([0,0], [0,3])
L2 = line([2,0], [5,5])

print(intersection(L1, L2))
point1 = (0.5, round(2.0, 2))
point2 = (round(0.998,2), round(1.6667, 2))
point3 = (2, round(1, 2))
print(point1, point2, point3)
print("IS ON")
print(is_on(point1, point3, point2))
