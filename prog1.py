# required data structures
open_set = set()
closed_set = set()
# store distance from start so far 
distance_from_start = {}
# define a dict that will help track which is the parent while reconstructing the path
parents = {}
# heuristic related data structures and functions
h = {
    'A': 11,
    'B': 6,
    'C': 5,
    'D': 7,
    'E': 3,
    'F': 6,
    'G': 5,
    'H': 3,
    'I': 1,
    'J': 0
}

# graph definition
Graph_nodes = {
    'A': [('B', 6), ('F', 3)],
    'B': [('A', 6), ('C', 3), ('D', 2)],
    'C': [('B', 3), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('E', 8)],
    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
    'F': [('A', 3), ('G', 1), ('H', 7)],
    'G': [('F', 1), ('I', 3)],
    'H': [('F', 7), ('I', 2)],
    'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
}

# function to compute f(n)=g(n)+h(n)
def f(n):
    return distance_from_start[n]+h[n]

# function to get next n
def get_next_n():
    n = None
    for v in open_set:
        if n == None or f(v) < f(n):
            # either if n is not set, or if it seems like path through v is better than currently chosen n
            # at the end of the loop, n will contain most feasible next node
            n = v
    return n

def get_neighbor_m(n):
    # for given node n, we attempt to find a suitable neighbour
    neighbour_set = None
    if n in Graph_nodes:
        neighbour_set = Graph_nodes[n]
    for (m, weight) in neighbour_set:
        # go thru the neighbours
        # find m that is not in open_set and closed_set (a new un-encountered node)
        if m not in open_set and m not in closed_set:
            # add to open_set to explore it
            open_set.add(m)
            # set parent of m to n, since we are now reaching this m from n
            parents[m] = n
            # add to distance_from_start
            distance_from_start[m] = distance_from_start[n] + weight
        # there is also another possibility where node was encountered before but
        # we are now seeing a shorter path to m through n, in which case,
        # we should update the parents[m] to n
        else:
            if distance_from_start[n] + weight < distance_from_start[m]:
                distance_from_start[m] = distance_from_start[n] + weight
                parents[m] = n
                # if m is in closed_set, remove and add to open_set to explore
                if m in closed_set:
                    closed_set.remove(m)
                    open_set.add(m)  

def get_path(start_node, stop_node):
    path = []
    curr_node = stop_node
    while parents[curr_node] != curr_node:
        path.append(curr_node)
        curr_node = parents[curr_node]
    path.append(start_node)
    path.reverse()
    print('Path found: {}'.format(path))
    return path

def aStar(start_node, stop_node): 
    # wkt distance from start for start_node is 0
    distance_from_start[start_node] = 0
    # parent of start is start_node itself
    parents[start_node] = start_node
    # go thru main loop for every node in open_set
    open_set.add(start_node)
    while len(open_set) > 0:
        # i.e, it has elements
        # find n in open_set such that f(n)=g(n)+h(n) is minimum
        n = get_next_n()
        if n == stop_node or Graph_nodes[n] == None:
            pass
            # if this n is end node or doesn't have any neighbours, then continue the loop
        else:
            # else, find suitable neighbour m
            get_neighbor_m(n)
        if n == None:
            # even after continuing the loop, if it still manages to come this far with n=None, 
            # means its the only node, didn't find path
            print('Path does not exist!')
            return None
        if n == stop_node:
            # even after continuing the loop, if it still manages to come this far with n=stop_node, 
            # means we have found a good path, start reconstructing the path
            return get_path(start_node, stop_node)
        # at this point, whatever n is, it will be explored in some way
        # so we can remove it from open_set and add to closed_set
        open_set.remove(n)
        closed_set.add(n)
    # if loop failed, then no path
    print('Path does not exist!')
    return None

aStar('A', 'J')