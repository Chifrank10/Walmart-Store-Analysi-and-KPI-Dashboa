import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Walmart Sales Dashboard", layout="wide")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("walmart.csv")

# Clean column names
df.columns = df.columns.str.strip()

# -----------------------------
# Clean Currency Columns
# -----------------------------

df["Sales"] = df["Sales"].replace('[\$, ]','', regex=True).astype(float)
df["unit_price"] = df["unit_price"].replace('[\$, ]','', regex=True).astype(float)

# -----------------------------
# Fix Date Format
# -----------------------------

df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

# Remove invalid dates
df = df.dropna(subset=["date"])

# -----------------------------
# Create Time Columns
# -----------------------------

df["Year"] = df["date"].dt.year.astype(int)
df["Month"] = df["date"].dt.month
df["Month_Name"] = df["date"].dt.month_name()
df["Week"] = df["date"].dt.isocalendar().week.astype(int)
df["Day"] = df["date"].dt.day

month_order = [
"January","February","March","April","May","June",
"July","August","September","October","November","December"
]

# -----------------------------
# Sidebar Navigation
# -----------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
"Go to",
["About Me","Sales Dashboard"]
)

# =====================================================
# ABOUT ME PAGE
# =====================================================

if page == "About Me":

    st.title("About the Analyst")

    st.write("""
**Chisom Ogbulie**

Data Analyst with **5+ years experience** using:

- SQL
- Python
- Excel
- Power BI

Passionate about transforming raw data into **actionable business insights**.

This project demonstrates the ability to:

• Clean messy real-world data  
• Build interactive dashboards  
• Perform trend analysis  
• Deliver insights for management decision-making
""")

    st.subheader("Skills Demonstrated")

    col1,col2,col3 = st.columns(3)

    col1.info("Python\n\nPandas\n\nStreamlit")
    col2.info("SQL\n\nData Cleaning\n\nEDA")
    col3.info("Data Visualization\n\nBusiness Insights\n\nDashboard Design")

# =====================================================
# SALES DASHBOARD PAGE
# =====================================================

elif page == "Sales Dashboard":

    st.title("Walmart Sales Analytics Dashboard")

    # -----------------------------
    # Filters
    # -----------------------------

    st.sidebar.header("Filters")

    category_filter = st.sidebar.multiselect(
    "Category",
    df["category"].unique(),
    default=df["category"].unique()
    )

    payment_filter = st.sidebar.multiselect(
    "Payment Method",
    df["payment_method"].unique(),
    default=df["payment_method"].unique()
    )

    year_filter = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
    )

    time_filter = st.sidebar.selectbox(
    "Trend Level",
    ["Day","Week","Month","Year"]
    )

    # -----------------------------
    # Apply Filters
    # -----------------------------

    df_filtered = df[
    (df["category"].isin(category_filter)) &
    (df["payment_method"].isin(payment_filter)) &
    (df["Year"].isin(year_filter))
    ]

    # -----------------------------
    # KPI CARDS
    # -----------------------------

    total_sales = df_filtered["Sales"].sum()
    transactions = df_filtered["invoice_id"].nunique()
    avg_sale = df_filtered["Sales"].mean()

    col1,col2,col3 = st.columns(3)

    col1.markdown(f"""
    <div style="background-color:#1f77b4;padding:25px;border-radius:10px;color:white">
    <h4>Total Sales</h4>
    <h2>${total_sales:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div style="background-color:#2ca02c;padding:25px;border-radius:10px;color:white">
    <h4>Transactions</h4>
    <h2>{transactions}</h2>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div style="background-color:#ff7f0e;padding:25px;border-radius:10px;color:white">
    <h4>Average Sale</h4>
    <h2>${avg_sale:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------
    # SALES BY CITY
    # -----------------------------

    st.subheader("Sales by City")

    city_sales = df_filtered.groupby("City")["Sales"].sum().reset_index()

    fig_city = px.bar(
    city_sales,
    x="City",
    y="Sales",
    color="City"
    )

    fig_city.update_layout(
    plot_bgcolor="white",
    yaxis=dict(tickprefix="$", tickformat=",")
    )

    st.plotly_chart(fig_city, use_container_width=True)

    # -----------------------------
    # SALES BY BRANCH
    # -----------------------------

    st.subheader("Sales by Branch")

    branch_sales = df_filtered.groupby("Branch")["Sales"].sum().reset_index()

    fig_branch = px.bar(
    branch_sales,
    x="Branch",
    y="Sales",
    color="Branch"
    )

    fig_branch.update_layout(
    plot_bgcolor="white",
    yaxis=dict(tickprefix="$", tickformat=",")
    )

    st.plotly_chart(fig_branch, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # TREND ANALYSIS
    # -----------------------------

    st.subheader("Sales Trend Analysis")

    if time_filter == "Day":

        trend = df_filtered.groupby("Day")["Sales"].sum().reset_index()

        fig = px.line(trend, x="Day", y="Sales", markers=True)

    elif time_filter == "Week":

        trend = df_filtered.groupby("Week")["Sales"].sum().reset_index()

        fig = px.line(trend, x="Week", y="Sales", markers=True)

    elif time_filter == "Month":

        trend = df_filtered.groupby(
        ["Year","Month","Month_Name"]
        )["Sales"].sum().reset_index()

        trend = trend.sort_values(["Year","Month"])

        fig = go.Figure()

        fig.add_trace(go.Bar(
        x=trend["Month_Name"],
        y=trend["Sales"],
        name="Sales"
        ))

        fig.add_trace(go.Scatter(
        x=trend["Month_Name"],
        y=trend["Sales"],
        mode="lines+markers",
        name="Trend"
        ))

        fig.update_layout(
        xaxis=dict(
        categoryorder="array",
        categoryarray=month_order
        )
        )

    else:

        trend = df_filtered.groupby("Year")["Sales"].sum().reset_index()

        fig = px.line(trend, x="Year", y="Sales", markers=True)

        fig.update_xaxes(type="category")

    fig.update_layout(
    plot_bgcolor="white",
    yaxis=dict(tickprefix="$", tickformat=",")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # BUSINESS INSIGHTS
    # -----------------------------

    st.subheader("Business Insights")

    top_city = city_sales.sort_values("Sales",ascending=False).iloc[0]["City"]
    top_category = df_filtered.groupby("category")["Sales"].sum().idxmax()
    top_payment = df_filtered.groupby("payment_method")["Sales"].sum().idxmax()

    st.success(f"Top Performing City: {top_city}")
    st.success(f"Top Category: {top_category}")
    st.success(f"Most Used Payment Method: {top_payment}")
