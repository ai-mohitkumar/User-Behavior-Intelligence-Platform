"""
🎯 Hybrid Recommendation Engine
Combines cluster-based + association rule-based recommendations
"""

import pandas as pd
import numpy as np
from itertools import combinations

class HybridRecommendationEngine:
    """
    Smart recommendations using:
    1. Cluster profiling
    2. Association rules (Apriori-based)
    3. Behavioral patterns
    """
    
    def __init__(self, data, cluster_assignments):
        self.data = data
        self.clusters = cluster_assignments
        self.add_cluster_labels(data)
        
    def add_cluster_labels(self, data):
        """Add cluster information to data"""
        data['cluster'] = self.clusters
    
    def mine_association_rules(self, min_support=0.1):
        """
        Mine product association rules
        Format: {product1, product2} -> high confidence they're bought together
        """
        try:
            if 'Description' not in self.data.columns or 'user_id' not in self.data.columns:
                return {}
            
            # Create product baskets per user
            baskets = self.data.groupby('user_id')['Description'].apply(list).values
            
            # Find frequent itemsets
            rules = {}
            for basket in baskets:
                unique_items = list(set(basket))
                
                # Find pairs
                for item1, item2 in combinations(unique_items, 2):
                    pair = tuple(sorted([item1, item2]))
                    if pair not in rules:
                        rules[pair] = {'count': 0, 'users': set()}
                    rules[pair]['count'] += 1
                    rules[pair]['users'].add(self.data[self.data['Description'] == item1]['user_id'].iloc[0])
            
            # Calculate support and filter
            total_users = self.data['user_id'].nunique()
            filtered_rules = {}
            
            for pair, info in sorted(rules.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
                support = len(info['users']) / total_users
                if support >= min_support:
                    filtered_rules[pair] = {
                        'support': float(support),
                        'count': info['count']
                    }
            
            return filtered_rules
        except:
            return {}
    
    def generate_cluster_recommendations(self):
        """Generate recommendations per cluster"""
        recommendations = {}
        
        unique_clusters = np.unique(self.clusters)
        
        for cluster in unique_clusters:
            cluster_data = self.data[self.clusters == cluster]
            
            # Analyze spending patterns
            avg_spend = cluster_data['total_spent'].mean() if 'total_spent' in cluster_data.columns else 0
            
            # Analyze purchase frequency
            avg_purchases = cluster_data['purchase_count'].mean() if 'purchase_count' in cluster_data.columns else 0
            
            # Analyze engagement
            avg_session = cluster_data['session_time'].mean() if 'session_time' in cluster_data.columns else 0
            
            # Top categories
            if 'category' in cluster_data.columns:
                top_categories = cluster_data['category'].value_counts().head(3).index.tolist()
            else:
                top_categories = []
            
            # Determine segment
            overall_avg_spend = self.data['total_spent'].mean() if 'total_spent' in self.data.columns else 0
            
            if avg_spend > overall_avg_spend * 1.5:
                segment = 'Premium'
                recs = self._get_premium_recommendations(top_categories)
            elif avg_spend > overall_avg_spend * 0.5:
                segment = 'Standard'
                recs = self._get_standard_recommendations(top_categories)
            else:
                segment = 'Budget'
                recs = self._get_budget_recommendations(top_categories)
            
            recommendations[int(cluster)] = {
                'segment': segment,
                'recommendations': recs,
                'metrics': {
                    'avg_spend': float(avg_spend),
                    'avg_purchases': float(avg_purchases),
                    'avg_engagement_min': float(avg_session),
                    'top_categories': top_categories,
                    'size': len(cluster_data)
                }
            }
        
        return recommendations
    
    def _get_premium_recommendations(self, categories):
        """Recommendations for premium segment"""
        base = [
            "🏆 VIP Membership (free shipping + exclusive access)",
            "💎 Premium product line",
            "🎁 Personal shopping assistant",
            "⭐ Priority customer support"
        ]
        
        if categories:
            base.append(f"🎯 Exclusive {categories[0]} collection")
        
        return base
    
    def _get_standard_recommendations(self, categories):
        """Recommendations for standard segment"""
        base = [
            "📊 Loyalty program enrollment",
            "🎟️ Regular promotional offers",
            "📦 Bundle deals",
            "💰 Seasonal discounts"
        ]
        
        if categories:
            base.append(f"🔍 Trending {categories[0]} items")
        
        return base
    
    def _get_budget_recommendations(self, categories):
        """Recommendations for budget segment"""
        base = [
            "🚀 Re-engagement welcome bonus",
            "💳 Value starter package",
            "🎉 Flash sales & limited offers",
            "📱 Mobile app exclusive deals"
        ]
        
        if categories:
            base.append(f"⭐ Popular basics in {categories[0]}")
        
        return base
    
    def generate_personalized_insights(self):
        """Generate personalized insights for users"""
        insights = {}
        
        for idx, row in self.data.iterrows():
            user_cluster = self.clusters[idx]
            
            insight_text = f"📊 User Profile: "
            
            if 'total_spent' in row:
                if row['total_spent'] > self.data['total_spent'].quantile(0.75):
                    insight_text += "High-value customer. "
                elif row['total_spent'] > self.data['total_spent'].quantile(0.25):
                    insight_text += "Regular customer. "
                else:
                    insight_text += "New/casual customer. "
            
            if 'purchase_count' in row:
                if row['purchase_count'] > self.data['purchase_count'].quantile(0.75):
                    insight_text += "Frequent buyer. "
            
            if 'session_time' in row:
                if row['session_time'] > self.data['session_time'].quantile(0.75):
                    insight_text += "Highly engaged. "
            
            insights[int(idx)] = insight_text.strip()
        
        return insights
    
    def get_cross_sell_opportunities(self):
        """Identify cross-sell opportunities"""
        rules = self.mine_association_rules()
        
        opportunities = []
        for (item1, item2), metrics in rules.items():
            opportunities.append({
                'product_1': item1,
                'product_2': item2,
                'confidence': f"{metrics['support']*100:.1f}%",
                'pattern': f"Customers buying {item1} often also buy {item2}"
            })
        
        return opportunities
    
    def run_full_recommendation_analysis(self):
        """Generate all recommendations"""
        print("\n" + "="*80)
        print("🎯 HYBRID RECOMMENDATION ENGINE - ANALYSIS")
        print("="*80)
        
        # 1. Cluster-based recommendations
        print("\n📍 Generating cluster-based recommendations...")
        cluster_recs = self.generate_cluster_recommendations()
        
        # 2. Association rules
        print("🔍 Mining association rules...")
        assoc_rules = self.mine_association_rules()
        
        # 3. Personalized insights
        print("👤 Generating personalized insights...")
        insights = self.generate_personalized_insights()
        
        # 4. Cross-sell opportunities
        print("🔄 Identifying cross-sell opportunities...")
        cross_sell = self.get_cross_sell_opportunities()
        
        print("\n" + "="*80)
        
        return {
            'cluster_recommendations': cluster_recs,
            'association_rules': assoc_rules,
            'personalized_insights': insights,
            'cross_sell_opportunities': cross_sell,
            'total_rules': len(assoc_rules),
            'total_opportunities': len(cross_sell)
        }
