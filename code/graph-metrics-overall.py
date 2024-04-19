import csv
import networkx as nx

# Read the graph data from the text file
def read_graph(filename):
  G = nx.Graph()
  with open(filename, 'r') as f:
    for line in f:
      head, edge, tail = line.strip().split('\t')
      G.add_edge(head, tail, type=edge)
  return G



# Compute the metrics of the graph and add them to a dictionary where keys are the metrics and values are the metric values.

def compute_metrics(G):
  metrics = {}

 
  metrics["Number of nodes"] = G.number_of_nodes()
  metrics["Number of edges"] = G.number_of_edges()
  metrics["Ratio edges to nodes"] = round(G.number_of_edges() / G.number_of_nodes(), 2)


    
  metrics["Degree centrality"] = nx.degree_centrality(G)
  metrics["Betweenness centrality"] = nx.betweenness_centrality(G)
  metrics["Closeness centrality"] = nx.closeness_centrality(G)
  return metrics

# Print the results to a csv.
def write_metrics_to_csv(metrics, filename):
  
  with open(filename, 'w', newline='') as csvfile:
    fieldnames = metrics.keys() # The metrics are the headers  
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(metrics)


if __name__ == "__main__":
    
    graph_file = '/Users/andreachristou/Documents/git/kge-impact/dataset/fb15k-238/test.txt' # Adjust path when you run the code for a different dataset and from a different location.

    graph = read_graph(graph_file)

  
    metrics = compute_metrics(graph)

        write_metrics_to_csv(metrics, 'metrics.csv')

    print("Metrics written to metrics.csv")
