# KGE Drift Code 

Just putting all my code here in this directory so I don't lose track of what I'm doing. 

Developed using python version 3.11.11

I went ahead and included a requirements.txt just in case, but really the only thing that should need to be installed is pykeen. I can also just include the environment files, which might be easier.

# generate_drift_data.py
generate_drift_data.py contains functions to train on each dataset and returns an object containing each triple which contain embeddings from each dataset `{ triple->dataset->head[], relation[], tail[] }`

The triples present in the final result represent triples that exist in all three datasets: T<sub>n</sub> ∈ 237 ∪ 238 ∪ 239

e.g.
```
{
    "triple_string": {
        "dataset_237": {"head": embedding[], "relation": embedding[], "tail": embedding[]},
        "dataset_238": {"head": embedding[], "relation": embedding[], "tail": embedding[]},
        "dataset_239": {"head": emebedding[], "relation": embedding[], "tail": embedding[]},
    },
    ...
}
```

Note: the script is pointed to the ../dataset/ directory

# save_drift_data.py
save_drift_data.py calls generate_drift_data.py and saves the results to a json file named drift_data.json. The resulting filesize is quite large, 4.75GB - this is the file you'll want to run

# grab_matrices.py
This script is a demonstration of the deterministic behavior of pykeen when using a fixed seed by calling pipeline() on the 237 dataset with num_epochs=0. It then grabs the matrix and saves to a file. It then does the same thing except with num_epochs set to default.
To set pykeen to deterministic simply set random.seed() and torch.manual_seed() to any number. This seeds all random number generation with a fixed seed ensuring deterministic output. 

# compare_matrices.py
This script compares the files outputted from grab_matrices.py and shows which are identical and which are different. 

# visualization 
Next step is hopefully to take the data and display it, unless tweaks to the generation step are needed.
