import pandas as pd
import numpy as np

import re
import textwrap

import matplotlib.pyplot as plt
import seaborn as sns
import os

import warnings
warnings.filterwarnings('ignore')  

from src.feature_engineering import EngineerFeatures
from src.data_extraction import DataExtraction
from src.model_training import ModelTrainer
from src.model_training import VisualizeOutput
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

# Define Regular Expression patterns
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


if __name__ == "__main__":
    # read and prepare data
    data = pd.read_csv("fraud_tools_team_ds_test/synthetic_dirty_transaction_logs.csv")
    data['raw_log'] = data['raw_log'].apply(lambda x: np.nan if x == 'MALFORMED_LOG' else x)
    data = data.dropna(subset=['raw_log'], ignore_index=True)

    # extract features from transaction log
    extractor = DataExtraction(df=data, pattern=PATTERN)
    df = (  
            extractor
            .extract_user_id('raw_log')
            .extract_timestamp('raw_log')
            .extract_action('raw_log')
            .extract_amount('raw_log')
            .extract_currency('raw_log')
            .extract_location('raw_log')
            .extract_device('raw_log')
            .extract_atm('raw_log')
            .get_data()
        )
    
    # engineer more features
    eng_features = EngineerFeatures(df)
    df = (
            eng_features
            .create_amount_in_dollars()
            .create_date()
            .create_time_features()
            .create_time_diff()
            .create_prev_location()
            .create_is_same_location()
            .create_is_atm_flag()
            .create_transaction_risk()
            .create_device_type()
            .create_is_same_device()
            .create_hour_risk()
            .create_avg_previous_amount()
            .create_amount_difference_from_avg()
            .get_data()
        )

    # select features and train DBScan model with eps of 3 and minsameple = 2N -1
    trainer = ModelTrainer(data=df, raw_data=df)
    df, raw_data = (
            trainer
            .select_features()
            .encode_categotical_features()
            .scale_numerical_data()
            .train_model(eps=3)
            .convert_to_2d()
            .get_data()
    )

    # save 2D pca result data for visualization
    df.to_csv('pca.csv', index=False)
    # save output for inspection
    raw_data.to_csv('raw_data.csv', index =False)

    visualize = VisualizeOutput(data=df)
    # visualize cluster
    visualize.visualize()

