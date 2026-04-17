"""
🔥 INTELLIGENT SYSTEM DEMONSTRATION
Complete showcase of all advanced features
"""

import pandas as pd
import io
import sys
sys.path.insert(0, "c:\\Users\\mohit kumar\\OneDrive\\Desktop\\optimization project")

from UserBehaviorApp.backend.ml_service_intelligent import run_intelligent_analysis

def demonstrate_intelligent_system():
    """Full system demonstration"""
    
    print("\n" + "="*100)
    print("🔥 INTELLIGENT ADAPTIVE CLUSTERING SYSTEM - FULL DEMONSTRATION")
    print("="*100)
    
    # Load the user behavior download file
    csv_path = "c:\\Users\\mohit kumar\\OneDrive\\Desktop\\optimization project\\UserBehaviorApp\\backend\\user_behavior_download.csv"
    
    print(f"\n📂 Loading data: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"✅ Data loaded: {len(df)} records, {len(df.columns)} columns")
    print(f"📊 Columns: {', '.join(df.columns.tolist())}")
    
    # Convert to BytesIO for analysis
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Run intelligent analysis
    print("\n" + "="*100)
    print("🧠 STARTING INTELLIGENT ANALYSIS...")
    print("="*100)
    
    results = run_intelligent_analysis(csv_buffer, has_labels=False)
    
    # Display results
    print("\n" + "="*100)
    print("📈 ANALYSIS RESULTS")
    print("="*100)
    
    # 1. Algorithm Selection
    print(f"\n🤖 AUTO-SELECTED ALGORITHM: {results['best_algorithm'].upper()}")
    print(f"   Algorithm Scores:")
    for algo, score in results['algorithm_scores'].items():
        print(f"     • {algo.capitalize()}: {score:.4f}")
    
    # 2. Clustering Quality
    print(f"\n📊 CLUSTERING QUALITY METRICS:")
    metrics = results['final_metrics']
    print(f"   • Silhouette Score: {metrics.get('silhouette', 0):.4f} {'⭐⭐ Excellent' if metrics.get('silhouette', 0) > 0.7 else '⭐ Good' if metrics.get('silhouette', 0) > 0.5 else '⚠️ Fair'}")
    print(f"   • Davies-Bouldin Index: {metrics.get('davies_bouldin', 0):.4f}")
    print(f"   • Calinski-Harabasz Index: {metrics.get('calinski_harabasz', 0):.2f}")
    print(f"   • 🔬 ICSO Score (Novel Metric): {metrics.get('icso_score', 0):.4f} ← Novel optimization metric!")
    
    # 3. Cluster Profiles
    print(f"\n👥 CLUSTER PROFILES (Business Intelligence):")
    profiles = results['cluster_profiles']
    for cluster_id, profile in profiles.items():
        print(f"\n   📍 Cluster {cluster_id}:")
        print(f"      Size: {profile['size']} users ({profile['percentage']:.1f}%)")
        print(f"      Label: {profile.get('business_label', 'N/A')}")
        
        if 'characteristics' in profile:
            chars = profile['characteristics']
            if 'total_spent' in chars:
                print(f"      Avg Spending: ${chars['total_spent']['mean']:.2f}")
            if 'purchase_count' in chars:
                print(f"      Avg Purchases: {chars['purchase_count']['mean']:.1f}")
            if 'session_time' in chars:
                print(f"      Avg Engagement: {chars['session_time']['mean']:.1f} min/session")
    
    # 4. Anomalies
    print(f"\n🔍 ANOMALY DETECTION (IsolationForest):")
    anomalies = results['anomalies']
    print(f"   Anomalies Found: {anomalies['n_anomalies']} users ({anomalies['percentage']:.1f}%)")
    print(f"   💡 Use for: Fraud detection, unusual behavior analysis")
    
    # 5. Smart Recommendations
    print(f"\n🎯 HYBRID RECOMMENDATIONS (Cluster + Association Rules):")
    recommendations = results['recommendations']
    for cluster_id, rec in recommendations.items():
        if isinstance(rec, dict):
            print(f"\n   📍 Cluster {cluster_id} ({rec['segment']} Segment):")
            for i, r in enumerate(rec['recommendations'][:3], 1):
                print(f"      {i}. {r}")
    
    # 6. Cross-Sell Opportunities
    print(f"\n🔄 CROSS-SELL OPPORTUNITIES (Association Rules):")
    opportunities = results['cross_sell_opportunities']
    if opportunities:
        for i, opp in enumerate(opportunities[:3], 1):
            print(f"   {i}. {opp['pattern']}")
            print(f"      Confidence: {opp['confidence']}")
    else:
        print("   ℹ️  No strong association rules found in this dataset")
    
    # 7. Key Insights
    print(f"\n💡 KEY INSIGHTS:")
    for i, insight in enumerate(results['insights'], 1):
        print(f"   {i}. {insight}")
    
    # 8. Summary
    print("\n" + "="*100)
    print("✨ SYSTEM CAPABILITIES DEMONSTRATED")
    print("="*100)
    print("""
    ✅ AutoML - Automatic algorithm selection (KMeans vs DBSCAN vs Hierarchical)
    ✅ Hybrid Scoring - Combined metrics for optimal clustering
    ✅ Novel ICSO Metric - Custom optimization score for cluster quality
    ✅ Cluster Profiling - Automatic business intelligence categorization
    ✅ Anomaly Detection - Identify unusual user behaviors
    ✅ Hybrid Recommendations - Combine clustering + association rules
    ✅ Cross-Sell Intelligence - Product affinity analysis
    ✅ Explainable Results - Understand why users cluster together
    """)
    
    print("\n" + "="*100)
    print("🏆 WHAT MAKES THIS SYSTEM UNIQUE")
    print("="*100)
    print("""
    1️⃣  AUTO-ALGORITHM SELECTION
        Unlike most projects that only use KMeans, this system tests and selects
        the best algorithm (KMeans, DBSCAN, or Hierarchical) based on your data.
        
    2️⃣  NOVEL ICSO METRIC
        A custom metric combining inter-cluster separation with intra-cluster variance.
        This is research-level innovation!
        
    3️⃣  HYBRID SCORING
        Combines Silhouette (0.5) + DBI (0.3) + CH (0.2) for comprehensive evaluation.
        Shows mathematical sophistication.
        
    4️⃣  PRODUCTION-READY
        Includes anomaly detection, recommendations, and business profiling.
        Ready for real-world deployment.
        
    5️⃣  EXPLAINABLE AI
        Every cluster gets a profile explaining characteristics and recommendations.
        Business stakeholders can understand the results.
    """)
    
    print("\n" + "="*100)
    print("🎤 VIVA TALKING POINTS")
    print("="*100)
    print("""
    Q: "What makes your clustering system different?"
    A: "Unlike traditional systems, our framework introduces adaptive algorithm selection,
        a novel ICSO metric for cluster quality assessment, and hybrid evaluation scoring
        that combines multiple metrics for comprehensive clustering validation."
    
    Q: "How do you ensure clustering quality?"
    A: "We employ a multi-metric approach combining Silhouette score, Davies-Bouldin index,
        and Calinski-Harabasz score with custom weights. Additionally, our ICSO metric
        specifically measures cluster separation optimality."
    
    Q: "What about real-world applications?"
    A: "The system includes anomaly detection for fraud/unusual behavior, hybrid recommendations
        combining cluster profiling with association rules, and business intelligence
        categorization. It's production-ready."
    """)
    
    return results

if __name__ == "__main__":
    results = demonstrate_intelligent_system()
    print("\n✅ Demonstration Complete!")
