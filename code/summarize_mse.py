import pandas as pd
import json
from sys import argv
from os import path
from glob import glob
from ast import literal_eval
import numpy as np


def get_dataset_mses(dsname, rootdir):
    datapath = path.join(rootdir, dsname.replace(" ", "-"))
    print("searching: {}".format(path.join(datapath, "*.mses.csv")))

    datafile = glob(path.join(datapath, "*mseraw.csv"))[0]
    return(pd.read_csv(datafile, converters={'MSEs': literal_eval}))


def improvement(mses, over = 'OLS'):
    OLS = np.mean(mses.MSEs[mses.method == over].iloc[0])
    improvement_raw = np.array([np.mean(x) for x in mses.MSEs.values]) - OLS

    improvement_pct = np.divide(improvement_raw, OLS) * 100

    mses['improvement_pct'] = improvement_pct
    mses['improvement_raw'] = improvement_raw
    return(mses)



def main():
    # load dataset info
    dsinfo = json.load(open(argv[1]))
    print("found datasets: {}".format(
        ", ".join([d['name'].replace(" ", "-") for d in dsinfo])))


    # just one dataset?
    dsname = None
    try:
        dsname = argv[3]
        print("using dataset \"{}\"".format(dsname))
    except:
        print("using all datasets")

    # look for dataset mses files

    files = []
    for ds in dsinfo:
        if dsname != None and ds['name'] != dsname:
            # skip all that aren't focal ds
            continue;
        try:
            files.append(get_dataset_mses(ds['name'], argv[2]))
        except Exception:
            print("Error finding MSEs for dataset {}".format(ds['name']))
            continue

    # compute improvement over OLS over all methods
    improvements = []
    for file in files:
        try:
            improvements.append(improvement(file))
        except:
            continue
    improvements = pd.concat(improvements)

    # compute average improvement across datasets for all methods:
    methods = improvements.method.unique()
    for method in methods:
        avg_improvement_pct = np.mean(improvements.improvement_pct[improvements.method == method].values)
        avg_improvement_raw = np.mean(improvements.improvement_raw[improvements.method == method].values)
        print("average improvement of {} over OLS is {}% (raw: {})".format(method, avg_improvement_pct, avg_improvement_raw))




if __name__ == "__main__":
    exit(main())
