import pandas as pd

df = pd.read_csv(r"C:\Users\KIIT\Downloads\restaurant_sales.csv")

print("\n--- DATASET INFO ---")
df.info()

print("\n--- SUMMARY STATISTICS ---")
print(df.describe())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print(df.head())
print(df.shape)
print("\n--- CLEANING DATE ---")

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y"
)

print(df["Date"].head())
print(df["Date"].dtype)
print("\n--- NUMERIC COLUMN CHECK ---")

numeric_columns = [
    "Price",
    "Quantity",
    "Revenue",
    "Profit",
    "Profit Margin"
]

print(df[numeric_columns].dtypes)

print("\n--- NEGATIVE VALUES ---")
print((df[numeric_columns] < 0).sum())
print("\n--- PRODUCT PERFORMANCE ---")

product_analysis = df.groupby("Product").agg(
    quantity_sold=("Quantity", "sum"),
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
).sort_values("revenue", ascending=False)

print(product_analysis)
print("\n--- CITY PERFORMANCE ---")

city_analysis = df.groupby("City").agg(
    quantity_sold=("Quantity", "sum"),
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
).sort_values("revenue", ascending=False)

print(city_analysis)
print("\n--- MANAGER PERFORMANCE ---")

manager_analysis = df.groupby("Manager").agg(
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum"),
    quantity_sold=("Quantity", "sum")
).sort_values("revenue", ascending=False)

print(manager_analysis)
print("\n--- PURCHASE TYPE PERFORMANCE ---")

purchase_analysis = df.groupby("Purchase Type").agg(
    quantity_sold=("Quantity", "sum"),
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
).sort_values("revenue", ascending=False)

print(purchase_analysis)


print("\n--- PAYMENT METHOD PERFORMANCE ---")

payment_analysis = df.groupby("Payment Method").agg(
    quantity_sold=("Quantity", "sum"),
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
).sort_values("revenue", ascending=False)

print(payment_analysis)
print("\n--- PRODUCT PROFITABILITY ---")

product_profitability = df.groupby("Product").agg(
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
)

product_profitability["profit_margin_pct"] = (
    product_profitability["profit"]
    / product_profitability["revenue"]
) * 100

product_profitability = product_profitability.sort_values(
    "profit", ascending=False
)

print(product_profitability)
print("\n--- CITY × PRODUCT PERFORMANCE ---")

city_product = df.groupby(["City", "Product"]).agg(
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum"),
    quantity_sold=("Quantity", "sum")
).sort_values("revenue", ascending=False)

print(city_product)
print("\n--- MANAGER × CITY PERFORMANCE ---")

manager_city = df.groupby(["Manager", "City"]).agg(
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
).sort_values("revenue", ascending=False)

print(manager_city)
print("\n--- HIGH-VALUE ORDERS ---")

high_value_orders = df[df["Revenue"] >= 1000]

print(high_value_orders[
    ["Order ID", "Product", "City", "Revenue", "Profit"]
].sort_values("Revenue", ascending=False))
print("\n--- TOP 5 PRODUCTS BY QUANTITY ---")

top_quantity_products = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_quantity_products)
print("\n--- TOP 5 PRODUCTS BY PROFIT ---")

top_profit_products = (
    df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_profit_products)
print("\n--- TOP 5 PRODUCTS BY PROFIT ---")

top_profit_products = (
    df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_profit_products)
print("\n--- MONTHLY REVENUE ---")

monthly_revenue = (
    df.groupby(df["Date"].dt.month)
    .agg(revenue=("Revenue", "sum"))
    .sort_index()
)

print(monthly_revenue)
print("\n--- MONTHLY PROFIT ---")

monthly_profit = (
    df.groupby(df["Date"].dt.month)
    .agg(profit=("Profit", "sum"))
    .sort_index()
)

print(monthly_profit)
print("\n--- MONTHLY PROFIT ---")

monthly_profit = (
    df.groupby(df["Date"].dt.month)
    .agg(profit=("Profit", "sum"))
    .sort_index()
)

print(monthly_profit)
print("\n--- MONTHLY REVENUE ---")

monthly_revenue = (
    df.groupby(df["Date"].dt.month)
    .agg(revenue=("Revenue", "sum"))
    .sort_index()
)

print(monthly_revenue)
print("\n--- MONTHLY PROFIT ---")

monthly_profit = (
    df.groupby(df["Date"].dt.month)
    .agg(profit=("Profit", "sum"))
    .sort_index()
)

print(monthly_profit)
print("\n--- MONTHLY PROFIT ---")

monthly_profit = (
    df.groupby(df["Date"].dt.month)
    .agg(profit=("Profit", "sum"))
    .sort_index()
)

print(monthly_profit)
print("\n--- MONTHLY PERFORMANCE ---")

monthly_performance = (
    df.groupby(df["Date"].dt.month)
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum"),
        quantity_sold=("Quantity", "sum")
    )
    .sort_index()
)

print(monthly_performance)
print("\n--- MONTHLY PERFORMANCE WITH MONTH NAMES ---")

monthly_performance_named = (
    df.groupby(df["Date"].dt.month)
    .agg(
        revenue=("Revenue", "sum"),
        profit=("Profit", "sum"),
        quantity_sold=("Quantity", "sum")
    )
    .sort_index()
)

monthly_performance_named.index = monthly_performance_named.index.map(
    lambda x: pd.Timestamp(2022, x, 1).strftime("%B")
)

print(monthly_performance_named)


print("\n--- BEST AND WORST MONTHS ---")

best_month = monthly_performance_named["revenue"].idxmax()
best_revenue = monthly_performance_named["revenue"].max()

worst_month = monthly_performance_named["revenue"].idxmin()
worst_revenue = monthly_performance_named["revenue"].min()

print("Best Revenue Month:", best_month)
print("Best Revenue:", best_revenue)

print("Lowest Revenue Month:", worst_month)
print("Lowest Revenue:", worst_revenue)
print("\n--- BEST REVENUE MONTH ---")

best_month = monthly_performance["revenue"].idxmax()
best_month_revenue = monthly_performance["revenue"].max()

print("Best Month:", best_month)
print("Revenue:", best_month_revenue)
print("\n--- LOWEST REVENUE MONTH ---")

lowest_month = monthly_performance["revenue"].idxmin()
lowest_month_revenue = monthly_performance["revenue"].min()

print("Lowest Month:", lowest_month)
print("Revenue:", lowest_month_revenue)
print("\n--- BEST AND WORST MONTHS ---")

best_month = monthly_performance_named["revenue"].idxmax()
best_revenue = monthly_performance_named["revenue"].max()

worst_month = monthly_performance_named["revenue"].idxmin()
worst_revenue = monthly_performance_named["revenue"].min()

print("Best Revenue Month:", best_month)
print("Best Revenue:", best_revenue)

print("Lowest Revenue Month:", worst_month)
print("Lowest Revenue:", worst_revenue)
# ========================================
# STEP 7 — ADVANCED ANALYSIS
# ========================================

# 7.1 City × Product
print("\n--- CITY × PRODUCT ANALYSIS ---")

city_product = df.groupby(["City", "Product"]).agg(
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum"),
    quantity_sold=("Quantity", "sum")
).sort_values("revenue", ascending=False)

print(city_product)


# 7.2 Manager × City
print("\n--- MANAGER × CITY ANALYSIS ---")

manager_city = df.groupby(["Manager", "City"]).agg(
    revenue=("Revenue", "sum"),
    profit=("Profit", "sum")
).sort_values("revenue", ascending=False)

print(manager_city)


# 7.3 High-Value Orders
print("\n--- HIGH-VALUE ORDERS ---")

high_value_orders = df[df["Revenue"] >= 1000]

print(
    high_value_orders[
        ["Order ID", "Product", "City", "Revenue", "Profit"]
    ].sort_values("Revenue", ascending=False)
)


# 7.4 Top 5 Products by Quantity
print("\n--- TOP 5 PRODUCTS BY QUANTITY ---")

top_quantity = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_quantity)


# 7.5 Top 5 Products by Profit
print("\n--- TOP 5 PRODUCTS BY PROFIT ---")

top_profit = (
    df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_profit)
# ========================================
# STEP 8 — BUSINESS INSIGHTS
# ========================================

print("\n--- KEY BUSINESS INSIGHTS ---")

# Best product by revenue
best_product = (
    df.groupby("Product")["Revenue"]
    .sum()
    .idxmax()
)

best_product_revenue = (
    df.groupby("Product")["Revenue"]
    .sum()
    .max()
)

print("Best Product by Revenue:", best_product)
print("Revenue:", best_product_revenue)


# Best city by revenue
best_city = (
    df.groupby("City")["Revenue"]
    .sum()
    .idxmax()
)

best_city_revenue = (
    df.groupby("City")["Revenue"]
    .sum()
    .max()
)

print("Best City by Revenue:", best_city)
print("Revenue:", best_city_revenue)


# Most profitable product
most_profitable_product = (
    df.groupby("Product")["Profit"]
    .sum()
    .idxmax()
)

most_profitable_product_profit = (
    df.groupby("Product")["Profit"]
    .sum()
    .max()
)

print("Most Profitable Product:", most_profitable_product)
print("Profit:", most_profitable_product_profit)


# Best manager by profit
best_manager = (
    df.groupby("Manager")["Profit"]
    .sum()
    .idxmax()
)

best_manager_profit = (
    df.groupby("Manager")["Profit"]
    .sum()
    .max()
)

print("Best Manager by Profit:", best_manager)
print("Profit:", best_manager_profit)


# Best revenue month
best_month = monthly_performance_named["revenue"].idxmax()
best_month_revenue = monthly_performance_named["revenue"].max()

print("Best Revenue Month:", best_month)
print("Revenue:", best_month_revenue)


# Highest-value order
highest_order = df.loc[df["Revenue"].idxmax()]

print("Highest Revenue Order ID:", highest_order["Order ID"])
print("Highest Revenue Order:", highest_order["Revenue"])
print("Highest Revenue Product:", highest_order["Product"])