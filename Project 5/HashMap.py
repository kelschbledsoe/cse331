"""
Algorithm to implement a hash map utilizing a list of lists.
"""


class HashMap:
    """
    A hash map implemented using a list of lists.
    Method for handling hash conditions: chaining. Keep a list of values associated with the same key.
    """
    def __init__(self, load_factor=1.00):
        # You may change the default maximum load factor
        self.max_load_factor = load_factor
        # Other initialization code can go here
        self.nodes = 0      # Number of nodes
        self.table = [[] for _ in range(11)]    # Data structure for Hashmap
        self.bucket = 11       # Number of spots in table

    def __len__(self):
        """
        Length Function
        :return: The number of key-value pairs in the table
        """
        return self.nodes

    def buckets(self):
        """
        Counts the number of slots that your map has for storing items
        :return: Number of slots
        """
        return self.bucket

    def load(self):
        """
        Function to compute the load factor: the average number of items per slot
        :returns: The current load factor of the table
        """
        return self.nodes / len(self.table)

    def __contains__(self, key):
        """
        Test if an association with the given key exists
        :param key: Item to search for
        :return: True is in, False otherwise
        """
        try:
            # See if can get item
            self.__getitem__(key)
            return True
        except KeyError:
            # If does not exist
            return False

    def __getitem__(self, key):
        """
        Determines which value item is associated with a given key
        :param key: Item to get value for
        :return: Value associated w the given key
        """
        # Get bucket
        i = hash(key) % (self.bucket - 1)
        bucket = self.table[i]
        for item in bucket:
            # if item in bucket, return value
            if key == item[0]:
                return item[1]
        # value not found
        raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Setter function - adds associations to the map
        No return
        :param key: Key for new item
        :param value: Value for new item
        """
        # Get bucket
        i = hash(key) % (self.bucket - 1)
        bucket = self.table[i]
        for item in bucket:
            # if key exists, update value
            if key == item[0]:
                item[1] = value
                # see if need to resize
                self.check_size()
                return
        # add key if does not exist
        bucket.append([key, value])
        self.nodes += 1
        self.check_size()

    def __delitem__(self, key):
        """
        Delete function - remove associations from map
        No return
        :param key: Key of pair to be deleted
        """
        # Get bucket
        i = hash(key) % (self.bucket - 1)
        bucket = self.table[i]
        for i, item in enumerate(bucket):
            # delete key
            if key == item[0]:
                bucket.pop(i)
                self.nodes -= 1
                self.check_size()
                return
        # key does not exist
        raise KeyError(key)

    def __iter__(self):
        """
        Make iterator of items
        :return:
        """
        for bucket in self.table:
            for item in bucket:
                # key, value
                yield item[0], item[1]

    def clear(self):
        """
        Clears the table by resetting the variables and making a new table
        """
        self.nodes = 0
        self.table = [[] for _ in range(11)]
        self.bucket = 11

    def keys(self):
        """
        Return list of all keys in table
        :return: list of keys
        """
        # use iterator
        return set(k for k, v in self)

    # supplied methods

    def __repr__(self):
        """
        A string representation of this map
        :return: A string representing this map
        """
        return '{{{0}}}'.format(','.join('{0}:{1}'.format(k, v) for k, v in self))

    def __bool__(self):
        """
        Checks if there are items in the map
        :return True if the map is non-empty
        """
        return not self.is_empty()

    def is_empty(self):
        """
        Checks that there are no items in the map
        :return: True if there are no bindings
        """
        return len(self) == 0

    # Helper functions can go here
    def check_size(self):
        """
        Function to check the size and determine if and how to resize
        """
        # table too big
        if self.load() <= (self.max_load_factor / 4) and self.bucket > 2:
            self.bucket = self.bucket//2
            self.resize(self.bucket)
        # table too small
        if self.load() >= self.max_load_factor:
            self.bucket = 2 * self.bucket - 1
            self.resize(self.bucket)

    def resize(self, size):
        """
        Resize fucntion
        :param size: new size for table
        """
        # store old values
        old = [[k, v] for k, v in self]
        # make new table
        self.table = [[] for _ in range(size)]
        # add values in new table
        for k, v in old:
            self.table[hash(k) % (size-1)].append([k, v])


# Required Function
def year_count(input_hashmap):
    """
    Function to count the number of students born in the given year
    :input: A HashMap of student name and its birth year
    :returns: A HashMap of the year and the number of students born in that year
    """
    # HashMap to store the values
    year_hash = HashMap()
    for (_, value) in input_hashmap:
        try:
            # Count is the number of students born in that year
            # Value is the year
            count = year_hash[value]
            year_hash[value] = count + 1
        except KeyError:
            # If year has not been added to year_hash yet
            year_hash[value] = 1
    return year_hash
