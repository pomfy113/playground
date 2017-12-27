def answer(h, q):
    unit = tree(h)
    
    results = []
    for i in q:
        find = unit.data[i-1].parent
        if find == -1:
            results.append(-1)
        else:
            results.append(unit.data.index(find))
    return(results)

class node(object):
    def __init__(self, parent):
        self.parent = parent
        self.right = None
        self.left = None

class tree(object):
    def __init__(self, height):
        self.root = None
        self.size = 1
        self.data = []

        self.build(height, self.root)
        self.traverse(self.root)


    def build(self, height, parent):
        if height > 0:
            if self.root is None:
                newnode = node(-1)
                self.root = newnode
                self.build(height-1, newnode)
            else:
                parent.left = node(parent)
                self.build(height-1, parent.left)
                parent.right = node(parent)
                self.build(height-1, parent.right)
        else:
            return

    def traverse(self, node):
        if node.left:
            self.traverse(node.left)
        if node.right:
            self.traverse(node.right)
        self.data.append(node)



answer(3, [1, 2, 3, 4, 5, 6, 7])
