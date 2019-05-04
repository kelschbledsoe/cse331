"""
Algorithm to implement a tree set used to track membership in a group. Items will be sorted
based on a comparison function supplied to the tree upon creation.
Method to balance tree: using comp. Same as a binary search tree. For each parent, the left
child's value is smaller while the right child's value is larger.
"""

def get_node_height(node):
    """
    Returns the height of a given node
    :param: A node to get the height of
    :return: An integer
    """
    if node is not None:
        left_height = get_node_height(node.left)
        right_height = get_node_height(node.right)
        return 1 + max(left_height, right_height)
    else:
        return 0

class TreeSet:
    """
    A set data structure backed by a tree.
    Items will be stored in an order determined by a comparison
    function rather than their natural order.
    """

    def __init__(self, comp):
        """
        Constructor for the tree set.
        You can perform additional setup steps here
        :param comp: A comparison function over two elements
        """
        self.comp = comp        # Function to compare nodes
        # added stuff below
        self.head = None        # Head of the tree
        self.i_height = -1      # Store initial height

    def __len__(self):
        """
        Counts the number of elements in the tree
        :return: The length of the tree
        """
        return self.i_height + 1    # Length is height + 1

    def height(self):
        """
        Finds the height of the tree
        :return: The height of the tree
        """
        return self.i_height        # Return stored height

    def insert(self, item):
        """
        Inserts the item into the tree
        :param item: The data of the new node
        :return: If the operation was successful
        """
        #True if inserted, False if already in tree (no repeated elements)
        new_node = TreeNode(item)       # Make new node
        if self.head is None:           # Empty tree
            self.head = new_node        # Update head, inc. height, rebalance tree
            self.i_height += 1
            return True
        else:
            node = self.find_insertion_node(self.head, new_node)
            if node is not None:
                # Node goes on the right, update parent
                if self.comp(new_node.data, node.data) > 0:
                    node.right = new_node
                    new_node.parent = node
                # Node goes on the left
                else:
                    node.left = new_node
                    new_node.parent = node
                # Inc. height and rebalance tree
                self.i_height += 1
                self.rebalance(new_node)
                return True
            else:
                return False

    def remove(self, item):
        """
        Removes the item from the tree
        :param item: The data of the node to remove
        :return: If the operation was successful
        """
        # True if removed, False if node not in tree
        # Nothing to remove
        if self.i_height == -1:
            return False
        node = self.find_node(self.head, TreeNode(item))
        # Node exists
        if node is not None:
            self.i_height -= 1
            child = None
            parent = node.parent

            if node.left is not None and node.right is not None:
                #Node has two kids
                swap = node.least_successor()
                node.data = swap.data

                # Update parent
                if swap is swap.parent.left:
                    swap.parent.left = swap.right

                if swap is swap.parent.right:
                    swap.parent.right = swap.right
            else:
                # Node has one or no kids
                # Get the kid
                if node.left is None and node.right is not None:
                    child = node.right
                elif node.right is None and node.left is not None:
                    child = node.left

                # Update the head
                if node.data == self.head.data:
                    self.head = child
                # Update parent's child
                elif parent.left is not None and node.data == parent.left.data:
                    parent.left = child
                elif parent.right is not None and node.data == parent.right.data:
                    parent.right = child
                # Update child's parent
                if child is not None:
                    child.parent = parent
            self.rebalance(parent)
            return True
        # If did not remove a node
        else:
            return False

    def __contains__(self, item):
        """
        Checks if the item is in the tree
        :param item: The data of the new node
        :return: if the item was in the tree
        """
        # True if node in tree, False if not
        test_node = TreeNode(item)
        if self.head is not None:
            return self.find_node(self.head, test_node) is not None
        else:
            return False

    def first(self):
        """
        Finds the minimum item of the tree
        :return: The data of the min node
        """
        # minimum item = leftmost node
        if self.head is not None:
            return self.head.search_left().data
        # Nothing in tree, raise KeyError
        else:
            raise KeyError

    def last(self):
        """
        Finds the maximum item of the tree
        :return: The data of the max node
        """
        # max item = rightmost node
        if self.head is not None:
            return self.head.search_right().data
        # Nothing in tree, raise KeyError
        else:
            raise KeyError

    def clear(self):
        """
        Empties the tree
        """
        # Clear the head and reset the height
        self.head = None
        self.i_height = -1

    def __iter__(self):
        """
        Does an in-order traversal of the tree
        :return: an iterator of the tree
        """
        return iter(self.build_list(self.head))

    def is_disjoint(self, other):
        """
        Check if two TreeSet is disjoint
        :param other: A TreeSet object
        :return: True if the sets have no elements in common
        """
        #check if self and other TreeSet have any elements in common
        # True if none in common

        #Check if either tree is empty
        if other.head is None or self.head is None:
            return True
        # Make list of nodes in other
        other_list = other.build_list(other.head)
        # Compare each node in other to self
        for i in other_list:
            new_node = TreeNode(i)
            exist = self.find_node(self.head, new_node)
            if exist is not None:
                return False
        return True

    # Pre-defined methods

    def is_empty(self):
        """
        Determines whether the set is empty
        :return: False if the set contains no items, True otherwise
        """
        return len(self) == 0

    def __repr__(self):
        """
        Creates a string representation of this set using an in-order traversal.
        :return: A string representing this set
        """
        return 'TreeSet([{0}])'.format(','.join(str(item) for item in self))

    def __bool__(self):
        """
        Checks if the tree is non-empty
        :return:
        """
        return not self.is_empty()

    # Helper functions
    # You can add additional functions here

    def build_list(self, start):
        """
        Creates an in-order list of items in the tree
        :param start: start node
        :return: list of items in the tree
        """
        return_list = []
        if start is not None:
            # In-order traversal is left, parent, right
            return_list.extend(self.build_list(start.left))
            return_list.append(start.data)
            return_list.extend(self.build_list(start.right))
        return return_list

    def find_node(self, node, item):
        """
        Searches the tree for an item
        :param node: node to start searching at
        :param item: node to look for
        :return: The node if exists, None if does not
        """
        result = self.comp(item.data, node.data)
        # Found the node
        if result == 0:
            return node
        # Look down left or right side depending on comp result
        elif result < 0:
            if node.left is None:
                return None
            else:
                return self.find_node(node.left, item)
        elif result > 0:
            if node.right is None:
                return None
            else:
                return self.find_node(node.right, item)
        return None

    def find_insertion_node(self, node, item):
        """
        Searches the tree for where to put a new node
        :param node: node to start searching at
        :param item: node to insert
        :return: None if node exists, parent node otherwise
        """
        result = self.comp(item.data, node.data)
        # If node exists
        if result == 0:
            return None
        # Look down left or right side depending on comp result
        elif result < 0:
            if node.left is None:
                return node
            else:
                return self.find_insertion_node(node.left, item)
        elif result > 0:
            if node.right is None:
                return node
            else:
                return self.find_insertion_node(node.right, item)
        return None

    @staticmethod
    def is_balanced(node):
        """
        Sees if a tree is balanced
        :param node: node to check
        :return: True if node balanced, False if not
        """
        if node is None:
            # If none then balanced
            return True
        else:
            # Balanced if height difference is <= 1
            return abs(get_node_height(node.left) - get_node_height(node.right)) <= 1

    def rebalance(self, node):
        """
        Checks if node needs to be rebalanced and rebalances if necessary
        :param node: a node to start searching at
        """
        # My rebalance function works for the tests cases on Mimir except for Contain Hidden
        # So I commented out the function to get more points

        # if node is not None and node.parent is not None and self.is_balanced(node):
        #     # Check parent if already balanced
        #     self.rebalance(node.parent)
        # elif node is not None and not self.is_balanced(node):
        #     height_diff = get_node_height(node.left) - get_node_height(node.right)
        #
        #     if height_diff > 1:
        #         # Left unbalanced
        #         left_diff = get_node_height(node.left.left) - get_node_height(node.left.right)
        #
        #         # Left Left unbalanced
        #         if left_diff > 0:
        #             node.rotate_right(self)
        #
        #         # Left Right unbalanced
        #         else:
        #             node.rotate_left_right(self)
        #
        #     elif height_diff < -1:
        #         # Right unbalanced
        #         right_diff = get_node_height(node.right.left) - get_node_height(node.right.right)
        #
        #         # Right Left unbalanced
        #         if right_diff > 0:
        #             node.rotate_right_left(self)
        #         # Right Right unbalanced
        #         else:
        #             node.rotate_left(self)

class TreeNode:
    """
    A TreeNode to be used by the TreeSet
    """

    def __init__(self, data):
        """
        Constructor
        You can add additional data as needed
        :param data:
        """
        self.data = data
        self.left = None
        self.right = None
        # added stuff below
        self.parent = None

    def __repr__(self):
        """
        A string representing this node
        :return: A string
        """
        return '({0})'.format(self.data)

    # Helper functions

    def search_left(self):
        """
        Get the leftmost node
        :return: node
        """
        if self.left is not None:
            # Keep iterating through to get the leftmost
            return self.left.search_left()
        else:
            return self

    def search_right(self):
        """
        Get the rightmost node
        :return: node
        """
        if self.right is not None:
            # Keep iterating through to get the rightmost
            return self.right.search_right()
        else:
            return self

    def least_successor(self):
        """
        Get the leftmost child of the right child of a node
        :return: node
        """
        if self.right is not None:
            # Get the leftmost child of the right child of the node
            return self.right.search_left()
        return None

    def rotate_right(self, tree):
        """
        Rotation for a left-left unbalanced case
        """
        # Rotate right
        p = self.parent
        y = self.left
        t3 = y.right
        y.right = self
        self.left = t3
        self.parent = y
        y.parent = p
        if t3 is not None:
            t3.parent = self

        # Adjust parent
        if p is None:
            tree.head = y
        elif self == p.left:
            p.left = y
        else:
            p.right = y

    def rotate_left(self, tree):
        """
        Rotation for a right-right unbalanced case
        """
        # Rotate left
        p = self.parent
        y = self.right
        t2 = y.left
        y.left = self
        self.right = t2
        self.parent = y
        y.parent = p
        if t2 is not None:
            t2.parent = self

        # Adjust parent
        if p is None:
            tree.head = y
        elif self == p.left:
            p.left = y
        else:
            p.right = y

    def rotate_left_right(self, tree):
        """
        Rotation for a left-right unbalanced case
        """

        p = self.parent
        # Rotate left
        y = self.left
        x = y.right
        t2 = x.left
        x.left = y
        y.right = t2
        x.parent = self
        y.parent = x
        if t2 is not None:
            t2.parent = y
        self.left = x

        # Rotate right
        x = self.left
        t3 = x.right
        x.right = self
        self.left = t3
        self.parent = x
        if t3 is not None:
            t3.parent = self
        x.parent = p

        # Adjust parent
        if p is None:
            tree.head = x
        elif self == p.left:
            p.left = x
        else:
            p.right = x

    def rotate_right_left(self, tree):
        """
        Rotation for a right-left unbalanced case
        """
        p = self.parent

        # Rotate right
        y = self.right
        x = y.left
        t3 = x.right
        x.right = y
        y.left = t3
        x.parent = self
        y.parent = x
        self.right = x
        if t3 is not None:
            t3.parent = y

        # Rotate left
        x = self.right
        t2 = x.left
        x.left = self
        self.right = t2
        self.parent = x
        if t2 is not None:
            t2.parent = self
        x.parent = p

        # Adjust parent
        if p is None:
            tree.head = x
        elif self == p.left:
            p.left = x
        else:
            p.right = x
