import matplotlib.pyplot as plt
import math
import random
import numpy as np


class Node:
    def __init__(self, *values):
        self.values = values if len(values) > 1 else values[0]
        self.adjacent = {}

    def add_edge(self, neighbor, weight=1):
        self.adjacent[neighbor] = weight

    def __repr__(self):
        return f"Node({self.values})"

    def __hash__(self):
        return hash(self.values)


class Edge:
    def __init__(self, node1, node2, weight=1, isDirected=False):
        if not all(isinstance(n, Node) for n in (node1, node2)):
            raise TypeError("As extremidades da aresta devem ser objetos Node.")
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.isDirected = isDirected
        node1.add_edge(node2, weight)
        if not isDirected:
            node2.add_edge(node1, weight)

    def __repr__(self):
        direction = "->" if self.isDirected else "--"
        return f"{self.node1} {direction} {self.node2} (w={self.weight})"


class Graph:
    def __init__(self, isDirected=False):
        self.isDirected = isDirected
        self.nodes = [] 
        self.edges = []
        self.adj = {}  
        self._adj_matrix = np.array([])

    def add_node(self, node: 'Node'):
        if not isinstance(node, Node):
            raise TypeError("O parâmetro deve ser um objeto Node.")
        if node not in self.nodes:
            self.nodes.append(node)
            self.adj[node] = []
            self._update_adj_matrix()

    def add_edge(self, node1: 'Node', node2: 'Node', weight=1):
        self.add_node(node1)
        self.add_node(node2)
        if (node2, weight) not in self.adj[node1]:
            self.adj[node1].append((node2, weight))
        if not self.isDirected and (node1, weight) not in self.adj[node2]:
            self.adj[node2].append((node1, weight))
        self.edges.append((node1, node2, weight))
        self._update_adj_matrix()

    def remove_node(self, node: 'Node'):
        if node not in self.nodes:
            return
        for n in self.adj:
            self.adj[n] = [(nbr, w) for nbr, w in self.adj[n] if nbr != node]
        del self.adj[node]
        self.nodes.remove(node)
        self.edges = [e for e in self.edges if e[0] != node and e[1] != node]
        self._update_adj_matrix()

    def remove_edge(self, node1: 'Node', node2: 'Node'):
        if node1 not in self.nodes or node2 not in self.nodes:
            return
        self.adj[node1] = [(nbr, w) for nbr, w in self.adj[node1] if nbr != node2]
        if not self.isDirected:
            self.adj[node2] = [(nbr, w) for nbr, w in self.adj[node2] if nbr != node1]
        self.edges = [e for e in self.edges if not ((e[0] == node1 and e[1] == node2) or 
                                                   (not self.isDirected and e[0] == node2 and e[1] == node1))]
        self._update_adj_matrix()


    def _update_adj_matrix(self):
        n = len(self.nodes)
        self._adj_matrix = np.zeros((n, n), dtype=float)
        for i, node in enumerate(self.nodes):
            for neighbor, weight in self.adj[node]:
                j = self.nodes.index(neighbor)
                self._adj_matrix[i, j] = weight
                if not self.isDirected:
                    self._adj_matrix[j, i] = weight

    @property
    def adj_matrix(self):
        self._update_adj_matrix()
        return self._adj_matrix

    def show_matrix(self):
        matrix = self.adj_matrix
        labels = [str(node.values) for node in self.nodes]
        print("Matriz de Adjacência:")
        print("    " + "  ".join(labels))
        for i, row in enumerate(matrix):
            print(f"{labels[i]:>3} {row}")

    def show(self):
        print("Listas de Adjacência:")
        for node, neighbors in self.adj.items():
            vizinhos = ', '.join(f"{nbr.values} (w={w})" for nbr, w in neighbors)
            print(f"{node.values} -> [{vizinhos}]")

    def plot(self):
        n = len(self.nodes)
        if n == 0:
            print("Grafo vazio.")
            return
        positions = {}
        nodes_list = list(self.nodes)
        for i, node in enumerate(nodes_list):
            angle = 2 * math.pi * i / n
            positions[node] = (math.cos(angle), math.sin(angle))
        for node, (x, y) in positions.items():
            plt.scatter(x, y, color="red", s=120)
            plt.text(x + 0.03, y + 0.03, str(node.values), fontsize=11, weight="bold")
        for node, neighbors in self.adj.items():
            for neighbor, weight in neighbors:
                x1, y1 = positions[node]
                x2, y2 = positions[neighbor]
                if self.isDirected:
                    dx, dy = x2 - x1, y2 - y1
                    plt.arrow(x1, y1, dx, dy, head_width=0.05, length_includes_head=True, color="black")
                else:
                    plt.plot([x1, x2], [y1, y2], color="black")
                xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                plt.text(xm, ym, str(weight), fontsize=9, color="blue")
        plt.axis("off")
        plt.show()

    def is_subgraph(G1, G2):
        """ Comparar as entradas das matrizes de adjacência (O(|V'|²)) """
        return False

    def random_graph(num_nodes, num_edges, prob, isDirected=False):
        G = Graph()
        for i in range(num_nodes):
            G.add_node(i+1)
        for _ in range(num_edges):
            node1 = random.choice(list(G.adj.keys()))
            node2 = random.choice(list(G.adj.keys()))
            if random.random() < prob:
                G.add_edge(node1, node2)
        return G

    def is_path(self, G, path:list):
        """ Ver se é caminho e se ele é simples """
        pass