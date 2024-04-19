import os
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt

#  Directory pathing, might need modifications pending where script is ran
input_path = "../dataset"
dataset="fb15k-238"
# dataset="fb15k-239" 
data_path = os.path.join(input_path,f"{dataset}")
data_file = os.path.join(data_path, "test.txt")
print(data_path)

# Parse h,r,t from dataset file
head = []
relation = []
tail  = []

with open(data_file, "r") as inp:
    lines = [ line for line in inp.readlines()]

# Create NetworkX Graph
netx_g = nx.Graph()

for line in lines[0:100]:
    h, r, t = line.split("\t")
    netx_g.add_edge(h, t, label=r)
    
# Graph Stats
total_facts = len(lines)
num_nodes = netx_g.number_of_nodes()
num_edges = netx_g.number_of_edges()

pos = nx.spring_layout(netx_g, seed=42, k=0.9)

print(f'Total Number of Facts: {total_facts}')
print(f'Number of nodes: {num_nodes}')
print(f'Number of edges: {num_edges}')
print(f'Ratio edges to nodes: {round(num_edges / num_nodes, 2)}')

# Visualize NetworkX Graph
pos = nx.spring_layout(netx_g, seed=42, k=0.9)
labels = nx.get_edge_attributes(netx_g, 'label')

## Degree of Centrality
degree_centrality = nx.degree_centrality(netx_g)
for node, centrality in degree_centrality.items():
    print(f'{node}: Degree Centrality = {centrality:.6f}')


## Betweenness
betweenness_centrality = nx.betweenness_centrality(netx_g)
for node, centrality in betweenness_centrality.items():
    print(f'Betweenness Centrality of {node}: {centrality:.4f}')

## Node Closeness
closeness_centrality = nx.closeness_centrality(netx_g)
for node, centrality in closeness_centrality.items():
    print(f'Closeness Centrality of {node}: {centrality:.4f}')

