import sys
import random

class Node():
    def __init__(self, value) -> None:
        self.data = value
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1          # 1 = Red, 0 = Black

class RBTree():
    def __init__(self) -> None:
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def pre_order_helper(self, node):
        if node != self.TNULL:
            sys.stdout.write(str(node.data) + " ")# print(str(node.data) + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    def in_order_helper(self, node):
        if node != self.TNULL:
            self.in_order_helper(node.left)
            sys.stdout.write(str(node.data) + " ")
            self.in_order_helper(node.right)
    
    def post_order_helper(self, node):
        if node != self.TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(str(node.data) + " ")
    
    def search_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node
        
        if key < node.data:
            return self.search_helper(node.left, key)
        return self.search_helper(node.right, key)

    def pre_order(self):
        self.pre_order_helper(self.root)
        print('\n')

    def in_order(self):
        self.in_order_helper(self.root)
        print('\n')

    def post_order(self):
        self.post_order_helper(self.root)
        print('\n')
    
    def search(self, k):
        return self.search_helper(self.root, k)

    def min_node(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node
    
    def max_node(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node
    
    def predecessor(self, x):
        if x.left != self.TNULL:
            return self.max_node(x.left)
        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent
        return y
    
    def successor(self, x):
        if x.right != self.TNULL:
            return self.min_node(x.right)
        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y
    
    def insert_helper(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:           #    1
                u = k.parent.parent.left                    #       3
                if u.color == 1:                            #    2
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u= k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right
        
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return
        
        if node.parent.parent == None:
            return
        self.insert_helper(node)
        
    def get_root(self):
        return self.root
    
    def delete(self, data):
        self.delete_helper(self.root, data)

    def print_tree(self):
        self.__print_helper(self.root, '', True)

    def delete_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node
            if node.data < key:
                node = node.right
            else:
                node = node.left
        if z == self.TNULL:
            print("NODE NOT PRESENT IN TREE")
            return
        
        y = z
        y_og_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.min_node(z.right)
            y_og_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            
            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_og_color == 0:
            self.delete_fix(x)
    
    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent


# MY USER SPECIFIC SCENARIO:
if __name__ == '__main__':
    RBT = RBTree()
    # Change the value of nums2 to your user specific needs to check for Red-Black Tree Operations
    nums2 = [27, 56, 77, 69, 55, 21, 31, 43, 89, 97]

    # To make a Red-Black of specific values use this, for user specific inputs:
    def specific_nodes():
        # num_element = 10
        for i in range(len(nums2)):
            RBT.insert(nums2[i])
        print(f"NODES IN TREE : {nums2}")
        del_key2 = int(input("Enter the node to be deleted : "))
        return del_key2

    # For random values to be inserted in a Red-Black Tree:
    def rand_nodes():
        num_elements = int(input("ENTER NUMBER OF NODES IN TREE : "))
        nums = [random.randint(0, 101) for _ in range(num_elements)]
        for i in range(len(nums)):
            RBT.insert(nums[i])
        print(f'INPUT ARRAY : {num_elements}')
        del_key = random.choice(nums)
        return (nums, del_key)

    def display(num_elements, del_key):
        print('-'*len(num_elements)*3)
        print( 'Tree after Insetions of elements :')
        RBT.print_tree()
        print('\n')

        print('-'*len(num_elements)*3)
        print(f"Tree after Deletion of {del_key}, chosen randomly :")
        RBT.delete(del_key)
        RBT.print_tree()
        print('\n')

        print('-'*len(num_elements)*3)
        print(f'IN-ORDER Traversal   : ')
        RBT.in_order()

        print('-'*len(num_elements)*3)
        print(f'PRE-ORDER Traversal  : ')
        RBT.pre_order()

        print('-'*len(num_elements)*3)
        print(f'POST-ORDER Traversal : ')
        RBT.post_order()

        print('-'*len(num_elements)*3)

    print("For Random Inputs enter 1  / For User Specific input enter 0  / To End input -1: ")
    flag = input("Enter Value : ")

    if flag == '0':
        # Use this for your user specific inputs:
        del_key2 = specific_nodes()
        display(nums2, del_key2)
        nums2.remove(del_key2)

    elif flag == '1':
        # For random inputs:
        nums, del_key = rand_nodes()
        display(nums, del_key)    
            
    else:
        print("INVALID CHOICE")