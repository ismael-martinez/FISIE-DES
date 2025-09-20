from random import seed, random
seed(100)

class Node:
    n_id = 0
    def __init__(self):
        self.pred = []
        self.next = []
        self.id = Node.n_id
        Node.n_id+=1

    def add_pred(self, node):
        self.pred.append(node)
    def add_next(self, node):
        self.next.append(node)
    def connect(self, next):
        self.add_next(next)
        next.add_pred(self)
class TDG:


    def __init__(self, depth=2, width=3):
        Node.n_id = 0
        self.root = Node()

        layer = [None]*depth
        # Initialize
        for d in range(depth):
            layer[d] = [Node() for w in range(width)]

        # One linear path
        self.root.connect(layer[0][0])
        for d in range(depth-1):
            layer[d][0].connect(layer[d+1][0])

        # First layer
        for w, l in enumerate(layer[0]):
            if w == 0:
                continue
            if random() < 0.3:
                self.root.connect(layer[0][w])

        # Remove unused nodes
        new_layer = []
        for w, l in enumerate(layer[0]):
            if layer[0][w].pred:
                new_layer.append(layer[0][w])
        layer[0] = new_layer

        for d in range(depth-1):
            for w, l in enumerate(layer[d]):
                for w2, l2 in enumerate(layer[d+1]):
                    if (w == 0 and w2 == 0):
                        continue
                    if random() < 0.3:
                        layer[d][w].connect(layer[d+1][w2])

            new_layer = []
            for w, l in enumerate(layer[d+1]):
                if layer[d+1][w].pred:
                    new_layer.append(layer[d+1][w])
            layer[d+1] = new_layer

        self.sink = Node()
        # All hanging nodes to sink
        for d in range(depth):
            for w, l in enumerate(layer[d]):
                if not l.next:
                    layer[d][w].connect(self.sink)

        self.nodes = [self.root]
        for d in range(depth):
            self.nodes.extend(layer[d])
        self.nodes.append(self.sink)
        for i, n in enumerate(self.nodes):
            n.id = i



t = TDG(2,3)
for n in t.nodes:
    # pr = [p.id for p in n.pred]
    # print(pr)
    nx = [m.id for m in n.next]
    print(nx)
