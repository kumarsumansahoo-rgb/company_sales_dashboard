import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Company Sales | Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Light corporate styling
st.markdown("""
<style>
    .stApp { background: #f5f7fb; color: #172033; }
    section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e7ebf2; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e7ebf2; padding: 16px 18px;
        border-radius: 14px; box-shadow: 0 2px 8px rgba(25, 42, 70, .04);
    }
    div[data-testid="stMetricLabel"] { color: #64748b; }
    div[data-testid="stMetricValue"] { color: #172033; }
    .main-title { font-size: 2rem; font-weight: 750; color: #172033; margin-bottom: 0; }
    .sub-title { color: #64748b; margin-top: 2px; margin-bottom: 22px; }
    .section-title { font-size: 1.15rem; font-weight: 700; color: #172033; margin: 8px 0 10px; }
    .insight {
        background: #ffffff; border: 1px solid #e7ebf2; border-left: 4px solid #3978f6;
        border-radius: 10px; padding: 13px 16px; margin-bottom: 10px; color: #334155;
    }
    div[data-testid="stDataFrame"] { border: 1px solid #e7ebf2; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).parent / "data" / "sample_sales_data.csv"

@st.cache_data
def load_data(file_bytes=None):
    if file_bytes is not None:
        data = pd.read_csv(file_bytes)
    else:
        data = pd.read_csv(DATA_PATH)
    required = {"Order Date", "Revenue", "Profit", "Product", "Category", "Region", "Quantity"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    for col in ["Revenue", "Profit", "Quantity"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=["Order Date", "Revenue", "Profit", "Quantity"])
    data["Month"] = data["Order Date"].dt.to_period("M").dt.to_timestamp()
    data["Month Label"] = data["Month"].dt.strftime("%b %Y")
    return data

st.sidebar.markdown("## 📊 Sales Analytics")
st.sidebar.caption("Company performance dashboard")
uploaded = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])
try:
    df = load_data(uploaded)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.info("Use a CSV with columns such as Order Date, Revenue, Profit, Product, Category, Region and Quantity.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

def options(col):
    return sorted(df[col].dropna().astype(str).unique().tolist()) if col in df.columns else []

selected_regions = st.sidebar.multiselect("Region", options("Region"), default=options("Region"))
selected_categories = st.sidebar.multiselect("Category", options("Category"), default=options("Category"))
selected_channels = st.sidebar.multiselect("Sales Channel", options("Sales Channel"), default=options("Sales Channel")) if "Sales Channel" in df.columns else []

filtered = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date) &
    (df["Region"].astype(str).isin(selected_regions)) &
    (df["Category"].astype(str).isin(selected_categories))
].copy()
if "Sales Channel" in filtered.columns:
    filtered = filtered[filtered["Sales Channel"].astype(str).isin(selected_channels)]

st.markdown('<div class="main-title">Company Sales Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A clear view of revenue, profitability, products and regional performance.</div>', unsafe_allow_html=True)

if filtered.empty:
    st.warning("No records match the selected filters. Change your filters to view the dashboard.")
    st.stop()

total_revenue = filtered["Revenue"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order ID"].nunique() if "Order ID" in filtered.columns else len(filtered)
total_units = filtered["Quantity"].sum()
margin = (total_profit / total_revenue * 100) if total_revenue else 0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
m2.metric("Total Profit", f"₹{total_profit:,.0f}")
m3.metric("Orders", f"{total_orders:,.0f}")
m4.metric("Units Sold", f"{total_units:,.0f}")
m5.metric("Profit Margin", f"{margin:.1f}%")

st.markdown("---")
left, right = st.columns([1.55, 1])
with left:
    st.markdown('<div class="section-title">Revenue over time</div>', unsafe_allow_html=True)
    monthly = filtered.groupby("Month", as_index=False).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    fig = px.line(monthly, x="Month", y=["Revenue", "Profit"], markers=True,
                  labels={"value": "Amount (₹)", "Month": "Month", "variable": "Metric"},
                  color_discrete_sequence=["#3978f6", "#16a085"])
    fig.update_layout(template="plotly_white", margin=dict(l=10,r=10,t=15,b=10),
                      legend_title_text="", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown('<div class="section-title">Revenue by region</div>', unsafe_allow_html=True)
    region = filtered.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    fig = px.pie(region, names="Region", values="Revenue", hole=.58,
                 color_discrete_sequence=["#3978f6", "#16a085", "#f4a340", "#8b70d6", "#e56b8a"])
    fig.update_layout(template="plotly_white", margin=dict(l=5,r=5,t=15,b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.markdown('<div class="section-title">Category performance</div>', unsafe_allow_html=True)
    category = filtered.groupby("Category", as_index=False).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
    fig = px.bar(category.sort_values("Revenue", ascending=True), x="Revenue", y="Category",
                 orientation="h", color="Profit", color_continuous_scale="Blues",
                 labels={"Revenue": "Revenue (₹)", "Category": "", "Profit": "Profit (₹)"})
    fig.update_layout(template="plotly_white", margin=dict(l=5,r=5,t=15,b=5), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown('<div class="section-title">Top 10 products by revenue</div>', unsafe_allow_html=True)
    products = filtered.groupby("Product", as_index=False)["Revenue"].sum().nlargest(10, "Revenue")
    fig = px.bar(products.sort_values("Revenue"), x="Revenue", y="Product", orientation="h",
                 color="Revenue", color_continuous_scale="Teal",
                 labels={"Revenue": "Revenue (₹)", "Product": ""})
    fig.update_layout(template="plotly_white", margin=dict(l=5,r=5,t=15,b=5), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-title">Business insights</div>', unsafe_allow_html=True)
best_region = region.iloc[0]["Region"] if not region.empty else "—"
best_category = category.loc[category["Revenue"].idxmax(), "Category"] if not category.empty else "—"
best_product = products.loc[products["Revenue"].idxmax(), "Product"] if not products.empty else "—"
avg_order = total_revenue / total_orders if total_orders else 0
insights = [
    f"<b>{best_region}</b> is the leading region by revenue in the selected period.",
    f"<b>{best_category}</b> is the highest-revenue product category.",
    f"<b>{best_product}</b> is the top product by revenue among the filtered records.",
    f"Average revenue per order is <b>₹{avg_order:,.0f}</b>, with an overall profit margin of <b>{margin:.1f}%</b>."
]
for item in insights:
    st.markdown(f'<div class="insight">• {item}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="section-title">Detailed sales records</div>', unsafe_allow_html=True)
show_cols = [c for c in ["Order ID", "Order Date", "Customer", "City", "Region", "Sales Channel",
                          "Sales Representative", "Product", "Category", "Quantity", "Revenue", "Profit"] if c in filtered.columns]
st.dataframe(filtered[show_cols].sort_values("Order Date", ascending=False),
             use_container_width=True, hide_index=True)
csv_download = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered records (CSV)", data=csv_download,
                   file_name="filtered_sales_records.csv", mime="text/csv")

st.caption("Demo project • Dataset is synthetic sample data created for learning and portfolio demonstration.")
