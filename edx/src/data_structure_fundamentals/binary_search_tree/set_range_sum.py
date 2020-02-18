import sys, threading

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

class SplayNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.sum = value

    def update(self):
        self.sum = self.value + (self.left.sum if self.left is not None else 0) + (self.right.sum if self.right is not None else 0)

    def __str__(self):
        return '(' + str(self.value) + ' ' + str(self.sum) + ')'

class SplayTree:
    def __init__(self, root=None):
        self.root = root

    def delete(self, root, value):
        if root is None:
            return root
        k = self.splay(root, value)
        if k.value != value:
            return k
        if k.left is None:
            return k.right
        else:
            temp = k
            new_root = self.splay(k.left, value)
            new_root.right = temp.right
            temp = None
            return new_root

    def search(self, root, value):
        return self.splay(root, value)

    def insert(self, root, value):
        if root is None:
            return SplayNode(value)
        else:
            # Splaying the tree will bring the node having given key to the root
            # If one such exists, then no action needs to be taken
            # If such node doesn't exist then splay operation will bring up
            # the node before or after the value to be inserted
            root = self.splay(root, value)
            n = SplayNode(value)
            if root.value == value:
                return root
            # If it returned the value following the given key then
            # Put the left subtree of current root as left subtree of the newly created node
            elif root.value > value:
                n.right = root
                n.left = root.left
                root.left = None
                root.update()
                n.update()
                return n
            elif root.value < value:
                n.left = root
                n.right = root.right
                root.right = None
                root.update()
                n.update()
                return n


    def left_rotate(self, gp):
        p = gp.right
        gp.right = p.left
        p.left = gp
        gp.update()
        p.update()
        return p

    def right_rotate(self, gp):
        p = gp.left
        gp.left = p.right
        p.right = gp
        gp.update()
        p.update()
        return p

    def merge(self, left, right):
        if left is None:
            return right
        if right is None:
            return left
        right_root = right
        while right.left is not None:
            right = right.left
        right_root = self.splay(right_root, right.value)
        right_root.left = left
        right_root.update()
        return right_root

    def range_sum(self, root, low, high):
        result = 0
        if root is None:
            return 0
        root = self.splay(root, low)
        if root.value >= low and root.value <= high:
            result += root.value
        if root.right is not None:
            root.right = self.splay(root.right, high)
            if root.right.value >= low and root.right.value <= high:
                result += root.right.value
            if root.right.left is not None:
                result += root.right.left.sum
        self.root = root
        return result

    def splay(self, root, value):
        # Either the root is empty or value already exists as roo
        if root is None or root.value == value:
            return root
        elif root.value > value: # reach for left subtree
            if root.left is None:
                # value is not present in the tree
                return root
            if root.left.value > value:
                # This will bubble up value node as root.left.left
                root.left.left = self.splay(root.left.left, value)
                root = self.right_rotate(root)
            elif root.left.value < value: # Zig Zag (left right case)
                root.left.right = self.splay(root.left.right, value)
                if root.left.right is not None:
                    root.left = self.left_rotate(root.left)
            return root if root.left is None else self.right_rotate(root)
        else:
            if root.right is None:
                return root
            if root.right.value > value:
                root.right.left = self.splay(root.right.left, value)
                if root.right.left is not None:
                    root.right = self.right_rotate(root.right)
            elif root.right.value < value:
                root.right.right = self.splay(root.right.right, value)
                root = self.left_rotate(root)
            return root if root.right is None else self.left_rotate(root)

class Set:
    def __init__(self):
        root = None
        self.splay_tree = SplayTree(root)
        self.splay_tree.root = root

    def insert(self, value):
        self.splay_tree.root = self.splay_tree.insert(self.splay_tree.root, value)

    def delete(self, value):
        self.splay_tree.root = self.splay_tree.delete(self.splay_tree.root, value)

    def search(self, value):
        self.splay_tree.root = self.splay_tree.search(self.splay_tree.root, value)
        if self.splay_tree.root is not None:
            if self.splay_tree.root.value == value:
                return "Found"
        return "Not found"

    def range_sum(self, low, high):
        return self.splay_tree.range_sum(self.splay_tree.root, low, high)

def main(params):
    last_sum_result = 0
    MODULO = 1000000001
    s = Set()
    with open(params, 'r') if len(params) > 1 else sys.stdin as f:
        n = int(f.readline())
        for i in range(n):
            line = f.readline().split()
            if line[0] == "+":
                s.insert((int(line[1]) + last_sum_result) % MODULO)
            elif line[0] == "-":
                s.delete((int(line[1]) + last_sum_result) % MODULO)
            elif line[0] == "?":
                print(s.search((int(line[1]) + last_sum_result) % MODULO))
            elif line[0] == "s":
                res = s.range_sum((int(line[1]) + last_sum_result) % MODULO, (int(line[2]) + last_sum_result) % MODULO)
                print(res)
                last_sum_result = res % MODULO
    sys.exit(0)

params = []
if len(sys.argv) > 1:
    params = sys.argv[1]
threading.Thread(target=main, args=[params]).start()