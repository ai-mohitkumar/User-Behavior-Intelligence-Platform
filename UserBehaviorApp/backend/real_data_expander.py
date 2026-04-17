"""
Advanced Real Data Expansion & Segmentation
Expands the 15-row real dataset to 5000 rows using statistical patterns
Adds supervised segments based on behavioral analysis
"""

import pandas as pd
import numpy as np
from scipy import stats

def analyze_real_data_patterns(csv_path="real_user_data_15.csv"):
    """Extract statistical patterns from real data"""
    df = pd.read_csv(csv_path)
    
    patterns = {
        'age': {'mean': df['age'].mean(), 'std': df['age'].std()},
        'total_spent': {'mean': df['total_spent'].mean(), 'std': df['total_spent'].std()},
        'purchase_count': {'mean': df['purchase_count'].mean(), 'std': df['purchase_count'].std()},
        'avg_order_value': {'mean': df['avg_order_value'].mean(), 'std': df['avg_order_value'].std()},
        'session_time': {'mean': df['session_time'].mean(), 'std': df['session_time'].std()},
        'pages_visited': {'mean': df['pages_visited'].mean(), 'std': df['pages_visited'].std()},
        'last_login_days': {'mean': df['last_login_days'].mean(), 'std': df['last_login_days'].std()},
        'categories': df['category'].unique().tolist(),
        'gender_dist': df['gender'].value_counts(normalize=True).to_dict(),
    }
    
    return patterns

def segment_users(total_spent, purchase_count, session_time):
    """
    Create user segments based on behavioral patterns
    High Value: High spending + frequency + engagement
    Medium Value: Moderate metrics
    Low Value: Low metrics
    """
    # Normalize scores
    spend_score = total_spent / 10000  # 0-1 scale
    freq_score = purchase_count / 50   # 0-1 scale
    engagement_score = session_time / 70  # 0-1 scale
    
    # Composite score
    composite = (spend_score * 0.5 + freq_score * 0.3 + engagement_score * 0.2)
    
    if composite >= 0.65:
        return "High Value"
    elif composite >= 0.35:
        return "Medium Value"
    else:
        return "Low Value"

def generate_extended_dataset(n_users=5000, random_state=42):
    """Generate 5000+ users using real data patterns"""
    np.random.seed(random_state)
    
    # Extract patterns from real data
    patterns = analyze_real_data_patterns()
    
    users = []
    
    for i in range(n_users):
        # Generate from observed distributions
        age = int(np.max([18, np.random.normal(patterns['age']['mean'], patterns['age']['std'])]))
        age = np.min([80, age])  # Cap at 80
        
        gender = np.random.choice(['M', 'F'], p=[0.5, 0.5])
        
        category = np.random.choice(patterns['categories'])
        
        # Correlated metrics
        total_spent = np.max([100, np.random.normal(patterns['total_spent']['mean'], patterns['total_spent']['std'])])
        purchase_count = int(np.max([1, np.random.normal(patterns['purchase_count']['mean'], patterns['purchase_count']['std'])]))
        avg_order_value = total_spent / purchase_count
        
        session_time = int(np.max([5, np.random.normal(patterns['session_time']['mean'], patterns['session_time']['std'])]))
        pages_visited = int(np.max([3, np.random.normal(patterns['pages_visited']['mean'], patterns['pages_visited']['std'])]))
        last_login_days = int(np.max([0, np.random.normal(patterns['last_login_days']['mean'], patterns['last_login_days']['std'])]))
        last_login_days = np.min([30, last_login_days])  # Cap at 30 days
        
        # Generate segment
        segment = segment_users(total_spent, purchase_count, session_time)
        
        user = {
            'user_id': i + 1,
            'age': age,
            'gender': gender,
            'total_spent': round(total_spent, 2),
            'purchase_count': purchase_count,
            'avg_order_value': round(avg_order_value, 2),
            'session_time': session_time,
            'pages_visited': pages_visited,
            'last_login_days': last_login_days,
            'category': category,
            'user_segment': segment
        }
        users.append(user)
    
    return pd.DataFrame(users)

def save_extended_dataset(filepath, n_users=5000):
    """Generate and save the extended dataset"""
    df = generate_extended_dataset(n_users)
    df.to_csv(filepath, index=False)
    
    print(f"✅ Extended dataset generated: {filepath}")
    print(f"   📊 Total users: {len(df)}")
    print(f"   📊 Features: {', '.join(df.columns[:-1])}")
    print(f"\n📈 Segment Distribution:")
    for segment, count in df['user_segment'].value_counts().items():
        print(f"   {segment}: {count} users ({100*count/len(df):.1f}%)")
    print(f"\n💰 Spending Analysis by Segment:")
    print(df.groupby('user_segment')[['total_spent', 'purchase_count', 'session_time']].mean().round(2))
    print(f"\n👥 Demographics:")
    print(f"   Age range: {df['age'].min()}-{df['age'].max()} (avg: {df['age'].mean():.1f})")
    print(f"   Gender: {dict(df['gender'].value_counts())}")
    print(f"   Top categories: {', '.join(df['category'].value_counts().head(3).index.tolist())}")
    
    return df

if __name__ == "__main__":
    df = save_extended_dataset("user_behavior_real_patterns_5000.csv", n_users=5000)
