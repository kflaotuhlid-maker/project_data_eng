import pandas as pd
import numpy as np

def clean_data(input_path, output_path):
    print("Loading data...")
    df = pd.read_csv(input_path)
    
    print("Initial shape:", df.shape)
    
    # Drop customerID as it's not useful for analysis
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
        print("Dropped customerID column.")
    
    # Handle TotalCharges missing values (spaces to NaN)
    print("Cleaning TotalCharges...")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Check how many NaNs in TotalCharges
    missing_charges = df['TotalCharges'].isna().sum()
    print(f"Missing TotalCharges values: {missing_charges}")
    
    # Since there are very few missing TotalCharges (usually 11 out of 7043), dropping them is safest
    df = df.dropna(subset=['TotalCharges'])
    print(f"Dropped {missing_charges} rows with missing TotalCharges. Shape is now {df.shape}")
    
    # Remove duplicates if any
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Dropped {duplicates} duplicate rows. Shape is now {df.shape}")
    else:
        print("No duplicate rows found.")
        
    # Standardize binary categorical values
    binary_columns = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    print("Standardizing binary columns to 1/0...")
    for col in binary_columns:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})
            
    # Save to output path
    print(f"Saving cleaned dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Data cleaning complete!")

if __name__ == "__main__":
    INPUT_FILE = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    OUTPUT_FILE = "Cleaned_Telco_Customer_Churn.csv"
    clean_data(INPUT_FILE, OUTPUT_FILE)
