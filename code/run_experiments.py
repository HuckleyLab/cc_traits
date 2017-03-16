import TraitData
from permutation_analysis import Permutation
import argparse
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold

import algos

parser = argparse.ArgumentParser(description="""Runs permutation testing on
                                 various algorithms to elucidate the baseline
                                 effect of traits on range shift
                                 predictability. 
                                 """)
## Data Options
parser.add_argument("traitData", type=str, help="Trait Data CSV File")
parser.add_argument("responseVar", type=str, help="Response Variable Name")
parser.add_argument("--cats", type=str, nargs='*', help="Names of "
                    "categorical variables to be one-hot encoded.")
parser.add_argument("--drop", type=str, nargs='*',
                    help="Names of variables to remove from analysis.", 
                    required=False)

def drop_na_enum(string):
    if string == "feature":
        return 1
    if string == "sample":
        return 0

parser.add_argument("--na", choices=["sample", "feature"],
                    help="Drop N/A values either by sample of feature. "
                    "\"sample\" drops any sample with an N/A feature, and "
                    "\"feature\" drops and feature with an n/a sample")


## Experiment Options
parser.add_argument("--algo", required=True,
                    choices=["SVR", "MARS", "RF", "Linear"], nargs='+',
                    help="Learning Algorithm (Multiple supported)")
parser.add_argument("--perms", default=1000, type=int,
                    help="Number of permutations to run. Default = 1000"
                    "(Optional)", required=False)


args = parser.parse_args()
if args.na:
    args.na = drop_na_enum(args.na) ## convert to number

## TODO: traitdata is redundant here--happens in each file. work on this. 

algo_args = (args.traitData,
             args.responseVar,
             args.drop,
             args.cats,
             args.na)

if "SVR" in args.algo:
    algos.SVR_permutation(*algo_args)

if "MARS" in args.algo:
    algos.MARS_permutation(*algo_args)

if "RF" in args.algo:
    algos.RF_permutation(*algo_args)

if "Linear" in args.algo:
    raise NotImplementedError("Linear Model Not Yet Implemented.")