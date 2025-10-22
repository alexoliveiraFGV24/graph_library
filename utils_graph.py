from graph import *

def is_subgraph(G1: Graph, G2:Graph):
    return False

# Função para gerar uma rede de Barabasi-Albert
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

def is_path(G: Graph, path):
    """ Ver se é caminho e se ele é simples """
    pass