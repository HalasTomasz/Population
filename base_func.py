def calc_dist(graph, permutation):
    dis = 0
    for i in range(0, len(permutation)):
        dis = dis + graph[permutation[i]][permutation[(i + 1) % len(permutation)]]['weight']
    return dis

def inversion(permutation, i, j):
    while i < j:
        permutation[i], permutation[j] = permutation[j], permutation[i]
        i += 1
        j -= 1
    return permutation
