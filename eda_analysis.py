import pandas as pd

def run_eda(input_path, output_md_path):
    df = pd.read_csv(input_path)
    
    with open(output_md_path, 'w') as f:
        f.write("# Exploratory Data Analysis: Telco Customer Churn\n\n")
        
        f.write("## Summary Statistics\n")
        f.write("```\n")
        f.write(df[['tenure', 'MonthlyCharges', 'TotalCharges']].describe().to_string())
        f.write("\n```\n\n")
        
        f.write("## Churn Distribution\n")
        churn_counts = df['Churn'].value_counts(normalize=True) * 100
        f.write(f"- Non-Churners (0): {churn_counts[0]:.2f}%\n")
        f.write(f"- Churners (1): {churn_counts[1]:.2f}%\n\n")
        
        f.write("## Key Relationships with Churn\n\n")
        
        f.write("### 1. Contract Type vs Churn\n")
        contract_churn = df.groupby('Contract')['Churn'].mean() * 100
        f.write("Percentage of customers who churned by contract type:\n")
        for contract, pct in contract_churn.items():
            f.write(f"- {contract}: {pct:.2f}%\n")
        f.write("\n*Insight*: Customers with Month-to-month contracts are significantly more likely to churn compared to those with One or Two-year contracts.\n\n")
        
        f.write("### 2. Monthly Charges vs Churn\n")
        charges_churn = df.groupby('Churn')['MonthlyCharges'].mean()
        f.write(f"- Average Monthly Charges for Non-Churners: ${charges_churn[0]:.2f}\n")
        f.write(f"- Average Monthly Charges for Churners: ${charges_churn[1]:.2f}\n")
        f.write("\n*Insight*: Churners tend to have higher average monthly charges, indicating price sensitivity or dissatisfaction with higher-tier plans.\n\n")
        
        f.write("### 3. Tenure vs Churn\n")
        tenure_churn = df.groupby('Churn')['tenure'].mean()
        f.write(f"- Average Tenure for Non-Churners: {tenure_churn[0]:.2f} months\n")
        f.write(f"- Average Tenure for Churners: {tenure_churn[1]:.2f} months\n")
        f.write("\n*Insight*: New customers (lower tenure) are at the highest risk of churning. Loyalty increases with time.\n\n")
        
        f.write("### 4. Services Impact on Churn (Internet Service)\n")
        internet_churn = df.groupby('InternetService')['Churn'].mean() * 100
        for service, pct in internet_churn.items():
            f.write(f"- {service}: {pct:.2f}% churn rate\n")
        f.write("\n*Insight*: Fiber optic customers have a disproportionately high churn rate, suggesting possible issues with service quality, reliability, or price-to-value ratio for Fiber optic.\n\n")

        f.write("### 5. Services Impact on Churn (Tech Support)\n")
        tech_churn = df.groupby('TechSupport')['Churn'].mean() * 100
        for service, pct in tech_churn.items():
            f.write(f"- {service}: {pct:.2f}% churn rate\n")
        f.write("\n*Insight*: Customers without Tech Support churn much more frequently. Providing or encouraging Tech Support may reduce churn.\n\n")

if __name__ == "__main__":
    INPUT_FILE = "Cleaned_Telco_Customer_Churn.csv"
    OUTPUT_FILE = r"C:\Users\DELL\.gemini\antigravity\brain\2f049ad1-68f2-455f-b2b2-a12648f3c2f8\analysis_results.md"
    run_eda(INPUT_FILE, OUTPUT_FILE)
