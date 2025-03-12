import pandas as pd
import numpy as np


class BestModel:
    
    def __init__(self, name, model, scaler, imputer, features):
       self.name = name,
       self.model = model
       self.scaler = scaler
       self.imputer = imputer
       self.features = features
       self.prediction_data = None
       self.X = None
    
    
    def missing_input(self):
        
        
        miss = set(self.features) - set(self.prediction_data.index)
        occ = set(self.features) - set(miss)
        
        data = self.prediction_data.loc[list(occ),:]
        
        if len(miss) > 0:
            df_nan = pd.DataFrame(np.nan, index=list(miss), columns=self.prediction_data.columns)
            data = pd.concat([data, df_nan])
            data = data.loc[list(self.features),:]
        
        self.X = data.T
            
        
        
    def imputation(self):
        
        X_imputed = self.imputer.transform(np.array(self.X)) 
        self.X = X_imputed
    
    def scale(self):
        
        X_scaled = self.scaler.transform(self.X)  # Scaling
        self.X = X_scaled


    def predict(self, data:pd.DataFrame):
        
        self.prediction_data = data
        
        self.missing_input()
        self.imputation()
        self.scale()
        
        predicion = self.model.predict(self.X)
        
        return predicion


        
        