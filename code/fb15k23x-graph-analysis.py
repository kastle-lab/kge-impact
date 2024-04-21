import os
import re
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
'''
    Use NetworkX to generate graph metrics
'''
#  Directory pathing, might need modifications pending where script is ran
input_path = "../dataset"
output_path = "../graph-metrics/output"
#dataset="fb15k-237"
#dataset="fb15k-238"
dataset="fb15k-239" 
trainOrTest = "train"
data_path = os.path.join(input_path,f"{dataset}")
data_file = os.path.join(data_path, f"{trainOrTest}.txt")
print(data_path)

# Parse h,r,t from dataset file
head = []
relation = []
tail  = []

with open(data_file, "r") as inp:
    lines = [ line for line in inp.readlines()]

# Create NetworkX Graph
netx_g = nx.Graph()

for line in lines:
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
with open(os.path.join(output_path, f"{dataset}-{trainOrTest}-deg-centrality.out"), "w") as out:
    for node, centrality in degree_centrality.items():
        out.write(f'{node}: Degree Centrality = {centrality:.6f}\n')
        print(f'{node}: Degree Centrality = {centrality:.6f}')


## Betweenness
betweenness_centrality = nx.betweenness_centrality(netx_g)
with open(os.path.join(output_path, f"{dataset}-{trainOrTest}-betweenness.out"), "w") as out:
    for node, centrality in betweenness_centrality.items():
        out.write(f'Betweenness Centrality of {node}: {centrality:.4f}\n')
        print(f'Betweenness Centrality of {node}: {centrality:.4f}')

## Node Closeness
closeness_centrality = nx.closeness_centrality(netx_g)
with open(os.path.join(output_path, f"{dataset}-{trainOrTest}-node-closeness.out"), "w") as out:
    for node, centrality in closeness_centrality.items():
        out.write(f'Closeness Centrality of {node}: {centrality:.4f}\n')
        print(f'Closeness Centrality of {node}: {centrality:.4f}')

'''
    NetworkX creates output files 
    This script cleans the output files to have results in a single row
'''
##  Clean produced files with regex
input_path = '../graph-metrics/output'
files = os.listdir(input_path)

for f_name in files:
    file_path = os.path.join(input_path, f_name)
    with open(file_path, "r") as inp:
        file_text = inp.read()
        file_text = file_text.replace("\n:", " :") # Regex finds dirty lines and moves to corresponding result

    with open(file_path, "w") as out:
        out.write(file_text)