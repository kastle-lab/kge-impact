# Experiment Pipeline

* SKG Generation
* SKG training and evaluation
* SKG training vizualization
* Graph Metric calculation and report


## SKG Generation

### SKG-237

- **Imports**:  
  - `random` and `os` for file operations and randomization.

- **Functions**:  
  - **`parse_centrality(file_path)`**: Parses node degree centralities from `.out` file of FB15k-237 graph-metric .out file that contains its degree centrality number.
  - **`generate_triples(num_triples, num_relationships, num_entities, centrality_constraints=None)`**:  
    Generates unique triples for entities and relationships with optional centrality constraints.  
  - **`split_triples(triples, train_ratio, valid_ratio)`**: Splits triples into training, validation, and test sets.  
  - **`save_to_file(triples, filename)`**: Saves triples to `.tsv` files.

- **Graph Initialization**:  
  - **Entities**: `14,541` unique entities.
  - **Relationships**: `237` unique relationships.
  - **Triples**: `310,114` total triples generated.

- **Centrality Constraints**:  
  - Optional, applies degree centrality data from a `.out` file to specific nodes.

- **Data Splitting**:  
  - Ratios: Training (70%), Validation (20%), Test (10%).  
  - Ensures no overlap between sets.

- **Output**:  
  - Directory: `create-237-1` or `create-237`.  
  - Files: `train.tsv`, `valid.tsv`, and `test.tsv`.

- **Execution**:  
  - Centrality-based: Parses centralities and generates triples with constraints.  
  - Randomized: Generates triples without constraints.

- **Run Instructions**:  
  - Update `centrality_file` path for `.out` file if using constraints.  
  - Execute script with `python <script_name>.py`.


### SKG 4,5 ( and variations ), 6

- **Setup**:  
  - Installs required libraries (e.g., `rdflib`).
  - Defines namespaces and initializes synthetic knowledge graphs (SKGs).

- **Graph Initialization**:  
  - Creates six SKGs: basic (`skg4`, `skg5`, `skg6`) and complex (`skg5r`, `skg5rs`, `skg5rsc`).

- **Node Creation**:  
  - Generates `1000` central nodes and their classes.
  - Links central nodes to peripheral nodes using relationships.

- **Graph Population**:  
  - Adds reified triples and context nodes for complex SKGs.
  - Defines subclass hierarchies for `skg6`.

- **Serialization**:  
  - Saves populated SKGs in `.ttl` format.

- **Triple Splitting**:  
  - Converts `.ttl` files into train, validation, and test `.tsv` files with an 80/10/10 split.

- **Visualization**:  
  - Converts SKGs into NetworkX graphs.
  - Provides static visualizations (NetworkX) and interactive visualizations (PyVis).
  

## SKG Training and Evaluation

*  This repo contains the bash scripts used to train and evaluate all the SKGs, their hyperparameters are different since SKG-237 and SKG-4,5,6 are different in size and density. They are evaluate the same way.


## SKG training data vizualisation of TransE entities and relationships

### t-SNE
- **Install Required Libraries**  
  - Installs the necessary Python libraries:
    - `sklearn` for t-SNE implementation.
    - `matplotlib` for plotting.
    - `numpy` for numerical operations.

- **Load Pre-trained Embeddings**  
  - Loads TransE entity and relation embeddings from `.npy` files located on Google Drive.

- **Combine Embeddings**  
  - Combines entity and relation embeddings into a single array for t-SNE processing.

- **Apply t-SNE Dimensionality Reduction**  
  - Reduces the dimensionality of the combined embeddings to 2D for visualization:
    - `n_components=2`: Reduces embeddings to two dimensions.
    - `perplexity=30`: Sets the t-SNE perplexity parameter.
    - `n_iter=1000`: Runs the optimization for 1000 iterations.

- **Separate Entity and Relation Projections**  
  - Splits the 2D t-SNE results into separate arrays for entities and relations.

- **Generate a Scatter Plot**  
  - Plots the t-SNE projections:
    - Entities are visualized as blue dots.
    - Relations are visualized as red crosses.
    - Titles, labels, and legends are added for clarity.

- **Save the Visualization**  
  - Saves the generated plot to Google Drive as a `.png` file.

- **Display the Plot**  
  - Optionally displays the plot in the Colab environment.
 

### UMAP

- **Load Pre-trained Embeddings**  
  - Loads TransE entity and relation embeddings from `.npy` files located on Google Drive.

- **Apply UMAP Dimensionality Reduction**  
  - Reduces the dimensionality of the entity embeddings to 2D for visualization:
    - `n_components=2`: Reduces embeddings to two dimensions.
    - `random_state=42`: Ensures reproducibility.

- **Normalize Embeddings for Colormap**  
  - Creates a colormap based on embedding clusters or distances:
    - Normalizes embedding values to adjust for large scale variations (optional).

- **Generate a Scatter Plot**  
  - Plots the UMAP projections of entity embeddings:
    - Points are color-coded based on their position along the first UMAP dimension.
    - A color bar is added to represent embedding values.
    - Titles and axis labels enhance clarity.

- **Save the Visualization**  
  - Saves the generated plot to Google Drive as a `.png` file.

- **Display the Plot**  
  - Optionally displays the plot in the Colab environment.


## Graph Metrics for SKGs, FB15k-237,238,239 and report of statistics

### Merge the split data

- **Define Dataset Paths**  
  - Constructs the full path for each dataset and the output file (`merged.txt`).

- **Merge Dataset Splits**  
  - Opens or creates the `merged.txt` file for each dataset.
  - Sequentially reads the contents of the `train.tsv`, `valid.tsv`, and `test.tsv` files:
    - Checks if each file exists before reading.
    - Writes the contents of each split file into `merged.txt`.


### Graph Metrics calculation

- **Graph Creation**  
  - Reads triples from the `merged.txt` file of each dataset.
  - Constructs a graph using NetworkX:
    - Nodes represent entities.
    - Edges represent relationships between entities, with labels for relations.
  - Skips improperly formatted lines and logs a warning.

- **Calculate Metrics**  
  - Computes key graph statistics:
    - Total number of facts (triples).
    - Number of nodes and edges in the graph.
    - Ratio of edges to nodes.
  - Performs parallel computation of centrality measures using `ProcessPoolExecutor`:
    - **Degree Centrality**: Measures the number of direct connections each node has.
    - **Betweenness Centrality**: Quantifies the importance of a node in terms of paths passing through it.
    - **Closeness Centrality**: Assesses how close a node is to all other nodes.

### Graph Metrics report generation

- **Input Files**: The script reads `.out` files from a specified directory 
- **Metrics Extracted**: 
  - Total number of facts
  - Number of nodes
  - Number of edges
  - Ratio of edges to nodes
  - Degree, Betweenness, and Closeness centrality (min, max, and average)
- **Output**: A CSV file  containing the extracted metrics.







