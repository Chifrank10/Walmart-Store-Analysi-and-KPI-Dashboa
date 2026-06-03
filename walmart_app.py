import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Walmart Sales Dashboard", layout="wide")

# =====================================================
# PROFESSIONAL UI THEME
# =====================================================
st.markdown("""
<style>

/* Sky blue background */
.stApp {
    background: linear-gradient(135deg, #87CEEB, #B0E0E6);
    color: #0B1F3A;
}

/* Sidebar (transparent yellow) */
section[data-testid="stSidebar"] {
    background: rgba(255, 215, 0, 0.25);
}

/* KPI cards */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 12px;
    padding: 12px;
    color: black;
}

/* Headings */
h1, h2, h3 {
    color: #0B1F3A !important;
}

/* Better spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
DATA_FILE = Path(__file__).parent / "clean_data.csv"
df = pd.read_csv(DATA_FILE)

df.columns = df.columns.str.strip()

# =====================================================
# CLEAN DATA
# =====================================================
df["Sales"] = df["Sales"].replace('[\$, ]', '', regex=True).astype(float)
df["unit_price"] = df["unit_price"].replace('[\$, ]', '', regex=True).astype(float)

df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
df = df.dropna(subset=["date"])

# =====================================================
# TIME FEATURES
# =====================================================
df["Year"] = df["date"].dt.year.astype(int)
df["Month"] = df["date"].dt.month
df["Month_Name"] = df["date"].dt.month_name()
df["Week"] = df["date"].dt.isocalendar().week.astype(int)
df["Day"] = df["date"].dt.day

month_order = [
"January","February","March","April","May","June",
"July","August","September","October","November","December"
]

# =====================================================
# NAVIGATION
# =====================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About Me", "Sales Dashboard"])

# =====================================================
# ABOUT PAGE
# =====================================================
if page == "About Me":

    st.title("About the Analyst")

    st.write("""
**Data Analyst Portfolio Project**

Skills:
- Python (Pandas, Plotly, Streamlit)
- SQL
- Power BI
- Data Cleaning & Visualization
""")

# =====================================================
# SALES DASHBOARD
# =====================================================
elif page == "Sales Dashboard":

    st.title("Walmart Sales Analytics Dashboard")

    # =================================================
    # FILTERS
    # =================================================
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
        ["Day", "Week", "Month", "Year"]
    )

    # =================================================
    # FILTER DATA
    # =================================================
    df_filtered = df[
        (df["category"].isin(category_filter)) &
        (df["payment_method"].isin(payment_filter)) &
        (df["Year"].isin(year_filter))
    ]

    # 🚨 SAFE CHECK (prevents slicer crash)
    if df_filtered.empty:
        st.warning("No data available for selected filters. Adjust slicers.")
        st.stop()

    # =================================================
    # KPI CARDS
    # =================================================
    total_sales = df_filtered["Sales"].sum()
    transactions = df_filtered["invoice_id"].nunique()
    avg_sale = df_filtered["Sales"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Transactions", f"{transactions}")
    col3.metric("Average Sale", f"${avg_sale:,.2f}")

    st.markdown("---")

    # =================================================
    # CITY PERFORMANCE
    # =================================================
    st.subheader("City Performance (Top & Bottom 10)")

    city_sales = df_filtered.groupby("City")["Sales"].sum().reset_index()

    top_cities = city_sales.sort_values("Sales", ascending=False).head(10)
    worst_cities = city_sales.sort_values("Sales", ascending=True).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.write("🔥 Top 10 Cities")
        fig = px.bar(top_cities, x="City", y="Sales", color="Sales")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("⚠ Worst 10 Cities")
        fig = px.bar(worst_cities, x="City", y="Sales", color="Sales")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =================================================
    # BRANCH PERFORMANCE
    # =================================================
    st.subheader("Branch Performance (Top & Bottom 10)")

    branch_sales = df_filtered.groupby("Branch")["Sales"].sum().reset_index()

    top_branches = branch_sales.sort_values("Sales", ascending=False).head(10)
    worst_branches = branch_sales.sort_values("Sales", ascending=True).head(10)

    col1, col2 = st.columns(2)

    with col1:
        st.write("🔥 Top 10 Branches")
        fig = px.bar(top_branches, x="Branch", y="Sales", color="Sales")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("⚠ Worst 10 Branches")
        fig = px.bar(worst_branches, x="Branch", y="Sales", color="Sales")
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =================================================
    # CATEGORY PIE CHART
    # =================================================
    st.subheader("Sales Distribution by Category")

    category_sales = df_filtered.groupby("category")["Sales"].sum().reset_index()

    fig_pie = px.pie(
        category_sales,
        names="category",
        values="Sales",
        hole=0.4
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # =================================================
    # FUNNEL CHART
    # =================================================
    st.subheader("Sales Funnel (Top Cities Flow)")

    funnel_data = city_sales.sort_values("Sales", ascending=False).head(5)

    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data["City"],
        x=funnel_data["Sales"]
    ))

    st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("---")

    # =================================================
    # TREND ANALYSIS
    # =================================================
    st.subheader("Sales Trend Analysis")

    if time_filter == "Day":
        trend = df_filtered.groupby("Day")["Sales"].sum().reset_index()
        fig = px.line(trend, x="Day", y="Sales", markers=True)

    elif time_filter == "Week":
        trend = df_filtered.groupby("Week")["Sales"].sum().reset_index()
        fig = px.line(trend, x="Week", y="Sales", markers=True)

    elif time_filter == "Month":
        trend = df_filtered.groupby(
            ["Year", "Month", "Month_Name"]
        )["Sales"].sum().reset_index()

        trend = trend.sort_values(["Year", "Month"])

        fig = px.line(trend, x="Month_Name", y="Sales", markers=True)

    else:
        trend = df_filtered.groupby("Year")["Sales"].sum().reset_index()
        fig = px.line(trend, x="Year", y="Sales", markers=True)

    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =================================================
    # INSIGHTS
    # =================================================
    st.subheader("Business Insights")

    top_city = city_sales.sort_values("Sales", ascending=False)["City"].iloc[0]
    top_category = df_filtered.groupby("category")["Sales"].sum().idxmax()
    top_payment = df_filtered.groupby("payment_method")["Sales"].sum().idxmax()

    st.success(f"Top City: {top_city}")
    st.success(f"Top Category: {top_category}")
    st.success(f"Top Payment Method: {top_payment}")
