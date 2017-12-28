# coord = ((20, 30))
#
# for x, y in coord:
#     print(x, y)

from collections import deque

x = deque()
x.append(1)
x.append(2)
x.append(3)
print(x)
x.popleft()
print(x)
x.popleft()

if x:
    print("True")
else:
    print("False")
