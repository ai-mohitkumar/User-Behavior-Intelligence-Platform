"""
Validation and Testing Script for Advanced Dataset Integration
Tests the full pipeline with the labeled dataset
"""

import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, "c:\\Users\\mohit kumar\\OneDrive\\Desktop\\optimization project")

from UserBehaviorApp.backend.dataset_generator import generate_advanced_dataset
from UserBehaviorApp.backend.ml_service import run_analysis
import io

def test_advanced_pipeline():
    """Test full pipeline with labeled data"""
    print("🚀 Testing Advanced ML Pipeline with Supervised Validation\n")
    
    # Generate dataset
    print("📊 Generating advanced dataset (5000 users)...")
    df = generate_advanced_dataset(n_users=5000)
    
    print(f"✅ Dataset created: {len(df)} users")
    print(f"   Segments: {df['user_segment'].value_counts().to_dict()}\n")
    
    # Display sample
    print("📋 Sample data:")
    print(df.head())
    print()
    
    # Convert to file-like object for analysis
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Run analysis WITH labeled data
    print("🧠 Running clustering analysis with supervised validation...\n")
    results = run_analysis(csv_buffer, has_labels=True)
    
    # Display results
    print("=" * 60)
    print("📈 CLUSTERING RESULTS")
    print("=" * 60)
    print(f"Optimal Clusters (K): {results['best_k']}")
    print(f"Total Users Analyzed: {results['n_users']}\n")
    
    print("📊 Unsupervised Metrics (Clustering Quality):")
    for key, value in results['final_metrics'].items():
        if key != 'cluster_mapping':
            print(f"   {key}: {value:.4f}")
    
    if results['supervised_metrics']:
        print("\n🎯 Supervised Metrics (vs. Known Segments):")
        for key, value in results['supervised_metrics'].items():
            if key != 'cluster_mapping':
                print(f"   {key}: {value:.4f}")
        
        if 'cluster_mapping' in results['supervised_metrics']:
            print(f"\n   Cluster Mapping:")
            for cluster_id, segment in results['supervised_metrics']['cluster_mapping'].items():
                print(f"      Cluster {cluster_id} → {segment}")
    
    print("\n💡 Insights:")
    for insight in results['insights']:
        print(f"   {insight}")
    
    print("\n📌 Recommendations:")
    for rec in results['recommendations'][:3]:
        print(f"   {rec}")
    
    print("\n📊 Segment Distribution:")
    for segment, count in results['segment_distribution'].items():
        print(f"   {segment}: {count} users ({100*count/results['n_users']:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✅ Pipeline test completed successfully!")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    test_advanced_pipeline()
