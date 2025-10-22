import matplotlib.pyplot as plt
import math
import random


# TODO:
# Adaptar para colocar peso nas arestas


""" Classe para a representação de um nó """
class Node:
    def __init__(self, *values):
        self.values = values


""" Classe para a representação de uma aresta """
class Edge:
    def __init__(self, node1, node2, weight=1, isDirected=False):
        self.weight = weight
        if isDirected:
            pass
        else:
            pass


""" Classe com métodos básicos de um grafo """
class Graph:
    def __init__(self, isDirected=False):
        self.adj = dict()  # Dicionário de adjacência
        self.adj_matrix = []
        self.isDirected = isDirected

    # Função para adicinar um novo nó no grafo (inicializo a lista de adjacência do nó como vazia)
    def add_node(self, value):
        if value not in self.adj:
            self.adj[value] = list()

    # Função para adicionar uma nova aresta (atualizo a lista de adjacência dos nós, conforme a direção do grafo)
    def add_edge(self, node1, node2, weight=1):
        self.add_node(node1.values)
        self.add_node(node2.values)
        self.adj[node1.values].append((node2.values, weight))
        if not self.isDirected:
            self.adj[node2.values].append((node1.values, weight))

    def remove_edge(self, node1, node2, weight):
        pass

    # Função para mostrar as adjacências dos nós
    def show(self):
        for node in self.adj:
            print(f"{node} -> {self.adj[node]}")

    # Função para plotar o grafo
    def plot(self):

        # Nós do grafo
        nodes = list(self.adj.keys())
        n = len(nodes)
        positions = {}

        # Coloca os nós em um círculo
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / n
            positions[node] = (math.cos(angle), math.sin(angle))

        # Plota as posições dos nós (gráfico de dispersão)
        for node, (x, y) in positions.items():
            plt.scatter(x, y, color="red", s=100)
            plt.text(x + 0.03, y + 0.03, str(node), fontsize=12)

        # Plota as arestas
        for node, neighbors in self.adj.items():
            for neighbor in neighbors:
                x1, y1 = positions[node]
                x2, y2 = positions[neighbor]
                if self.isDirected: # Desenhando a direção das arestas
                    dx = x2 - x1
                    dy = y2 - y1
                    plt.arrow(x1, y1, dx, dy, head_width=0.03, length_includes_head=True, color="black")
                else:
                    plt.plot([x1, x2], [y1, y2], color="black")

        # Tirando os eixos e mostrando o plot
        plt.axis('off')
        plt.show()