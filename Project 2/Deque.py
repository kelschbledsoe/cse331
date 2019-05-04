"""
Algorithm to implement a double-ended queue used to store and manipulate
data. Also, implement other methods to modify the deque.
"""
######################
# Deque.py
######################
class Node:
    """
    A node class to be used by the Deque class
    """
    def __init__(self, data):
        #Initialize the nodes
        self.data = data
        self.next_node = None
        self.prev_node = None
    def __repr__(self):
        """Returns a representation of the data of the node """
        return self.data
class Deque:
    """
    A double-ended queue
    """
    def __init__(self):
        """
        Initializes an empty Deque
        """
        self.head = None
        self.tail = None
        self.length = 0
    def __len__(self):
        """
        Computes the number of elements in the Deque
        :return: The size of the Deque
        """
        return self.length
    def peek_front(self):
        """
        Looks at, but does not remove, the first element
        :return: The first element
        """
        #Make sure length != 0, the deque is not empty
        if not self:
            raise IndexError
        else:
            return self.head.data
    def peek_back(self):
        """
        Looks at, but does not remove, the last element
        :return: The last element
        """
        #Make sure length != 0, the deque is not empty
        if not self:
            raise IndexError
        else:
            return self.tail.data
    def push_front(self, e):
        """
        Inserts an element at the front of the Deque
        :param e: An element to insert
        """
        #make the node to add
        new_node = Node(e)
        #make sure the deque is not empty
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            #insert the new node where the head was
            self.head.prev_node = new_node
            new_node.next_node = self.head
            self.head = new_node
        #increment length
        self.length += 1
    def push_back(self, e):
        """
        Inserts an element at the back of the Deque
        :param e: An element to insert
        """
        #make the node to add
        new_node = Node(e)
        #make sure the deque is not empty
        if self.tail is None:
            self.tail = new_node
            self.head = new_node
        else:
            #insert the new node where the tail was
            self.tail.next_node = new_node
            new_node.prev_node = self.tail
            self.tail = new_node
        #increment length
        self.length += 1
    def pop_front(self):
        """
        Removes and returns the first element
        :return: The (former) first element
        """
        #make sure there is a node to pop
        if self.length == 0:
            raise IndexError
        else:
            #store the node to pop
            node_data = self.head.data
            #update the head
            self.head = self.head.next_node
            #check the deque is not empty
            if self.head is not None:
                self.head.prev_node = None
            #decrement length
            self.length -= 1
            return node_data
    def pop_back(self):
        """
        Removes and returns the last element
        :return: The (former) last element
        """
        #make sure there is a node to pop
        if self.length == 0:
            raise IndexError
        else:
            #store the node to pop
            node_data = self.tail.data
            #update the tail
            self.tail = self.tail.prev_node
            #check the deque is not empty
            if self.tail is not None:
                self.tail.next_node = None
            #decrement length
            self.length -= 1
            return node_data
    def clear(self):
        """
        Removes all elements from the Deque
        """
        #Erase pointers to the deque
        self.tail = None
        self.head = None
        #Reset the length
        self.length = 0
    def __iter__(self):
        """
        Iterates over this Deque from front to back
        :return: An iterator
        """
        node = self.head
        #loop until the end of the deque
        while node is not None:
            #return the node's data
            yield node.data
            node = node.next_node
    def extend(self, other):
        """
        Takes a Deque object and adds each of its elements to the back of self
        :param other: A Deque object
        """
        #iterate through other
        for i in other:
            #add each element to the back of self
            Deque.push_back(self, i)
    def drop_between(self, start, end):
        """
        Deletes elements from the Deque that within the range [start, end)
        :param start: indicates the first position of the range
        :param end: indicates the last position of the range(does not drop this element)
        """
        #check the range
        if start < 0 or end > len(self) or start > end:
            raise IndexError
        node_start = self.head
        node_end = self.head
        #find the node at start
        for _ in range(start):
            node_start = node_start.next_node
        #find the node at end
        for _ in range(end):
            node_end = node_end.next_node
        #Delete elements in the range [start, end)
        #Consider all cases
        if node_start == self.head:
            self.head = node_end
            if node_end is not None:
                node_end.prev_node = None
        else:
            node_start.prev_node.next_node = node_end
        if node_end is None:
            node_start = self.tail
        else:
            node_end.prev_node = node_start.prev_node
        #modify length
        self.length -= (end-start)
    def count_if(self, criteria):
        """
        counts how many elements of the Deque satisfy the criteria
        :param criteria: a bool function that takes an element of the Deque
        and returns true if that element matches the criteria and false otherwise
        :return: How many elements satisfy the criteria
        """
        count = 0
        node = self.head
        #iterate through Deque
        while node is not None:
            #if satisfy the criteria
            if criteria(node.data):
                count += 1
            node = node.next_node
        return count
    # provided functions
    def is_empty(self):
        """
        Checks if the Deque is empty
        :return: True if the Deque contains no elements, False otherwise
        """
        return len(self) == 0
    def __repr__(self):
        """
        A string representation of this Deque
        :return: A string
        """
        return 'Deque([{0}])'.format(','.join(str(item) for item in self))
    