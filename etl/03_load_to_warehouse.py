import os
import sys
import django
import pandas as pd
import numpy as np
from datetime import datetime

# Set up Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finveda_backend.settings')
django.setup()

from companies.models import Company, Sector, FiscalYear
from financials.models import ProfitLoss, BalanceSheet, CashFlow

def standardize_year(year_str):
    if pd.isna(year_str) or year_str == 'NULL':
        return None
    year_str = str(year_str).strip()
    match = django.utils.text.re.match(r"(\w+)-(\d{2})", year_str)
    if match:
        month, yy = match.groups()
        return f"{month} 20{yy}"
    return year_str

def load_data():
    raw_dir = "data/raw"
    print(f"[{datetime.now()}] Starting load to warehouse...")

    # 1. Load Companies
    if os.path.exists(f"{raw_dir}/companies.xlsx"):
        df = pd.read_excel(f"{raw_dir}/companies.xlsx", skiprows=1, header=None)
        for _, row in df.iterrows():
            try:
                symbol = str(row[0]).strip()
                if not symbol or symbol == 'nan': continue
                Company.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        'company_name': str(row[2]).strip(),
                        'company_logo': str(row[1]).strip(),
                        'website': str(row[5]).strip() if pd.notna(row[5]) else None,
                        'nse_url': str(row[6]).strip() if pd.notna(row[6]) else None,
                        'bse_url': str(row[7]).strip() if pd.notna(row[7]) else None,
                        'face_value': float(row[8]) if pd.notna(row[8]) and str(row[8]) != 'nan' else None,
                        'book_value': float(row[9]) if pd.notna(row[9]) and str(row[9]) != 'nan' else None,
                        'about_company': str(row[4]).strip() if pd.notna(row[4]) else None,
                    }
                )
            except Exception as e:
                print(f"Error loading company {row[0]}: {e}")
        print(f"Loaded companies.")

    # 2. Load Profit Loss
    if os.path.exists(f"{raw_dir}/profitandloss.xlsx"):
        df_pl = pd.read_excel(f"{raw_dir}/profitandloss.xlsx", skiprows=1, header=None)
        # Assuming: 0: symbol, 1: year_label, 2: sales, 3: exp, 4: op, 5: opm, 6: other, 7: int, 8: dep, 9: pbt, 10: tax, 11: net, 12: eps, 13: div
        for _, row in df_pl.iterrows():
            try:
                symbol = str(row[0]).strip()
                label = standardize_year(row[1])
                if not symbol or not label: continue
                
                comp = Company.objects.get(symbol=symbol)
                
                # Get or create Fiscal Year
                fy_val = 2025
                match = django.utils.text.re.search(r"20\d{2}", label)
                if match: fy_val = int(match.group())
                
                year, _ = FiscalYear.objects.get_or_create(
                    year_label=label,
                    defaults={'fiscal_year': fy_val, 'sort_order': fy_val * 10}
                )
                
                ProfitLoss.objects.update_or_create(
                    company=comp, year=year,
                    defaults={
                        'sales': float(row[2]) if pd.notna(row[2]) and str(row[2]) != 'nan' else 0,
                        'expenses': float(row[3]) if pd.notna(row[3]) and str(row[3]) != 'nan' else 0,
                        'operating_profit': float(row[4]) if pd.notna(row[4]) and str(row[4]) != 'nan' else 0,
                        'opm_pct': float(row[5]) if pd.notna(row[5]) and str(row[5]) != 'nan' else 0,
                        'net_profit': float(row[11]) if pd.notna(row[11]) and str(row[11]) != 'nan' else 0,
                    }
                )
            except Exception as e:
                pass # Skip if company not found or other errors
        print("Loaded Profit & Loss data.")

    # 3. Load Balance Sheet
    if os.path.exists(f"{raw_dir}/balancesheet.xlsx"):
        df_bs = pd.read_excel(f"{raw_dir}/balancesheet.xlsx", skiprows=1, header=None)
        for _, row in df_bs.iterrows():
            try:
                symbol = str(row[0]).strip()
                label = standardize_year(row[1])
                comp = Company.objects.get(symbol=symbol)
                year = FiscalYear.objects.get(year_label=label)
                
                BalanceSheet.objects.update_or_create(
                    company=comp, year=year,
                    defaults={
                        'equity_capital': float(row[2]) if pd.notna(row[2]) and str(row[2]) != 'nan' else 0,
                        'reserves': float(row[3]) if pd.notna(row[3]) and str(row[3]) != 'nan' else 0,
                        'borrowings': float(row[4]) if pd.notna(row[4]) and str(row[4]) != 'nan' else 0,
                        'total_assets': float(row[11]) if pd.notna(row[11]) and str(row[11]) != 'nan' else 0,
                    }
                )
            except:
                pass
        print("Loaded Balance Sheet data.")

    print("Load complete.")

if __name__ == "__main__":
    load_data()
