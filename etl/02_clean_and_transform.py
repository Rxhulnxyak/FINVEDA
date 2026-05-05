import pandas as pd
import os
from datetime import datetime

def clean_and_transform():
    print(f"[{datetime.now()}] Starting cleaning and transformation...")
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Process Sectors
    if os.path.exists(f"{raw_dir}/companies.csv"):
        companies_df = pd.read_csv(f"{raw_dir}/companies.csv")
        sectors = companies_df['sector'].unique()
        sectors_df = pd.DataFrame(sectors, columns=['sector_name'])
        sectors_df.to_csv(f"{processed_dir}/sectors.csv", index=False)
        print(f"Extracted {len(sectors_df)} sectors.")

    # 2. Process Companies
    if os.path.exists(f"{raw_dir}/companies.csv"):
        companies_df = pd.read_csv(f"{raw_dir}/companies.csv")
        # Rename columns to match Django models
        companies_df = companies_df.rename(columns={
            'name': 'company_name',
            'logo': 'company_logo',
            'nse': 'nse_url',
            'bse': 'bse_url',
            'about': 'about_company'
        })
        companies_df.to_csv(f"{processed_dir}/companies.csv", index=False)
        print(f"Processed {len(companies_df)} companies.")

    # 3. Process Financials (P&L, BS, CF)
    for table in ["profitandloss", "balancesheet", "cashflow"]:
        path = f"{raw_dir}/{table}.csv"
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Handle numeric columns
            numeric_cols = df.columns.difference(['symbol', 'year'])
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Map table names to model-friendly names
            model_name = table.replace("profitandloss", "profit_loss")
            df.to_csv(f"{processed_dir}/{model_name}.csv", index=False)
            print(f"Processed {len(df)} rows for {model_name}.")

if __name__ == "__main__":
    clean_and_transform()
