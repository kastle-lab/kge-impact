import os
import networkx as nx
from concurrent.futures import ProcessPoolExecutor
import itertools

input_path = "/home/w535axc/experiment/code"
output_path = "/home/w535axc/experiment/graph-metrics/output"
os.makedirs(output_path, exist_ok=True)

# List of datasets to process, change depending on dataset and path

datasets = ["output-4b","output-5b","output-6b"]
def create_graph(lines):
    netx_g = nx.Graph()
    for i, line in enumerate(lines):
        parts = line.split("\t")
        if len(parts) == 3:
            h, r, t = parts
            netx_g.add_edge(h, t, label=r)
        else:
            print(f"Skipping line {i + 1} due to unexpected format (found {len(parts)} parts): {line}")
    return netx_g

def calculate_and_write_metrics(dataset):
    data_path = os.path.join(input_path, dataset)
    data_file = os.path.join(data_path, "merged.txt")
    output_file = os.path.join(output_path, f"{dataset}-metrics.out")
    print(f"Processing {data_file}")

    try:
        with open(data_file, "r") as inp:
            lines = [line.strip() for line in inp.readlines()]
        print(f"Loaded {len(lines)} lines from {data_file}")
    except FileNotFoundError:
        print(f"File {data_file} not found. Skipping.")
        return

    # Create the graph
    print("Creating graph...")
    netx_g = create_graph(lines)
    print("Graph created.")

   
    total_facts = len(lines)
    num_nodes = netx_g.number_of_nodes()
    num_edges = netx_g.number_of_edges()

    print(f"Graph statistics - Total facts: {total_facts}, Nodes: {num_nodes}, Edges: {num_edges}")

    with open(output_file, "w") as out:
        out.write(f'{dataset}\n')
        out.write(f'Total Number of Facts: {total_facts}\n')
        out.write(f'Number of nodes: {num_nodes}\n')
        out.write(f'Number of edges: {num_edges}\n')
        out.write(f'Ratio edges to nodes: {round(num_edges / num_nodes, 2) if num_nodes > 0 else "N/A"}\n\n')

        # Run centrality calculations in parallel
        print("Starting parallel centrality calculations...")
        with ProcessPoolExecutor() as executor:
            future_deg = executor.submit(nx.degree_centrality, netx_g)
            future_betw = executor.submit(nx.betweenness_centrality, netx_g)
            future_close = executor.submit(nx.closeness_centrality, netx_g)

            print("Calculating Degree Centrality...")
            degree_centrality = future_deg.result()
            print("Degree Centrality calculated.")

            print("Calculating Betweenness Centrality...")
            betweenness_centrality = future_betw.result()
            print("Betweenness Centrality calculated.")

            print("Calculating Closeness Centrality...")
            closeness_centrality = future_close.result()
            print("Closeness Centrality calculated.")

        # Write Degree Centrality
        out.write("Degree Centrality:\n")
        for node, centrality in degree_centrality.items():
            out.write(f'{node}: Degree Centrality = {centrality:.6f}\n')

        # Write Betweenness Centrality
        out.write("\nBetweenness Centrality:\n")
        for node, centrality in betweenness_centrality.items():
            out.write(f'{node}: Betweenness Centrality = {centrality:.4f}\n')

        # Write Closeness Centrality
        out.write("\nCloseness Centrality:\n")
        for node, centrality in closeness_centrality.items():
            out.write(f'{node}: Closeness Centrality = {centrality:.4f}\n')

    print(f"Metrics for {dataset} written to {output_file}")

# Process datasets
for dataset in datasets:
    calculate_and_write_metrics(dataset)
