# Problem Statement :
'''
Customer churn is a significant challenge for financial institutions, as retaining existing customers is often more cost-effective than acquiring new ones. The dataset contains information about bank customers, including demographic details (e.g., age, gender, geography), financial attributes (e.g., credit score, balance, estimated salary), and banking behavior (e.g., tenure, number of products, activity status). However, the bank lacks a clear understanding of the factors driving customer churn and a predictive mechanism to identify customers at risk of leaving. The goal is to analyze this dataset to uncover patterns and build a predictive model that can accurately identify customers likely to churn, enabling the bank to take proactive measures to improve retention.
'''

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

