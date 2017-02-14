# Trait Drivers of Geographic Range Shifts 
[Tony Cannistra](http://www.anthonycannistra.com) and the [Buckley Lab](http://faculty.washington.edu/lbuckley) at the University of Washington Department of Biology. 

[angert]: http://onlinelibrary.wiley.com/doi/10.1111/j.1461-0248.2011.01620.x/full

__Problem Statement:__ We have a data set consisting of trait values and historic range shifts for several taxonomies. An [original paper][angert] attempted to examine the influence of these trait values on range shifts using linear modeling, but was largely unsuccessful. The challenge is to develop a method for understanding the interactions between these trait variables and the response variable of range shift. 

__Research Methods Abstract__: Here we address a pressing need, both in theoretical functional ecology and in more applied pursuits, to enhance the power of functional trait data to elucidate drivers of climate-induced geographic range shifts across multiple taxonomic groups. Previous studies attempting to evaluate relationships between traits and range shifts have relied upon linear mixed modeling to assess hypothetical driving relationships. Acknowledging that many geographic range shift responses to trait values are nonlinear in nature, we develop a method which uses nonlinear predictive modeling methods from machine learning to extract more nuanced patterns in trait values to be used in prediction of geographic range shifts. We consider several prediction methods including random forests, support vector regression, and neural networks in pursuit of this goal. Our evaluation framework leverages permutation testing and cross-validation to assess prediction errors on actual historic range shift data. 

__Methods__:

* We use Python to implement several nonlinear regression approaches. 
* We use cross-validation to assess average mean squared error by partitioning our data into training and testing sets and evaluating performance. 
* We use perturbation testing on the input to create a null distribution of random effects in these models. 
* We use the null distribution of these errors to assess algorithm performance. 
* We utilize variable importance measures to assess effect sizes in our predictions, which have the potential to hone feature selection in future geographic range shift modeling approaches. 
