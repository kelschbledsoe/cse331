"""
A dynamic program that solves the longest increasing subsequence problem.
Objective: find the longest possible subsequence whose items are stringly increasing.
Method for computing the LIS: In the find_list function, inc_s is a list used to store the items from the seq in
increasing order along with each item's prev item. It stores in increasing order by considering if the list is empty,
if the item is larger than the current largest in the list, and utilizing the helper function find_insert_index. Once
every item in the seq has been checked, the find_path function is called on inc_s to determine the path to create the
subsequence. The result is stored as variable r_path. r_path is reversed for the subsequence to be increasing.
"""


class Item:
    """
    Item class used by LIS to store the data and previous node
    """
    def __init__(self, value, previous):
        """
        Makes new instance of Item class
        :param value: value of Item
        :param previous: previous Item in the increasing subsequence
        """
        self.val = value
        self.prev = previous

    def find_path(self):
        """
        Build path of LIS
        :return: List of previous items in the LIS
        """
        path = [self.val]
        if self.prev is not None:
            # Build the path
            return path+self.prev.find_path()
        return path


def verify_subseq(seq, subseq):
    """
    See if one sequence is subsequence of another
    :param seq: Larger sequence
    :param subseq: Sequence to check
    :return: True or False if sequence is a subsequence of another
    """
    # Use place to know where you are in subsequence
    place = 0
    # Check each char in the sequence
    for char in seq:
        if place == len(subseq):
            return True
        # If you find a character, move to the next
        if char == subseq[place]:
            place += 1
    # Reached the end of the list
    return place == len(subseq)


def verify_increasing(seq):
    """
    See if sequence is in increasing order
    :param seq: Sequence to check
    :return: True or False if seq is increasing
    """
    # Loop through the sequence
    for i in range(len(seq) - 1):
        # Not in increasing order
        if seq[i] >= seq[i + 1]:
            return False
    return True


def find_lis(seq):
    """
    Finds longest increasing subsequence of the given sequence
    :param seq: Sequence to search
    :return: List representing increasing subsequence
    """
    inc_s = []
    for item in seq:
        # If inc_s is empty
        if not inc_s:
            inc_s.append([Item(item, None)])
        # If item is larger than the last largest
        elif inc_s[-1][-1].val < item:
            inc_s.append([Item(item, inc_s[-1][-1])])
        # Figure out where to put the next item
        # Have helper function do a lot of the math
        else:
            index = find_insert_index(inc_s, item, 0, len(inc_s))
            # Set the prev
            if index == 0:
                prev = None
            else:
                prev = inc_s[index-1][-1]
            # Add the item
            inc_s[index].append(Item(item, prev))
    # Build the path then reverse to return it
    r_path = inc_s[-1][-1].find_path()
    r_path.reverse()
    return r_path


### Helper Functions ###


def find_insert_index(seq, item, start, end):
    """
    Find place to put new item
    :param seq: Sequence to search
    :param item: Item to place
    :param start: Start index of where to look
    :param end: End index of where to look
    :return: Index to place item at
    """
    # Middle index
    middle = (end + start)//2
    if (end - start) <= 2:
        # Determine if go on start, end, or after last stack
        if seq and seq[start][-1].val >= item:
            return start
        elif seq and seq[end - 1][-1].val >= item:
            return end - 1
        else:
            return end
    # Look through first half of seq
    elif seq[middle][-1].val > item:
        return find_insert_index(seq, item, 0, middle + 1)
    # Look through second half of sez
    elif seq[middle][-1].val < item:
        return find_insert_index(seq, item, middle, end)
    # If items are equal
    return middle
