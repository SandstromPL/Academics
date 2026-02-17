import networkx as nx
import matplotlib.pyplot as pt

G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_edge(1,2)
for i in range (1,11):
    G.add_edge(i,i+1)

nx.draw(G,with_labels="True")
pt.show()
for node in G.nodes:
    print(G.degree(node))

for node in G.node:
    print(nx.betweenness_centrality(G))