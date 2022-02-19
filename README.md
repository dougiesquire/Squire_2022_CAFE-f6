Assessment of CAFE-f6 hindcasts/forecasts
==============================

Skill benchmarking of the CAFE-f6 decadal hindcast/forecast dataset

Project Organization
------------

    ├── LICENSE
    ├── Makefile            <- Makefile with commands like `make data`
    ├── README.md           <- The top-level README for developers using this project.
    ├── data
    │   ├── config          <- Configuration files for processing the raw data
    │   ├── processed       <- The postprocessed data
    │   ├── raw             <- The original, immutable data (or symlinks to them)
    │   └── testing         <- The data used while checking CAFE-f6 forecast reproducibility
    │
    ├── docs                <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── notebooks           <- Jupyter notebooks containing analyses. Numbers are used for ordering
    │                          where appropriate
    │
    ├── references          <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports             <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures         <- Generated graphics and figures to be used in reporting
    │
    ├── environment.yml     <- The environment file for reproducing the conda analysis environment
    │
    ├── setup.py            <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                 <- Source code for use in this project.
    │   ├── __init__.py     <- Makes src a Python module
    │   │
    │   ├── prepare_data.py <- Codes for generating the processed data from the raw data
    │   │
    │   └── utils.py        <- Utility codes, including processing methods required to generate the 
    │                          processed data
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

Data Preparation
----------------
Steps for preparing the various datasets used in this project are specified in yaml files stored in `data/config`. Code for preparing data from a specified yaml file is in `src/prepare_data.py`:
```
$ python src/prepare_data.py -h
usage: prepare_data.py [-h] [--config_dir CONFIG_DIR] [--save_dir SAVE_DIR] config

Process a raw dataset according to a provided config file

positional arguments:
  config                Configuration file to process

optional arguments:
  -h, --help            show this help message and exit
  --config_dir CONFIG_DIR
                        Location of directory containing config file(s) to use,
                        defaults to <project_dir>/data/config/
  --save_dir SAVE_DIR   Location of directory to save processed data to, defaults to
                        <project_dir>/data/processed/
```

To prepare a particular dataset, run:
```
make data config=<name-of-config>
```

