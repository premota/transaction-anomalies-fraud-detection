import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt





class EngineerFeatures:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @staticmethod
    def _convert_to_dollars(amount, currency)->'EngineerFeatures':
        if currency == '€':
            amount_dollars = amount * 1.6
            return amount_dollars
        elif currency == '£':
            amount_dollars = amount * 1.33
            return amount_dollars 
        else:
            return amount
    
    def create_amount_in_dollars(self)->'EngineerFeatures':
        self.data['amount_in_dollars'] = self.data.apply(
                                        lambda row: self._convert_to_dollars(row['amount'], row['currency']), axis=1
                                        )
        return self 
    
    def create_date(self)->'EngineerFeatures':
        self.data['date'] = self.data['timestamp'].dt.date 
        return self


    def create_time_features(self)->'EngineerFeatures':
        self.data['hour'] = self.data['timestamp'].dt.hour
        self.data['day'] = self.data['timestamp'].dt.day
        self.data['month'] = self.data['timestamp'].dt.month
        self.data['year'] = self.data['timestamp'].dt.year

        #sort data
        self.data = self.data.sort_values(['user_id', 'timestamp'])
        return self 

    def create_time_diff(self)->'EngineerFeatures':
        # sort data
        self.data = self.data.sort_values(['user_id', 'timestamp'])
        self.data['txn_time_diff_hours'] = (
                                            self.data.groupby('user_id')['timestamp']
                                            .diff()
                                            .dt.total_seconds() / 3600
                                        )
        self.data['txn_time_diff_hours'] = self.data['txn_time_diff_hours'].fillna(-1)
        return self 

    def create_prev_location(self)->'EngineerFeatures':
        # sort data
        self.data = self.data.sort_values(['user_id', 'timestamp'])
        self.data['prev_location'] = self.data.groupby('user_id')['location'].shift()
        return self

    def create_is_same_location(self)->'EngineerFeatures':
        self.data['is_same_location'] = self.data['location'] == self.data['prev_location']
        self.data = self.data.drop(['prev_location'], axis=1)
        return self

    def create_is_atm_flag(self)->'EngineerFeatures':
        self.data['is_atm'] = self.data['atm'].apply(lambda x: True if x == 'atm' else False)

        # drop atm column
        self.data = self.data.drop(['atm'], axis=1)
        return self
    
    def create_transaction_risk(self)->'EngineerFeatures':
        transaction_risk_map = {
                    "cashout": "high",
                    "withdrawal": "high",
                    "refund": "high",
                    "transfer": "high",
                    "debit": "moderate",
                    "purchase": "moderate",
                    "deposit": "low",
                    "top-up": "low"
                        }
        self.data['transaction_risk'] = self.data['action'].map(transaction_risk_map)
        return self 

    def create_device_type(self)->'EngineerFeatures':
        phone_map = {
                    "samsung galaxy s10": "smart",
                    "xiaomi mi 11": "smart",
                    "huawei p30": "smart",
                    "pixel 6": "smart",
                    "iphone 13": "smart",
                    "nokia 3310": "non-smart",
                    "none": "non-smart"
                    }
        self.data['device_type'] = self.data['device'].map(phone_map)
        return self

    def create_is_same_device(self)->'EngineerFeatures':
        # Check if current location is same as previous
        self.data['prev_device'] = self.data.groupby('user_id')['device'].shift()

        # Create feature: is_same_location
        self.data['is_same_device'] = self.data['location'] == self.data['prev_device']
        self.data = self.data.drop(['prev_device'], axis=1)
        return self

    def create_hour_risk(self)->'EngineerFeatures':
        self.data['hour_risk'] = self.data['hour'].apply(lambda x: 'High' if x <= 6 or x >= 22 else 'Low')
        return self

    def create_avg_previous_amount(self)->'EngineerFeatures':
        self.data = self.data.sort_values(['user_id', 'timestamp'])
        self.data['avg_prev_amount'] = (self.data.groupby(['user_id'])['amount_in_dollars']
                                            .apply(lambda x: x.shift().expanding().mean())
                                            .reset_index(level=0,drop=True)
                                            .fillna(self.data['amount_in_dollars']))
        return self
    
    def create_amount_difference_from_avg(self)->'EngineerFeatures':
        self.data['amount_difference_from_avg'] = self.data['amount_in_dollars'] - self.data['avg_prev_amount']
        return self

    def get_data(self) -> pd.DataFrame:
        return self.data 

