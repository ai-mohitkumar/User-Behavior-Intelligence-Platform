"""
Comprehensive Dataset Comparison & Analysis
Compares real data (15 rows), synthetic data (5000), and expanded real patterns (5000)
"""

import pandas as pd
import io
import sys
import os
sys.path.insert(0, "c:\\Users\\mohit kumar\\OneDrive\\Desktop\\optimization project")

from UserBehaviorApp.backend.ml_service import run_analysis

def load_and_analyze_dataset(csv_path, dataset_name, has_labels=False):
    """Load dataset and run full analysis"""
    print(f"\n{'='*70}")
    print(f"📊 ANALYZING: {dataset_name}")
    print(f"{'='*70}")
    
    # Load dataset
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded: {len(df)} users")
    print(f"✅ Features: {len(df.columns)} columns")
    print(f"✅ Memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n")
    
    # Display summary stats
    print("📈 Dataset Summary:")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if 'user_id' in numeric_cols:
        numeric_cols.remove('user_id')
    
    summary = df[numeric_cols].describe().loc[['mean', 'min', 'max', 'std']].round(2)
    print(summary)
    
    # Check for labels
    has_labels_in_file = 'user_segment' in df.columns or 'segment' in df.columns
    print(f"\n🎯 Supervised Labels: {'✅ Yes' if has_labels_in_file else '❌ No'}")
    if has_labels_in_file:
        print(f"   Distribution: {dict(df['user_segment'].value_counts())}")
    
    # Prepare for analysis
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Run analysis
    print(f"\n🧠 Running clustering analysis...")
    results = run_analysis(csv_buffer, has_labels=has_labels_in_file)
    
    return results, df

def compare_datasets():
    """Run comprehensive comparison"""
    print("\n" + "="*70)
    print("🚀 COMPREHENSIVE DATASET COMPARISON & ANALYSIS")
    print("="*70)
    
    datasets = [
        ("real_user_data_15.csv", "Real Data (15 users - Original)", False),
        ("user_behavior_dataset_5000.csv", "Synthetic Data (5000 users - Behavioral)", False),
        ("user_behavior_real_patterns_5000.csv", "Real Patterns (5000 users - Expanded)", True),
    ]
    
    all_results = {}
    
    for csv_path, dataset_name, has_labels in datasets:
        full_path = f"c:\\Users\\mohit kumar\\OneDrive\\Desktop\\optimization project\\UserBehaviorApp\\backend\\{csv_path}"
        
        if not os.path.exists(full_path):
            print(f"⚠️  Skipping {dataset_name} - file not found")
            continue
        
        try:
            results, df = load_and_analyze_dataset(full_path, dataset_name, has_labels)
            all_results[dataset_name] = {
                'results': results,
                'df': df,
                'n_users': len(df)
            }
            
            # Display key metrics
            print("\n📊 CLUSTERING RESULTS:")
            print(f"   Optimal K: {results['best_k']}")
            print(f"   Silhouette Score: {results['final_metrics'].get('silhouette', 'N/A'):.4f}")
            print(f"   Davies-Bouldin: {results['final_metrics'].get('davies_bouldin', 'N/A'):.4f}")
            print(f"   Calinski-Harabasz: {results['final_metrics'].get('calinski_harabasz', 'N/A'):.2f}")
            
            if results['supervised_metrics']:
                print(f"\n🎯 SUPERVISED METRICS:")
                print(f"   Accuracy: {results['supervised_metrics'].get('accuracy', 'N/A'):.4f}")
                print(f"   F1-Score: {results['supervised_metrics'].get('f1_weighted', 'N/A'):.4f}")
                print(f"   Precision: {results['supervised_metrics'].get('precision_weighted', 'N/A'):.4f}")
            
            print(f"\n💡 INSIGHTS:")
            for insight in results['insights'][:3]:
                print(f"   {insight}")
                
        except Exception as e:
            print(f"❌ Error analyzing {dataset_name}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Comparison Summary
    print("\n" + "="*70)
    print("📊 COMPARISON SUMMARY")
    print("="*70)
    
    comparison_data = []
    for dataset_name, data in all_results.items():
        comparison_data.append({
            'Dataset': dataset_name,
            'Users': data['n_users'],
            'K': data['results']['best_k'],
            'Silhouette': f"{data['results']['final_metrics'].get('silhouette', 0):.4f}",
            'Accuracy': f"{data['results']['supervised_metrics'].get('accuracy', 0):.4f}" if data['results']['supervised_metrics'] else "N/A"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    print("\n" + comparison_df.to_string(index=False))
    
    # Recommendations
    print("\n" + "="*70)
    print("🎯 RECOMMENDATIONS")
    print("="*70)
    print("""
✅ Dataset Selection:
   • Use Real Patterns (5000) for most accurate ML modeling
   • Use Synthetic (5000) for algorithm testing & benchmarking
   • Use Real Data (15) for dashboard demo/validation

🔥 Business Value:
   ✓ High Value Segment: Target with premium offerings
   ✓ Medium Value Segment: Focus on retention marketing  
   ✓ Low Value Segment: Engagement campaigns & re-activation

📈 Next Steps:
   1. Upload any dataset to web app for interactive visualization
   2. Compare clustering results across different algorithms
   3. Build predictive model for segment classification
   4. Monitor accuracy metrics over time
    """)

if __name__ == "__main__":
    compare_datasets()
