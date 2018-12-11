import pandas as pd
import json
from sys import argv
from os import path
from glob import glob
from ast import literal_eval
import numpy as np

"""
summarize_mse.py | tony cannistra 2018 (tonycan@uw.edu)
for "Enhancing the Power of Traits..."

Intended to be run post-analysis to summarize mean mean_squared_error
values across all datasets for each model type. answers the question:
"how does model X compare to model Y in MSE across all datasets"

Usage:
    python3 summarize_mse.py <JSON data specification file>
                             <results root directory>
                             <optional: dataset name - just look at one>
                             <optional: 'mean' or 'median' for combination
                             (default = 'mean')>

"""

def get_dataset_mses(dsname, rootdir):
    """
        finds MSE data for single dataset
        by looking for ./rootdir/dsname/*.mses.csv
    """
    datapath = path.join(rootdir, dsname.replace(" ", "-"))
    print("searching: {}".format(path.join(datapath, "*mseraw.csv")))


    datafile = glob(path.join(datapath, "*mseraw.csv"))[0]
    print(datafile)
    return(pd.read_csv(datafile, converters={'MSEs': literal_eval}))


def improvement(mses, over = 'OLS', how = 'mean'):
    """
        computes percent improvement in MSE for all methods
        in mses (a dataframe with 'method' and 'MSEs' columns)
        over method <over>

        how: 'mean' to compare means across Methods
             'median' to compare medians across methods
    """
    comparator = np.mean
    if how == 'median':
        comparator = np.median

    OLS = comparator(mses.MSEs[mses.method == over].iloc[0])
    improvement_raw = np.array([comparator(x) for x in mses.MSEs.values]) - OLS

    improvement_pct = np.divide(improvement_raw, OLS) * 100

    mses['improvement_pct'] = improvement_pct
    mses['improvement_raw'] = improvement_raw
    return(mses)



def main():
    # load dataset info
    dsinfo = json.load(open(argv[1])) # argv[1] = json specification file

    print("found datasets: {}".format(
        ", ".join([d['name'].replace(" ", "-") for d in dsinfo])))

    # just one dataset? (argv[3] does not exist)
    dsname = None
    comparator = 'mean'
    try:
        thirdArg = argv[3]
        if (thirdArg not in ['mean', 'median']):
            dsname = thirdArg
        else:
            comparator = argv[3]
            raise Exception()

        print("using dataset \"{}\"".format(dsname))
    except:
        print("using all datasets")

    # mean or median?
    try:
        comparator = argv[4]
    except:
        pass


    # look for dataset mses files

    files = []
    for ds in dsinfo:
        if dsname != None and ds['name'] != dsname:
            # skip all that aren't focal ds if one exists
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
            improvements.append(improvement(file, how = comparator))
        except Exception as e:
            print(e)
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
