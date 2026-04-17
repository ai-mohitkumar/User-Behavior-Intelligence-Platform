"""
Advanced User Behavior Dataset Generator
Generates realistic synthetic user behavior with pre-defined segments
Creates a hybrid dataset: unsupervised (features) + supervised (labels)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_advanced_dataset(n_users=5000, random_state=42):
    """
    Generate advanced user behavior dataset with realistic segmentation
    
    Segments:
    - High Value: Heavy spenders, frequent purchases, high engagement
    - Medium Value: Moderate spending, regular purchases
    - Low Value: Light spenders, infrequent purchases
    
    Features:
    - purchase_count: Number of purchases made
    - total_spent: Historical spending amount
    - avg_order_value: Average spending per transaction
    - days_active: Days since first purchase
    - last_purchase_days: Days since last purchase
    - category_diversity: Number of different categories purchased
    - return_rate: Percentage of returned items
    - discount_usage: Percentage of purchases with discounts
    """
    np.random.seed(random_state)
    
    # Define segment distributions
    n_high = int(n_users * 0.20)      # 20% High Value
    n_medium = int(n_users * 0.50)    # 50% Medium Value
    n_low = int(n_users * 0.30)       # 30% Low Value
    
    users = []
    
    # === HIGH VALUE SEGMENT ===
    for i in range(n_high):
        user = {
            'user_id': f'USR_{i:05d}',
            'purchase_count': np.random.randint(50, 150),
            'total_spent': np.random.normal(8000, 2000),
            'avg_order_value': np.random.normal(250, 60),
            'days_active': np.random.randint(500, 1500),
            'last_purchase_days': np.random.randint(0, 30),
            'category_diversity': np.random.randint(15, 25),
            'return_rate': np.random.normal(0.05, 0.03),
            'discount_usage': np.random.normal(0.20, 0.10),
            'user_segment': 'High Value'
        }
        users.append(user)
    
    # === MEDIUM VALUE SEGMENT ===
    for i in range(n_medium):
        user = {
            'user_id': f'USR_{n_high + i:05d}',
            'purchase_count': np.random.randint(15, 50),
            'total_spent': np.random.normal(2500, 800),
            'avg_order_value': np.random.normal(100, 30),
            'days_active': np.random.randint(200, 800),
            'last_purchase_days': np.random.randint(0, 90),
            'category_diversity': np.random.randint(8, 15),
            'return_rate': np.random.normal(0.08, 0.04),
            'discount_usage': np.random.normal(0.35, 0.15),
            'user_segment': 'Medium Value'
        }
        users.append(user)
    
    # === LOW VALUE SEGMENT ===
    for i in range(n_low):
        user = {
            'user_id': f'USR_{n_high + n_medium + i:05d}',
            'purchase_count': np.random.randint(1, 15),
            'total_spent': np.random.normal(500, 200),
            'avg_order_value': np.random.normal(50, 20),
            'days_active': np.random.randint(30, 300),
            'last_purchase_days': np.random.randint(0, 180),
            'category_diversity': np.random.randint(1, 8),
            'return_rate': np.random.normal(0.12, 0.06),
            'discount_usage': np.random.normal(0.50, 0.20),
            'user_segment': 'Low Value'
        }
        users.append(user)
    
    # Create DataFrame
    df = pd.DataFrame(users)
    
    # Ensure positive values
    df['total_spent'] = df['total_spent'].abs()
    df['avg_order_value'] = df['avg_order_value'].abs()
    df['return_rate'] = df['return_rate'].clip(0, 1)
    df['discount_usage'] = df['discount_usage'].clip(0, 1)
    df['purchase_count'] = df['purchase_count'].astype(int)
    df['days_active'] = df['days_active'].astype(int)
    df['last_purchase_days'] = df['last_purchase_days'].astype(int)
    df['category_diversity'] = df['category_diversity'].astype(int)
    
    # Shuffle
    df = df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    
    return df

def save_dataset(filepath, n_users=5000):
    """Generate and save the advanced dataset"""
    df = generate_advanced_dataset(n_users)
    df.to_csv(filepath, index=False)
    print(f"✅ Dataset generated: {filepath}")
    print(f"   📊 Total users: {len(df)}")
    print(f"   📊 Features: {', '.join(df.columns[1:-1])}")
    print(f"   📊 Segments: {df['user_segment'].value_counts().to_dict()}")
    return df

if __name__ == "__main__":
    df = save_dataset("user_behavior_dataset_5000.csv", n_users=5000)
    print("\n📈 Dataset Summary:")
    print(df.groupby('user_segment')[['total_spent', 'purchase_count', 'avg_order_value']].mean())
