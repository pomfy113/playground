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
        self.data = None
        self.left = None
        self.right = None

class btree(object):
    """Btree set-up."""
    def __init__(self, height):
        self.size = 0
        self.root = None

        # Build an empty btree based on height
        self.build(height)
        print("Build done")

        # Used for labeling
        self.counter = 0
        # Labeling the nodes via post-order traversal
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


    # def build(self, height, depth=0, node=None):
    #     # If done with building
    #     if depth == height:
    #         return
    #     else:
    #         # First things first: the root
    #         if depth == 0:
    #             depth += 1
    #             node = btree_node()
    #             self.root = node
    #             self.size += 1
    #             # Recursive call
    #             self.build(height, depth, node)
    #         else:
    #             # Going down one!
    #             depth += 1
    #             # Make left node, then build down
    #             node.left = btree_node()
    #             node.left.parent = node
    #             self.size += 1
    #             self.build(height, depth, node.left)
    #
    #             # Same; make right node, then build down
    #             node.right = btree_node()
    #             node.right.parent = node
    #             self.size += 1
    #             self.build(height, depth, node.right)


    def build_labels(self, node):
        """Labeling using post-order."""
        if node.left:
            self.build_labels(node.left)
        if node.right:
            self.build_labels(node.right)
        # Labeling!
        node.data = self._traverse_helper()

        return

    def _traverse_helper(self):
        """For labeling."""
        self.counter += 1
        return self.counter

    def find(self, items):
        # Preloading the lookup; need to keep the order
        # Default items -1
        result = []
        for i in items:
            self.search(self.root, i, result.append)
        return result

    def search(self, node, item, visit, parent=None):
        if node.data == item:
            if parent:
                visit(parent.data)
            else:
                visit(-1)
            return
        if node.data > item and node.left:
            if node.left.data >= item:
                parent = node
                self.search(node.left, item, visit, parent)
            else:
                parent = node
                self.search(node.right, item, visit, parent)


h = 20
q = [7, 3, 5, 1]
print(answer(h, q))
