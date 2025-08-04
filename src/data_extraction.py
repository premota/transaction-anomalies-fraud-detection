import pandas as pd
import numpy as np

import re
import textwrap



from src.regex_patterns import (
                                user_id_pattern,
                                time_stamp_pattern,
                                action_pattern,
                                amount_pattern,
                                currency_pattern,
                                location_pattern,
                                device_pattern,
                                atm_pattern
                            )

PATTERN = {
                'user_id_pattern' : user_id_pattern,
                'time_stamp_pattern':time_stamp_pattern,
                'action_pattern' :action_pattern,
                'amount_pattern': amount_pattern,
                'currency_pattern' : currency_pattern,
                'location_pattern' : location_pattern,
                'device_pattern' :device_pattern,
                'atm_pattern' :atm_pattern
}



class DataExtraction:
    def __init__(self, df: pd.DataFrame, pattern: dict):
        self.df = df.copy()
        self.pattern = pattern

    
    def _convert_to_lower(self):
        # Convert all features to lower case
        for col in self.df.select_dtypes(include='object').columns.to_list():
            self.df[col] = self.df[col].str.lower()
        return self.df

    def extract_user_id(self, col: str)->'DataExtraction':
        self.df['user_id'] = self.df[col].apply(lambda x: self.pattern['user_id_pattern'].findall(x)[0])
        return self

    def extract_timestamp(self, col: str)->'DataExtraction':
        self.df['timestamp'] = self.df[col].apply(lambda x: self.pattern['time_stamp_pattern'].findall(x)[0])
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], format='mixed', dayfirst=True  )
        return self
    
    def extract_action(self, col: str)->'DataExtraction':
        self.df['action'] = self.df[col].apply(lambda x: (self.pattern['action_pattern'].findall(x.lower()))[0])
        return self
    
    def extract_amount(self, col: str)->'DataExtraction':
        self.df['amount'] = self.df[col].apply(lambda x: (self.pattern['amount_pattern'].findall(x.lower()))[0])
        self.df['amount'] = self.df['amount'].astype(float)
        return self
    
    def extract_currency(self, col: str)->'DataExtraction':
        self.df['currency'] = self.df[col].apply(
                                lambda x: (self.pattern['currency_pattern'].findall(x))[0] 
                                            if (self.pattern['currency_pattern'].findall(x)) != [] 
                                            else np.nan
                                )
        self.df['currency'] = self.df['currency'].fillna('none')
        return self

    def extract_location(self, col: str)->'DataExtraction':
        self.df['location'] = self.df[col].apply(
                                lambda x: (self.pattern['location_pattern'].findall(x.lower()))[0] 
                                            if (self.pattern['location_pattern'].findall(x.lower())) != [] 
                                            else np.nan
                                )
        self.df['location'] = self.df['location'].fillna('none')
        return self
    
    def extract_device(self, col: str)->'DataExtraction':
        self.df['device'] = self.df[col].apply(
                                lambda x: self.pattern['device_pattern'].findall(x)[0] 
                                            if self.pattern['device_pattern'].findall(x) != [] 
                                            else np.nan
                                )
        self.df['device'] = self.df['device'].fillna('none')
        return self
    
    def extract_atm(self, col: str)->'DataExtraction':
        self.df['atm'] = self.df[col].apply(
                                lambda x: self.pattern['atm_pattern'].findall(x.lower())[0] 
                                            if self.pattern['atm_pattern'].findall(x.lower()) != [] 
                                            else np.nan
                                )
        
        return self
    
    def get_data(self) -> pd.DataFrame:
        self.df = self._convert_to_lower()
        return self.df
    


