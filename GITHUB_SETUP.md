# GitHub setup guide

This guide helps you publish the dashboard repository and clone it onto another computer.

## Before publishing

- Review and customize the code so you understand each metric, chart, and filter.
- Keep the sample CSV identified as synthetic demonstration data. Do not claim it is real company data.
- If you replace the sample file with real company data, make sure you have permission and remove customer-identifying or confidential information.
- Never commit passwords, API keys, access tokens, or private company data.

## 1. Create a GitHub repository

1. Sign in to GitHub and choose **New repository**.
2. Name it `company-sales-analysis-dashboard`.
3. Choose Public or Private according to your preference.
4. Do not initialize it with a README, `.gitignore`, or license because this project already includes its own files.
5. Create the repository and copy its HTTPS URL. It will look like:
   `https://github.com/YOUR-USERNAME/company-sales-analysis-dashboard.git`

## 2. Push this project from VS Code

Open the extracted project folder in VS Code. In Terminal → New Terminal, run:

```powershell
git init
git add .
git status
git commit -m "Create company sales analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/company-sales-analysis-dashboard.git
git push -u origin main
```

Replace the example URL with your own repository URL. If Git asks you to sign in, complete GitHub's browser-based authentication. Do not paste a password or token into project files.

If `git remote add origin` says the remote already exists, check it with:

```powershell
git remote -v
```

If needed, update it:

```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/company-sales-analysis-dashboard.git
```

## 3. Pull updates later

From the project folder:

```powershell
git pull origin main
```

If you want a fresh copy on another computer:

```powershell
git clone https://github.com/YOUR-USERNAME/company-sales-analysis-dashboard.git
cd company-sales-analysis-dashboard
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

## 4. Typical update workflow

After editing files:

```powershell
git status
git add .
git commit -m "Improve sales dashboard visuals and insights"
git push
```

## 5. Suggested repository description

Interactive company sales analysis dashboard built with Python, Streamlit, Pandas and Plotly. Includes KPI tracking, date and category filters, product and regional analysis, business insights, and CSV export using a clearly labelled synthetic sample dataset.

## 6. Suggested topics

`python` `streamlit` `data-analysis` `data-visualization` `plotly` `pandas` `sales-dashboard`

## Note about authorship

Use this as a starter project: personalize the layout, add analysis you have verified, and make sure you can explain the code. A truthful portfolio description can say that you built and customized the dashboard using synthetic sample data. Do not imply the sample records came from a real company.
