# kge-impact
This repository contains the supporting code and data files for our experiment. 

# code
The scripts found in this directory were developed using `Python 3.7.9`, `3.9.x`, and `3.10.x`. Researchers may need to adjust the scripts to appropriately point to the correct directories.

`test_parse.py` is used to generate `head`, `relation`, and `tail` files, which can be used with `dglke_predict`.

# dataset
## ablation
The data files found in this sub-directory contains the exclusive extension we implemented into fb15k-237 to generate fb15k-238 and -239.

## fb15k-237
The `{train, test, valid}.txt` files are the original files used in the benchmarking dataset FB15k-237

## fb15k-238 and -239
These files can be generated with the script [`code/fb15k237-classifying.py`]. The existing files are the files used in the experiment.