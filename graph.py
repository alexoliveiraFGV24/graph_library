import matplotlib.pyplot as plt
import math
import random


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
        self.adj = {}  # Lista de adjacência: {Node: [(vizinho, peso)]}
        self.adj_matrix = {}  # Matriz de adjacência: {Node: {Node: peso}}

    def add_node(self, node: Node):
        if not isinstance(node, Node):
            raise TypeError("O parâmetro deve ser um objeto Node.")
        if node not in self.nodes:
            self.nodes.append(node)
            self.adj[node] = []
            self.adj_matrix[node] = {}

    def add_edge(self, edge: Edge):
        node1, node2, weight = edge.node1, edge.node2, edge.weight
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
            self.adj_matrix[node1][node2] = weight
        if not self.isDirected and node1 not in self.adj[node2]:
            self.adj[node2].append(node1)
            self.adj_matrix[node2][node1] = weight
        if (node1, node2, weight) not in self.edges:
            self.edges.append((node1, node2, weight))

    def remove_node(self, node: Node):
        if node not in self.nodes:
            return
        for n in list(self.adj.keys()):
            self.adj[n] = [(nbr, w) for nbr, w in self.adj[n] if nbr != node]
            self.adj_matrix[n].pop(node, None)
        del self.adj[node]
        del self.adj_matrix[node]
        self.nodes.remove(node)
        self.edges = [e for e in self.edges if e[0] != node and e[1] != node]

    def remove_edge(self, edge: Edge):
        node1, node2 = edge.node1, edge.node2
        if (node1 not in self.nodes) or (node2 not in self.nodes):
            return
        self.adj[node1] = [(nbr, w) for nbr, w in self.adj[node1] if nbr != node2]
        self.adj_matrix[node1].pop(node2, None)
        if not self.isDirected:
            self.adj[node2] = [(nbr, w) for nbr, w in self.adj[node2] if nbr != node1]
            self.adj_matrix[node2].pop(node1, None)
        self.edges = [
            e for e in self.edges
            if not ((e[0] == node1 and e[1] == node2) or
                    (not self.isDirected and e[0] == node2 and e[1] == node1))
        ]

    def show_adj_matrix(self):
        nodes = list(self.adj_matrix.keys())
        print("\nMatriz de Adjacência:")
        header = "     " + " ".join(f"{n.values:^6}" for n in nodes)
        print(header)
        for u in nodes:
            row = [f"{self.adj_matrix[u].get(v, 0):^6}" for v in nodes]
            print(f"{u.values:^5} {' '.join(row)}")

    def show_adj_list(self):
        print("\nListas de Adjacência:")
        for node, neighbors in self.adj.items():
            vizinhos = ', '.join(f"{nbr.values} (w={w})" for nbr, w in neighbors)
            print(f"{node.values} -> [{vizinhos}]")

    def plot_graph(self):
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

    def random_graph(self, num_nodes, num_edges, prob, isDirected=False):
        G = Graph()
        for i in range(num_nodes):
            G.add_node(i+1)
        for _ in range(num_edges):
            node1 = random.choice(list(G.adj.keys()))
            node2 = random.choice(list(G.adj.keys()))
            if random.random() < prob:
                G.add_edge(node1, node2)
        return G
    
    def is_subgraph(self, G1:'Graph', G2:'Graph'):
        """ Vê se G2 é subgrafo de G1 """
        if not G2:
            return True
        if len(G2.nodes) > len(G1.nodes):
            return False
        for edge_G2 in G2.edges:
            if edge_G2 in G1.edges:
                continue
            else:
                return False
        return True

    def is_path(self, G:'Graph', path:list):
        """ Ver se o caminho path é caminho de G, além de dizer se ele é simples """
        n = len(path)
        if n == 0:
            return True
        for i in range(1, n):
            node = path[i-1]
            node_next = path[i]
            if not node_next in G.adj[node]:
                return False
        return True