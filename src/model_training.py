import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors




class ModelTrainer:
    def __init__(self, data:pd.DataFrame, raw_data:pd.DataFrame):
        self.data = data
        self.raw_data = raw_data

    def select_features(self)->pd.DataFrame:
        features = [
            'action', 'currency',
            'location', 'device','amount_in_dollars', 'hour', 'day',
             'txn_time_diff_hours', 'is_same_location', 'is_atm',
            'transaction_risk', 'device_type', 'is_same_device', 'hour_risk', 
            'avg_prev_amount', 'amount_difference_from_avg'
        ]
        self.data = self.data[features]
        return self
    
    
    def encode_categotical_features(self):
        df = self.data.copy()
        currency_map = {
            'none': 0,    
            '$': 1,      
            '€': 2,       
            '£': 3        
        }
        transaction_risk_map = {
            'low': 1,
            'moderate': 2,
            'high': 3
        }
        df['currency'] = df['currency'].map(currency_map)
        df['transaction_risk'] = df['transaction_risk'].map(transaction_risk_map)
        one_hot_encode_features = ['action', 'location', 'device', 'is_atm', 'is_same_device', 'hour_risk', 'device_type', 'is_same_location']
        
        # initialize encoder
        self.onehotencoder = OneHotEncoder(drop='if_binary', sparse=False, handle_unknown='ignore')

        # Fit and transform the data
        encoded_data = self.onehotencoder.fit_transform(df[one_hot_encode_features])
        encoded_cols = self.onehotencoder.get_feature_names_out(one_hot_encode_features)
        encoded_df = pd.DataFrame(encoded_data, columns=encoded_cols, index=df.index)
        final_df = pd.concat([df.drop(one_hot_encode_features, axis=1), encoded_df], axis=1)
        self.data = final_df
        return self


    def scale_numerical_data(self):
        df = self.data.copy()
        # instantiate scaler
        scaler = StandardScaler()

        # select numerical features
        columns = ['amount_in_dollars', 'hour', 'day', 'txn_time_diff_hours', 'avg_prev_amount', 'amount_difference_from_avg']

        #apply scaler
        scaled_array = scaler.fit_transform(df[columns])
        scaled_df = pd.DataFrame(scaled_array, columns=[f"{col}_scaled" for col in columns], index=self.data.index)

        # Combine scaled numerical with original data (dropping original numerics if you prefer)
        df = df.drop(columns, axis=1)
        self.data = pd.concat([df, scaled_df], axis=1)

        return self
    

    def train_model(self, eps):
        
        # Apply DBSCAN with default parameters
        dbscan = DBSCAN(eps=eps, min_samples= ((2 * self.data.shape[1]) - 1))  
        clusters = dbscan.fit_predict(self.data)

        # Add cluster labels to DataFrame
        self.data['cluster'] = clusters
        self.raw_data['cluster'] = clusters
        return self
    

    def convert_to_2d(self):
        df = self.data.copy()
        df = df.drop(['cluster'], axis = 1)

        #initialize pca
        pca = PCA(n_components=2, random_state=360)

        #fit pca
        pca_array = pca.fit_transform(df)
        pca_df = pd.DataFrame(data = pca_array, index=self.data.index)
        pca_df['cluster'] = self.data['cluster']  
        self.data = pca_df
        return self
    

    def get_data(self) -> pd.DataFrame:
        return self.data , self.raw_data


class VisualizeOutput:
    def __init__(self, data):
        self.data = data

    def visualize(self):
        sns.scatterplot(x = self.data[0],y=self.data[1],hue=self.data["cluster"],palette=["red", "blue"])
        plt.show()

