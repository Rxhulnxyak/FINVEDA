import os
import pandas as pd
from django.core.management.base import BaseCommand
from companies.models import Sector, Company, FiscalYear
from financials.models import ProfitLoss, BalanceSheet, CashFlow

class Command(BaseCommand):
    help = 'Loads cleaned financial data from CSVs into the database'

    def handle(self, *args, **options):
        # Use absolute path relative to the project root
        from django.conf import settings
        project_root = settings.BASE_DIR.parent
        processed_dir = os.path.join(project_root, "data", "processed")

        # 1. Load Sectors
        self.stdout.write("Loading Sectors...")
        sectors_df = pd.read_csv(os.path.join(processed_dir, "sectors.csv"))
        for _, row in sectors_df.iterrows():
            Sector.objects.get_or_create(sector_name=row['sector_name'])

        # 2. Load Companies
        self.stdout.write("Loading Companies...")
        companies_df = pd.read_csv(os.path.join(processed_dir, "companies.csv"))
        for _, row in companies_df.iterrows():
            sector = Sector.objects.filter(sector_name=row['sector']).first()
            Company.objects.update_or_create(
                symbol=row['symbol'],
                defaults={
                    'company_name': row['company_name'],
                    'sector': sector,
                    'sub_sector': row['sub_sector'],
                    'company_logo': row['company_logo'],
                    'website': row['website'],
                    'nse_url': row['nse_url'],
                    'bse_url': row['bse_url'],
                    'face_value': row['face_value'],
                    'book_value': row['book_value'],
                    'about_company': row['about_company']
                }
            )

        # 3. Load Financials
        self.load_financials(processed_dir)

    def load_financials(self, processed_dir):
        # This is a bit more complex because of FiscalYear foreign keys
        # We'll assume the 'year' column in CSV is the year_label (e.g. "Mar 2024")
        
        # P&L
        if os.path.exists(os.path.join(processed_dir, "profit_loss.csv")):
            self.stdout.write("Loading P&L Data...")
            df = pd.read_csv(os.path.join(processed_dir, "profit_loss.csv"))
            for _, row in df.iterrows():
                company = Company.objects.filter(symbol=row['symbol']).first()
                if not company: continue
                
                year_label = row['year']
                fiscal_year, created = FiscalYear.objects.get_or_create(
                    year_label=year_label,
                    defaults={'fiscal_year': int(year_label.split()[-1]), 'sort_order': 0}
                )
                
                ProfitLoss.objects.update_or_create(
                    company=company,
                    year=fiscal_year,
                    defaults={
                        'sales': row['sales'],
                        'expenses': row['expenses'],
                        'operating_profit': row['op'],
                        'opm_pct': row['opm'],
                        'other_income': row['other_income'],
                        'interest': row['interest'],
                        'depreciation': row['depreciation'],
                        'profit_before_tax': row['pbt'],
                        'tax_pct': row['tax'],
                        'net_profit': row['net_profit'],
                        'eps': row['eps'],
                        'dividend_payout_pct': row['dividend']
                    }
                )

        # Balance Sheet
        if os.path.exists(os.path.join(processed_dir, "balancesheet.csv")):
            self.stdout.write("Loading Balance Sheet Data...")
            df = pd.read_csv(os.path.join(processed_dir, "balancesheet.csv"))
            for _, row in df.iterrows():
                company = Company.objects.filter(symbol=row['symbol']).first()
                if not company: continue
                
                year_label = row['year']
                fiscal_year, _ = FiscalYear.objects.get_or_create(
                    year_label=year_label,
                    defaults={'fiscal_year': int(year_label.split()[-1]), 'sort_order': 0}
                )
                
                # Compute debt to equity if possible
                equity = row['equity']
                borrowings = row['borrowings']
                d_e = borrowings / equity if equity and equity != 0 else 0

                BalanceSheet.objects.update_or_create(
                    company=company,
                    year=fiscal_year,
                    defaults={
                        'equity_capital': row['equity'],
                        'reserves': row['reserves'],
                        'borrowings': row['borrowings'],
                        'other_liabilities': row['liabilities'],
                        'total_liabilities': row['total_liabilities'],
                        'fixed_assets': row['fixed_assets'],
                        'cwip': row['cwip'],
                        'investments': row['investments'],
                        'other_assets': row['other_assets'],
                        'total_assets': row['total_assets'],
                        'debt_to_equity': d_e
                    }
                )

        # Cash Flow
        if os.path.exists(os.path.join(processed_dir, "cashflow.csv")):
            self.stdout.write("Loading Cash Flow Data...")
            df = pd.read_csv(os.path.join(processed_dir, "cashflow.csv"))
            for _, row in df.iterrows():
                company = Company.objects.filter(symbol=row['symbol']).first()
                if not company: continue
                
                year_label = row['year']
                fiscal_year, _ = FiscalYear.objects.get_or_create(
                    year_label=year_label,
                    defaults={'fiscal_year': int(year_label.split()[-1]), 'sort_order': 0}
                )
                
                CashFlow.objects.update_or_create(
                    company=company,
                    year=fiscal_year,
                    defaults={
                        'operating_activity': row['operating'],
                        'investing_activity': row['investing'],
                        'financing_activity': row['financing'],
                        'net_cash_flow': row['net_cash'],
                        'free_cash_flow': row['operating'] + row['investing'] # Simplified FCF
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded financial data!'))
