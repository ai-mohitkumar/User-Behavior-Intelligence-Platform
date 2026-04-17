"""
Real Data Transformer
Converts real user data to the format expected by the ML pipeline
Generates InvoiceNo, quantity, price, and Description columns
"""

import pandas as pd
import numpy as np

def transform_real_data_for_analysis(input_csv="real_user_data_15.csv", output_csv="user_behavior_download.csv"):
    """
    Transform real user data to include required columns for pattern mining
    """
    # Load real data
    df = pd.read_csv(input_csv)
    
    print(f"📋 Loading original data: {len(df)} users")
    
    # Create expanded transaction format
    # Each user can have multiple transactions
    transactions = []
    
    categories_by_type = {
        'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Camera'],
        'Fashion': ['Shirt', 'Jeans', 'Jacket', 'Shoes', 'Dress'],
        'Groceries': ['Milk', 'Bread', 'Vegetables', 'Fruits', 'Meat'],
        'Home': ['Chair', 'Table', 'Lamp', 'Rug', 'Pillow'],
        'Beauty': ['Shampoo', 'Cream', 'Lipstick', 'Foundation', 'Lotion'],
        'Sports': ['Shoes', 'Ball', 'Mat', 'Weights', 'Racket']
    }
    
    invoice_counter = 1
    
    for idx, row in df.iterrows():
        # Create multiple invoices per user based on purchase count
        user_purchase_count = int(row['purchase_count'])
        
        for _ in range(min(user_purchase_count, 10)):  # Cap at 10 invoices per user
            # Random quantity (1-5 items per transaction)
            quantity = np.random.randint(1, 6)
            
            # Price derived from avg_order_value
            avg_price = row['avg_order_value'] / quantity
            price = np.random.normal(avg_price, avg_price * 0.2)  # Add variance
            price = max(10, price)  # Minimum $10
            
            # Get product from category
            category = row['category']
            products = categories_by_type.get(category, ['Product'])
            description = np.random.choice(products)
            
            # Create invoice
            invoice_no = f"INV{invoice_counter:06d}"
            invoice_counter += 1
            
            transaction = {
                'InvoiceNo': invoice_no,
                'user_id': row['user_id'],
                'age': row['age'],
                'gender': row['gender'],
                'total_spent': row['total_spent'],
                'purchase_count': row['purchase_count'],
                'avg_order_value': row['avg_order_value'],
                'session_time': row['session_time'],
                'pages_visited': row['pages_visited'],
                'last_login_days': row['last_login_days'],
                'category': row['category'],
                'quantity': quantity,
                'price': round(price, 2),
                'Description': description
            }
            
            transactions.append(transaction)
    
    # Create DataFrame
    df_transactions = pd.DataFrame(transactions)
    
    # Save
    df_transactions.to_csv(output_csv, index=False)
    
    print(f"✅ Transformed data saved: {output_csv}")
    print(f"   📊 Total transactions: {len(df_transactions)}")
    print(f"   📊 Columns: {', '.join(df_transactions.columns.tolist())}")
    print(f"\n📈 Data Summary:")
    print(f"   Invoices: {df_transactions['InvoiceNo'].nunique()}")
    print(f"   Users: {df_transactions['user_id'].nunique()}")
    print(f"   Products: {df_transactions['Description'].nunique()}")
    print(f"   Categories: {', '.join(df_transactions['category'].unique())}")
    print(f"\n💰 Transaction Stats:")
    print(f"   Avg Quantity: {df_transactions['quantity'].mean():.2f}")
    print(f"   Avg Price: ${df_transactions['price'].mean():.2f}")
    print(f"   Total Value: ${df_transactions['quantity'].sum() * df_transactions['price'].mean():.2f}")
    
    return df_transactions

if __name__ == "__main__":
    df = transform_real_data_for_analysis()
    print("\n✅ Data ready for upload to web app!")
    print(f"File: user_behavior_download.csv")
