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



# ! Objective 1: Explore how customer background affects churn

# Age bins
df['AgeGroup'] = pd.cut(df['Age'], bins=[18, 30, 45, 60, 92], labels=['18-30', '31-45', '46-60', '60+'])

# Churn by Age Group
plt.figure(figsize=(8, 6))
sns.barplot(x='AgeGroup', y='Exited', hue='AgeGroup', data=df, palette='Set2')
plt.title('Churn Rate by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Churn Rate')
plt.show()

# Churn by Gender
plt.figure(figsize=(8, 6))
sns.barplot(x='Gender', y='Exited', data=df, hue='Gender', palette='Set2')
plt.title('Churn Rate by Gender')
plt.xlabel('Gender')
plt.ylabel('Churn Rate')
plt.legend()
plt.show()

# Churn by Geography
plt.figure(figsize=(8, 6))
sns.barplot(x='Geography', y='Exited', hue='Geography', data=df, palette='Set2')
plt.title('Churn Rate by Geography')
plt.xlabel('Geography')
plt.ylabel('Churn Rate')
plt.show()
