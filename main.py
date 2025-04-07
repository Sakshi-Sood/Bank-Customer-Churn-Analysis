# Problem Statement :
'''
Bank Customer Churn: The goal is to identify key behavioral and demographic factors driving customer churn in a bank and provide insights to improve retention.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ! Load the dataset
df = pd.read_excel('Bank_Churn.xlsx')

#! EDA

print("First 5 rows of the dataset: \n")
print(df.head())

print("Information about the dataset: ")
print(df.info())

print("Missing Values: \n")
print(df.isnull().sum())

print("Columns: ")
print(df.columns.tolist() , "\n")

# ! Check for duplicates
duplicates = df.duplicated().sum()
print(f'Duplicates: {duplicates}\n')

print("Statistical Summary: \n")
print(df.describe())

print("Data Types: ")
print(df.dtypes)

print("\nUnique Values: ")
print(df.nunique())


# ! Correlation matrix to identify relationships between features

plt.figure(figsize=(8, 6)) 
selected_columns = ['Age', 'Balance', 'IsActiveMember','NumOfProducts','CreditScore','Tenure','HasCrCard' ,'EstimatedSalary', 'Exited']
sns.heatmap(df[selected_columns].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.xticks(fontsize=7, rotation=30)
plt.yticks(fontsize=7)
plt.show()



