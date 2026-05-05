# FinVeda: Enterprise Financial Intelligence Platform

FinVeda is a production-grade financial analysis platform designed to ingest, process, and visualize complex financial data for Nifty 100 companies. Built with a robust Django/React stack and a custom ETL pipeline, it translates raw SQL dumps into actionable financial insights.

## 🚀 Key Features

- **Automated ETL Pipeline**: Custom regex-based SQL parser to extract data from legacy MySQL dumps.
- **Financial Modeling**: Support for multi-year Profit & Loss statements, Balance Sheets, and Cash Flow analysis.
- **Sector Analytics**: Hierarchical geographic and sector-based grouping for comparative analysis.
- **Modern Dashboard**: Glassmorphic React interface with high-performance metric cards and status indicators.
- **Agentic Integration**: Compatible with the Kolimarii AI Assistant for voice-activated financial queries.

## 🛠️ Architecture

### Backend (Django REST Framework)
- **Modular Design**: Separate apps for `companies`, `financials`, and `analytics`.
- **Advanced Serialization**: Deep-nested serializers to provide comprehensive company snapshots in a single API call.
- **Custom Management Commands**: Built-in CLI tools for bulk data ingestion.

### Frontend (React + Vite)
- **Design System**: Built on `DM Sans` and `Outfit` typography with a custom glassmorphism CSS engine.
- **State Management**: Reactive data fetching with Axios and Hooks.

### Data Layer (ETL)
1. **01_Extraction**: Raw SQL dump parsing to CSV.
2. **02_Transformation**: Data cleaning, numeric standardization, and model mapping.
3. **03_Loading**: Automated DB ingestion via Django ORM.

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js & npm
- PostgreSQL (or SQLite for dev)

### Backend Setup
1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```
2. Install dependencies:
   ```powershell
   pip install -r ../requirements.txt
   ```
3. Initialize the database:
   ```powershell
   python manage.py migrate
   ```

### Data Ingestion
Run the ETL pipeline from the root directory:
```powershell
python etl/01_extract_from_mysql.py
python etl/02_clean_and_transform.py
python backend/manage.py load_financials
```

### Frontend Setup
1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   ```
2. Install packages:
   ```powershell
   npm install
   ```
3. Launch the dashboard:
   ```powershell
   npm run dev
   ```

## 📈 Usage
Once running, navigate to `http://localhost:5173` to explore the financial dashboard. Use the search bar to filter companies by Symbol or Sector.

## 🛡️ Security
FinVeda implements standard Django security practices, including CORS headers for frontend communication and environment-based configuration for API keys.

---
*Built as an enterprise-grade fintech portfolio piece.*
