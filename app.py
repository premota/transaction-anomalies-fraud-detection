import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# The app title
st.title('Anomaly Data Visualization')


@st.cache_data
def load_data():
    #read data
    df = pd.read_csv('pca.csv')
    raw_data = pd.read_csv('raw_data.csv')
    return df, raw_data

df, raw_data = load_data()

# Display the top 20 rows of the DataFrame
# st.header('Top 20 Rows of Data')
# st.dataframe(df.head(20))

# Create a section for the scatter plot
st.header('Scatter Plot Visualization')


# Create and display the plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x=df['0'],
    y=df['1'],
    hue=df['cluster'],
    palette=["red", "blue"],
    ax=ax
)
plt.title(f'scatter plot showing outliers')
st.pyplot(fig)
