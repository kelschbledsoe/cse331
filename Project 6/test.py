from Graph import Graph

g = Graph(101)
# Path
for i in range(100):
    g.insert_edge(i, (i + 1), i + 1)

# Validate
for i in range(101):
    for j in range(i + 1, 101):
        print((i + 1) == j, g.are_connected(i, j), '{0} -> {1}'.format(i, j))
        if (i + 1) == j:
            print(g.are_connected(j, i), '{1} -> {0}'.format(i, j))
        else:
            print(g.are_connected(j, i), '{1} -> {0}'.format(i, j))
        print(g.does_path_exist(i, j), '{0} -> {1}'.format(i, j))
        print(g.does_path_exist(j, i), '{1} -> {0}'.format(i, j))
        p = g.find_min_weight_path(i, j)
        print(j - i, len(p) - 1, '{0} -> {1}'.format(i, j))
print(5050, g.path_weight(g.find_min_weight_path(0, 100)))