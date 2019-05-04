"""
Algorithm to sort a list of People alphabetically
Can sort by first or last name
"""
class Person:
    """
    Class for elements of data
    Person.first is first name
    Person.last is last  name
    Person.email is their email
    """
    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email
    def __str__(self):
        return '{0} {1} <{2}>'.format(self.first, self.last, self.email)
    def __repr__(self):
        return '({0}, {1}, {2})'.format(self.first, self.last, self.email)
    def __eq__(self, other):
        return self.first == other.first and self.last == other.last and self.email == other.email
def merge(left, right, ordering):
    """
    Merges two lists in alphabetical order
    :param a: a list of People
    :param b: a list of People
    :param c: a function that orders two People
    :return: a merged list of param a and b, and a count of the comparisons
    """
    merged = []
    count = 0
    while left and right:
        #count of number of comparisons made
        count += 1
        #Get the correct name from either side
        if ordering(left[0], right[0]):
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
    #Add remaining names to the merged list
    if left:
        merged += left
    if right:
        merged += right
    #the merged list and count
    return merged, count
def merge_sort(roster, ordering):
    """
    Sorts roster using the ordering function and merge sort
    :param a: a list of People
    :param b: a function that orders two people
    :return: a sorted version of roster
    """
    count = 0
    #already sorted if only one item
    if len(roster) <= 1:
        return roster, count
    #Sort left and right sides
    left, l_count = merge_sort(roster[len(roster)//2:], ordering)
    right, r_count = merge_sort(roster[:len(roster)//2], ordering)
    #Merge the lists
    merged_list, m_count = merge(left, right, ordering)
    #Add the counts
    count += l_count + r_count + m_count
    #the merged list and count
    return merged_list, count
def order_first_name(a, b):
    """
    Orders two people by their first names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    if (a.first < b.first) or (a.first == b.first and a.last < b.last):
        return True
    return False
def order_last_name(a, b):
    """
    Orders two people by their last names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    if (a.last < b.last) or (a.last == b.last and a.first < b.first):
        return True
    return False
def is_alphabetized(roster, ordering):
    """
    Checks whether the roster of names is alphabetized in the given order
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: True if the roster is alphabetized and False otherwise
    """
    for i in range(1, len(roster)):
        if roster[i-1] == roster[i]:
            continue
        elif not ordering(roster[i-1], roster[i]): #if not ordered
            return False
    return True
def alphabetize(roster, ordering):
    """
    Alphabetizes the roster according to the given ordering
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: a sorted version of roster
    :return: the number of comparisons made
    """
    roster, count = merge_sort(roster, ordering)
    return (list(roster), count)
