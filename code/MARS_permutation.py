import TraitData
from pyearth import Earth
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from permutation_analysis import Permutation
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import numpy as np

benchmark_only = False

datafile = "../data/plants5.csv"

responseVar = "migration_m"

drop_features = ["Taxon",
                 "migr_sterr_m",
                 "shift + 2SE",
                 'signif_shift',
                 "signif_shift2",
                 "dispmode01",
                 "DispModeEng",  # what is this
                 "shift + 2SE",
                 ]

categorical_features = ["oceanity",
                        "dispersal_mode",
                        "BreedSysCode",
                        "Grime"]

td = TraitData.TraitData(datafile,
                         responseVar,
                         drop_features,
                         categorical_features,
                         dropNA=1)

SCORING = "neg_mean_squared_error"

# get 30% train test split for gridsearch.
X, x_test, Y, y_test = td.train_test_split(0.30)

# Set up MARS model

mars = Earth()

# run permutation testing


def evaluation_function(model, features, target):
    return -cross_val_score(model, features, target, cv=KFold(5), scoring=SCORING, n_jobs=1).mean()

permTester = Permutation(mars, td.X, td.Y, evaluation_function, verbose=True)

print("Benchmark:", permTester.benchmark())
if benchmark_only:
        exit(1)

permTester.execute_test(n_tests=1000, threads=40)
plot = sns.distplot(permTester.results, rug=True)
plot.set_xlabel("Mean Squared Error")
plot.set_ylabel("Probability Density")
plot.figure.savefig("permutation_results.png")
plt.close()
plot = sns.boxplot(permTester.results)
plot.figure.savefig("permutation_box.png")

