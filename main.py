import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset
data = pd.read_excel('SalesData.xlsx')

# Display the first few rows of the dataset
print(data.head())

# Display the columns of the dataset
print(data.columns)

print(data.info())
print(data.describe())
print(data.isnull().sum())