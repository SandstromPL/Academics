graph = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]

def check_right(vertex, path, pos):
    if not graph[path[pos-1]][vertex]:
        return False

    for i in range(pos):
        if (path[i] == vertex):
            return False
    return True

def hamCycleBacktrack(path, pos, n):
    if (pos == n):
        return graph[path[pos-1]][path[0]]
    for i in range(1, n):
        if (check_right(i, path, pos) == True):
            path[pos] = i;
            if (hamCycleBacktrack(path, pos+1, n) == True):
                return True
            path[pos] = -1;

    return False

def hamCycle():
    n = len(graph)
    path = [-1]*n

    path[0] = 0
    if (hamCycleBacktrack(path, 1, n) == False):
        return {-1}
    return path

path = hamCycle()
print(path)
