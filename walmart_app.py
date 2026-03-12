import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Walmart Sales Dashboard",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv("Walmart.csv")
df.columns = df.columns.str.strip()

# Clean Sales column (remove $ and convert to float)
df["Sales"] = df["Sales"].astype(str).str.replace("$","").str.replace(",","").astype(float)

# Clean unit_price column
df["unit_price"] = df["unit_price"].astype(str).str.replace("$","").str.replace(",","").astype(float)

# Quantity numeric
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)

# Correctly parse dates
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
df["time"] = pd.to_datetime(df["time"], errors="coerce")

# Time features
df["Day"] = df["date"].dt.date
df["Week"] = df["date"].dt.isocalendar().week
df["Month"] = df["date"].dt.month
df["Month_Name"] = df["date"].dt.month_name()
df["Year"] = df["date"].dt.year

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["About Me", "Sales Overview", "Trend Analysis", "Business Insights"]
)

st.sidebar.markdown("### Filters")
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
time_filter = st.sidebar.selectbox(
    "Time Analysis Level",
    ["Day", "Week", "Month", "Year"]
)

df_filtered = df[
    (df["category"].isin(category_filter)) &
    (df["payment_method"].isin(payment_filter))
]

# --------------------------------------------------
# PAGE 1: ABOUT ME
# --------------------------------------------------
if page == "About Me":
    col1, col2 = st.columns([1,2])
    with col1:
        st.image("profile.png", width=220)
    with col2:
        st.title("Chisom Ogbulie")
        st.write("""
        Senior Data Analyst with 5+ years experience in
        SQL, Python, Power BI, and business intelligence.
        I specialize in transforming raw data into actionable insights
        that support strategic decision making.
        """)
    st.markdown("---")
    st.subheader("Skills")
    st.write("""
    • SQL Analytics  
    • Python Data Analysis  
    • Power BI Dashboards  
    • Business Intelligence  
    • Data Storytelling
    """)

# --------------------------------------------------
# PAGE 2: SALES OVERVIEW
# --------------------------------------------------
elif page == "Sales Overview":
    st.title("Sales Performance Overview")
    col1, col2 = st.columns(2)

    # Sales by City
    city_sales = df_filtered.groupby("City")["Sales"].sum().reset_index()
    fig_city = px.bar(city_sales, x="City", y="Sales", color="City", text="Sales", title="Sales by City")
    fig_city.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
    fig_city.update_layout(
        plot_bgcolor="white",
        xaxis_title="City",
        yaxis_title="Total Sales ($)",
        yaxis=dict(tickprefix="$", tickformat=","),
        showlegend=False
    )
    col1.plotly_chart(fig_city, use_container_width=True)

    # Sales by Branch
    store_sales = df_filtered.groupby("Branch")["Sales"].sum().reset_index()
    fig_store = px.bar(store_sales, x="Branch", y="Sales", color="Branch", text="Sales", title="Sales by Branch")
    fig_store.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
    fig_store.update_layout(
        plot_bgcolor="white",
        xaxis_title="Branch",
        yaxis_title="Total Sales ($)",
        yaxis=dict(tickprefix="$", tickformat=","),
        showlegend=False
    )
    col2.plotly_chart(fig_store, use_container_width=True)

# --------------------------------------------------
# PAGE 3: TREND ANALYSIS
# --------------------------------------------------
elif page == "Trend Analysis":
    st.title("Sales Trend Analysis")

    if time_filter == "Day":
        trend = df_filtered.groupby("Day")["Sales"].sum().reset_index()
        fig = px.line(trend, x="Day", y="Sales", markers=True, title="Daily Sales Trend")

    elif time_filter == "Week":
        trend = df_filtered.groupby("Week")["Sales"].sum().reset_index()
        fig = px.line(trend, x="Week", y="Sales", markers=True, title="Weekly Sales Trend")

    elif time_filter == "Month":
        # Combo chart: bar + line
        trend = df_filtered.groupby("Month_Name")["Sales"].sum().reset_index()
        trend = trend.sort_values("Month_Name")  # Ensure chronological order

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=trend["Month_Name"],
            y=trend["Sales"],
            name="Monthly Sales",
            marker_color='steelblue'
        ))
        fig.add_trace(go.Scatter(
            x=trend["Month_Name"],
            y=trend["Sales"],
            name="Sales Trend",
            mode="lines+markers",
            marker_color='darkorange'
        ))
        fig.update_layout(
            title="Monthly Sales Trend (Bar + Line)",
            plot_bgcolor="white",
            xaxis_title="Month",
            yaxis_title="Sales ($)",
            yaxis=dict(tickprefix="$", tickformat=","),
            legend=dict(x=0.01, y=0.99)
        )

    else:
        trend = df_filtered.groupby("Year")["Sales"].sum().reset_index()
        fig = px.line(trend, x="Year", y="Sales", markers=True, title="Yearly Sales Trend")

    # Format y-axis for all charts
    fig.update_traces(texttemplate='$%{y:,.0f}')
    fig.update_layout(yaxis=dict(tickprefix="$", tickformat=","))

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# PAGE 4: BUSINESS INSIGHTS
# --------------------------------------------------
elif page == "Business Insights":
    st.title("Business Insights")

    best_city = df_filtered.groupby("City")["Sales"].sum().idxmax()
    best_category = df_filtered.groupby("category")["Sales"].sum().idxmax()
    best_payment = df_filtered.groupby("payment_method")["Sales"].sum().idxmax()

    st.success(f"Best Performing City: **{best_city}**")
    st.success(f"Top Selling Category: **{best_category}**")
    st.success(f"Most Used Payment Method: **{best_payment}**")