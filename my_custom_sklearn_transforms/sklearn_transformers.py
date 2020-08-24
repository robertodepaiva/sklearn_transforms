from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
import numpy
import pandas

# All sklearn Transforms must have the `transform` and `fit` methods
class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Primeiro realizamos a cópia do dataframe 'X' de entrada
        data = X.copy()
        # Retornamos um novo dataframe sem as colunas indesejadas
        return data.drop(labels=self.columns, axis='columns')


class AjusteDesafio4(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns;

    def fit(self, inputdata, results=None):
        self.calcula(
            inputdata=inputdata, 
            results=results,
            dofit=True)
        return self
    
    def transform(self, inputdata):
        print("transform inputdata.columns = ")
        print(inputdata.columns)
        return self.calcula(
            inputdata=inputdata, 
            results=None,
            dofit=False
        )
        

    #def transform(self, inputdata):
    def calcula(self, inputdata, results=None, dofit=False):
        return inputdata;
