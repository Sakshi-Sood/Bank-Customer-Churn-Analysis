# Problem Statement :
'''
Bank Customer Churn: The goal is to identify key behavioral and demographic factors driving customer churn in a bank and provide insights to improve retention.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ! Load the dataset
data = pd.read_excel('Bank_Churn.xlsx')
df = data.head(5000).copy()  

#! EDA

print("First 5 rows of the dataset: ")
print(df.head())

print("\nInformation about the dataset: ")
print(df.info())

print("\nMissing Values: ")
print(df.isnull().sum())

print("\nColumns: ")
print(df.columns.tolist())


# ! Check for duplicates

duplicates = df.duplicated().sum()
print(f'Duplicates: {duplicates}')

print("\nStatistical Summary: ")
print(df.describe())

print("\nData Types: ")
print(df.dtypes)

print("\nUnique Values: ")
print(df.nunique())


# ! Outlier detection using IQR method

numerical_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
outlier_summary = {}

for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary[col] = len(outliers)

outlier_summary_df = pd.DataFrame(list(outlier_summary.items()), columns=['Column', 'Outlier_Count'])
print(outlier_summary_df)


# ! Correlation matrix to identify relationships between features

plt.figure(figsize=(8, 6)) 
selected_columns = ['Age', 'Balance', 'IsActiveMember','NumOfProducts','CreditScore','Tenure','HasCrCard' ,'EstimatedSalary', 'Exited']
sns.heatmap(df[selected_columns].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()



# ! Objective 1: Explore how customer background affects churn

# Age bins
df['AgeGroup'] = pd.cut(df['Age'], bins=[18, 30, 45, 60, 92], labels=['18-30', '31-45', '46-60', '60+'])

## ? Churn by Age Group

plt.figure(figsize=(8, 6))
sns.barplot(x='AgeGroup', y='Exited', hue='AgeGroup', data=df, palette='Set2')
plt.title('Churn Rate by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Churn Rate')
plt.show()


## ? Churn by Gender

gender_churn = df.groupby('Gender')['Exited'].mean()
plt.figure(figsize=(8, 6))
plt.pie(
    gender_churn, 
    labels=gender_churn.index, 
    autopct='%1.1f%%', 
    colors=['#8fd9b6', '#ff9999'], 
    startangle=90, 
    explode=(0.05, 0.05), 
    textprops={'fontsize': 12}  
)
plt.title('Churn Rate by Gender')  
plt.show()


## ? Churn by Geography

plt.figure(figsize=(8, 6))
sns.barplot(x='Geography', y='Exited', hue='Geography', data=df, palette='Set2')
plt.title('Churn Rate by Geography')
plt.xlabel('Geography')
plt.ylabel('Churn Rate')
plt.show()


# ! Objective 2: Look into financial habits and their impact – Find out whether factors like how much money a customer keeps in their account or how many products they use influence their decision to stay or leave.

## ? Box Plot for Balance vs Exited

plt.figure(figsize=(8, 6))
sns.boxplot(x="Exited", y="Balance", hue="Exited", data=df, palette="Pastel1")
plt.title("Account Balance Distribution by Exit/Churn Status")
plt.xlabel('Customer Churned (0=No, 1=Yes)')
plt.ylabel('Account Balance')
plt.tight_layout()
plt.show()


## ? Churn Rate by Number of Products

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
product_churn = df.groupby('NumOfProducts')['Exited'].mean().reset_index()

sns.barplot(ax=axes[0], x='NumOfProducts', y='Exited', hue='Exited', data=product_churn, palette='Pastel1', legend=False)
axes[0].set_title('Churn Rate by Number of Products')
axes[0].set_xlabel('Number of Products')
axes[0].set_ylabel('Churn Rate')

for index, row in product_churn.iterrows():
    axes[0].text(row['NumOfProducts'] - 1, row['Exited'] + 0.02, f"{row['Exited']:.2f}", ha='center', va='bottom', fontsize=10)


## ? Distribution of products by churn status

sns.countplot(ax=axes[1], x='NumOfProducts', hue='Exited', data=df, palette='Pastel1')
axes[1].set_title('Number of Products Distribution by Churn Status')
axes[1].set_xlabel('Number of Products')
axes[1].set_ylabel('Count')
axes[1].legend(title='Churned', labels=['No', 'Yes'])

plt.tight_layout()
plt.show()


# ! Objective 3: Examine engagement levels - Analyze if being an active user or owning a credit card has any connection with whether customers choose to churn.

## ? Pie charts showing the proportion of active members vs non-active members

plt.subplot(1, 2, 1)
active_members = df[df['IsActiveMember'] == 1]['Exited'].value_counts()
plt.pie(active_members, labels=['Stayed', 'Churned'], autopct='%1.1f%%', colors=['#8fd9b6', '#ff9999'], startangle=90, explode=(0.05, 0.05))
plt.title('Active Members Churn Rate')

plt.subplot(1, 2, 2)
inactive_members = df[df['IsActiveMember'] == 0]['Exited'].value_counts()
plt.pie(inactive_members, labels=['Stayed', 'Churned'], autopct='%1.1f%%', colors=['#8fd9b6', '#ff9999'], startangle=90, explode=(0.05, 0.05))
plt.title('Inactive Members Churn Rate')

plt.suptitle('Churn Rate by Activity Status', fontsize=24, fontweight='bold', color='black')
plt.tight_layout()
plt.show()


## ? Churn Rate on the basis of engagement types

engagement_churn = pd.DataFrame({
    'Active Members': [df[df['IsActiveMember'] == 1]['Exited'].mean()],
    'Inactive Members': [df[df['IsActiveMember'] == 0]['Exited'].mean()],
    'Credit Card Holders': [df[df['HasCrCard'] == 1]['Exited'].mean()],
    'No Credit Card': [df[df['HasCrCard'] == 0]['Exited'].mean()]
})

engagement_churn = engagement_churn.T
engagement_churn.columns = ['Churn Rate']

engagement_churn.sort_values('Churn Rate', ascending=False).plot(
    kind='barh', 
    color=sns.color_palette('viridis', 4)
)

plt.title('Churn Rate by Engagement Type', fontsize=14)
plt.xlabel('Churn Rate (Proportion)', fontsize=10)


for i, v in enumerate(engagement_churn.sort_values('Churn Rate', ascending=False)['Churn Rate']):
    plt.text(v + 0.005, i, f'{v:.2%}', va='center', fontweight='bold')

plt.tight_layout()
plt.show()


# ! Objective 4: Investigate the impact of customer tenure on churn – Determine if the length of time a customer has been with the bank influences their likelihood to leave.

## ? Churn rate by tenure

tenure_churn_rate = df.groupby("Tenure")["Exited"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=tenure_churn_rate, x="Tenure", y="Exited", marker="o", color="red")
plt.title("Churn Rate by Tenure")
plt.xlabel("Tenure (Years)")
plt.ylabel("Churn Rate")
plt.grid(True)
plt.tight_layout()
plt.show()

# ! Objective 5: Spot unusual credit behaviors – Identify customers with unusually high or low credit scores and see if those outliers are more likely to leave.

Q1 = df['CreditScore'].quantile(0.25)
Q3 = df['CreditScore'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df['CreditScoreCategory'] = 'Normal'
df.loc[df['CreditScore'] < lower_bound, 'CreditScoreCategory'] = 'Low'
df.loc[df['CreditScore'] > upper_bound, 'CreditScoreCategory'] = 'High'

plt.figure(figsize=(12, 5))

## ? Subplot 1: Box Plot for CreditScore to Spot Outliers

plt.subplot(1, 2, 1)
sns.boxplot(y='CreditScore', data=df, color='skyblue')
plt.title('Box Plot of Credit Scores\n(Identifying Outliers)')
plt.ylabel('Credit Score')

## ? Subplot 2: Bar Plot for Churn Rate by CreditScore Category

plt.subplot(1, 2, 2)
sns.barplot(x='CreditScoreCategory', y='Exited', data=df, hue='CreditScoreCategory',
            estimator=lambda x: sum(x) / len(x), palette='pastel',
            order=['Low', 'Normal', 'High'])
plt.title('Churn Rate by Credit Score Category')
plt.xlabel('Credit Score Category')
plt.ylabel('Churn Rate')

plt.tight_layout()
plt.show()


# ! Objective 6: To analyze the relationship between balance and the number of products held by customers, and how these factors relate to churn.

## ? Combined Analysis: Balance and Number of Products

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

## ? Plot 1: Average Balance by Number of Products and Churn Status

pivot_data = df.pivot_table(index='NumOfProducts', columns='Exited', values='Balance', aggfunc='mean')
pivot_data.columns = ['Stayed', 'Churned']
pivot_data.plot(kind='bar', color=['#8fd9b6', '#ff9999'], ax=axes[0])

axes[0].set_title('Average Balance by Number of Products and Churn Status')
axes[0].set_xlabel('Number of Products')
axes[0].set_ylabel('Average Balance')
axes[0].legend(title='Churn Status', loc='upper center')

## ? Plot 2: Churn Rate by Zero Balance Status

df['ZeroBalance'] = df['Balance'] == 0
zero_balance_churn = df.groupby('ZeroBalance')['Exited'].mean().reset_index()

sns.barplot(x='Exited', y='ZeroBalance', hue='ZeroBalance', data=zero_balance_churn, palette='Set2', orient='h', ax=axes[1])

axes[1].set_title('Churn Rate by Zero Balance Status')
axes[1].set_ylabel('Balance Status')
axes[1].set_xlabel('Churn Rate')
axes[1].set_yticks([0, 1])
axes[1].set_yticklabels(['Non-Zero Balance', 'Zero Balance'])

plt.tight_layout()
plt.show()