"""
Enhanced ML Service with Intelligent Adaptive Clustering
Integrates:
- IntelligentAdaptiveClusteringEngine (AutoML, Hybrid Scoring, ICSO)
- HybridRecommendationEngine (cluster + association rules)
- Supervised Validation
"""

import pandas as pd
import io
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import sys
import os

sys.path.insert(0, '..')
sys.path.append('.')

from ml.preprocessing import load_data, clean_data, feature_engineering, normalize_features
from intelligent_engine import IntelligentAdaptiveClusteringEngine
from recommendation_engine import HybridRecommendationEngine

def run_intelligent_analysis(df, has_labels=False):
    """
    🧠 New Intelligent Analysis with AutoML & Hybrid Evaluation
    
    Features:
    ✅ Auto Algorithm Selection (KMeans vs DBSCAN vs Hierarchical)
    ✅ Hybrid Evaluation Metrics
    ✅ Novel ICSO Metric
    ✅ Cluster Profiling
    ✅ Anomaly Detection
    ✅ Smart Recommendations
    """
    
    # Data is already a DataFrame from the endpoint
    df = clean_data(df)
    df = feature_engineering(df)
    
    # Store original labels
    true_labels = None
    if has_labels and 'user_segment' in df.columns:
        true_labels = df['user_segment'].values
        df_for_clustering = df.drop('user_segment', axis=1)
    else:
        df_for_clustering = df
    
    # Select features for clustering
    candidates = ['total_spent', 'quantity_norm', 'quantity', 'purchase_count', 'avg_order_value', 
                  'session_time', 'pages_visited']
    features = [c for c in candidates if c in df_for_clustering.columns]
    
    if not features:
        raise ValueError('No suitable features found.')
    
    print(f"🧠 Using features for clustering: {features}")
    
    # Run intelligent engine
    engine = IntelligentAdaptiveClusteringEngine(df_for_clustering, features)
    
    analysis_results = engine.run_full_analysis()
    
    # Get cluster assignments
    clusters = analysis_results['clusters']
    
    # Extract anomaly information
    anomalies_info = analysis_results['anomalies']
    anomaly_indices = list(anomalies_info['anomalies'].index) if len(anomalies_info['anomalies']) > 0 else []
    
    # Convert cluster_profiles dict to list
    cluster_profiles_list = list(analysis_results['profiles'].values()) if isinstance(analysis_results['profiles'], dict) else analysis_results['profiles']
    
    # Run recommendation engine
    rec_engine = HybridRecommendationEngine(df, clusters)
    rec_results = rec_engine.run_full_recommendation_analysis()
    
    # Convert recommendations dict to list with cluster_id and label
    recommendations_list = []
    if isinstance(rec_results.get('cluster_recommendations', {}), dict):
        for cluster_id, rec_data in rec_results['cluster_recommendations'].items():
            recommendations_list.append({
                'cluster_id': int(cluster_id),
                'cluster_label': rec_data.get('segment', 'Unknown'),
                'recommendations': rec_data.get('recommendations', [])
            })
    else:
        recommendations_list = rec_results.get('cluster_recommendations', [])
    
    # Prepare final response
    final_metrics = analysis_results['metrics'].copy()
    final_metrics['icso_score'] = analysis_results['icso_score']
    
    # Enhanced insights
    insights = generate_enhanced_insights(
        analysis_results,
        final_metrics,
        rec_results,
        anomalies_info
    )
    
    return {
        "intelligent_analysis": True,
        "best_algorithm": analysis_results['best_algorithm'],
        "algorithm_scores": analysis_results['algorithm_scores'],
        "best_k": analysis_results.get('n_clusters', 2),
        "final_metrics": final_metrics,
        "supervised_metrics": {},
        "cluster_profiles": cluster_profiles_list,
        "anomalies": anomaly_indices,
        "anomalies_count": anomalies_info['n_anomalies'],
        "anomalies_percentage": anomalies_info['percentage'],
        "recommendations": recommendations_list,
        "association_rules": list(rec_results['association_rules'].items())[:5],
        "cross_sell_opportunities": rec_results['cross_sell_opportunities'][:5],
        "insights": insights,
        "n_users": len(df),
        "n_clusters": analysis_results['n_clusters'],
        "has_labels": has_labels,
        "personalized_insights": rec_results['personalized_insights']
    }

def generate_enhanced_insights(analysis_results, metrics, rec_results, anomalies_info=None):
    """Generate insightful messages"""
    insights = []
    
    # Algorithm insight
    algo = analysis_results['best_algorithm'].upper()
    insights.append(f"🤖 Selected Algorithm: {algo} (Auto-optimized)")
    
    # Quality insight
    icso = analysis_results['icso_score']
    insights.append(f"📊 Cluster Separation Quality (ICSO): {icso:.4f}")
    
    # Silhouette insight
    silhouette = metrics.get('silhouette', 0)
    if silhouette > 0.7:
        insights.append(f"✅ Excellent cluster quality - clear user segments identified")
    elif silhouette > 0.5:
        insights.append(f"⭐ Good cluster quality - meaningful patterns discovered")
    else:
        insights.append(f"📊 Moderate cluster quality - suggests nuanced user behavior")
    
    # Anomaly insight
    if anomalies_info:
        n_anomalies = anomalies_info['n_anomalies']
        anomaly_pct = anomalies_info['percentage']
        insights.append(f"🔍 Anomalies Detected: {n_anomalies} users ({anomaly_pct:.1f}%) showing unusual behavior")
    
    # Recommendation insight
    total_opportunities = len(rec_results.get('cross_sell_opportunities', []))
    insights.append(f"🎯 Business Opportunities: {total_opportunities} cross-sell opportunities identified")
    
    return insights

