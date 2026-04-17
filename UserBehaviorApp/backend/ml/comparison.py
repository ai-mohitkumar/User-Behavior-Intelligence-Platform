import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from .clustering import cluster_quality, apply_kmeans

def apply_dbscan(df, features, eps=0.5, min_samples=2):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    labels = dbscan.fit_predict(df[features])
    df_ = df.copy()
    df_['cluster'] = labels
    return df_, dbscan

def apply_hierarchical(df, features, n_clusters=4, linkage='ward'):
    hier = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    labels = hier.fit_predict(df[features])
    df_ = df.copy()
    df_['cluster'] = labels
    return df_, hier

def compare_algorithms(df, features, best_k=4):
    results = []
    
    # KMeans
    df_km, kmeans = apply_kmeans(df, features, best_k)
    scores_km = cluster_quality(df, features, df_km['cluster'])
    results.append({'algorithm': 'KMeans', **scores_km})
    
    # DBSCAN best eps
    eps_list = [0.3, 0.5, 0.8]
    best_eps_score = -1
    best_eps = 0.5
    for eps in eps_list:
        df_db, _ = apply_dbscan(df, features, eps=eps)
        scores = cluster_quality(df, features, df_db['cluster'])
        if scores['silhouette'] > best_eps_score:
            best_eps_score = scores['silhouette']
            best_eps = eps
    df_db, dbscan = apply_dbscan(df, features, eps=best_eps)
    scores_db = cluster_quality(df, features, df_db['cluster'])
    results.append({'algorithm': f'DBSCAN(eps={best_eps})', **scores_db})
    
    # Hierarchical
    df_hier, hier = apply_hierarchical(df, features, best_k)
    scores_hier = cluster_quality(df, features, df_hier['cluster'])
    results.append({'algorithm': 'Hierarchical', **scores_hier})
    
    table = pd.DataFrame(results).round(4)
    best_idx = table['silhouette'].idxmax()
    best_algo = table.loc[best_idx, 'algorithm']
    
    return table.to_dict('records'), best_algo

