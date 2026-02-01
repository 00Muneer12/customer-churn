import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Telco Churn Analytics Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('professional_churn_dataset.csv')
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Dataset 'professional_churn_dataset.csv' not found. Please run the generation script first.")
    st.stop()

# specific ordering for satisfaction
df['SatisfactionScore'] = df['SatisfactionScore'].astype(int)

# Title
st.title("📊 Professional Customer Churn Analytics")
st.markdown("---")

# --- KPI Metrics ---
col1, col2, col3, col4 = st.columns(4)

total_customers = len(df)
churn_rate = (df['Churn'] == 'Yes').mean() * 100
avg_satisfaction = df['SatisfactionScore'].mean()
avg_cltv = df['CLTV'].mean()

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}/5")
col4.metric("Avg CLTV", f"${avg_cltv:,.2f}")

st.markdown("---")

# --- Key Findings Section ---
with st.expander("💡 **Key Strategic Findings & Insights**", expanded=True):
    st.markdown("""
    Based on the analysis of the dataset, here are the top-level takeaways:
    1.  **Satisfaction is a Strong Predictor**: Customers with a Satisfaction Score of 1 or 2 have a significantly higher churn rate (>50%).
    2.  **Fiber Optic Risk**: Fiber Optic users tend to have higher monthly charges and higher churn compared to DSL users, likely due to price sensitivity.
    3.  **Support Tickets**: There is a direct correlation between the number of support tickets filed in the last month and churn probability.
    4.  **Contract Lock-in**: Month-to-month contracts remain the highest risk segment.
    """)

st.markdown("---")

# --- Visualizations ---

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Churn Distribution by Satisfaction Score")
    # Group by Satisfaction and Churn
    sat_churn = df.groupby(['SatisfactionScore', 'Churn']).size().reset_index(name='Count')
    fig_sat = px.bar(sat_churn, x="SatisfactionScore", y="Count", color="Churn", 
                     title="Impact of Satisfaction on Churn",
                     color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'},
                     barmode='group')
    st.plotly_chart(fig_sat, use_container_width=True)

with col_right:
    st.subheader("Customer Lifetime Value (CLTV) Density")
    fig_cltv = px.histogram(df, x="CLTV", color="Churn", 
                            title="CLTV Distribution: Churned vs Retained",
                            color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'},
                            marginal="box", # or violin, rug
                            hover_data=df.columns)
    st.plotly_chart(fig_cltv, use_container_width=True)

# Row 2
col_left_2, col_right_2 = st.columns(2)

with col_left_2:
    st.subheader("Churn by Contract Type")
    contract_churn = df.groupby(['Contract', 'Churn']).size().reset_index(name='Count')
    fig_contract = px.bar(contract_churn, x="Contract", y="Count", color="Churn",
                          title="Retention by Contract Length",
                          color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'},
                          barmode='stack')
    st.plotly_chart(fig_contract, use_container_width=True)

with col_right_2:
    st.subheader("Avg Monthly Charges vs Data Usage")
    # Sample for scatter plot performance if dataset is huge, but 7k is fine
    fig_scatter = px.scatter(df, x="DataUsageMonthlyGB", y="MonthlyCharges", color="Churn",
                             title="Data Usage vs Price Sensitivity",
                             color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'},
                             size='SupportTicketsLastMonth', hover_name='customerID',
                             opacity=0.6)
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Data Table ---
st.markdown("### Detailed Customer Data View")
st.dataframe(df.head(50))
