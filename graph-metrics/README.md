# Graph Metrics Interpretation

* This document is for future interpretation of the graph metrics collected from our dataset.

## Node-Edge Ratio

* The bigger the value, the more information flows through the graph. Meaning a node can be connected to other nodes with nultiple edges, making it well-connected.
* If the ratio is close to 1, it just shows that is balanced.
* When the ratio is low/ close to 0, it indicates that the graph is scattered and therefore not well connected since the nodes don't communicate well with each other.

## Degree centrality

* It counts how many edges each node has - the most degree central actor is the one with the most ties.
* In this case, we can figure out how many relationships a particular entity has with other entities in the KG.
* Entities possessing a high degree of centrality may be fundamental notions in a particular domain or field of knowledge [1]. 

## Betweenness centrality

* Betweenness centrality captures which nodes are important in the flow of the network. * It makes use of the shortest paths in the network.
* A node's importance for the smooth movement of commodities in a network increases with its betweenness [1].

## Closeness centrality

* For a given node, is the average distance from that node to all other nodes. Closeness is then the reciprocal of farness (1/farness) [1].

### References

[1. Centrality](https://bookdown.org/markhoff/social_network_analysis/centrality.html)

