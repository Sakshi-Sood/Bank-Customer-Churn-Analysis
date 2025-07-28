# Bank Customer Churn Analysis - Streamlit Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Bank Customer Churn Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .objective-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)   

@st.cache_data  
def load_data():
    """Load and preprocess the dataset"""
    data = pd.read_excel('Bank_Churn.xlsx')
    df = data.head(5000).copy()
    
    # Add age groups
    df['AgeGroup'] = pd.cut(df['Age'], bins=[18, 30, 45, 60, 92], labels=['18-30', '31-45', '46-60', '60+'])
    
    # Add credit score categories
    Q1 = df['CreditScore'].quantile(0.25)
    Q3 = df['CreditScore'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df['CreditScoreCategory'] = 'Normal'
    df.loc[df['CreditScore'] < lower_bound, 'CreditScoreCategory'] = 'Low'
    df.loc[df['CreditScore'] > upper_bound, 'CreditScoreCategory'] = 'High'
    
    # Add zero balance indicator
    df['ZeroBalance'] = df['Balance'] == 0
    
    return df

def calculate_outliers(df):
    """Calculate outliers for numerical columns"""
    numerical_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
    outlier = {}
    
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier[col] = len(outliers)
    
    return pd.DataFrame(list(outlier.items()), columns=['Column', 'Outlier_Count'])

def create_correlation_heatmap(df):
    """Create correlation heatmap"""
    selected_columns = ['Age', 'Balance', 'IsActiveMember','NumOfProducts','CreditScore','Tenure','HasCrCard' ,'EstimatedSalary', 'Exited']
    corr_matrix = df[selected_columns].corr()
    
    fig = px.imshow(corr_matrix, 
                    text_auto=True, 
                    aspect="auto",
                    color_continuous_scale='RdBu',
                    title="Correlation Matrix of Key Features")
    fig.update_layout(width=800, height=600)
    return fig

def create_age_group_churn(df):
    """Create age group churn analysis"""
    age_churn = df.groupby('AgeGroup')['Exited'].mean().reset_index()
    
    fig = px.bar(age_churn, x='AgeGroup', y='Exited', 
                 title='Churn Rate by Age Group',
                 labels={'Exited': 'Churn Rate', 'AgeGroup': 'Age Group'},
                 color='Exited',
                 color_continuous_scale='Reds')
    fig.update_layout(showlegend=False)
    return fig

def create_gender_churn_pie(df):
    """Create gender churn pie chart"""
    gender_churn = df.groupby('Gender')['Exited'].mean().reset_index()
    
    fig = px.pie(gender_churn, values='Exited', names='Gender',
                 title='Churn Rate by Gender',
                 color_discrete_sequence=['#8fd9b6', '#ff9999'])
    return fig

def create_geography_churn(df):
    """Create geography churn analysis"""
    geo_churn = df.groupby('Geography')['Exited'].mean().reset_index()
    
    fig = px.bar(geo_churn, x='Geography', y='Exited',
                 title='Churn Rate by Geography',
                 labels={'Exited': 'Churn Rate'},
                 color='Exited',
                 color_continuous_scale='Blues')
    fig.update_layout(showlegend=False)
    return fig

def create_balance_boxplot(df):
    """Create balance distribution boxplot"""
    fig = px.box(df, x='Exited', y='Balance',
                 title='Account Balance Distribution by Churn Status',
                 labels={'Exited': 'Customer Churned (0=No, 1=Yes)', 'Balance': 'Account Balance'},
                 color='Exited',
                 color_discrete_sequence=['#8fd9b6', '#ff9999'])
    return fig

def create_products_analysis(df):
    """Create number of products analysis"""
    product_churn = df.groupby('NumOfProducts')['Exited'].mean().reset_index()
    product_count = df.groupby(['NumOfProducts', 'Exited']).size().reset_index(name='Count')
    
    # Create subplots
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=('Churn Rate by Number of Products', 
                                      'Product Distribution by Churn Status'))
    
    # Churn rate plot
    fig.add_trace(go.Bar(x=product_churn['NumOfProducts'], 
                         y=product_churn['Exited'],
                         name='Churn Rate',
                         marker_color='lightcoral'), row=1, col=1)
    
    # Product distribution plot
    for exit_status in [0, 1]:
        data = product_count[product_count['Exited'] == exit_status]
        fig.add_trace(go.Bar(x=data['NumOfProducts'], 
                             y=data['Count'],
                             name=f'{"Churned" if exit_status else "Stayed"}',
                             marker_color='#ff9999' if exit_status else '#8fd9b6'), row=1, col=2)
    
    fig.update_layout(height=500, showlegend=True)
    return fig

def create_activity_analysis(df):
    """Create activity member analysis"""
    engagement_data = {
        'Active Members': df[df['IsActiveMember'] == 1]['Exited'].mean(),
        'Inactive Members': df[df['IsActiveMember'] == 0]['Exited'].mean(),
        'Credit Card Holders': df[df['HasCrCard'] == 1]['Exited'].mean(),
        'No Credit Card': df[df['HasCrCard'] == 0]['Exited'].mean()
    }
    
    engagement_df = pd.DataFrame(list(engagement_data.items()), 
                                columns=['Engagement_Type', 'Churn_Rate'])
    engagement_df = engagement_df.sort_values('Churn_Rate', ascending=True)
    
    fig = px.bar(engagement_df, x='Churn_Rate', y='Engagement_Type',
                 orientation='h',
                 title='Churn Rate by Engagement Type',
                 labels={'Churn_Rate': 'Churn Rate', 'Engagement_Type': 'Engagement Type'},
                 color='Churn_Rate',
                 color_continuous_scale='Viridis')
    return fig

def create_tenure_analysis(df):
    """Create tenure analysis"""
    tenure_churn = df.groupby('Tenure')['Exited'].mean().reset_index()
    
    fig = px.line(tenure_churn, x='Tenure', y='Exited',
                  title='Churn Rate by Tenure',
                  labels={'Exited': 'Churn Rate', 'Tenure': 'Tenure (Years)'},
                  markers=True,
                  line_shape='linear')
    fig.update_traces(line_color='red', marker_color='red')
    return fig

def create_credit_score_analysis(df):
    """Create credit score analysis"""
    # Boxplot for credit scores
    fig1 = px.box(df, y='CreditScore',
                  title='Credit Score Distribution (Identifying Outliers)')
    
    # Churn rate by credit score category
    credit_churn = df.groupby('CreditScoreCategory')['Exited'].mean().reset_index()
    credit_churn = credit_churn.sort_values('Exited')
    
    fig2 = px.bar(credit_churn, x='CreditScoreCategory', y='Exited',
                  title='Churn Rate by Credit Score Category',
                  labels={'Exited': 'Churn Rate', 'CreditScoreCategory': 'Credit Score Category'},
                  color='Exited',
                  color_continuous_scale='Pastel1')
    
    return fig1, fig2

def create_balance_products_analysis(df):
    """Create balance and products combined analysis"""
    # Average balance by number of products and churn status
    pivot_data = df.pivot_table(index='NumOfProducts', columns='Exited', 
                               values='Balance', aggfunc='mean').reset_index()
    pivot_data = pivot_data.melt(id_vars=['NumOfProducts'], 
                                value_vars=[0, 1],
                                var_name='Exited', value_name='Average_Balance')
    pivot_data['Churn_Status'] = pivot_data['Exited'].map({0: 'Stayed', 1: 'Churned'})
    
    fig1 = px.bar(pivot_data, x='NumOfProducts', y='Average_Balance', 
                  color='Churn_Status',
                  title='Average Balance by Number of Products and Churn Status',
                  labels={'Average_Balance': 'Average Balance', 'NumOfProducts': 'Number of Products'},
                  color_discrete_sequence=['#8fd9b6', '#ff9999'],
                  barmode='group')
    
    # Churn rate by zero balance status
    zero_balance_churn = df.groupby('ZeroBalance')['Exited'].mean().reset_index()
    zero_balance_churn['Balance_Status'] = zero_balance_churn['ZeroBalance'].map({True: 'Zero Balance', False: 'Non-Zero Balance'})
    
    fig2 = px.bar(
    zero_balance_churn,
    x='Balance_Status',
    y='Exited',
    title='Churn Rate by Balance Status',
    labels={'Exited': 'Churn Rate', 'Balance_Status': 'Balance Status'},
    color='Balance_Status',
    color_discrete_sequence=['#8fd9b6', '#ff9999']
)
    
    return fig1, fig2

# Main Streamlit App
def main():
    st.markdown('<h1 class="main-header">🏦 Bank Customer Churn Analysis Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem;">
        <strong>Problem Statement:</strong> The goal is to identify key behavioral and demographic factors 
        driving customer churn in a bank and provide insights to improve retention.
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar
    st.sidebar.title("📊 Explore Analysis Sections")
    analysis_sections = [
        "📈 Dataset Overview",
        "🔍 Exploratory Data Analysis", 
        "👥 Customer Demographics",
        "💰 Financial Habits",
        "📱 Customer Engagement",
        "⏱️ Customer Tenure",
        "💳 Credit Score Analysis",
        "🔄 Balance & Products Analysis"
    ]
    
    selected_section = st.sidebar.selectbox("Choose Analysis Section:", analysis_sections)
    
    if selected_section == "📈 Dataset Overview":
        st.markdown('<div class="objective-header">Dataset Overview</div>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", len(df))
        with col2:
            st.metric("Churned Customers", df['Exited'].sum())
        with col3:
            st.metric("Churn Rate", f"{df['Exited'].mean():.2%}")
        with col4:
            st.metric("Active Members", df['IsActiveMember'].sum())
        
        # Dataset info
        st.subheader("Dataset Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**First 5 rows of the dataset:**")
            st.dataframe(df.head())
            
        with col2:
            st.write("**Dataset Statistics:**")
            st.write(f"- **Shape:** {df.shape}")
            st.write(f"- **Missing Values:** {df.isnull().sum().sum()}")
            st.write(f"- **Duplicates:** {df.duplicated().sum()}")
            st.write(f"- **Columns:** {', '.join(df.columns.tolist())}")
    
    elif selected_section == "🔍 Exploratory Data Analysis":
        st.markdown('<div class="objective-header">Exploratory Data Analysis</div>', unsafe_allow_html=True)
        
        # Statistical summary
        st.subheader("Statistical Summary")
        st.dataframe(df.describe())
        
        # Outlier detection
        st.subheader("Outlier Detection (IQR Method)")
        outlier_df = calculate_outliers(df)
        st.dataframe(outlier_df)
        
        # Correlation matrix
        st.subheader("Feature Correlation Analysis")
        fig_corr = create_correlation_heatmap(df)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    elif selected_section == "👥 Customer Demographics":
        st.markdown('<div class="objective-header">Objective 1: Customer Demographics Impact on Churn</div>', 
                    unsafe_allow_html=True)
        
        st.write("Exploring how customer background affects churn rates.")
        
        # Age group analysis
        st.subheader("Churn Rate by Age Group")
        fig_age = create_age_group_churn(df)
        st.plotly_chart(fig_age, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Churn Rate by Gender")
            fig_gender = create_gender_churn_pie(df)
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            st.subheader("Churn Rate by Geography")
            fig_geo = create_geography_churn(df)
            st.plotly_chart(fig_geo, use_container_width=True)
    
    elif selected_section == "💰 Financial Habits":
        st.markdown('<div class="objective-header">Objective 2: Financial Habits Impact</div>', 
                    unsafe_allow_html=True)
        
        st.write("Analyzing how account balance and number of products influence churn decisions.")
        
        # Balance analysis
        st.subheader("Account Balance Distribution by Churn Status")
        fig_balance = create_balance_boxplot(df)
        st.plotly_chart(fig_balance, use_container_width=True)
        
        # Products analysis
        st.subheader("Number of Products Analysis")
        fig_products = create_products_analysis(df)
        st.plotly_chart(fig_products, use_container_width=True)
    
    elif selected_section == "📱 Customer Engagement":
        st.markdown('<div class="objective-header">Objective 3: Customer Engagement Levels</div>', 
                    unsafe_allow_html=True)
        
        st.write("Examining if being an active member or credit card ownership affects churn.")
        
        # Activity analysis
        st.subheader("Churn Rate by Engagement Type")
        fig_engagement = create_activity_analysis(df)
        st.plotly_chart(fig_engagement, use_container_width=True)
        
        # Activity status breakdown
        col1, col2 = st.columns(2)
        with col1:
            active_churn = df[df['IsActiveMember'] == 1]['Exited'].mean()
            st.metric("Active Members Churn Rate", f"{active_churn:.2%}")
        with col2:
            inactive_churn = df[df['IsActiveMember'] == 0]['Exited'].mean()
            st.metric("Inactive Members Churn Rate", f"{inactive_churn:.2%}")
    
    elif selected_section == "⏱️ Customer Tenure":
        st.markdown('<div class="objective-header">Objective 4: Customer Tenure Impact</div>', 
                    unsafe_allow_html=True)
        
        st.write("Investigating how the length of customer relationship affects churn likelihood.")
        
        st.subheader("Churn Rate by Tenure")
        fig_tenure = create_tenure_analysis(df)
        st.plotly_chart(fig_tenure, use_container_width=True)
        
        # Tenure insights
        avg_tenure_churned = df[df['Exited'] == 1]['Tenure'].mean()
        avg_tenure_stayed = df[df['Exited'] == 0]['Tenure'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Tenure (Churned)", f"{avg_tenure_churned:.1f} years")
        with col2:
            st.metric("Average Tenure (Stayed)", f"{avg_tenure_stayed:.1f} years")
    
    elif selected_section == "💳 Credit Score Analysis":
        st.markdown('<div class="objective-header">Objective 5: Credit Score Outliers</div>', 
                    unsafe_allow_html=True)
        
        st.write("Identifying customers with unusual credit scores and their churn patterns.")
        
        fig_credit_box, fig_credit_churn = create_credit_score_analysis(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_credit_box, use_container_width=True)
        with col2:
            st.plotly_chart(fig_credit_churn, use_container_width=True)
    
    elif selected_section == "🔄 Balance & Products Analysis":
        st.markdown('<div class="objective-header">Objective 6: Balance & Products Relationship</div>', 
                    unsafe_allow_html=True)
        
        st.write("Analyzing the relationship between account balance and number of products held.")
        
        fig_balance_products, fig_zero_balance = create_balance_products_analysis(df)
        
        st.subheader("Average Balance by Products and Churn Status")
        st.plotly_chart(fig_balance_products, use_container_width=True)
        
        st.subheader("Churn Rate by Balance Status")
        st.plotly_chart(fig_zero_balance, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Dashboard created with Streamlit** 🚀")

if __name__ == "__main__":
    main()
