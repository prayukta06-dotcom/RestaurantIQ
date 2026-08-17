# RestaurantIQ

## Restaurant Sales Analytics & AI-Powered Anomaly Detection

RestaurantIQ is an end-to-end restaurant analytics project that uses Python, SQL, Machine Learning, and Power BI to turn restaurant sales data into actionable business insights.

## Objective

The project helps restaurant management understand:

- Revenue performance
- Profitability
- Product performance
- City performance
- Order trends
- Monthly revenue trends
- Unusual transactions
- Business opportunities

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- SQL
- Power BI
- GitHub

## Project Workflow

Raw Restaurant Data
↓
Data Cleaning
↓
SQL Analysis
↓
Python Analysis
↓
Machine Learning
↓
Anomaly Detection
↓
Power BI Dashboard
↓
Business Insights

## Machine Learning

RestaurantIQ uses the Isolation Forest algorithm from Scikit-learn for anomaly detection.

The model analyzes:

- Price
- Quantity
- Revenue
- Profit
- Profit Margin

It identifies transactions that are unusual compared with the normal patterns in the dataset.

An unusual transaction is not automatically fraudulent. It is a transaction that should be investigated further.

## Power BI Dashboard

The dashboard includes:

### KPI Cards

- Total Revenue
- Total Orders
- Total Profit
- Total Quantity

### Filters

- Product
- City
- Purchase Type
- Date

### Charts

- Revenue by Product
- Revenue by City
- Profit by Product
- Monthly Revenue

## Python Analysis

Python was used for:

- Data cleaning
- Data transformation
- Exploratory analysis
- Business metrics
- Chart generation
- Machine-learning anomaly detection

## Output

The machine-learning analysis creates:

`ai_analysis_results.csv`

This file contains the restaurant data together with the AI anomaly classification.

## Business Value

RestaurantIQ helps management:

- Identify high-performing products
- Identify strong-performing cities
- Understand profitability
- Monitor revenue trends
- Detect unusual transactions
- Make data-driven decisions

## Project Structure

```text
RestaurantIQ/
├── restaurant_analysis.py
├── charts.py
├── ai_insights.py
├── ai_analysis_results.csv
├── RestaurantIQ.pbix
├── README.md
└── charts/
    ├── revenue_by_product.png
    ├── revenue_by_city.png
    ├── profit_by_product.png
    └── monthly_revenue.png
    ## Future Improvements

- Sales forecasting
- Customer segmentation
- Product demand forecasting
- Automated dashboard refresh
- More advanced anomaly detection

## Conclusion

RestaurantIQ combines data analytics, machine learning, and interactive business intelligence into a decision-support solution for restaurant management.

