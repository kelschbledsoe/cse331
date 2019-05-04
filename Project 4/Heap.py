"""
Algorithm to implement a heap-based priority queue using a list.
"""


class Heap:
    """
    A heap-based priority queue
    Items in the queue are ordered according to a comparison function
    Duplicate elements are allowed
    Implemented the Heap as a list
    Code for len, insert, extract, parent, left, right, min, has_left,
        has_right, sift_down, swap, and sift_up is from pages 377-378 of the textbook
    """

    def __init__(self, comp):
        """
        Constructor
        :param comp: A comparison function determining the priority of the included elements
        """
        self.comp = comp
        # Added Members
        self.data = []

    def __len__(self):
        """
        Finds the number of items in the heap
        :return: The size
        """
        return len(self.data)

    def peek(self):
        """
        Finds the item of highest priority
        :return: The item of highest priority
        """
        return self.data[0]

    def insert(self, item):
        """
        Adds the item to the heap
        :param item: An item to insert
        """
        # Add the item then sift it up until restore heap properties
        self.data.append(item)
        self.sift_up(len(self.data) - 1)

    def extract(self):
        """
        Removes the item of highest priority
        :return: the item of highest priority
        """
        # Check if you can extract something
        if self.is_empty():
            raise IndexError
        # Swap and remove first and last elements
        self.swap(0, len(self.data) - 1)
        item = self.data.pop(-1)
        # Sift down until restore heap properties
        self.sift_down(0)
        return item

    def extend(self, seq):
        """
        Adds all elements from the given sequence to the heap
        :param seq: An iterable sequence
        """
        # Load all items then loop backwards
        self.data.extend(seq)
        for i in range(len(self.data)//2, -1, -1):
            self.sift_down(i)

    def replace(self, item):
        """
        Adds the item the to the heap and returns the new highest-priority item
        Faster than insert followed by extract.
        :param item: An item to insert
        :return: The item of highest priority
        """
        # If length is zero or item is the highest-priority, just return the item
        if not self.data or self.comp(item, self.data[0]):
            return item
        # Append the new item, swap with the highest-priority
        self.data.append(item)
        self.swap(0, len(self.data) - 1)
        # Return the highest-priority and reposition the new item
        highest_priority = self.data.pop(-1)
        self.sift_down(0)
        return highest_priority

    def clear(self):
        """
        Removes all items from the heap
        """
        # Empty the list
        self.data = []

    def __iter__(self):
        """
        An iterator for this heap
        :return: An iterator
        """
        return iter(self.data)

    # Supplied methods

    def __bool__(self):
        """
        Checks if this heap contains items
        :return: True if the heap is non-empty
        """
        return not self.is_empty()

    def is_empty(self):
        """
        Checks if this heap is empty
        :return: True if the heap is empty
        """
        return len(self) == 0

    def __repr__(self):
        """
        A string representation of this heap
        :return:
        """
        return 'Heap([{0}])'.format(','.join(str(item) for item in self))

    # Added methods
    def sift_up(self, i):
        """
        Move elements in the heap until they meet criteria
        :param i: index of element
        """
        p = parent(i)
        # Only swap if not at first element and need to swap
        if i > 0 and self.comp(self.data[i], self.data[p]):
            # Swap
            self.swap(i, p)
            self.sift_up(p)

    def swap(self, i, j):
        """
        Swap two elements in heap
        :param i: index of first elem
        :param j: index of second elem
        """
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def sift_down(self, i):
        """
        Move elements in heap until they meet criteria
        :param i: index
        """
        if self.has_left(i):
            l = left(i)
            smallest_child = l
            # Check if right child is smaller
            if self.has_right(i):
                r = right(i)
                if self.comp(self.data[r], self.data[l]):
                    smallest_child = r
            # Check if swap smallest child
            if self.comp(self.data[smallest_child], self.data[i]):
                self.swap(i, smallest_child)
                self.sift_down(smallest_child)

    def has_left(self, i):
        """
        check if item has left child
        :param i: item to check
        :return: True or False
        """
        return left(i) < len(self.data)

    def has_right(self, i):
        """
        check if item has right child
        :param i: item to check
        :return: True or False
        """
        return right(i) < len(self.data)

# Required Non-heap member function


def find_median(seq):
    """
    Finds the median (middle) item of the given sequence.
    Ties are broken arbitrarily.
    Strategy - extend seq to each heap then do n//2+1 extractions to determine the median
    :param seq: an iterable sequence
    :return: the median element
    """
    # If seq is empty
    if not seq:
        raise IndexError

    # Extend seq to each heap. Affected by lambda
    min_heap = Heap(lambda a, b: a < b)
    min_heap.extend(seq)
    max_heap = Heap(lambda a, b: a > b)
    max_heap.extend(seq)

    # Doing n//2+1 returns the median
    for _ in range(len(max_heap)//2+1):
        max_mid = max_heap.extract()
    for _ in range(len(min_heap)//2+1):
        min_mid = min_heap.extract()

    # If seq is even, can return either median item
    if len(seq)%2 == 1:
        return max_mid
    return min_mid


def parent(i):
    """
    Return the parent index of given index
    :param i: item to get parent of
    :return: index of parent
    """
    return (i - 1) // 2


def left(i):
    """
    Return the left child index of given index
    :param i: item to get left child of
    :return: index of left child
    """
    return 2 * i + 1


def right(i):
    """
    Return the right child index of given index
    :param i: item to get right child of
    :return: index of right child
    """
    return 2 * i + 2
