#!/usr/bin/python3

import unittest

from TreeSet import TreeSet


def natural_order(x, y):
    if x == y:
        return 0
    elif x < y:
        return -1
    else:
        return 1


def reverse_order(x, y):
    return natural_order(y, x)


def case_insensitive_order(x, y):
    return natural_order(x.lower(), y.lower())


class TreeSetTests(unittest.TestCase):

    def test_is_empty(self):
        tree = TreeSet(natural_order)
        self.assertTrue(tree.is_empty())
        tree.insert(0)
        self.assertFalse(tree.is_empty())
        tree.remove(0)
        self.assertTrue(tree.is_empty())

    def test_len(self):
        tree = TreeSet(natural_order)
        self.assertEqual(0, len(tree))
        for i in range(0, 20):
            tree.insert(i)
            self.assertEqual(i + 1, len(tree))
        # 2 points for passing here
        for i in range(0, 20):
            tree.insert(i)
            self.assertEqual(20, len(tree))

    def test_height(self):
        import math
        tree = TreeSet(natural_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        self.assertEqual(-1, tree.height())
        for index, item in enumerate(sequence):
            tree.insert(item)
            self.assertGreaterEqual(index, tree.height())
            self.assertLessEqual(math.floor(math.log2(index + 1)), tree.height())
        # 1 point for passing to here
        self.assertGreaterEqual(8, tree.height()) # 3 points for passing here
        self.assertGreaterEqual(7, tree.height()) # 5 points for passing here

    def test_insert(self):
        tree = TreeSet(natural_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        for item in sequence:
            self.assertFalse(item in tree)
            self.assertTrue(tree.insert(item))
            self.assertTrue(item in tree)
        # 4 points for passing here
        for item in sequence:
            self.assertTrue(item in tree)
            self.assertFalse(tree.insert(item))
            self.assertTrue(item in tree)
        # 8 points for passing here

    def test_remove(self):
        tree = TreeSet(natural_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        for item in sequence:
            tree.insert(item)
        for item in range(-5, 20):
            self.assertTrue(item in tree)
            self.assertTrue(tree.remove(item))
            self.assertFalse(item in tree)
        # 4 points for passing here
        for item in range(-5, 20):
            self.assertFalse(item in tree)
            self.assertFalse(tree.remove(item))
            self.assertFalse(item in tree)
        # 8 points for passing here

    def test_contains(self):
        tree = TreeSet(natural_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        for item in sequence:
            self.assertFalse(item in tree)
            tree.insert(item)
            self.assertTrue(item in tree)
        # 4 points for passing here
        for item in range(-5, 20):
            self.assertTrue(item in tree)
            tree.remove(item)
            self.assertFalse(item in tree)
        # 8 points for passing here

    def test_first(self):
        tree = TreeSet(natural_order)
        self.assertRaises(KeyError, tree.first)
        # 1 point for passing here
        tree.insert(5)
        self.assertEqual(5, tree.first())
        # 2 points for passing here
        tree.insert(7)
        self.assertEqual(5, tree.first())
        tree.insert(3)
        self.assertEqual(3, tree.first())
        tree.insert(6)
        self.assertEqual(3, tree.first())
        tree.insert(4)
        self.assertEqual(3, tree.first())
        tree.insert(8)
        self.assertEqual(3, tree.first())
        tree.insert(9)
        self.assertEqual(3, tree.first())
        tree.insert(2)
        self.assertEqual(2, tree.first())
        tree.insert(1)
        self.assertEqual(1, tree.first())
        tree.insert(0)
        self.assertEqual(0, tree.first())
        # 4 points for passing here

    def test_last(self):
        tree = TreeSet(natural_order)
        self.assertRaises(KeyError, tree.last)
        # 1 point for passing here
        tree.insert(5)
        self.assertEqual(5, tree.last())
        # 2 points for passing here
        tree.insert(7)
        self.assertEqual(7, tree.last())
        tree.insert(3)
        self.assertEqual(7, tree.last())
        tree.insert(6)
        self.assertEqual(7, tree.last())
        tree.insert(4)
        self.assertEqual(7, tree.last())
        tree.insert(8)
        self.assertEqual(8, tree.last())
        tree.insert(9)
        self.assertEqual(9, tree.last())
        tree.insert(2)
        self.assertEqual(9, tree.last())
        tree.insert(1)
        self.assertEqual(9, tree.last())
        tree.insert(0)
        self.assertEqual(9, tree.last())
        # 4 points for passing here

    def test_clear(self):
        tree = TreeSet(natural_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        for item in sequence:
            tree.insert(item)
        self.assertFalse(tree.is_empty())
        tree.clear()
        self.assertTrue(tree.is_empty())
        # 3 points for passing here
        self.assertRaises(KeyError, tree.first)
        self.assertRaises(KeyError, tree.last)
        # 5 points for passing here

    def test_iter(self):
        tree = TreeSet(natural_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        for i in sequence:
            tree.insert(i)
        self.assertEqual(len(sequence), len([x for x in tree]))
        # 2 points for passing here
        for x, y in zip(range(-5, 20), tree):
            self.assertEqual(x, y)
        # 8 points for passing here

    def test_reverse(self):
        tree = TreeSet(reverse_order)
        sequence = [-4, 11, 6, 18, -1, 8, 13, 0, 3, 19, -5, 7, 9, 12, 2, 17, 4, 1, 10, -3, 5, 14, 15, 16, -2]
        for i in sequence:
            tree.insert(i)
        self.assertEqual(19, tree.first())
        self.assertEqual(-5, tree.last())
        # 3 points for passing here
        for x, y in zip(reversed(range(-5, 20)), tree):
            self.assertEqual(x, y)
        # 8 points for passing here

    def test_sequence(self):
        tree = TreeSet(natural_order)
        self.assertTrue(tree.insert(5))
        self.assertTrue(tree.insert(7))
        self.assertTrue(tree.insert(11))
        self.assertFalse(tree.insert(7))
        self.assertEqual(5, tree.first())
        self.assertEqual(11, tree.last())
        self.assertEqual([5, 7, 11], [x for x in tree])
        self.assertTrue(5 in tree)
        self.assertTrue(7 in tree)
        self.assertTrue(11 in tree)
        self.assertFalse(3 in tree)
        self.assertTrue(tree.remove(7))
        self.assertFalse(7 in tree)
        self.assertFalse(tree.remove(7))
        self.assertEqual(2, len(tree))
        self.assertFalse(7 in tree)
        # 4 points for passing here
        tree.clear()
        self.assertTrue(tree.is_empty())
        self.assertFalse(5 in tree)
        self.assertTrue(tree.insert(5))
        self.assertEqual(1, len(tree))
        # 8 points for passing here

    def test_string(self):
        with open('phonetic.txt', 'r') as reader:
            tree = TreeSet(case_insensitive_order)
            for line in reader:
                line = line.strip()
                if line.startswith('+'):
                    tree.insert(line[1:])
                elif line.startswith('-'):
                    tree.remove(line[1:])
            self.assertEqual(26, len(tree))
            self.assertEqual('alfa', tree.first())
            self.assertEqual('Zulu', tree.last())
            # 3 points for passing here
            sol = ['alfa', 'bravo', 'Charlie', 'delta', 'echo', 'foxtrot',
                   'golf', 'hotel', 'India', 'Juliett', 'kilo', 'Lima', 'Mike',
                   'November', 'Oscar', 'papa', 'Quebec', 'Romeo', 'sierra', 'tango',
                   'uniform', 'Victor', 'whiskey', 'x-ray', 'Yankee', 'Zulu']
            for ex, act in zip(sol, tree):
                self.assertEqual(ex, act)
        # 8 points for passing here

    def test_balanced(self):
        import math
        tree = TreeSet(natural_order)
        for i in range(0, 1024):
            tree.insert(i)
            self.assertLessEqual(math.floor(math.log2(i + 1)), tree.height())
            self.assertGreaterEqual(2 * math.floor(math.log2(i + 1)), tree.height())
        # Special : This deals with the complexity.
        # If they pass this, they probably get an 8 on complexity (but check their height function)
        # If the tests take a long time, their height function is probably not constant time


if __name__ == '__main__':
    unittest.main()
