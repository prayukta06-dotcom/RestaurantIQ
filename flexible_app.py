```python
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
# BASIC STYLING
# =========================================================

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
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.title("🍽️ RestaurantIQ")

st.subheader(
    "Restaurant Sales Intelligence Dashboard"
)

st.write(
    "Upload a restaurant CSV or Excel file and "
    "RestaurantIQ will adapt its analysis to your data."
)

st.divider()


# =========================================================
# FILE UPLOAD
# =========================================================

st.sidebar.title("🍽️ RestaurantIQ")

st.sidebar.caption("Upload your restaurant data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


# =========================================================
# LOAD FILE
# =========================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a CSV or Excel file from the sidebar "
        "to begin."
    )

    st.write("### Supported files")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("📄 **CSV**")
        st.write("Comma-separated restaurant data")

    with col2:
        st.write("📊 **Excel**")
        st.write("`.xlsx` and `.xls` files")

    with col3:
        st.write("🔄 **Flexible columns**")
        st.write("Map your own column names")

    st.stop()


try:

    if uploaded_file.name.lower().endswith(".csv"):

        raw_df = pd.read_csv(uploaded_file)

    else:

        raw_df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(
        f"Could not read the uploaded file: {e}"
    )

    st.stop()


# =========================================================
# SHOW UPLOADED DATA
# =========================================================

st.success(
    f"Successfully loaded **{uploaded_file.name}**"
)

st.write(
    f"Rows: **{len(raw_df):,}** | "
    f"Columns: **{len(raw_df.columns):,}**"
)

with st.expander("Preview uploaded data"):

    st.dataframe(
        raw_df.head(10),
        use_container_width=True
    )


# =========================================================
# COLUMN MAPPING
# =========================================================

st.header("🔗 Column Mapping")

st.write(
    "RestaurantIQ detected your columns. "
    "Choose which column represents each business field."
)


available_columns = ["— Not available —"] + list(
    raw_df.columns
)


def auto_detect(possible_names):

    lower_map = {
        str(column).strip().lower(): column
        for column in raw_df.columns
    }

    for name in possible_names:

        if name.lower() in lower_map:

            return lower_map[name.lower()]

    for column in raw_df.columns:

        column_text = str(column).strip().lower()

        for name in possible_names:

            if name.lower() in column_text:

                return column

    return "— Not available —"


# ---------------------------------------------------------
# DETECT COMMON COLUMN NAMES
# ---------------------------------------------------------

default_date = auto_detect([
    "date",
    "order date",
    "transaction date",
    "sale date",
    "datetime",
    "timestamp"
])

default_product = auto_detect([
    "product",
    "product name",
    "item",
    "item name",
    "dish",
    "dish name",
    "menu item"
])

default_quantity = auto_detect([
    "quantity",
    "qty",
    "units",
    "units sold",
    "quantity sold"
])

default_price = auto_detect([
    "price",
    "unit price",
    "selling price",
    "sale price"
])

default_revenue = auto_detect([
    "revenue",
    "sales",
    "total sales",
    "total revenue",
    "amount",
    "sales amount"
])

default_cost = auto_detect([
    "cost",
    "unit cost",
    "food cost",
    "purchase cost"
])

default_city = auto_detect([
    "city",
    "location",
    "branch",
    "restaurant",
    "outlet"
])

default_manager = auto_detect([
    "manager",
    "manager name",
    "supervisor"
])

default_order = auto_detect([
    "order id",
    "order_id",
    "transaction id",
    "transaction_id",
    "invoice id",
    "invoice_id"
])


# =========================================================
# MAPPING UI
# =========================================================

col1, col2 = st.columns(2)


with col1:

    date_column = st.selectbox(
        "📅 Date column",
        available_columns,
        index=(
            available_columns.index(default_date)
            if default_date in available_columns
            else 0
        )
    )

    product_column = st.selectbox(
        "🍔 Product column",
        available_columns,
        index=(
            available_columns.index(default_product)
            if default_product in available_columns
            else 0
        )
    )

    quantity_column = st.selectbox(
        "📦 Quantity column",
        available_columns,
        index=(
            available_columns.index(default_quantity)
            if default_quantity in available_columns
            else 0
        )
    )

    price_column = st.selectbox(
        "💵 Price column",
        available_columns,
        index=(
            available_columns.index(default_price)
            if default_price in available_columns
            else 0
        )
    )

    revenue_column = st.selectbox(
        "💰 Revenue column",
        available_columns,
        index=(
            available_columns.index(default_revenue)
            if default_revenue in available_columns
            else 0
        )
    )


with col2:

    cost_column = st.selectbox(
        "💸 Cost column",
        available_columns,
        index=(
            available_columns.index(default_cost)
            if default_cost in available_columns
            else 0
        )
    )

    city_column = st.selectbox(
        "🌍 City / Location column",
        available_columns,
        index=(
            available_columns.index(default_city)
            if default_city in available_columns
            else 0
        )
    )

    manager_column = st.selectbox(
        "👨‍💼 Manager column",
        available_columns,
        index=(
            available_columns.index(default_manager)
            if default_manager in available_columns
            else 0
        )
    )

    order_column = st.selectbox(
        "🧾 Order ID column",
        available_columns,
        index=(
            available_columns.index(default_order)
            if default_order in available_columns
            else 0
        )
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.divider()

analyze = st.button(
    "🚀 Analyze Restaurant Data",
    type="primary"
)


if not analyze:

    st.info(
        "Select the appropriate columns above, "
        "then click **Analyze Restaurant Data**."
    )

    st.stop()


# =========================================================
# CREATE STANDARDIZED DATASET
# =========================================================

df = raw_df.copy()


def get_column(selected_column):

    if selected_column == "— Not available —":

        return None

    return selected_column


date_source = get_column(date_column)
product_source = get_column(product_column)
quantity_source = get_column(quantity_column)
price_source = get_column(price_column)
revenue_source = get_column(revenue_column)
cost_source = get_column(cost_column)
city_source = get_column(city_column)
manager_source = get_column(manager_column)
order_source = get_column(order_column)


# ---------------------------------------------------------
# DATE
# ---------------------------------------------------------

if date_source is not None:

    df["RIQ_Date"] = pd.to_datetime(
        df[date_source],
        errors="coerce"
    )

else:

    df["RIQ_Date"] = pd.NaT


# ---------------------------------------------------------
# PRODUCT
# ---------------------------------------------------------

if product_source is not None:

    df["RIQ_Product"] = (
        df[product_source]
        .astype(str)
    )

else:

    df["RIQ_Product"] = "Unknown"


# ---------------------------------------------------------
# QUANTITY
# ---------------------------------------------------------

if quantity_source is not None:

    df["RIQ_Quantity"] = pd.to_numeric(
        df[quantity_source],
        errors="coerce"
    ).fillna(0)

else:

    df["RIQ_Quantity"] = 0


# ---------------------------------------------------------
# PRICE
# ---------------------------------------------------------

if price_source is not None:

    df["RIQ_Price"] = pd.to_numeric(
        df[price_source],
        errors="coerce"
    ).fillna(0)

else:

    df["RIQ_Price"] = 0


# ---------------------------------------------------------
# REVENUE
# ---------------------------------------------------------

if revenue_source is not None:

    df["RIQ_Revenue"] = pd.to_numeric(
        df[revenue_source],
        errors="coerce"
    ).fillna(0)

elif quantity_source is not None and price_source is not None:

    df["RIQ_Revenue"] = (
        df["RIQ_Quantity"] *
        df["RIQ_Price"]
    )

else:

    df["RIQ_Revenue"] = 0


# ---------------------------------------------------------
# COST
# ---------------------------------------------------------

if cost_source is not None:

    df["RIQ_Cost"] = pd.to_numeric(
        df[cost_source],
        errors="coerce"
    ).fillna(0)

else:

    df["RIQ_Cost"] = 0


# ---------------------------------------------------------
# PROFIT
# ---------------------------------------------------------

if cost_source is not None:

    df["RIQ_Profit"] = (
        df["RIQ_Revenue"] -
        (
            df["RIQ_Cost"] *
            df["RIQ_Quantity"]
        )
    )

else:

    df["RIQ_Profit"] = 0


# ---------------------------------------------------------
# CITY
# ---------------------------------------------------------

if city_source is not None:

    df["RIQ_City"] = (
        df[city_source]
        .astype(str)
    )

else:

    df["RIQ_City"] = "Not Available"


# ---------------------------------------------------------
# MANAGER
# ---------------------------------------------------------

if manager_source is not None:

    df["RIQ_Manager"] = (
        df[manager_source]
        .astype(str)
    )

else:

    df["RIQ_Manager"] = "Not Available"


# ---------------------------------------------------------
# ORDER ID
# ---------------------------------------------------------

if order_source is not None:

    df["RIQ_Order"] = (
        df[order_source]
        .astype(str)
    )

else:

    df["RIQ_Order"] = df.index.astype(str)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = df["RIQ_Revenue"].sum()

total_profit = df["RIQ_Profit"].sum()

total_quantity = df["RIQ_Quantity"].sum()

total_orders = df["RIQ_Order"].nunique()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


with col2:

    if cost_source is not None:

        st.metric(
            "Total Profit",
            f"₹{total_profit:,.0f}"
        )

    else:

        st.metric(
            "Total Profit",
            "N/A"
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


# =========================================================
# REVENUE TREND
# =========================================================

if date_source is not None:

    st.divider()

    st.header("📈 Revenue Trend")

    trend_df = (
        df.dropna(subset=["RIQ_Date"])
        .groupby("RIQ_Date")["RIQ_Revenue"]
        .sum()
        .reset_index()
    )

    if not trend_df.empty:

        fig = px.line(
            trend_df,
            x="RIQ_Date",
            y="RIQ_Revenue",
            markers=True,
            title="Revenue Over Time"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

if product_source is not None:

    st.divider()

    st.header("🍔 Product Analysis")

    col1, col2 = st.columns(2)


    product_revenue = (
        df.groupby("RIQ_Product")["RIQ_Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


    with col1:

        fig = px.bar(
            product_revenue,
            x="RIQ_Product",
            y="RIQ_Revenue",
            title="Revenue by Product"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    product_quantity = (
        df.groupby("RIQ_Product")["RIQ_Quantity"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


    with col2:

        fig = px.bar(
            product_quantity,
            x="RIQ_Product",
            y="RIQ_Quantity",
            title="Quantity Sold by Product"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CITY ANALYSIS
# =========================================================

if city_source is not None:

    st.divider()

    st.header("🌍 Location Analysis")

    city_revenue = (
        df.groupby("RIQ_City")["RIQ_Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        city_revenue,
        x="RIQ_City",
        y="RIQ_Revenue",
        title="Revenue by Location"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MANAGER ANALYSIS
# =========================================================

if manager_source is not None:

    st.divider()

    st.header("👨‍💼 Manager Performance")

    manager_revenue = (
        df.groupby("RIQ_Manager")["RIQ_Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        manager_revenue,
        x="RIQ_Manager",
        y="RIQ_Revenue",
        title="Revenue by Manager"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.divider()

st.header("💡 Business Insights")


if product_source is not None and not df.empty:

    best_product = (
        df.groupby("RIQ_Product")["RIQ_Revenue"]
        .sum()
        .idxmax()
    )

    best_product_revenue = (
        df.groupby("RIQ_Product")["RIQ_Revenue"]
        .sum()
        .max()
    )

    st.success(
        f"🏆 Top revenue product: **{best_product}** "
        f"with ₹{best_product_revenue:,.0f} revenue."
    )


if city_source is not None and not df.empty:

    best_city = (
        df.groupby("RIQ_City")["RIQ_Revenue"]
        .sum()
        .idxmax()
    )

    best_city_revenue = (
        df.groupby("RIQ_City")["RIQ_Revenue"]
        .sum()
        .max()
    )

    st.info(
        f"🌍 Top revenue location: **{best_city}** "
        f"with ₹{best_city_revenue:,.0f} revenue."
    )


if cost_source is None:

    st.warning(
        "⚠️ Profit analysis is unavailable because "
        "no cost column was provided."
    )


# =========================================================
# DATA PREVIEW
# =========================================================

st.divider()

st.header("📋 Uploaded Data")

st.dataframe(
    raw_df,
    use_container_width=True,
    hide_index=True
)
```
