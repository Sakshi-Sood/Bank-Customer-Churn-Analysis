import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_excel('Bank_Churn.xlsx')

# Check for  the structure, missing values and data types
print(data.head())
print(data.info())
print(data.isnull().sum())

print(data.columns.tolist() , "\n")
# Check for duplicates
duplicates = data.duplicated().sum()
print(f'Duplicates: {duplicates}\n')

print("Summary Statistics: \n")
print(data.describe())
