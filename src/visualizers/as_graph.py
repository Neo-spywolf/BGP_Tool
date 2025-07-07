import networkx as nx
import matplotlib.pyplot as plt

def draw_as_paths(paths, prefix):
    G = nx.DiGraph()
    for path in paths:
        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i+1])

    plt.figure(figsize=(10, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=10)
    plt.title(f"AS Path Graph for {prefix}")
    plt.tight_layout()
    plt.show()

