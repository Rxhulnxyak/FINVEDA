import os
import re
import pandas as pd
from datetime import datetime
import csv
from io import StringIO

def parse_sql_dump(sql_file_path):
    print(f"[{datetime.now()}] Starting extraction from {sql_file_path}...")
    
    if not os.path.exists(sql_file_path):
        print(f"Error: {sql_file_path} not found.")
        return

    with open(sql_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    tables = {}
    current_table = None
    
    # Pattern to find INSERT INTO `table_name`
    insert_start_pattern = re.compile(r"INSERT INTO `(\w+)` VALUES")

    for line in lines:
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        match = insert_start_pattern.search(line)
        if match:
            current_table = match.group(1)
            if current_table not in tables:
                tables[current_table] = []
            
            # Extract the values part: VALUES (v1, v2), (v3, v4);
            values_part = line.split("VALUES", 1)[1].strip()
            # Remove trailing semicolon if present
            if values_part.endswith(';'):
                values_part = values_part[:-1]
                
            # Parse value sets: (v1, v2), (v3, v4)
            # This regex handles simple nested parentheses and quotes reasonably well
            value_sets = re.findall(r"\((.*?)\)(?:,|$)", values_part)
            
            for v_set in value_sets:
                # Use CSV reader to handle quoted strings with commas correctly
                # Note: MySQL uses single quotes, CSV reader default is double quotes
                f_io = StringIO(v_set.replace('NULL', ''))
                reader = csv.reader(f_io, quotechar="'", skipinitialspace=True)
                try:
                    row = next(reader)
                    tables[current_table].append(row)
                except StopIteration:
                    continue

    # Define column mappings for standard tables
    columns = {
        "companies": ["symbol", "name", "sector", "sub_sector", "logo", "website", "nse", "bse", "face_value", "book_value", "about"],
        "profitandloss": ["symbol", "year", "sales", "expenses", "op", "opm", "other_income", "interest", "depreciation", "pbt", "tax", "net_profit", "eps", "dividend"],
        "balancesheet": ["symbol", "year", "equity", "reserves", "borrowings", "liabilities", "total_liabilities", "fixed_assets", "cwip", "investments", "other_assets", "total_assets"],
        "cashflow": ["symbol", "year", "operating", "investing", "financing", "net_cash"]
    }

    # Save to CSVs
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)

    for table_name, data in tables.items():
        cols = columns.get(table_name, None)
        df = pd.DataFrame(data)
        
        # If columns match the expected count, assign them
        if cols and len(df.columns) == len(cols):
            df.columns = cols
            
        output_path = f"{raw_dir}/{table_name}.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved {table_name} to {output_path} ({len(df)} rows)")

if __name__ == "__main__":
    sql_path = "data/raw/scriptticker.sql"
    parse_sql_dump(sql_path)
