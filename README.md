# test-opt-dmd
A repository to test Optimized Dynamic Mode Decomposition (optDMD)

The purpose of this repository is to test the optimized dynamic mode decomposition (optDMD) algorithm proposed by [Askham and Kutz (2018)](https://epubs.siam.org/doi/10.1137/M1124176).

Implementations of the optDMD algorithm can be found in the following repositories:

- [optdmd](https://github.com/duqbo/optdmd), written in MATLAB
- [PyDMD](https://github.com/PyDMD/PyDMD), written in Python. Here we focus on the `BOPDMD` class.

## Getting started

To get started, clone this repository, create a virtual environment, and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the optDMD in Python

Run the script `bopdmd_test.py` to test the `BOPDMD` class from the `PyDMD` package. By default, it will read the pre-generated data in `data/data.mat`, run the optDMD algorithm, and plot the results.

```bash
python bopdmd_test.py
```

You will notice that the algorithm cannot converge on this dataset, and does not provide a good reconstruction of the data. This is due to a bug in the implementation of the `BOPDMD` class.

If you want to test running `BOPDMD` on a different dataset, you can do so using the `SignalGenerator` class.

### Running the optDMD in MATLAB

If you have MATLAB installed, you can run the optDMD algorithm using the `optdmd` package, which is included in this repo as a Git submodule. To run the algorithm, start a MATLAB session in the `optdmd` directory and run the following commands:

```matlab
run setup.m
run examples/optdmd_test.m
```

By default, the algorithm will read the pre-generated data in `data/data.mat` and run the optDMD algorithm. You will notice that in this case, the algorithm converges and accurately captures the dynamics of the data.
