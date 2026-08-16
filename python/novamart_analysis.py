# ============================================================
# NOVAMART SALES PERFORMANCE & BUSINESS ANALYTICS
# Python Data Analysis Project
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")
order_details = pd.read_csv("data/order_details.csv")

print("\n========== DATASET SIZES ==========")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Order Details:", order_details.shape)


# ============================================================
# 2. DATA INSPECTION
# ============================================================

print("\n========== CUSTOMERS ==========")
print(customers.head())

print("\n========== PRODUCTS ==========")
print(products.head())

print("\n========== ORDERS ==========")
print(orders.head())

print("\n========== ORDER DETAILS ==========")
print(order_details.head())


# ============================================================
# 3. DATA TYPES
# ============================================================

print("\n========== DATA TYPES ==========")

print("\nCustomers:")
print(customers.dtypes)

print("\nProducts:")
print(products.dtypes)

print("\nOrders:")
print(orders.dtypes)

print("\nOrder Details:")
print(order_details.dtypes)


# ============================================================
# 4. CONVERT ORDER DATE
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

print("\nOrder date converted successfully.")


# ============================================================
# 5. MISSING VALUE CHECK
# ============================================================

print("\n========== MISSING VALUES ==========")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Details:")
print(order_details.isnull().sum())


# ============================================================
# 6. DUPLICATE CHECK
# ============================================================

print("\n========== DUPLICATE CHECK ==========")

print(
    "Duplicate customer rows:",
    customers.duplicated().sum()
)

print(
    "Duplicate product rows:",
    products.duplicated().sum()
)

print(
    "Duplicate order rows:",
    orders.duplicated().sum()
)

print(
    "Duplicate order-detail rows:",
    order_details.duplicated().sum()
)


# ============================================================
# 7. PRIMARY KEY VALIDATION
# ============================================================

print("\n========== PRIMARY KEY VALIDATION ==========")

print(
    "Duplicate customer IDs:",
    customers["customer_id"].duplicated().sum()
)

print(
    "Duplicate product IDs:",
    products["product_id"].duplicated().sum()
)

print(
    "Duplicate order IDs:",
    orders["order_id"].duplicated().sum()
)

print(
    "Duplicate order-product combinations:",
    order_details.duplicated(
        subset=["order_id", "product_id"]
    ).sum()
)


# ============================================================
# 8. DESCRIPTIVE STATISTICS
# ============================================================

print("\n========== PRODUCT STATISTICS ==========")

print(
    products[
        ["unit_cost", "unit_price"]
    ].describe()
)

print("\n========== ORDER DETAIL STATISTICS ==========")

print(
    order_details[
        ["quantity", "discount"]
    ].describe()
)


# ============================================================
# 9. CREATE SALES DATASET
# ============================================================

print("\n========== CREATING SALES DATASET ==========")

sales = order_details.merge(
    products,
    on="product_id",
    how="left"
)

# Revenue
sales["revenue"] = (
    sales["unit_price"]
    * sales["quantity"]
    * (1 - sales["discount"])
)

# Cost
sales["cost"] = (
    sales["unit_cost"]
    * sales["quantity"]
)

# Profit
sales["profit"] = (
    sales["revenue"]
    - sales["cost"]
)

# Add order information
sales = sales.merge(
    orders,
    on="order_id",
    how="left"
)

print("Sales dataset shape:", sales.shape)


# ============================================================
# 10. OVERALL BUSINESS KPIs
# ============================================================

total_revenue = sales["revenue"].sum()

total_cost = sales["cost"].sum()

total_profit = sales["profit"].sum()

profit_margin = (
    total_profit
    / total_revenue
    * 100
)

total_orders = orders["order_id"].nunique()

total_customers = customers["customer_id"].nunique()

total_products = products["product_id"].nunique()

total_units = sales["quantity"].sum()

average_order_value = (
    total_revenue
    / total_orders
)


print("\n========== NOVAMART BUSINESS KPIs ==========")

print(
    f"Total Revenue       : ₹{total_revenue:,.2f}"
)

print(
    f"Total Cost          : ₹{total_cost:,.2f}"
)

print(
    f"Total Profit        : ₹{total_profit:,.2f}"
)

print(
    f"Profit Margin       : {profit_margin:.2f}%"
)

print(
    f"Total Orders        : {total_orders:,}"
)

print(
    f"Total Customers     : {total_customers:,}"
)

print(
    f"Total Products      : {total_products:,}"
)

print(
    f"Units Sold          : {total_units:,}"
)

print(
    f"Average Order Value : ₹{average_order_value:,.2f}"
)


# ============================================================
# 11. CATEGORY ANALYSIS
# ============================================================

category_sales = (
    sales
    .groupby("category")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

category_sales["profit_margin"] = (
    category_sales["profit"]
    / category_sales["revenue"]
    * 100
)

print("\n========== CATEGORY PERFORMANCE ==========")

print(category_sales)


# ============================================================
# 12. REVENUE BY CATEGORY CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_sales.index,
    category_sales["revenue"]
)

plt.title(
    "Revenue by Product Category"
)

plt.xlabel("Category")

plt.ylabel("Revenue")

plt.xticks(rotation=30)

plt.tight_layout()

plt.show()


# ============================================================
# 13. MONTHLY SALES ANALYSIS
# ============================================================

monthly_sales = (
    sales
    .groupby(
        sales["order_date"].dt.to_period("M")
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)

monthly_sales["month"] = (
    monthly_sales["order_date"]
    .astype(str)
)

monthly_sales["profit_margin"] = (
    monthly_sales["profit"]
    / monthly_sales["revenue"]
    * 100
)

print("\n========== MONTHLY PERFORMANCE ==========")

print(
    monthly_sales[
        [
            "month",
            "revenue",
            "profit",
            "orders",
            "profit_margin"
        ]
    ]
)


# ============================================================
# 14. MONTHLY REVENUE CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["month"],
    monthly_sales["revenue"],
    marker="o"
)

plt.title(
    "Monthly Revenue Trend"
)

plt.xlabel("Month")

plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 15. MONTH-OVER-MONTH GROWTH
# ============================================================

monthly_sales["previous_revenue"] = (
    monthly_sales["revenue"].shift(1)
)

monthly_sales["growth_percentage"] = (
    (
        monthly_sales["revenue"]
        - monthly_sales["previous_revenue"]
    )
    / monthly_sales["previous_revenue"]
    * 100
)

print("\n========== MONTHLY GROWTH ==========")

print(
    monthly_sales[
        [
            "month",
            "revenue",
            "previous_revenue",
            "growth_percentage"
        ]
    ]
)


# ============================================================
# 16. REGIONAL ANALYSIS
# ============================================================

regional_sales = (
    sales
    .groupby("region")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units=("quantity", "sum")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

regional_sales["profit_margin"] = (
    regional_sales["profit"]
    / regional_sales["revenue"]
    * 100
)

print("\n========== REGIONAL PERFORMANCE ==========")

print(regional_sales)


# ============================================================
# 17. SALES CHANNEL ANALYSIS
# ============================================================

channel_sales = (
    sales
    .groupby("sales_channel")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        units=("quantity", "sum")
    )
)

channel_sales["profit_margin"] = (
    channel_sales["profit"]
    / channel_sales["revenue"]
    * 100
)

channel_sales["average_order_value"] = (
    channel_sales["revenue"]
    / channel_sales["orders"]
)

print("\n========== SALES CHANNEL PERFORMANCE ==========")

print(channel_sales)


# ============================================================
# 18. CUSTOMER SEGMENT ANALYSIS
# ============================================================

customer_sales = sales.merge(
    customers[
        [
            "customer_id",
            "customer_name",
            "customer_segment"
        ]
    ],
    on="customer_id",
    how="left"
)

segment_sales = (
    customer_sales
    .groupby("customer_segment")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

segment_sales["profit_margin"] = (
    segment_sales["profit"]
    / segment_sales["revenue"]
    * 100
)

print("\n========== CUSTOMER SEGMENT PERFORMANCE ==========")

print(segment_sales)


# ============================================================
# 19. TOP 10 CUSTOMERS
# ============================================================

top_customers = (
    customer_sales
    .groupby(
        [
            "customer_id",
            "customer_name",
            "customer_segment"
        ]
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)

print("\n========== TOP 10 CUSTOMERS ==========")

print(
    top_customers.head(10)
)


# ============================================================
# 20. REPEAT CUSTOMER ANALYSIS
# ============================================================

orders_per_customer = (
    orders
    .groupby("customer_id")["order_id"]
    .nunique()
)

repeat_customers = (
    orders_per_customer > 1
).sum()

repeat_customer_rate = (
    repeat_customers
    / total_customers
    * 100
)

print("\n========== CUSTOMER RETENTION ==========")

print(
    "Repeat Customers:",
    repeat_customers
)

print(
    f"Repeat Customer Rate: "
    f"{repeat_customer_rate:.2f}%"
)


# ============================================================
# 21. DISCOUNT ANALYSIS
# ============================================================

discount_analysis = (
    sales
    .groupby("discount")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units=("quantity", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)

discount_analysis["profit_margin"] = (
    discount_analysis["profit"]
    / discount_analysis["revenue"]
    * 100
)

print("\n========== DISCOUNT ANALYSIS ==========")

print(discount_analysis)


# ============================================================
# 22. DISCOUNT VS PROFIT MARGIN
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    discount_analysis["discount"] * 100,
    discount_analysis["profit_margin"],
    marker="o"
)

plt.title(
    "Discount Level vs Profit Margin"
)

plt.xlabel(
    "Discount (%)"
)

plt.ylabel(
    "Profit Margin (%)"
)

plt.tight_layout()

plt.show()


# ============================================================
# 23. PRODUCT PERFORMANCE
# ============================================================

product_sales = (
    sales
    .groupby(
        [
            "product_id",
            "product_name",
            "category"
        ]
    )
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units=("quantity", "sum"),
        orders=("order_id", "nunique")
    )
)

product_sales["profit_margin"] = (
    product_sales["profit"]
    / product_sales["revenue"]
    * 100
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")

print(
    product_sales
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(10)
)


# ============================================================
# 24. HIGH REVENUE / LOW MARGIN PRODUCTS
# ============================================================

high_revenue_low_margin = (
    product_sales[
        (product_sales["revenue"] > 500000)
        &
        (product_sales["profit_margin"] < 30)
    ]
    .sort_values(
        "revenue",
        ascending=False
    )
)

print(
    "\n========== HIGH REVENUE / LOW MARGIN PRODUCTS =========="
)

print(high_revenue_low_margin)


# ============================================================
# 25. DATA INTEGRITY VALIDATION
# ============================================================

invalid_customer_ids = (
    set(orders["customer_id"])
    - set(customers["customer_id"])
)

invalid_order_ids = (
    set(order_details["order_id"])
    - set(orders["order_id"])
)

invalid_product_ids = (
    set(order_details["product_id"])
    - set(products["product_id"])
)

print("\n========== DATA INTEGRITY ==========")

print(
    "Invalid Customer IDs:",
    len(invalid_customer_ids)
)

print(
    "Invalid Order IDs:",
    len(invalid_order_ids)
)

print(
    "Invalid Product IDs:",
    len(invalid_product_ids)
)


# ============================================================
# 26. FINAL SUMMARY
# ============================================================

best_category = (
    category_sales["revenue"]
    .idxmax()
)

best_region = (
    regional_sales["revenue"]
    .idxmax()
)

best_channel = (
    channel_sales["revenue"]
    .idxmax()
)

best_customer_segment = (
    segment_sales["revenue"]
    .idxmax()
)

best_month = (
    monthly_sales.loc[
        monthly_sales["revenue"].idxmax(),
        "month"
    ]
)

print("\n==============================================")
print("        NOVAMART BUSINESS SUMMARY")
print("==============================================")

print(
    f"Highest Revenue Category : {best_category}"
)

print(
    f"Best Performing Region   : {best_region}"
)

print(
    f"Best Sales Channel       : {best_channel}"
)

print(
    f"Best Customer Segment    : {best_customer_segment}"
)

print(
    f"Highest Revenue Month    : {best_month}"
)

print(
    f"Overall Profit Margin    : {profit_margin:.2f}%"
)

print(
    f"Repeat Customer Rate     : {repeat_customer_rate:.2f}%"
)

print("==============================================")