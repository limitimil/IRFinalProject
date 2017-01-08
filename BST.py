class Node:
    def __init__(self, val):
        self.l_child = None
        self.r_child = None
        self.data = val

def binary_insert(root, node):
    if root is None:
        root = node
    else:
        if root.data > node.data:
            if root.l_child is None:
                root.l_child = node
            else:
                binary_insert(root.l_child, node)
        else:
            if root.r_child is None:
                root.r_child = node
            else:
                binary_insert(root.r_child, node)
def binary_insert_check_unique(root, node):
    if root is None:
        root = node
    else:
        if root.data > node.data:
            if root.l_child is None:
                root.l_child = node
            else:
                binary_insert_check_unique(root.l_child, node)
        elif root.data < node.data:
            if root.r_child is None:
                root.r_child = node
            else:
                binary_insert_check_unique(root.r_child, node)
        else:
            return False
    return True

def in_order_print(root):
    if not root:
        return
    in_order_print(root.l_child)
    print root.data
    in_order_print(root.r_child)

def pre_order_print(root):
    if not root:
        return        
    print root.data
    pre_order_print(root.l_child)
    pre_order_print(root.r_child)  
if __name__ == '__main__': 
    r = Node(3)
    binary_insert_check_unique(r, Node(7))
    binary_insert_check_unique(r, Node(1))
    binary_insert_check_unique(r, Node(5))
    binary_insert_check_unique(r, Node(5))
    print "in order:"
    in_order_print(r)

    print "pre order"
    pre_order_print(r)
