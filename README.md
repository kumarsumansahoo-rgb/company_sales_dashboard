# Company Sales Analysis & Visualization Dashboard

A light-themed, interactive sales analytics dashboard built with Python, Streamlit, Pandas and Plotly.

## Features
- KPI cards: revenue, profit, order count, units sold and profit margin
- Date, region, category and sales-channel filters
- Monthly revenue and profit trend
- Regional revenue share
- Category and top-product performance
- Automatically generated business insights
- Detailed filtered records and CSV export
- Upload your own CSV dataset from the sidebar

## Dataset
`data/sample_sales_data.csv` contains 1,200 **synthetic sample orders** for demonstration and learning. It is not real company data. Replace it with an authorized company dataset before presenting company-specific findings.

## Run locally (Windows / VS Code)

1. Install Python 3.10 or newer.
2. Extract the project ZIP and open the `company_sales_dashboard` folder in VS Code.
3. Open the VS Code terminal (Terminal → New Terminal).
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this for the current terminal only, then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

6. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Start the dashboard:

   ```powershell
   python -m streamlit run app.py
   ```

8. Streamlit will show a local URL, normally `http://localhost:8501`. Open it in your browser. Keep the terminal running while using the dashboard.

## Use your own dataset
Use the **Upload your sales CSV** control in the sidebar. The CSV must include these columns:
- `Order Date`
- `Revenue`
- `Profit`
- `Product`
- `Category`
- `Region`
- `Quantity`

Optional columns used for extra details: `Order ID`, `Customer`, `City`, `Sales Channel`, `Sales Representative`.

Make sure dates are parseable and revenue/profit/quantity are numeric. The dashboard uses Indian Rupee formatting (₹); change the labels in `app.py` if your source data uses another currency.

## Suggested portfolio description
**Company Sales Analysis & Visualization Dashboard** — Developed an interactive sales analytics dashboard using Python, Streamlit, Pandas and Plotly. Analyzed synthetic transactional data to track revenue, profit, order volume, product/category performance and regional trends. Added interactive filters, automated insight summaries and CSV export.

Customize the theme, add your own analysis, and be prepared to explain how each metric and chart is calculated. Do not describe the sample data as actual company records.


## Publish on GitHub

See [`GITHUB_SETUP.md`](GITHUB_SETUP.md) for repository creation, push, pull, clone and update commands.

## Portfolio and data note

This is a portfolio learning project using **synthetic sample sales records**. Customize the dashboard, verify the analysis, and be ready to explain your work. Do not present the generated sample records as confidential or actual company data.
