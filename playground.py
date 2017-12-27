def answer(h, q):
    errorcheck(h, q)
    flux = btree(h)
    return flux.find(q)

def errorcheck(h, q):
    """Within bounds."""
    if 1 > h or h > 30:
        raise ValueError
    for item in q:
        if 1 > item or item > (2**h-1):
            raise ValueError

class btree_node(object):
    """Node set-up."""
    def __init__(self):
        self.left = None
        self.right = None

class btree(object):
    """Btree set-up."""
    def __init__(self, height):
        self.root = None
        # Build an empty btree based on height
        self.build(height)
        # Used for labeling
        self.counter = 0
        # Labeling the nodes via post-order traversal
        self.items = []
        self.build_labels(self.root)


    def build(self, height, node=None):
        # If done with building
        if height > 0:
            if node is None:
                node = btree_node()
                self.root = node
                height -= 1
                self.build(height, node)
            else:
                height -= 1
                node.left = btree_node()
                self.build(height, node.left)

                node.right = btree_node()
                self.build(height, node.right)
        else:
            return

    def build_labels(self, node):
        """Labeling using post-order."""
        if node.left:
            self.build_labels(node.left)
        if node.right:
            self.build_labels(node.right)
        # Labeling!
        self.items.append(node)
        return


    def find(self, items):
        # Preloading the lookup; need to keep the order
        # Default items -1
        result = []

        for item in items:
            print(self.items[item])

        return result


h = 15
q = [7, 3, 5, 1]
print(answer(h, q))
