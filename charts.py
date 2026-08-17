import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv(r"C:\Users\KIIT\Downloads\restaurant_sales.csv")

# Convert Date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y"
)

# Create charts folder
os.makedirs("charts", exist_ok=True)


# ========================================
# 6.1 — REVENUE BY PRODUCT
# ========================================

product_revenue = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
product_revenue.plot(kind="bar")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/revenue_by_product.png", dpi=300, bbox_inches="tight")
plt.close()


# ========================================
# 6.2 — REVENUE BY CITY
# ========================================

city_revenue = (
    df.groupby("City")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
city_revenue.plot(kind="bar")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/revenue_by_city.png", dpi=300, bbox_inches="tight")
plt.close()


# ========================================
# 6.3 — PROFIT BY PRODUCT
# ========================================

product_profit = (
    df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
product_profit.plot(kind="bar")
plt.title("Profit by Product")
plt.xlabel("Product")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/profit_by_product.png", dpi=300, bbox_inches="tight")
plt.close()


# ========================================
# 6.4 — MONTHLY REVENUE TREND
# ========================================

monthly_revenue = (
    df.groupby(df["Date"].dt.month)["Revenue"]
    .sum()
    .sort_index()
)

monthly_revenue.index = monthly_revenue.index.map(
    lambda x: pd.Timestamp(2022, x, 1).strftime("%B")
)

plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png", dpi=300, bbox_inches="tight")
plt.close()


print("All 4 charts created successfully!")