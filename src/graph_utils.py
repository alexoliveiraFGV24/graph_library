from collections import deque
import heapq
import random
from structs import Graph, UnionFind



def dfs_preorder(self, v):
    marcado = [False] * self.num_nodes
    visitados = []
    pilha = [v]
    while pilha:
        v = pilha.pop()
        if not marcado[v]:
            marcado[v] = True
            visitados.append(v)
            for u, weight in reversed(self.graph[v]):
                if weight != 1:
                    raise ValueError("Grafo com pesos diferentes de 1")
                else:
                    if not marcado[u]:
                        pilha.append(u)
    return visitados


# Explorar todos os vértices e arestas percorrendo cada caminho até o final antes de retroceder
# O(V + E)
def dfs_postorder(self, v):
    marcado = [False] * self.num_nodes
    visitados = []
    pilha = [(v, False)]
    while pilha:
        v, processado = pilha.pop()
        if processado:
            visitados.append(v)
            continue
        marcado[v] = True
        pilha.append((v, True)) 
        for u, weight in reversed(self.graph[v]):
            if weight != 1:
                raise ValueError("Grafo com pesos diferentes de 1")
            else:
                if not marcado[u]:
                    pilha.append((u, False))
    return visitados


# Explorar o grafo camada por camada, ou nível por nível, garantindo que:
# todos os vértices a distância 1 do início sejam visitados primeiro,
# depois todos a distância 2,
# depois distância 3,
# e assim por diante.
# O(V + E)
def bfs(self, v):
    marcado = [False] * self.num_nodes
    visitados = []
    fila = deque([v])
    marcado[v] = True
    visitados.append(v)
    while fila:
        v = fila.popleft()
        for u, weight in self.graph[v]:
            if weight != 1:
                raise ValueError("Grafo com pesos diferentes de 1")
            else:    
                if not marcado[u]:
                    marcado[u] = True
                    fila.append(u)
                    visitados.append(u)
    return visitados


# Encontrar a cpt num grafo dirigido e sem pesos negativos
# O((V+E)logV)
def dijsktra_cpt(graph, v, u):
    n = len(graph)
    distancias = [float("inf")] * n
    distancias[v] = 0
    marcados = [False] * n
    heap = []
    heapq.heappush((v, 0))
    while heap:
        v, _ = heapq.heappop(heap)
        if marcados[v]:
            continue
        marcados[v] = True
        for u, peso in graph[v]:
            if peso < 0:
                raise ValueError("Grafo com pesos negativos")
            else:
                if marcados[u]:
                    continue
                if distancias[v] + peso < distancias[u]:
                    distancias[u] = distancias[v] + peso
                    heapq.heappush(heap, (u, distancias[u]))
    return distancias[u]


# Encontrar a cpt num grafo dirigido
# O(VE)
def bellmanford_cpt(self, origem, destino):
    dist = [float("inf")] * self.num_nodes
    dist[origem] = 0
    for _ in range(self.num_nodes - 1):
        atualizado = False
        for v, u, peso in self.graph:
            if dist[v] != float("inf") and dist[v] + peso < dist[u]:
                dist[u] = dist[v] + peso
                atualizado = True
        if not atualizado:
            break
    for (v, u, peso) in self.graph:
        if dist[v] != float("inf") and dist[v] + peso < dist[u]:
            return None
    return dist[destino]


# O((V+E)logV)
def prim_mst(self):
    if self.directed:
        raise ValueError("O grafo é dirigido")
    else:
        marcados = [False] * self.num_nodes
        start = random.randint(0, self.num_nodes-1)
        marcados[start] = True
        heap = []
        mst = []
        soma = 0
        for v, weight in self.graph[start]:
            heapq.heappush(heap, (weight, start, v))
        while heap:
            weight_ab, a, b = heapq.heappop(heap)
            if marcados[b]:
                continue
            mst.append((a, b, weight_ab))
            soma += weight_ab
            marcados[b] = True
            for c, weight_bc in self.graph[b]:
                if not marcados[c]:
                    heapq.heappush(heap, (weight_bc, b, c))
        return mst, soma


# O((V+E)logV)
def kruskal_mst(self):
    if self.directed:
        raise ValueError("O grafo é dirigido")
    else:
        self.edges.sort(key=lambda x: x[2])
        uf = UnionFind(self.num_nodes)
        mst = []
        soma = 0
        for start, end, weight in self.edges:
            if uf.find(start) != uf.find(end):
                uf.union(start, end)
                mst.append((start, end, weight))
                soma += weight
                if len(mst) == self.num_nodes - 1:
                    break
        return mst, soma


# O(V+E)
def conected_components(self):
    pass


def topological_order(self):
    pass


def subgraph(self, other_graph):
    pass


# O(len(path))
def exist_path(self, path):
    for start, end in path:
        pass


def has_cycle(self):
    pass


def fordfulkerson(self):
    pass

def random_graph(self, num_nodes, num_edges, weight_max, prob, isDirected=False):
    G = Graph(isDirected)
    for _ in range(num_nodes):
        G.add_node()
    for _ in range(num_edges):
        node1 = random.randint(0, num_nodes - 1)
        node2 = random.randint(0, num_nodes - 1)
        while node1 == node2:
            node2 = random.randint(0, num_nodes - 1)
        weight = random.randint(1, weight_max)
        if random.random() < prob:
            egde = node1, node2, weight
            G.add_edge(egde)
    return G