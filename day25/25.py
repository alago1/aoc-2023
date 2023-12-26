from collections import defaultdict, deque, Counter
from itertools import combinations, cycle
from itertools import product as cartesian_product, count as count_from
from functools import lru_cache, reduce
from math import gcd, prod
from copy import deepcopy
import heapq
import re

try:
    from math import lcm
except ImportError:
    def lcm(*args):
        return reduce(lambda x, y: abs(x * y) // gcd(x, y), args)

def visualize(graph):
    import graphviz
    g = graphviz.Graph('G', filename='graph.gv')
    g.format = 'svg'

    edges = {tuple(sorted((node, edge))) for node, edges in graph.items() for edge in edges}

    for node1, node2 in enumerate(edges):        
        g.edge(node1, node2, label=f'{node1}-{node2}')
    
    g.render('graph.gv').replace('\\', '/')

def parse(filename):
    with open(filename) as file:
        lines = [x.strip().split(': ') for x in file.readlines()]
    
    graph = defaultdict(set)

    for line in lines:
        node, edges = line
        for edge in edges.split(' '):
            graph[node].add(edge)
            graph[edge].add(node)
    
    return dict(graph)

def cheese(graph):
    graph = deepcopy(graph)

    bad_edges = [
        ('mxv', 'sdv'),
        ('gqr', 'vbk'),
        ('klj', 'scr'),
    ]

    for node1, node2 in bad_edges:
        graph[node1].discard(node2)
        graph[node2].discard(node1)

    return graph

def bfs_count(graph):
    start = next(k for k in graph.keys())

    queue = deque([start])
    visited = set()

    while queue:
        node = queue.popleft()
        for edge in graph[node]:
            if edge not in visited:
                visited.add(edge)
                queue.append(edge)
    
    return len(visited)

def part1(graph):
    # The cheesy strategy is to plot the graph as an svg with graphviz
    # then look at the labels of obviously problematic edges
    # and remove them from the graph

    graph = cheese(graph)

    first_comp_node_count = bfs_count(graph)
    other_comp_node_count = len(graph.keys()) - first_comp_node_count

    return first_comp_node_count * other_comp_node_count

def part2(graph):
    pass

if __name__ == '__main__':
    graph = parse('input.txt')
    print(f"Part 1: {part1(graph)}")
    print(f"Part 2: {part2(graph)}")
