<center><h1> Improving range shift predictions: enhancing the power of traits </h1>

[Tony Cannistra](http://www.anthonycannistra.com) and [Lauren Buckley](http://faculty.washington.edu/lbuckley) at the University of Washington Department of Biology.

</center>




[angert]: http://onlinelibrary.wiley.com/doi/10.1111/j.1461-0248.2011.01620.x/full

**Question**: Can nonlinear methods improve the predictive value of species' traits with regard to climate-driven range shifts?

## Abstract

Accurately predicting species’ range shifts in response to environmental change is a central ecological objective and applied imperative. Species’ functional traits are powerful predictors of responses in detailed studies and have thus been extensively incorporated in predictive frameworks such as vulnerability analyses.  In synthetic analyses, traits emerge as significant but weak predictors of species’ range shifts across recent climate change. These studies assume linearity in the relationship between a trait and its function, while detailed empirical work often reveals unimodal relationships, thresholds, and other nonlinearities in many trait-function relationships. We hypothesize that the use of linear modeling approaches fails to capture these nonlinearities and therefore may be under-powering traits to predict range shifts. We evaluate the predictive performance of four different machine learning approaches that can capture nonlinear relationships (ridge-regularized linear regression, ridge-regularized kernel regression, support vector regression, and random forests). We validate our models using four multi-decadal range shift datasets in montane plants, montane small mammals, and marine fish. We show that nonlinear approaches perform substantially better than least-squares linear modeling in reproducing historical range shifts. In addition, using novel model observation and interrogation techniques, we identify trait classes (e.g. dispersal- or diet-related traits) that are primary drivers of model predictions, which is consistent with expectation. However, disagreements among models in the directionality of trait predictors suggests limits to trait-based statistical predictive frameworks. Our results highlight that non-linear approaches promise substantially improved, but potentially still limited, capacity to leverage species traits to predict climate change responses in contexts such as species vulnerability analyses.

## Repository Structure [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HuckleyLab/cc_traits/master)


**[`code/`](./code)**: this folder contains all of the code required to run the analysis, the form of Python Jupyter Notebooks. This repository is Binder-enabled. Click the badge above or in [`code/README.md`](code/README.md) to launch an interactive Jupyter session to run the analysis in your browser.

**[`plots/`](./plots)**: contains final figures contained within the manuscript.

**[`data/`](./data)**: contains the data used to perform this analysis. Citations can be found in the manuscript.

## Analysis Workflow

After cloning this repository, the reproduction of the analysis for this publication is encapsulated into three primary steps.

1. **Perform Main Analysis for Each Dataset**: all analytical steps are encapsulated into `./code/0-Nonlinear-Trait-Modeling.ipynb`. They include:
   * Loading and pre-processing trait data.
   * Running OLS model.
   * Running all non-linear models.
   * Evaluating trait drivers of model predictions.
   * Producing plots of coefficients or Shapley values.
   * Producing MSE plots + boxplots.

   The `0-Nonlinear-Trait-Modeling.ipynb` notebook must be run once per dataset. See the documentation in the notebook for a description.

2. **Produce Summary Coefficient Plots**: after running all datasets through the `0-Nonlinear-Trait-Modeling.ipynb` notebook, the `1-Coefficient-Summary-Plots.ipynb` notebook can be used to produce summary plots comparing the values of the top 10 ranked traits for across datasets and models. The notebook describes this process.

3. **Summarize Performance Improvement**: finally, to compute figures describing the improvement (in MSE) of non-linear methods over the OLS baseline, we use the `./code/summarize_mse.py` code. See the code for documentation.

***Note**: many of the plots in the manuscript have been re-arranged, re-labeled, or otherwise modified from their raw state in graphic design tools to be suitable for publication*.
