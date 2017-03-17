import TraitData
from pyearth import Earth
from permutation_analysis import Permutation
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, cross_val_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def evaluation_function(model, features, target):
    return -cross_val_score(model, features, target,
                            cv=KFold(5), scoring='neg_mean_squared_error',
                            n_jobs=1).mean()

def MARS_benchmark(datafile, responseVar, drop_features,
                   categorical_features,
                   dropNA, SCORING='neg_mean_squared_error', split=0.30, 
                   *algoArgs):
    td = TraitData.TraitData(datafile,
                             responseVar,
                             drop_features,
                             categorical_features,
                             dropNA=dropNA)

    # get 30% train test split for gridsearch.

    # Set up MARS model

    mars = Earth(*algoArgs)

    # run permutation testing
    return evaluation_function(mars, scale(td.X), td.Y)


def MARS_permutation(datafile, responseVar, drop_features,
                     categorical_features,
                     dropNA, SCORING='neg_mean_squared_error', split=0.30,
                     permutations=1000,
                     threads=20):
    td = TraitData.TraitData(datafile,
                             responseVar,
                             drop_features,
                             categorical_features,
                             dropNA=dropNA)

    # get 30% train test split for gridsearch.
    X, x_test, Y, y_test = td.train_test_split(0.30)

    # Set up MARS model

    mars = Earth()

    # run permutation testing
    permTester = Permutation(mars, td.X, td.Y,
                             evaluation_function, verbose=True)

    print("Benchmark:", permTester.benchmark())

    permTester.execute_test(n_tests=permutations, threads=threads)
    plot = sns.distplot(permTester.results, rug=True)
    plot.set_xlabel("Mean Squared Error")
    plot.set_ylabel("Probability Density")
    plot.figure.savefig("MARS_permutation_results.png")
    plt.close()
    plot = sns.boxplot(permTester.results)
    plot.figure.savefig("MARS_permutation_box.png")
