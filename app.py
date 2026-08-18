```python
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="RestaurantIQ",
    page_icon="🍽️",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🍽️ RestaurantIQ")
st.subheader("Restaurant Sales Intelligence Dashboard")

st.write(
    "Analyze restaurant sales, revenue, profit and product "
    "performance using your RestaurantIQ data."
)

st.divider()

# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def load_csv(filename):
    """
    Load a CSV file if it exists in the GitHub repository.
    """
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename)
        except Exception as e:
            st.error(f"Could not read {filename}: {e}")

    return None


# ---------------------------------------------------------
# LOAD EXISTING DATA
# ---------------------------------------------------------

ai_results = load_csv("ai_analysis_results.csv")


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🍽️ RestaurantIQ")

st.sidebar.write(
    "Restaurant Sales Intelligence"
)

st.sidebar.divider()

st.sidebar.info(
    "Upload a CSV file below to analyze your restaurant data."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Sales Data",
    type=["csv"]
)


# ---------------------------------------------------------
# SELECT DATA SOURCE
# ---------------------------------------------------------

df = None

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        st.success(
            "Your CSV file has been uploaded successfully."
        )

    except Exception as e:

        st.error(
            f"Unable to read the uploaded file: {e}"
        )

elif ai_results is not None:

    df = ai_results


# ---------------------------------------------------------
# NO DATA AVAILABLE
# ---------------------------------------------------------

if df is None:

    st.info(
        "👈 Upload your restaurant CSV from the sidebar "
        "to begin the analysis."
    )

    st.write("### RestaurantIQ")

    st.write(
        "This dashboard will provide insights such as:"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### 💰 Revenue")
        st.write(
            "Analyze total and product-level revenue."
        )

    with col2:
        st.write("### 📦 Products")
        st.write(
            "Identify your best-performing products."
        )

    with col3:
        st.write("### 📈 Trends")
        st.write(
            "Understand changes in restaurant sales."
        )

    st.stop()


# ---------------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------------

st.header("📋 Data Overview")

st.write(
    f"Dataset contains **{df.shape[0]:,} rows** "
    f"and **{df.shape[1]:,} columns**."
)

st.dataframe(
    df.head(10),
    use_container_width=True
)


# ---------------------------------------------------------
# COLUMN DETECTION
# ---------------------------------------------------------

columns = df.columns.tolist()

lower_columns = {
    str(column).lower(): column
    for column in columns
}


def find_column(possible_names):

    for name in possible_names:

        if name.lower() in lower_columns:
            return lower_columns[name.lower()]

    return None


quantity_col = find_column([
    "quantity",
    "qty",
    "units",
    "units_sold"
])

price_col = find_column([
    "price",
    "unit_price",
    "selling_price",
    "sale_price"
])

cost_col = find_column([
    "cost",
    "unit_cost",
    "purchase_cost"
])

revenue_col = find_column([
    "revenue",
    "sales",
    "total_sales",
    "total_revenue"
])

profit_col = find_column([
    "profit",
    "total_profit"
])

product_col = find_column([
    "item",
    "product",
    "product_name",
    "item_name",
    "dish",
    "dish_name"
])


# ---------------------------------------------------------
# CALCULATE REVENUE
# ---------------------------------------------------------

if revenue_col is None:

    if quantity_col is not None and price_col is not None:

        df["Calculated Revenue"] = (
            pd.to_numeric(
                df[quantity_col],
                errors="coerce"
            ).fillna(0)
            *
            pd.to_numeric(
                df[price_col],
                errors="coerce"
            ).fillna(0)
        )

        revenue_col = "Calculated Revenue"


# ---------------------------------------------------------
# CALCULATE PROFIT
# ---------------------------------------------------------

if profit_col is None:

    if revenue_col is not None and cost_col is not None:

        revenue_values = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        ).fillna(0)

        cost_values = pd.to_numeric(
            df[cost_col],
            errors="coerce"
        ).fillna(0)

        if quantity_col is not None:

            quantity_values = pd.to_numeric(
                df[quantity_col],
                errors="coerce"
            ).fillna(0)

            df["Calculated Profit"] = (
                revenue_values
                -
                (cost_values * quantity_values)
            )

        else:

            df["Calculated Profit"] = (
                revenue_values - cost_values
            )

        profit_col = "Calculated Profit"


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


# Revenue KPI

with col1:

    if revenue_col is not None:

        total_revenue = pd.to_numeric(
            df[revenue_col],
            errors="coerce"
        ).fillna(0).sum()

        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

    else:

        st.metric(
            "Total Revenue",
            "N/A"
        )


# Profit KPI

with col2:

    if profit_col is not None:

        total_profit = pd.to_numeric(
            df[profit_col],
            errors="coerce"
        ).fillna(0).sum()

        st.metric(
            "Total Profit",
            f"₹{total_profit:,.2f}"
        )

    else:

        st.metric(
            "Total Profit",
            "N/A"
        )


# Quantity KPI

with col3:

    if quantity_col is not None:

        total_quantity = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        ).fillna(0).sum()

        st.metric(
            "Items Sold",
            f"{total_quantity:,.0f}"
        )

    else:

        st.metric(
            "Items Sold",
            "N/A"
        )


# Product KPI

with col4:

    if product_col is not None:

        number_products = df[product_col].nunique()

        st.metric(
            "Products",
            f"{number_products:,}"
        )

    else:

        st.metric(
            "Products",
            "N/A"
        )


# ---------------------------------------------------------
# PRODUCT ANALYSIS
# ---------------------------------------------------------

if product_col is not None:

    st.divider()

    st.header("🏆 Product Analysis")

    # Quantity by product

    if quantity_col is not None:

        product_quantity = (
            df.groupby(product_col)[quantity_col]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.subheader("Top-Selling Products")

        fig = px.bar(
            product_quantity,
            x=product_quantity.values,
            y=product_quantity.index,
            orientation="h",
            labels={
                "x": "Quantity Sold",
                "y": "Product"
            },
            title="Top 10 Products by Quantity Sold"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Revenue by product

    if revenue_col is not None:

        product_revenue = (
            df.groupby(product_col)[revenue_col]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.subheader("Top Products by Revenue")

        fig = px.bar(
            product_revenue,
            x=product_revenue.values,
            y=product_revenue.index,
            orientation="h",
            labels={
                "x": "Revenue",
                "y": "Product"
            },
            title="Top 10 Products by Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Profit by product

    if profit_col is not None:

        product_profit = (
            df.groupby(product_col)[profit_col]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.subheader("Most Profitable Products")

        fig = px.bar(
            product_profit,
            x=product_profit.values,
            y=product_profit.index,
            orientation="h",
            labels={
                "x": "Profit",
                "y": "Product"
            },
            title="Top 10 Products by Profit"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ---------------------------------------------------------
# DATA SUMMARY
# ---------------------------------------------------------

st.divider()

st.header("🔍 Data Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.write("### Dataset Columns")

    for column in columns:

        st.write(f"• {column}")


with summary_col2:

    st.write("### Detected Business Fields")

    st.write(
        f"Revenue: **{revenue_col or 'Not detected'}**"
    )

    st.write(
        f"Profit: **{profit_col or 'Not detected'}**"
    )

    st.write(
        f"Quantity: **{quantity_col or 'Not detected'}**"
    )

    st.write(
        f"Product: **{product_col or 'Not detected'}**"
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "RestaurantIQ — Restaurant Sales Intelligence"
)
```
