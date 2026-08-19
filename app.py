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
st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# =========================================================
# FILE UPLOAD
# =========================================================

st.sidebar.title("🍽️ RestaurantIQ")

st.sidebar.caption(
    "Upload your own restaurant data"
)

uploaded_file = st.sidebar.file_uploader(
    "Choose CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)
# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    if uploaded_file is not None:

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(uploaded_file)

    else:

        df = pd.read_csv("ai_analysis_results.csv")

    # Convert Date
    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # Convert numeric columns
    numeric_columns = [
        "Price",
        "Quantity",
        "Revenue",
        "Profit",
        "Profit Margin"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df

df = load_data()
# =========================================================
# FLEXIBLE COLUMN MAPPING
# =========================================================

if uploaded_file is not None:

    st.sidebar.header("🔗 Column Mapping")

    available_columns = list(df.columns)

    def find_column(possible_names):

        for column in available_columns:

            column_clean = str(column).strip().lower()

            for name in possible_names:

                if name.lower() == column_clean:
                    return column

        for column in available_columns:

            column_clean = str(column).strip().lower()

            for name in possible_names:

                if name.lower() in column_clean:
                    return column

        return None


    # -----------------------------------------------------
    # AUTOMATIC COLUMN DETECTION
    # -----------------------------------------------------

    detected_date = find_column([
        "date",
        "order date",
        "transaction date",
        "sale date"
    ])

    detected_product = find_column([
        "product",
        "product name",
        "item",
        "item name",
        "dish",
        "dish name",
        "menu item"
    ])

    detected_quantity = find_column([
        "quantity",
        "qty",
        "units",
        "units sold",
        "quantity sold"
    ])

    detected_price = find_column([
        "price",
        "unit price",
        "selling price",
        "sale price"
    ])

    detected_revenue = find_column([
        "revenue",
        "sales",
        "total sales",
        "total revenue",
        "sales amount"
    ])

    detected_profit = find_column([
        "profit",
        "net profit",
        "gross profit"
    ])

    detected_city = find_column([
        "city",
        "location",
        "branch",
        "outlet"
    ])

    detected_purchase = find_column([
        "purchase type",
        "order type",
        "sales channel",
        "channel"
    ])

    detected_payment = find_column([
        "payment method",
        "payment type",
        "payment"
    ])

    detected_manager = find_column([
        "manager",
        "manager name",
        "supervisor"
    ])

    detected_order = find_column([
        "order id",
        "order_id",
        "transaction id",
        "transaction_id",
        "invoice id",
        "invoice_id"
    ])


    # -----------------------------------------------------
    # COLUMN SELECTORS
    # -----------------------------------------------------

    def column_selector(label, detected):

        options = ["— Not available —"] + available_columns

        if detected in options:

            default_index = options.index(detected)

        else:

            default_index = 0

        return st.sidebar.selectbox(
            label,
            options,
            index=default_index
        )


    mapped_date = column_selector(
        "📅 Date",
        detected_date
    )

    mapped_product = column_selector(
        "🍔 Product",
        detected_product
    )

    mapped_quantity = column_selector(
        "📦 Quantity",
        detected_quantity
    )

    mapped_price = column_selector(
        "💵 Price",
        detected_price
    )

    mapped_revenue = column_selector(
        "💰 Revenue",
        detected_revenue
    )

    mapped_profit = column_selector(
        "📈 Profit",
        detected_profit
    )

    mapped_city = column_selector(
        "🌍 City / Location",
        detected_city
    )

    mapped_purchase = column_selector(
        "🛒 Purchase Type",
        detected_purchase
    )

    mapped_payment = column_selector(
        "💳 Payment Method",
        detected_payment
    )

    mapped_manager = column_selector(
        "👨‍💼 Manager",
        detected_manager
    )

    mapped_order = column_selector(
        "🧾 Order ID",
        detected_order
    )


    # -----------------------------------------------------
    # RENAME UPLOADED COLUMNS TO RESTAURANTIQ STANDARD
    # -----------------------------------------------------

    rename_map = {}

    mapping_pairs = {
        mapped_date: "Date",
        mapped_product: "Product",
        mapped_quantity: "Quantity",
        mapped_price: "Price",
        mapped_revenue: "Revenue",
        mapped_profit: "Profit",
        mapped_city: "City",
        mapped_purchase: "Purchase Type",
        mapped_payment: "Payment Method",
        mapped_manager: "Manager",
        mapped_order: "Order ID"
    }

    for source, target in mapping_pairs.items():

        if source != "— Not available —":

            rename_map[source] = target


    df = df.rename(columns=rename_map)


    # -----------------------------------------------------
    # CONVERT MAPPED COLUMNS
    # -----------------------------------------------------

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )


    numeric_columns = [
        "Price",
        "Quantity",
        "Revenue",
        "Profit",
        "Profit Margin"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )
# =========================================================

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

st.sidebar.title("🍽️ RestaurantIQ")
st.sidebar.caption("Sales Intelligence Filters")


# ---------------------------------------------------------
# PRODUCT FILTER
# ---------------------------------------------------------

if "Product" in df.columns:

    products = sorted(
        df["Product"].dropna().astype(str).unique()
    )

    selected_products = st.sidebar.multiselect(
        "Product",
        products,
        default=products
    )

else:

    selected_products = []


# ---------------------------------------------------------
# CITY FILTER
# ---------------------------------------------------------

if "City" in df.columns:

    cities = sorted(
        df["City"].dropna().astype(str).unique()
    )

    selected_cities = st.sidebar.multiselect(
        "City",
        cities,
        default=cities
    )

else:

    selected_cities = []


# ---------------------------------------------------------
# PURCHASE TYPE FILTER
# ---------------------------------------------------------

if "Purchase Type" in df.columns:

    purchase_types = sorted(
        df["Purchase Type"].dropna().astype(str).unique()
    )

    selected_purchase_types = st.sidebar.multiselect(
        "Purchase Type",
        purchase_types,
        default=purchase_types
    )

else:

    selected_purchase_types = []


# ---------------------------------------------------------
# PAYMENT METHOD FILTER
# ---------------------------------------------------------

if "Payment Method" in df.columns:

    payment_methods = sorted(
        df["Payment Method"].dropna().astype(str).unique()
    )

    selected_payment_methods = st.sidebar.multiselect(
        "Payment Method",
        payment_methods,
        default=payment_methods
    )

else:

    selected_payment_methods = []


# ---------------------------------------------------------
# DATE FILTER
# ---------------------------------------------------------

if "Date" in df.columns and df["Date"].notna().any():

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

else:

    selected_dates = ()

# =========================================================
# APPLY FILTERS
# =========================================================


if len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = df[
        (df["Product"].isin(selected_products)) &
        (df["City"].isin(selected_cities)) &
        (df["Purchase Type"].isin(selected_purchase_types)) &
        (df["Payment Method"].isin(selected_payment_methods)) &
        (df["Date"] >= start_date) &
        (df["Date"] <= end_date)
    ].copy()

else:

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
        f"{total_quantity:,.0f}"
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
# MANAGER ANALYSIS
# =========================================================

st.divider()

st.header("👨‍💼 Manager Performance")

col1, col2 = st.columns(2)


# Revenue by Manager

manager_revenue = (
    filtered_df
    .groupby("Manager")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

with col1:

    fig_manager_revenue = px.bar(
        manager_revenue,
        x="Manager",
        y="Revenue",
        title="Revenue by Manager",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_manager_revenue,
        use_container_width=True
    )


# Profit by Manager

manager_profit = (
    filtered_df
    .groupby("Manager")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

with col2:

    fig_manager_profit = px.bar(
        manager_profit,
        x="Manager",
        y="Profit",
        title="Profit by Manager",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_manager_profit,
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
# ADDITIONAL BUSINESS CHARTS
# =========================================================

st.divider()

st.header("📅 Additional Business Trends")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# MONTHLY REVENUE
# ---------------------------------------------------------

monthly_revenue = (
    filtered_df
    .assign(Month=filtered_df["Date"].dt.to_period("M").astype(str))
    .groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

with col1:

    fig_monthly_revenue = px.line(
        monthly_revenue,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue"
    )

    fig_monthly_revenue.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_monthly_revenue,
        use_container_width=True
    )


# ---------------------------------------------------------
# MONTHLY PROFIT
# ---------------------------------------------------------

monthly_profit = (
    filtered_df
    .assign(Month=filtered_df["Date"].dt.to_period("M").astype(str))
    .groupby("Month")["Profit"]
    .sum()
    .reset_index()
)

with col2:

    fig_monthly_profit = px.line(
        monthly_profit,
        x="Month",
        y="Profit",
        markers=True,
        title="Monthly Profit"
    )

    fig_monthly_profit.update_layout(
        xaxis_title="Month",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_monthly_profit,
        use_container_width=True
    )


# ---------------------------------------------------------
# ORDER COUNT ANALYSIS
# ---------------------------------------------------------

st.header("🧾 Order Behavior")

col1, col2 = st.columns(2)


# Orders by Payment Method

payment_orders = (
    filtered_df
    .groupby("Payment Method")["Order ID"]
    .nunique()
    .reset_index(name="Orders")
)

with col1:

    fig_payment_orders = px.bar(
        payment_orders,
        x="Payment Method",
        y="Orders",
        title="Orders by Payment Method",
        text_auto=True
    )

    fig_payment_orders.update_layout(
        xaxis_title="Payment Method",
        yaxis_title="Number of Orders"
    )

    st.plotly_chart(
        fig_payment_orders,
        use_container_width=True
    )


# Orders by Purchase Type

purchase_orders = (
    filtered_df
    .groupby("Purchase Type")["Order ID"]
    .nunique()
    .reset_index(name="Orders")
)

with col2:

    fig_purchase_orders = px.bar(
        purchase_orders,
        x="Purchase Type",
        y="Orders",
        title="Orders by Purchase Type",
        text_auto=True
    )

    fig_purchase_orders.update_layout(
        xaxis_title="Purchase Type",
        yaxis_title="Number of Orders"
    )

    st.plotly_chart(
        fig_purchase_orders,
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
# AI BUSINESS INSIGHTS
# =========================================================

st.divider()

st.header("🧠 AI Business Insights")

ai_col1, ai_col2 = st.columns(2)


with ai_col1:

    st.subheader("📌 AI Analysis")

    ai_results = (
        filtered_df["AI_Result"]
        .astype(str)
        .value_counts()
    )

    if not ai_results.empty:

        for result, count in ai_results.items():

            st.write(
                f"• **{result}** — {count} records"
            )

    else:

        st.info("No AI analysis available for the selected data.")


with ai_col2:

    st.subheader("🚨 AI Anomaly Status")

    anomaly_counts = (
        filtered_df["AI_Anomaly"]
        .astype(str)
        .value_counts()
    )

    if not anomaly_counts.empty:

        for status, count in anomaly_counts.items():

            if status.lower() == "normal":

                st.success(
                    f"✅ {status}: {count} records"
                )

            else:

                st.warning(
                    f"⚠️ {status}: {count} records"
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
