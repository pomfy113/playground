"""
So I got a long story about this.
- Originally, first thing that came to mind was a tree and all the fixings.
  Nodes had left, right, content, and their parent.
- Hit a memory error. Probably the tree itself. Removed the parent. Did
  old school "find".
- Hit another memory error. Okay, I'll find a way to remove the data.
  How do I even figure it out at this point? Mess with indeces on- oh.
  I don't NEED to make a tree.

Reminded me of a heap, and I eventually found out that
I can find parents with it using basic math.

I wasn't EXTREMELY versed into bitwise, but it looked like
it was the best way to handle it. Was the missing piece
of the puzzle:
    I knew what I wanted to do, but not the operations.
"""


def answer(h, q):
    """H is for height of tree, Q for numbers we're looking for."""
    parents = []

    # Grabs the list of numbers
    for item in q:
        result = bitwise(item)
        # If it's not within range, that needs to be -1
        # You can't get a number above the last num (2^h+1)
        if result not in range(1, 2**h+1):
            parents.append(-1)
        else:
            parents.append(result)
    return parents

def bitwise(item):
    """Checks for parents using an algorithm."""
    # Temporary; we still need the item for accumulator
    num = item
    while ((num+1) & num) != 0 and ((num+1) & (num+2)) != 0:
        binary = bin(num)[3:]
        num = int(binary, 2) + 1
    # Accumulator; diff between original and new num
    acc = item - num

    # If left,
    # multiplying it by 2 and adding 1 gives you the parent
    if (num+1) & num == 0:
        num = (num * 2) + 1
    # If right,
    # Just adding 1 gives you the parent
    else:
        num = num + 1
    # Add the rest
    num += acc

    return num
