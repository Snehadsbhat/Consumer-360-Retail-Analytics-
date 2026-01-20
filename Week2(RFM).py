
# ===============================
# 1. IMPORTS
# ===============================
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from mlxtend.frequent_patterns import apriori, association_rules
import warnings

warnings.filterwarnings("ignore")


# ===============================
# 2. DATABASE CONNECTION
# ===============================
DB_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": 3306,
    "database": "retail_analytics"
}

engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

print("✅ Database connection established")


# ===============================
# 3. LOAD SINGLE CUSTOMER VIEW
# ===============================
query_customer = """
SELECT 
    CustomerID,
    first_purchase_date,
    total_orders,
    total_revenue
FROM single_customer_view
"""

df = pd.read_sql(query_customer, engine)
df['first_purchase_date'] = pd.to_datetime(df['first_purchase_date'])

print(f"✅ Customer records loaded: {df.shape[0]}")


# ===============================
# 4. RFM CALCULATION
# ===============================
reference_date = df['first_purchase_date'].max() + pd.Timedelta(days=1)

df['Recency'] = (reference_date - df['first_purchase_date']).dt.days
df['Frequency'] = df['total_orders']
df['Monetary'] = df['total_revenue']


# ===============================
# 5. RFM SCORING (QUANTILE-BASED)
# ===============================
df['R_score'] = pd.qcut(df['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
df['F_score'] = pd.qcut(
    df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]
).astype(int)
df['M_score'] = pd.qcut(df['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

df['RFM_score'] = (
    df['R_score'].astype(str) +
    df['F_score'].astype(str) +
    df['M_score'].astype(str)
)

print("✅ RFM scoring completed")


# ===============================
# 6. CUSTOMER SEGMENTATION
# ===============================
def assign_segment(row):
    if row['R_score'] >= 4 and row['F_score'] >= 4 and row['M_score'] >= 4:
        return "Champions"
    elif row['R_score'] >= 3 and row['F_score'] >= 3:
        return "Loyalists"
    elif row['R_score'] <= 2 and row['F_score'] <= 2:
        return "Hibernating"
    elif row['R_score'] >= 4:
        return "Potential Loyalist"
    else:
        return "Others"


df['Segment'] = df.apply(assign_segment, axis=1)

print("✅ Customer segmentation completed")


# ===============================
# 7. SEGMENT VALIDATION (STATISTICAL AUDIT)
# ===============================
segment_validation = (
    df.groupby('Segment')['Monetary']
    .mean()
    .sort_values(ascending=False)
)

print("\n📊 Average Revenue by Segment:")
print(segment_validation)

print("\n📊 Segment Distribution:")
print(df['Segment'].value_counts())


# ===============================
# 8. MARKET BASKET ANALYSIS
# ===============================
query_transactions = """
SELECT InvoiceNo, StockCode
FROM fact_sales
"""

basket_df = pd.read_sql(query_transactions, engine)
print(f"\n✅ Transaction records loaded: {basket_df.shape[0]}")


# Create basket matrix
basket = (
    basket_df
    .groupby(['InvoiceNo', 'StockCode'])['StockCode']
    .count()
    .unstack()
    .fillna(0)
)

basket = basket.applymap(lambda x: 1 if x > 0 else 0)


# ===============================
# 9. APRIORI & ASSOCIATION RULES
# ===============================
frequent_itemsets = apriori(
    basket,
    min_support=0.02,
    use_colnames=True
)

rules = association_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=1
)

rules = rules.sort_values(by="lift", ascending=False)

print("\n🧺 Top Association Rules:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())


# ===============================
# 10. EXPORT RESULTS (OPTIONAL)
# ===============================
df.to_csv("rfm_customer_segments.csv", index=False)
rules.to_csv("association_rules.csv", index=False)

print("\n✅ Outputs saved:")
print("- rfm_customer_segments.csv")
print("- association_rules.csv")

