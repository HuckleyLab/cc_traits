The code to produce the analyses in this report is documented in two Jupyter notebooks:

1. [`0-Nonlinear-Trait-Modeling.ipynb`](./0-Nonlinear-Trait-Modeling.ipynb): describes the main analysis. Each run of this notebook produces, for a single dataset, a folder (`{dataset-name}-{timestamp/`) containing:
   * k-fold cross-validated means of coefficients, ordered by mean rank for each trait across methods (`{dataset-name}-coefs.csv`)
   * a plot of individual model coefficients, ranked (`{dataset-name}-{model}-ranks.png`)
   * a plot comparing cross-validated mean MSE values across methods (`{dataset-name}-msecompare.png`)
   * a boxplot demonstrating the distribution of MSE values in cross-validation for all methods (`{dataset-name}-msecompare-boxplot.png`)
1. [`1-Coefficient-Summary-Plots.ipynb`](./1-Coefficient-Summary-Plots.ipynb): describes the creation of plots comparing coefficient values across methods and datasets. Each run of this notebook produces a summary plot of the top 10 traits by coefficient rank across methods.

There are also two supporting files.

* `TraitData.py`, which is a supporting module for reading and processing the trait data files. See file for documentation.
* `summarize_mse.py`: compares mean model MSE performance across datasets to produce average performance improvement statistics. See file for documentation.

This code runs live in a browser using Binder. Click the badge below to start an interactive Jupyter session and run the notebooks.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HuckleyLab/cc_traits/master)
