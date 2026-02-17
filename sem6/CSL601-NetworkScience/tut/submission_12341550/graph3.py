import networkx as nx
import matplotlib.pyplot as pt

G = nx.Graph()
for i in range(0,10):
    G.add_node(i)
G.add_edge(1,5)
G.add_edge(1,4)
G.add_edge(4,5)
G.add_edge(5,0)
G.add_edge(4,0)
G.add_edge(3,2)
G.add_edge(4,2)
G.add_edge(4,3)
G.add_edge(6,2)
G.add_edge(6,7)
G.add_edge(0,7)
G.add_edge(0,2)
G.add_edge(1,9)
G.add_edge(8,9)

nx.draw(G,with_labels="True")
pt.show()

print("Degree:")
for node in G.nodes:
    print(f"Node {node}: {G.degree(node)}")

ecc = nx.eccentricity(G)

print("\nEccentricity:")
for node in G.nodes:
    print(f"Node {node}: {ecc[node]}")

bc = nx.betweenness_centrality(G)

print("\nBetweenness Centrality:")
for node in G.nodes:
    print(f"Node {node}: {bc[node]}")

cc = nx.closeness_centrality(G)

print("\nCloseness Centrality:")
for node in G.nodes:
    print(f"Node {node}: {cc[node]}")