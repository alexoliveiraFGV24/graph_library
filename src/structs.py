import math
import matplotlib.pyplot as plt


class Node:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.neighbors = {}

    def add_neighbor(self, neighbor_node, edge_or_weight):
        self.neighbors[neighbor_node] = edge_or_weight


class Edge:
    def __init__(self, node1, node2, weight=1, desc=None):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.desc = desc
        self.representation = (self.node1.index, self.node2.index, self.weight, self.desc)
        
    def __repr__(self):
        return f"Edge({self.node1.index} --({self.weight})--> {self.node2.index})"

 
class UnionFind:
    def __init__(self, n):
        self.parents = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        group_x = self.find(x)
        group_y = self.find(y)
        if group_x == group_y:    
            return 
        if self.rank[group_x] < self.rank[group_y]:
            self.parents[group_x] = group_y
        elif self.rank[group_x] > self.rank[group_y]:
            self.parents[group_y] = group_x
        else:
            self.parents[group_y] = group_x
            self.rank[group_x] += 1
    

class Graph:
    def __init__(self, isDirectd):
        self.nodes = {}
        self.edges = []
        self.isDirected = isDirectd

    def add_node(self, index, value):
        if not self.nodes.get(index):
            node = Node(index, value)
            self.nodes[index] = node

    def add_edge(self, index1, index2, weight, desc):
        if not self.nodes.get(index1) or not self.nodes.get(index2):
            raise ValueError("Os índices dos vértices não existem no grafo")
        node1 = self.nodes[index1]
        node2 = self.nodes[index2]
        edge = Edge(node1, node2, weight, desc)
        self.edges.append(edge)
        node1.add_neighbor(node2, weight)
        if not self.isDirected:
            node2.add_neighbor(node1, weight)

    def build_graph(edges, is_directed=False):
        if not edges:
            return Graph(is_directed)
        graph = Graph(is_directed)
        for v, u, weight in edges:
            graph.add_node(v, v)
            graph.add_node(u, u)
            graph.add_edge(v, u, weight=weight)
        return graph


    def plot_graph(self):
        if not self.nodes:
            raise ValueError("Grafo Vazio")
        positions = {}
        node_objects = list(self.nodes.values())
        num_nodes = len(node_objects)
        for i, node_obj in enumerate(node_objects):
            angle = 2 * math.pi * i / num_nodes
            positions[node_obj] = (math.cos(angle), math.sin(angle))
        for node_obj, (x, y) in positions.items():
            plt.scatter(x, y, color="red", s=120)
            plt.text(x + 0.03, y + 0.03, str(node_obj.value), fontsize=11, weight="bold")
        for node_obj in node_objects:
            x1, y1 = positions[node_obj]
            for neighbor_obj, weight in node_obj.neighbors.items():
                x2, y2 = positions[neighbor_obj]
                if not self.is_directed and node_obj.index > neighbor_obj.index:
                    continue
                if self.is_directed:
                    dx, dy = x2 - x1, y2 - y1
                    plt.arrow(x1, y1, dx, dy, 
                            head_width=0.04, head_length=0.06, 
                            length_includes_head=True, color="black")
                else:
                    plt.plot([x1, x2], [y1, y2], color="black")
                xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                plt.text(xm, ym, str(weight), fontsize=9, color="blue")
        plt.axis("off")
        plt.title(f"Grafo {'Direcionado' if self.is_directed else 'Não Direcionado'} ({num_nodes} Nós)")
        plt.show()