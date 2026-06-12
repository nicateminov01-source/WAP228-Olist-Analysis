import os
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DB_NAME = "olist_ecommerce.db"
OUTPUT_DIR = "outputs"

# Visualization style settings
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 11

def get_connection():
    return sqlite3.connect(DB_NAME)

def analyze_monthly_trends():
    """1. Monthly Order Count and Total Revenue Trend (JOIN & GROUP BY)"""
    print("[+] 1. Analyzing monthly trends...")
    query = """
        SELECT 
            strftime('%Y-%m', o.order_purchase_timestamp) as month,
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(p.payment_value) as total_revenue
        FROM orders o
        JOIN order_payments p ON o.order_id = p.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY month
        ORDER BY month;
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)
    
    # Filter for the core active period (2017-01 to 2018-08)
    df = df[(df['month'] >= '2017-01') & (df['month'] <= '2018-08')]

    # Dual-axis chart for Orders vs Revenue
    fig, ax1 = plt.subplots()

    color = '#1f77b4'
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Total Orders', color=color)
    sns.barplot(data=df, x='month', y='total_orders', ax=ax1, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    ax2 = ax1.twinx()
    color = '#d62728'
    ax2.set_ylabel('Total Revenue (R$)', color=color)
    sns.lineplot(data=df, x='month', y='total_revenue', ax=ax2, color=color, marker='o', sort=False, linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Monthly Order Count and Total Revenue Trends (2017 - 2018)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '1_monthly_trends.png'))
    plt.close()

def analyze_top_categories():
    """2. Top Selling Product Categories (Multi-JOIN & GROUP BY)"""
    print("[+] 2. Analyzing top-selling categories...")
    query = """
        SELECT 
            t.product_category_name_english as category,
            COUNT(i.order_id) as items_sold,
            SUM(i.price) as total_sales
        FROM order_items i
        JOIN products p ON i.product_id = p.product_id
        JOIN category_translation t ON p.product_category_name = t.product_category_name
        GROUP BY category
        ORDER BY items_sold DESC
        LIMIT 10;
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)
        
    sns.barplot(data=df, x='items_sold', y='category', palette='viridis')
    plt.title('Top 10 Selling Product Categories (by Volume)')
    plt.xlabel('Number of Items Sold')
    plt.ylabel('Category (English)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '2_top_categories.png'))
    plt.close()

def analyze_payment_methods():
    """3. Payment Methods Distribution"""
    print("[+] 3. Calculating payment methods distribution...")
    query = """
        SELECT 
            payment_type,
            COUNT(order_id) as usage_count,
            SUM(payment_value) as total_amount
        FROM order_payments
        GROUP BY payment_type
        ORDER BY usage_count DESC;
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    plt.figure(figsize=(8, 8))
    plt.pie(df['total_amount'], labels=df['payment_type'], autopct='%1.1f%%', 
            startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Total Transaction Volume Distribution by Payment Method')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '3_payment_methods.png'))
    plt.close()

def analyze_delivery_performance():
    """4. Delivery Performance Analysis (Actual Delivery Time)"""
    print("[+] 4. Extracting delivery performance analysis...")
    query = """
        SELECT 
            order_id,
            customer_state,
            (julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)) as actual_delivery_days,
            (julianday(order_estimated_delivery_date) - julianday(order_delivered_customer_date)) as delta_estimated_days
        FROM orders
        WHERE order_status = 'delivered' 
          AND order_delivered_customer_date IS NOT NULL;
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    # Filter outliers and focus on a realistic delivery window (1-30 days)
    filtered_df = df[(df['actual_delivery_days'] > 0) & (df['actual_delivery_days'] <= 30)]

    plt.figure(figsize=(10, 6))
    sns.histplot(data=filtered_df, x='actual_delivery_days', kde=True, color='purple', bins=30)
    plt.axvline(filtered_df['actual_delivery_days'].median(), color='red', linestyle='--', 
                label=f"Median Time: {filtered_df['actual_delivery_days'].median():.1f} Days")
    plt.title('Actual Delivery Time Distribution for Delivered Orders')
    plt.xlabel('Delivery Time (Days)')
    plt.ylabel('Number of Orders')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '4_delivery_performance.png'))
    plt.close()

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    if not os.path.exists(DB_NAME):
        print(f"[!] {DB_NAME} not found! Please run db_loader.py first.")
    else:
        analyze_monthly_trends()
        analyze_top_categories()
        analyze_payment_methods()
        analyze_delivery_performance()
        print(f"[+] All analytical charts have been successfully saved to the '{OUTPUT_DIR}/' folder!")
