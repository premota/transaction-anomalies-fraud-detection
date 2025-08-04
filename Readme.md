# The Solution contains 3 folders:
1. Fraud_tools_teams_df_test: Contains datasets and question
2. Notebook: Contains all experimentation carried out in attempt to arrive at a proper solution
3. src. contains the final solution broken down into multiple python files in a modular manner


4. model.training.pipeline.py links up the various module needed to create train and examine the model
5. app.py contains the code for a simplistic streamlit User Interface


# Data Parser/Extraction:
The transaction logs were parsed using regular expressions. This method was chosen for its speed and simplicity, especially under time constraints.

However, regular expressions can be fragile if the text format changes, the extraction might fail. A more robust approach (which wasn’t used due to time limitations) would be to fine-tune a lightweight encoder only language model like DistilBERT, which is available on Hugging Face. Such models can generalize better and extract relevant features even when patterns shift slightly.

That said, I studied the raw logs carefully and built reliable regex patterns to extract key fields, including:

- user_id
- timestamp
- action
- amount
- currency
- location
- device
- atm
These form the core of the structured data used downstream for feature engineering and modeling.

# Feature Engineering:
To effectively support the fraud detection model, I engineered features that capture temporal dynamics and behavioral patterns within each transaction.
Given that the objective was to detect fraudulent transactions not label users as fraudulent the feature engineering approach was transaction-centric, not user-centric. In other words, all computations and insights were derived at the transaction level rather than through user-level aggregation.

To help the model recognize subtle irregularities in user behavior, I created features that compare each transaction with the user's immediate transaction history. This enabled the detection of suspicious deviations in timing, amount, device usage, and location all of which are critical in identifying fraud in real-world systems.

Some of the key features created include:

- amount_in_dollars: The amounts transacted were converted to a standard currency for easy comparison
- date: Was created to indicate the particular day a transaction was made regardless of time.
- time_feature: To help indicate the time of the day (the aim is to deparate mid day from late night transactions)
- previous_location: This was created to be an indicator if the user constantly changes location or the location changed comapred to previous transaction. (a change in location should potential raise suspicision especially when compared in confluence to other suspecious behavours)

- is_atm: This would help indicate if that tranaction happpened via atm or not. Can give valueable insight when combined with other indicators

- transaction risk: Certain transactions are most likely more associated with fraud E.g. Cashout, withdrawal, refund, transafer. This feature basically classify transactions into high risk, moderate and low risk.

- device type: Not all devices were smart device. This alone isn't a strong indicator for fraud but in combination to certain attributes like time of transfer, location change etc, it might be a good indicator.

- is_same_device: An indicator to tell if the user is using a separate device from the one used to make previous transaction.

- hour risk: Late night and early mornings are suspecious hours and in conflunce to several indicators could, it could be a cause for alarm.

- avg_previous_amount: This aims to give the model some sense of the user's behaviour prior to the current transaction. i.e the average amount the user has been transacting. 

- amount_difference_from_avg: This gives a sense of hour much the current transaction differs from the user's previous typical behaviour. A high deviation from previous average is a good indicator to flag a transaction as an anomaly. A more advance way to do this would be to calculate the upper and lower control value which is typically 3 standard deviation away from the mean. Above that value is considered an anomaly.


# Model Training
I explored two anomaly detection models: Isolation Forest and DBSCAN.
A brief write up of the Isolation Forest can be found in the "Fraud_tools_teams_df_test" folder under the name "isolation_anomaly_detection".

DBSCAN (Density Based Spatial Clustering of Applications with Noise) is a clustering algorithm that groups together data points that are closely packed, while marking points that lie alone in low density areas as anomalies or noise. It works based on two key parameters: eps, which defines how close points need to be to be considered neighbors, and min_samples, the minimum number of neighbors required to form a dense region. Unlike other clustering methods, DBSCAN does not require the number of clusters to be specified in advance. Instead, it discovers clusters of varying shapes and sizes based purely on data distribution. This makes it especially useful for anomaly detection, as any data point that doesn’t belong to a dense region is automatically flagged as a potential outlier.


## Tuning DBScan:
The final model was created with DBSCAN. To get the appropriate hyperparameters for DBSCAN, I utilized KNN to find a reasonable value for epsilon (eps).
Since KNN tells me the distance of every data point to its k nearest neighbors, with a known value of k, I can get the most typical distance of every point to its farthest (i.e., kth) neighbor.

Since epsilon in DBSCAN defines the maximum distance within which two points are considered part of the same cluster, this k-distance helps me estimate a threshold that separates dense regions from sparse ones.
By plotting the sorted k-distance graph and identifying the elbow point (a point of sharp change), I can choose a value of eps that best captures the density threshold for forming clusters and identifying anomalies (outliers).

This value of eps ensures that points in dense regions are grouped together, while those in sparse regions are marked as noise. This makes DBSCAN effective for density based anomaly detection, especially in datasets with varying distributions and no prior assumption of the number of clusters.
                
With this technique i was able to narrow down the search space to a range of 3 to 3.9 for eps value and by exeprimenting with all values within that search space and visualizing the outcome, i selected the eps value with the least tendency for false postive and false negatve (3.0 eps).


# Outcome of Model
The model flagged 276 transactions as anomalies.

However, model predictions are best used in combination with rule-based filtering. By combining machine learning results with business rules and domain knowledge, we can make better decisions and reduce risk.

We can group flagged transactions into the following categories: 
- Transactions to block
- Transactions that requires 2FA
- Transactions that should be reviewed
- Transactions that needs monitoring

1. Blocked Transactions (combination of all below).:
- is_same_location =  False
- is_atm = False           
- transaction risk = High            
- is_same_device = False           
- hour_risk = High            

2. Transactions that require 2FA.:
- transaction_risk = High
- is_same_location = False
- is_same_device = False
- hour_risk = High

3. Transactions to place on Review:
- transaction_risk = High
- hour_risk = High
- device_type = Non-Smart

4. Every other anomalous transactions can be placed on Monitored



# Other techniques to try out (but couldn't due to time constraint):
- Model advanced data extraction technique
- ensemble method for fraud detected: The ouptut from machine learning would be more reliable when multiple algorithms flag a transaction to be fraudulent.
- Write modular codes to production standard (with logger, exceptions, api's etc)
- Design a more interactive UI to interact with output from model




# Guidlines on how to run project
1. Create a virtual enivronment and run 'pip install -r requirements.txt' to install packages

2. Run 'python model_training_pipeline.py' to run the data extraction down to model training process. 

OR

3. Run 'streamlit run app.py' to launch UI that displays the cluster plot


Looking forward to having the opportunity to discuss more on this work and more during a 1 on 1 interview. 

