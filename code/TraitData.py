import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer, scale
from numpy import number



class TraitData(object):
    """
            A representation of species-level trait data. 
            Input file must be CSV. 
            Options: 
                    dataFile: CSV containing response variable and trait values. 
                    responseVar: name of the variable in dataFile containing the response. 
                    dropFeatures: feature names to be removed from analysis. 
                    encodeFeatures: feature names to be one-hot encoded. 
                    dropNA: None does not drop any NA. 1 drops columns with any NAs. 0 drops rows with any NAs.  Default None. 
    """

    def __init__(self, dataFile, responseVar, dropFeatures,
                 encodeFeatures, dropNA=None, scale=False):
        super(TraitData, self).__init__()
        self.dataFile = dataFile
        self.dropFeatures = dropFeatures
        self.encodeFeatures = encodeFeatures
        self.dropNA = dropNA
        self.responseVar = responseVar
        self.feature_names = []
        self.scale = scale
        self.X, self.Y = self._process_file()

    def _process_file(self):
        master = pd.read_csv(self.dataFile)
        
        # one-hot encoding
        if len(self.encodeFeatures) > 0:
            try:
                master = pd.get_dummies(master, columns=self.encodeFeatures)
            except ValueError:
                print("Warning: One-hot encoding failed (perhaps columns to encode contained NaN).")
        
        # drop features 
        master = master.drop(self.dropFeatures, axis=1)
        
        # Drop NA
        if self.dropNA is not None:
            master.dropna(axis=self.dropNA, inplace=True)

        # scale numeric non-encoded features
        if self.scale:
            for idx, col in enumerate(master.select_dtypes(include=[number]).columns):
                if(col.split("_")[0] not in self.encodeFeatures):
                    master[col] = scale(master[col])
        

        # extract response
        Y = master[self.responseVar]
        master.drop([self.responseVar], inplace=True, axis=1)

        self.feature_names = list(master.columns.values)

        return master, Y

    def train_test_split(self, test_size=None):
        return train_test_split(self.X, self.Y, test_size=test_size)

    def impute_NaN(self):
        imp = Imputer(missing_values='NaN', strategy='mean')
        self.X = imp.fit_transform(self.X)
