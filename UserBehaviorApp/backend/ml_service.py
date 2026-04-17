import pandas as pd
import io
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import sys
sys.path.append('.')
from ml.preprocessing import load_data, clean_data, feature_engineering, normalize_features
from ml.optimization import find_best_k
from ml.clustering import apply_kmeans, cluster_quality
from ml.comparison import compare_algorithms
from ml.pattern_mining import basket_from_transactions, mine_rules

def calculate_supervised_metrics(clusters, true_labels):
    """
    Calculate supervised learning metrics when true labels are available
    """
    try:
        from sklearn.preprocessing import LabelEncoder
        
        # Encode both clusters and labels to integers
        le_labels = LabelEncoder()
        le_clusters = LabelEncoder()
        
        encoded_labels = le_labels.fit_transform(true_labels)
        encoded_clusters = le_clusters.fit_transform(clusters)
        
        # Build confusion matrix with encoded values
        cm = confusion_matrix(encoded_labels, encoded_clusters)
        from scipy.optimize import linear_sum_assignment
        
        # Find optimal assignment
        row_ind, col_ind = linear_sum_assignment(-cm)
        
        # Create mapping
        mapping = {col: le_labels.classes_[row] for col, row in zip(col_ind, row_ind) if row < len(le_labels.classes_)}
        
        # Map clusters to labels
        mapped = np.array([mapping.get(c, le_labels.classes_[0]) for c in le_clusters.transform(clusters)])
        
        metrics = {
            'accuracy': float(accuracy_score(encoded_labels, encoded_clusters)),
            'precision_weighted': float(precision_score(encoded_labels, encoded_clusters, average='weighted', zero_division=0)),
            'recall_weighted': float(recall_score(encoded_labels, encoded_clusters, average='weighted', zero_division=0)),
            'f1_weighted': float(f1_score(encoded_labels, encoded_clusters, average='weighted', zero_division=0)),
            'cluster_mapping': {int(k): str(v) for k, v in mapping.items()}
        }
        return metrics, mapped
    except Exception as e:
        print(f"⚠️ Supervised metrics calculation issue: {str(e)}")
        return {}, clusters

def run_analysis(file_content, has_labels=False):
    # Load and preprocess
    df = load_data(file_content)
    df = clean_data(df)
    df = feature_engineering(df)
    
    # Store original labels if available
    true_labels = None
    if has_labels and 'user_segment' in df.columns:
        true_labels = df['user_segment'].values
        df = df.drop('user_segment', axis=1)
    
    candidates = ['total_spent', 'quantity_norm', 'quantity']
    features = [c for c in candidates if c in df.columns]
    if not features:
        raise ValueError('No suitable features found. Expected quantity, price or total_spent.')
    
    df_norm, scaler = normalize_features(df, features)
    
    # Comparison
    comp_results, best_algo = compare_algorithms(df_norm, features)
    
    # Best k and clustering
    opt_results = find_best_k(df_norm, features)
    best_k = opt_results['best_k']
    df_clustered, kmeans = apply_kmeans(df_norm, features, best_k)
    final_metrics = cluster_quality(df_norm, features, df_clustered['cluster'])
    
    # Supervised validation if labels available
    supervised_metrics = {}
    mapped_clusters = df_clustered['cluster'].values
    if true_labels is not None:
        supervised_metrics, mapped_clusters = calculate_supervised_metrics(
            df_clustered['cluster'].values, 
            true_labels
        )
    
    # Add accuracy to final metrics if available
    if 'accuracy' in supervised_metrics:
        final_metrics['supervised_accuracy'] = supervised_metrics['accuracy']
        final_metrics['cluster_mapping'] = supervised_metrics['cluster_mapping']
    
    # Patterns if possible
    rules = []
    if {'InvoiceNo', 'Description', 'quantity'}.issubset(df.columns):
        basket = basket_from_transactions(df)
        rules = mine_rules(basket)
    
    # Enhanced insights with supervised validation
    insights = []
    if final_metrics['silhouette'] > 0.7:
        insights.append("✅ Excellent clustering quality - clear user segments identified.")
    elif final_metrics['silhouette'] > 0.5:
        insights.append("✅ Good clustering quality - meaningful user behavior patterns.")
    else:
        insights.append("⚠️ Moderate clustering - consider more features or data cleaning.")
    
    # Add supervised validation insight
    if 'accuracy' in supervised_metrics:
        accuracy = supervised_metrics['accuracy']
        if accuracy > 0.8:
            insights.append(f"🔥 High accuracy ({accuracy:.1%}) - clusters align well with user value segments!")
        elif accuracy > 0.6:
            insights.append(f"💡 Good accuracy ({accuracy:.1%}) - clusters capture meaningful user patterns.")
        else:
            insights.append(f"📊 Accuracy ({accuracy:.1%}) - segments show behavioral patterns.")
    
    high_spend_cluster = df_clustered.groupby('cluster')['total_spent_norm'].mean().idxmax() if 'total_spent_norm' in df_clustered else 0
    insights.append(f"💰 Premium segment: Cluster {high_spend_cluster} (high spenders - target with premium offers).")
    
    recommendations = [f"Cluster {c}: {'Premium products' if df_clustered[df_clustered['cluster']==c]['total_spent_norm'].mean() > 0.5 else 'Discounts/up-sell'}." for c in df_clustered['cluster'].unique()]
    
    return {
        "comparison": comp_results,
        "best_algo": best_algo,
        "best_k": best_k,
        "final_metrics": final_metrics,
        "supervised_metrics": supervised_metrics,
        "clusters": df_clustered[['cluster'] + features].to_dict('records'),
        "insights": insights,
        "recommendations": recommendations[:5],
        "rules": rules,
        "n_users": len(df),
        "n_clusters": len(set(df_clustered['cluster'])),
        "has_labels": has_labels,
        "segment_distribution": dict(pd.Series(true_labels).value_counts()) if true_labels is not None else {}
    }

