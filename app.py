import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Telco Customer Churn Dashboard", layout="wide")

st.title("Telco Customer Churn Dashboard")
st.markdown("This interactive dashboard provides insights into customer churn based on various factors without using any machine learning.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Telco_Customer_Churn.csv")
    # For visualizations, it's better to map 1/0 back to Yes/No for readability
    df['Churn_Label'] = df['Churn'].map({1: 'Yes', 0: 'No'})
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
contract_filter = st.sidebar.multiselect(
    "Select Contract Type:",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet_filter = st.sidebar.multiselect(
    "Select Internet Service:",
    options=df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

# Apply filters
filtered_df = df[(df["Contract"].isin(contract_filter)) & (df["InternetService"].isin(internet_filter))]

# KPIs
st.header("Overview")
col1, col2, col3 = st.columns(3)
total_customers = len(filtered_df)
churned_customers = filtered_df['Churn'].sum()
churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Average Churn Rate", f"{churn_rate:.2f}%")

st.markdown("---")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Distribution")
    fig_churn = px.pie(filtered_df, names='Churn_Label', title='Overall Churn vs Non-Churn', hole=0.4, color='Churn_Label', color_discrete_map={'Yes': 'red', 'No': 'green'})
    st.plotly_chart(fig_churn, use_container_width=True)

with col2:
    st.subheader("Monthly Charges vs Churn")
    fig_charges = px.box(filtered_df, x='Churn_Label', y='MonthlyCharges', color='Churn_Label', title='Distribution of Monthly Charges by Churn', color_discrete_map={'Yes': 'red', 'No': 'green'})
    st.plotly_chart(fig_charges, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Tenure vs Churn")
    fig_tenure = px.box(filtered_df, x='Churn_Label', y='tenure', color='Churn_Label', title='Distribution of Tenure (Months) by Churn', color_discrete_map={'Yes': 'red', 'No': 'green'})
    st.plotly_chart(fig_tenure, use_container_width=True)

with col4:
    st.subheader("Contract Type vs Churn")
    churn_contract = filtered_df.groupby(['Contract', 'Churn_Label']).size().reset_index(name='Count')
    fig_contract = px.bar(churn_contract, x='Contract', y='Count', color='Churn_Label', barmode='group', title='Churn by Contract Type', color_discrete_map={'Yes': 'red', 'No': 'green'})
    st.plotly_chart(fig_contract, use_container_width=True)

st.markdown("---")
st.subheader("Services Impact on Churn")

col5, col6 = st.columns(2)

with col5:
    churn_internet = filtered_df.groupby(['InternetService', 'Churn_Label']).size().reset_index(name='Count')
    fig_internet = px.bar(churn_internet, x='InternetService', y='Count', color='Churn_Label', barmode='group', title='Churn by Internet Service', color_discrete_map={'Yes': 'red', 'No': 'green'})
    st.plotly_chart(fig_internet, use_container_width=True)

with col6:
    churn_tech = filtered_df.groupby(['TechSupport', 'Churn_Label']).size().reset_index(name='Count')
    fig_tech = px.bar(churn_tech, x='TechSupport', y='Count', color='Churn_Label', barmode='group', title='Churn by Tech Support', color_discrete_map={'Yes': 'red', 'No': 'green'})
    st.plotly_chart(fig_tech, use_container_width=True)

st.markdown("### Data Preview")
st.dataframe(filtered_df.head())
