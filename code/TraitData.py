import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


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

    def __init__(self, dataFile, responseVar, dropFeatures, encodeFeatures, dropNA=None):
        super(TraitData, self).__init__()
        self.dataFile = dataFile
        self.dropFeatures = dropFeatures
        self.encodeFeatures = encodeFeatures
        self.dropNA = dropNA
        self.responseVar = responseVar
        self.feature_names = []
        self.X, self.Y = self._process_file()

    def _process_file(self):
        master = pd.read_csv(self.dataFile)
        # one-hot encoding
        if len(self.encodeFeatures) > 0:
            master = pd.get_dummies(master, columns=self.encodeFeatures)

        # extract features
        X = master.drop(self.dropFeatures, axis=1)
        if self.dropNA is not None:
            X.dropna(axis=self.dropNA, inplace=True)

        # extract response
        Y = X[self.responseVar]
        X.drop([self.responseVar], inplace=True, axis=1)

        self.feature_names = X.columns

        return X, Y

    def train_test_split(self, test_size=None):
        return train_test_split(self.X, self.Y, test_size=test_size)
