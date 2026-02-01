import pandas as pd
import numpy as np

def generate_professional_dataset():
    # Load existing data
    input_path = r'd:\customer-churn\WA_Fn-UseC_-Telco-Customer-Churn.csv'
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # 1. Cleaning
    # Convert TotalCharges to numeric, coercing errors to NaN
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)

    # 2. Enrichment (Synthetic Features)
    np.random.seed(42)

    # Convert Churn to numeric for logic (1=Yes, 0=No)
    df['ChurnNumeric'] = df['Churn'].map({'Yes': 1, 'No': 0})

    # Satisfaction Score (1-5)
    # Logic: Churned customers tend to have lower scores.
    def get_satisfaction(churn_status):
        if churn_status == 1:
            return np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.2, 0.05, 0.05])
        else:
            return np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.05, 0.2, 0.4, 0.3])
    
    df['SatisfactionScore'] = df['ChurnNumeric'].apply(get_satisfaction)

    # Data Usage GB (Monthly) based on Service
    def get_data_usage(row):
        service = row['InternetService']
        if service == 'Fiber optic':
            return max(0, np.random.normal(150, 50))
        elif service == 'DSL':
            return max(0, np.random.normal(50, 20))
        return 0

    df['DataUsageMonthlyGB'] = df.apply(get_data_usage, axis=1).round(1)

    # Customer Lifetime Value (CLTV)
    # Estimate future value + current value
    def get_cltv(row):
        current_value = row['TotalCharges']
        # Random future months estimate (6-36)
        future_months = np.random.randint(6, 37)
        if row['Churn'] == 'Yes':
            future_value = 0
        else:
            future_value = row['MonthlyCharges'] * future_months
        return round(current_value + future_value, 2)

    df['CLTV'] = df.apply(get_cltv, axis=1)

    # Support Tickets (Last Month)
    # Churners tend to have more tickets
    def get_tickets(churn_status):
        if churn_status == 1:
            return np.random.poisson(2)
        return np.random.poisson(0.5)

    df['SupportTicketsLastMonth'] = df['ChurnNumeric'].apply(get_tickets)

    # Drop temporary column
    df.drop(columns=['ChurnNumeric'], inplace=True)

    # Reorder basics
    cols = [c for c in df.columns if c != 'Churn'] + ['Churn']
    df = df[cols]
    
    output_path = r'd:\customer-churn\professional_churn_dataset.csv'
    df.to_csv(output_path, index=False)
    print(f"Successfully created professional dataset at: {output_path}")
    print("New Shape:", df.shape)
    print(df.head())

if __name__ == "__main__":
    generate_professional_dataset()
