# Bank Customer Churn

## 🎯Overview

This project aims to analyze customer churn in the banking sector and develop strategies to retain customers. The dataset used for this analysis contains information about bank customers, including their demographics, account information, and whether they have churned or not.
The goal is to identify patterns and factors that contribute to customer churn, allowing the bank to implement targeted retention strategies.

## 📝 Dataset Description

The dataset used in this project is the "Bank Customer Churn" dataset, which contains information about bank customers and their churn status. The dataset includes the following features:
| Field            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| CustomerId       | A unique identifier for each customer                                      |
| Surname          | The customer's last name                                                  |
| CreditScore      | A numerical value representing the customer's credit score                |
| Geography        | The country where the customer resides (France, Spain, or Germany)        |
| Gender           | The customer's gender (Male or Female)                                    |
| Age              | The customer's age                                                        |
| Tenure           | The number of years the customer has been with the bank                   |
| Balance          | The customer's account balance                                            |
| NumOfProducts    | The number of bank products the customer uses (e.g., savings account, credit card) |
| HasCrCard        | Whether the customer has a credit card (1 = yes, 0 = no)                  |
| IsActiveMember   | Whether the customer is an active member (1 = yes, 0 = no)                |
| EstimatedSalary  | The estimated salary of the customer                                      |
| Exited           | Whether the customer has churned (1 = yes, 0 = no)                        |

## 🗒️ Objectives for the Analysis

1. Explore how customer background affects churn – Understand if age, gender, or where a customer lives makes them more likely to leave the bank.

2. Look into financial habits and their impact – Find out whether factors like how much money a customer keeps in their account or how many products they use influence their decision to stay or leave.

3. Examine engagement levels – Analyze if being an active user or owning a credit card has any connection with whether customers choose to churn.

4. Spot unusual credit behaviors – Identify customers with unusually high or low credit scores and see if those outliers are more likely to leave.

5. Break down churn by customer segments – Compare churn rates across different groups (like based on tenure or income) to highlight which types of customers are most at risk of leaving.

6. Analyze how the combination of credit score and account balance influences churn.

## 📊 Data Visualizations

### 🚀 Key Insights and Findings

1. **Demographics and Churn**:
    - Customers aged between 46 and 60, particularly those residing in Germany, exhibit higher churn rates compared to other age groups and regions.
    - Gender analysis reveals that women are more likely to churn than men, highlighting potential demographic-specific factors influencing customer retention.

2. **Financial Behavior**:
    - Customers with lower account balances and fewer bank products are more prone to churn.
    - High-income customers with low engagement levels also exhibit higher churn rates.

3. **Engagement and Activity**:
    - Active members are significantly less likely to churn compared to inactive members.
    - Ownership of a credit card alone does not strongly correlate with churn but combined with other factors, it provides valuable insights.

4. **Credit Score and Outliers**:
    - Customers with extremely low or high credit scores show distinct churn patterns.
    - Outliers in credit scores often align with other risk factors, amplifying churn likelihood.

5. **Customer Segmentation**:
    - Customers with longer tenure tend to have lower churn rates; however, certain income brackets show exceptions to this trend.
    - Segmenting customers based on tenure and income effectively identifies groups that are more likely to churn, enabling targeted retention strategies.

6. **Combined Factors**:
    - A combination of low credit scores and low account balances is a strong predictor of churn.



## 🛠️ Tools and Technologies

- **Programming Language**: Python
- **Libraries**: Pandas, NumPy, Matplotlib, Seaborn, Streamlit, Plotly
- **Data Visualization**: Plotly, Matplotlib, Seaborn
- **Environment**: Jupyter Notebook
- **Version Control**: Git


## 🤝 Contribution

Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and submit a pull request. Please ensure your changes align with the project's objectives.

