import pandas as pd
from sklearn.ensemble import IsolationForest

# ========================================
# RESTAURANTIQ — LOCAL AI / ML ANALYSIS
# No API, no payment required
# ========================================

# Load restaurant data
df = pd.read_csv(r"C:\Users\KIIT\Downloads\restaurant_sales.csv")

# Convert Date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y"
)

print("\n========================================")
print("      RESTAURANTIQ AI ANALYSIS")
print("========================================")


# ========================================
# 1. PREPARE DATA FOR MACHINE LEARNING
# ========================================

features = df[
    ["Price", "Quantity", "Revenue", "Profit", "Profit Margin"]
].copy()


# ========================================
# 2. TRAIN AI MODEL
# ========================================

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(features)

# Predict anomalies
df["AI_Result"] = model.predict(features)

# -1 = unusual/anomalous
#  1 = normal
df["AI_Anomaly"] = df["AI_Result"].map({
    1: "Normal",
    -1: "Unusual"
})


# ========================================
# 3. FIND UNUSUAL ORDERS
# ========================================

unusual_orders = df[df["AI_Anomaly"] == "Unusual"].copy()

print("\n--- AI DETECTED UNUSUAL ORDERS ---")

print(
    unusual_orders[
        [
            "Order ID",
            "Product",
            "City",
            "Revenue",
            "Profit",
            "AI_Anomaly"
        ]
    ].sort_values(
        "Revenue",
        ascending=False
    ).to_string(index=False)
)


# ========================================
# 4. AI SUMMARY
# ========================================

total_orders = len(df)
unusual_count = len(unusual_orders)
normal_count = total_orders - unusual_count

unusual_percentage = (
    unusual_count / total_orders
) * 100


print("\n--- AI SUMMARY ---")

print("Total Orders:", total_orders)
print("Normal Orders:", normal_count)
print("Unusual Orders:", unusual_count)
print(
    "Unusual Order Percentage:",
    round(unusual_percentage, 2),
    "%"
)


# ========================================
# 5. BUSINESS INSIGHTS
# ========================================

best_product = (
    df.groupby("Product")["Revenue"]
    .sum()
    .idxmax()
)

best_city = (
    df.groupby("City")["Revenue"]
    .sum()
    .idxmax()
)

best_manager = (
    df.groupby("Manager")["Profit"]
    .sum()
    .idxmax()
)

highest_revenue_order = df.loc[
    df["Revenue"].idxmax()
]


print("\n--- AI BUSINESS INSIGHTS ---")

print(
    "1. Highest revenue product:",
    best_product
)

print(
    "2. Highest revenue city:",
    best_city
)

print(
    "3. Highest profit manager:",
    best_manager
)

print(
    "4. Highest revenue order:",
    highest_revenue_order["Order ID"]
)

print(
    "5. AI detected",
    unusual_count,
    "unusual orders."
)


# ========================================
# 6. RECOMMENDATIONS
# ========================================

print("\n--- AI RECOMMENDATIONS ---")

print(
    "• Investigate the unusual orders detected by the ML model."
)

print(
    "• Focus marketing and inventory planning on the highest-revenue products."
)

print(
    "• Prioritize the highest-performing cities for expansion and promotions."
)

print(
    "• Review unusually high or low transactions for possible data-entry or business issues."
)


# ========================================
# 7. SAVE AI RESULTS
# ========================================

df.to_csv(
    r"C:\RestaurantIQ\ai_analysis_results.csv",
    index=False
)

print("\n--- AI ANALYSIS COMPLETE ---")
print(
    "Results saved to: C:\\RestaurantIQ\\ai_analysis_results.csv"
)