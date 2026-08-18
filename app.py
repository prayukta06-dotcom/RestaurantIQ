import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RestaurantIQ",
    page_icon="🍽️",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("ai_analysis_results.csv")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_columns = [
        "Price",
        "Quantity",
        "Revenue",
        "Profit",
        "Profit Margin"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("🍽️ RestaurantIQ")

st.subheader(
    "Restaurant Sales Intelligence Dashboard"
)

st.write(
    "Analyze restaurant revenue, profit, products, "
    "customers, cities and sales patterns."
)

st.divider()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Filters")

# Product filter
products = sorted(df["Product"].dropna().unique())

selected_products = st.sidebar.multiselect(
    "Product",
    products,
    default=products
)

# City filter
cities = sorted(df["City"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "City",
    cities,
    default=cities
)

# Purchase type filter
purchase_types = sorted(
    df["Purchase Type"].dropna().unique()
)

selected_purchase_types = st.sidebar.multiselect(
    "Purchase Type",
    purchase_types,
    default=purchase_types
)

# Payment method filter
payment_methods = sorted(
    df["Payment Method"].dropna().unique()
)

selected_payment_methods = st.sidebar.multiselect(
    "Payment Method",
    payment_methods,
    default=payment_methods
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Product"].isin(selected_products)) &
    (df["City"].isin(selected_cities)) &
    (df["Purchase Type"].isin(selected_purchase_types)) &
    (df["Payment Method"].isin(selected_payment_methods))
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = filtered_df["Revenue"].sum()

total_profit = filtered_df["Profit"].sum()

total_quantity = filtered_df["Quantity"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_anomalies = (
    filtered_df["AI_Anomaly"]
    .astype(str)
    .str.lower()
    .ne("normal")
    .sum()
)


# =========================================================
# KPI DISPLAY
# =========================================================

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns([1.3, 1.3, 1, 1, 0.8])

with col1:
    st.metric(
        "Total Revenue",
 f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
       f"₹{total_profit:,.0f}" 
    )

with col3:
    st.metric(
        "Items Sold",
        f"{total_quantity:,.2f}"
    )

with col4:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col5:
    st.metric(
        "Anomalies",
        f"{total_anomalies:,}"
    )


# =========================================================
# SALES TREND
# =========================================================

st.divider()

st.header("📈 Revenue Trend")

daily_revenue = (
    filtered_df
    .groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

fig_revenue = px.line(
    daily_revenue,
    x="Date",
    y="Revenue",
    markers=True,
    title="Revenue Over Time"
)

fig_revenue.update_layout(
    xaxis_title="Date",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

st.divider()

st.header("🍔 Product Analysis")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# Revenue by Product
# ---------------------------------------------------------

product_revenue = (
    filtered_df
    .groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

with col1:

    fig_product_revenue = px.bar(
        product_revenue,
        x="Product",
        y="Revenue",
        title="Revenue by Product"
    )

    st.plotly_chart(
        fig_product_revenue,
        use_container_width=True
    )


# ---------------------------------------------------------
# Profit by Product
# ---------------------------------------------------------

product_profit = (
    filtered_df
    .groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

with col2:

    fig_product_profit = px.bar(
        product_profit,
        x="Product",
        y="Profit",
        title="Profit by Product"
    )

    st.plotly_chart(
        fig_product_profit,
        use_container_width=True
    )


# =========================================================
# CITY ANALYSIS
# =========================================================

st.divider()

st.header("🌍 City Analysis")

city_revenue = (
    filtered_df
    .groupby("City")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_city = px.bar(
    city_revenue,
    x="City",
    y="Revenue",
    title="Revenue by City"
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)


# =========================================================
# PURCHASE TYPE ANALYSIS
# =========================================================

st.divider()

st.header("🛒 Purchase Analysis")

col1, col2 = st.columns(2)


with col1:

    purchase_revenue = (
        filtered_df
        .groupby("Purchase Type")["Revenue"]
        .sum()
        .reset_index()
    )

    fig_purchase = px.pie(
        purchase_revenue,
        names="Purchase Type",
        values="Revenue",
        title="Revenue by Purchase Type"
    )

    st.plotly_chart(
        fig_purchase,
        use_container_width=True
    )


with col2:

    payment_revenue = (
        filtered_df
        .groupby("Payment Method")["Revenue"]
        .sum()
        .reset_index()
    )

    fig_payment = px.pie(
        payment_revenue,
        names="Payment Method",
        values="Revenue",
        title="Revenue by Payment Method"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


# =========================================================
# AI ANOMALY ANALYSIS
# =========================================================

st.divider()

st.header("🤖 AI Anomaly Analysis")

anomaly_df = filtered_df[
    filtered_df["AI_Anomaly"]
    .astype(str)
    .str.lower()
    .ne("normal")
]

if len(anomaly_df) == 0:

    st.success(
        "✅ No anomalies detected in the selected data."
    )

else:

    st.warning(
        f"⚠️ {len(anomaly_df)} anomalous records detected."
    )

    st.dataframe(
        anomaly_df[
            [
                "Order ID",
                "Date",
                "Product",
                "Revenue",
                "Profit",
                "AI_Anomaly"
            ]
        ],
        use_container_width=True
    )


# =========================================================
# TOP PERFORMERS
# =========================================================

st.divider()

st.header("🏆 Top Performers")

col1, col2, col3 = st.columns(3)


# Best-selling product
with col1:

    if not filtered_df.empty:

        top_product = (
            filtered_df
            .groupby("Product")["Quantity"]
            .sum()
            .idxmax()
        )

        top_quantity = (
            filtered_df
            .groupby("Product")["Quantity"]
            .sum()
            .max()
        )

        st.metric(
            "Best-Selling Product",
            top_product
        )

        st.write(
            f"{top_quantity:,.2f} units sold"
        )


# Most profitable product
with col2:

    if not filtered_df.empty:

        best_profit_product = (
            filtered_df
            .groupby("Product")["Profit"]
            .sum()
            .idxmax()
        )

        best_profit = (
            filtered_df
            .groupby("Product")["Profit"]
            .sum()
            .max()
        )

        st.metric(
            "Most Profitable Product",
            best_profit_product
        )

        st.write(
            f"₹{best_profit:,.2f} profit"
        )


# Highest revenue city
with col3:

    if not filtered_df.empty:

        best_city = (
            filtered_df
            .groupby("City")["Revenue"]
            .sum()
            .idxmax()
        )

        best_city_revenue = (
            filtered_df
            .groupby("City")["Revenue"]
            .sum()
            .max()
        )

        st.metric(
            "Top Revenue City",
            best_city
        )

        st.write(
            f"₹{best_city_revenue:,.2f} revenue"
        )


# =========================================================
# DATA TABLE
# =========================================================

st.divider()

st.header("📋 Restaurant Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "RestaurantIQ • Restaurant Sales Intelligence"
)
