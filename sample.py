#                  AUTHOR  : SHREY SAINI.
#                  SUBJECT : BST/AVL TREE OPERATIONS, INPUT = RANDOM ARRAY OF INTEGERS.

import sys
import random

class Node:                                     # Node Class Definition.
    def __init__(self, value) -> None:
        self.data = value
        self.left = None
        self.right = None
        self.height = 1

# AVL for now, plan to add Red Black Tree Properties in future.
class Tree:
    def createNode(self, data):                 # create a node.
        return Node(data)

    def get_height(self, node):                 # height.
        if not node:
            return 0
        return node.height

    def get_balance(self, node):                # balance_factors.
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def get_min_val_node(self, node):           # gets min val
        if node is None or node.left is None:
            return node
        return self.get_min_val_node(node.left)

    def insert(self, node, data):               # Node Insertion
        if node is None:
            return self.createNode(data)
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance_factor = self.get_balance(node)
        
        if balance_factor > 1:
            if data < node.left.data:
                return self.right_rotate(node)
            else:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)

        if balance_factor < -1:
            if data > node.right.data:
                return self.left_rotate(node)
            else:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)

        return node

    def left_rotate(self, z):                   # LL Rotate
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):                  # RR Rotate
        y = z.left
        T2 = y.right
        y.right = z
        z.left = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def search(self, node, data):               # Search
        if node is None or node.data == data:
            return node
        if node.data < data:
            return self.search(node.right, data)
        elif node.data > data:
            return self.search(node.left, data)
        else:
            return None
    
    def delete_node(self, node, data):          # Node Deletion
        if not node:
            return node
        elif data < node.data:
            node.left = self.delete_node(node.left, data)
        elif data > node.data:
            node.right = self.delete_node(node.right, data)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            temp = self.get_min_val_node(node.right)
            node.data = temp.data
            node.right = self.delete_node(node.right, temp.data)

        if node is None:
            return node
        
        node.height = 1 + max(self.get_height(node.left),self.get_height(node.right))

        balance_factor = self.get_balance(node)

        if balance_factor > 1:                  # Left Skewed Tree, 
            if self.get_balance(node.left) >= 0:
                return self.right_rotate(node)  # Perform RR Rotation.
            else:                               # Perform LR Rotation.
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)

        if balance_factor < -1:                 # Right Skewed Tree, 
            if self.get_balance(node.right) <= 0:
                return self.left_rotate(node)   # Perform LL Rotation.
            else:                               # Perform RL Rotation.
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)

        return node
    
    def pre_order(self, root):                  # Pre-Order Traversal              
        if root is not None:
            print(root.data)
            self.pre_order(root.left)
            self.pre_order(root.right)
    
    def in_order(self, root):                   # In-Order Traversal
        if root is not None:
            self.in_order(root.left)
            print(root.data)
            self.in_order(root.right)
    
    def post_order(self, root):                 # Post-Order Traversal
        if root is not None:
            self.post_order(root.left)
            self.post_order(root.right)
            print(root.data)

    def printHelper(self, curr, indent, last):  # To better visualize the tree structure of the BST/AVL Tree.
        if curr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(curr.data)
            self.printHelper(curr.left, indent, False)
            self.printHelper(curr.right, indent, True)

def main():

    myTree = Tree()
    root = None
    nums = [random.randint(0, 100) for _ in range(10)]
    # nums = [33, 13, 52, 9, 21, 61, 8, 11]
    for num in nums:
        root = myTree.insert(root, num)
    print(nums)
    myTree.printHelper(root, "", True)

    # print(f'INORDER before deletion   : {myTree.in_order(root)}\n')
    # print(f'PREORDER before deletion  : {myTree.pre_order(root)} \n')
    # print(f'POSTORDER before deletion : {myTree.post_order(root)} \n')

    key = random.choice(nums)
    print(f'Key to delete : {key}')
    
    root = myTree.delete_node(root, key)
    print("After Deletion: ")
    myTree.printHelper(root, "", True)

    # print(f'INORDER after deletion   : {myTree.in_order(root)}\n')
    # print(f'PREORDER after deletion  : {myTree.pre_order(root)} \n')
    # print(f'POSTORDER after deletion : {myTree.post_order(root)} \n')

if __name__ == '__main__':
    main()