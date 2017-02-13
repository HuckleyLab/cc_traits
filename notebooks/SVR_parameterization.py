import TraitData
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold
from skelarn.model_selection import GridSearchCV
from sklearn.svm import SVR 

### Read the Data

datafile = "../data/plants5.csv"

responseVar = "migration_m"

drop_features = ["Taxon",
                 "migr_sterr_m", 
                 "shift + 2SE", 
                 'signif_shift',
                 "signif_shift2",
                 "dispmode01",
                 "DispModeEng", ## what is this
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
						 dropNA = 1)

X, x_test, Y, y_test = td.train_test_split(0.30) ## get 30% train test split for gridsearch. 

### Set up SVR  + do grid search 

params_grid = {
	'C'     : np.logspace(-3,3,13), 
	'gamma' : np.logspace(-3,3,13)
}

gridSearch = GridSearchCV(base, 
						  params_grid = params_grid, 
						  scoring = SCORING,
						  n_jobs = -1,
						  error_score = 0,
						  cv = KFold(5))

gridSearch.fit(scale(X), Y)