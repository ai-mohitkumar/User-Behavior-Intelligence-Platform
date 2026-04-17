from .clustering import apply_kmeans, cluster_quality

def find_best_k(df, features, max_k=7):
    n_samples = len(df)
    k_range = range(2, min(max_k + 1, n_samples))
    best_score = -1.0
    best_k = None
    best_labels = None
    wcss_list = []
    all_scores = []

    for k in k_range:
        clustered, kmeans_model = apply_kmeans(df, features, k)
        scores = cluster_quality(df, features, clustered['cluster'])
        wcss = kmeans_model.inertia_
        wcss_list.append(wcss)
        all_scores.append({**scores, 'wcss': wcss})
        score = scores['silhouette']
        if score > best_score:
            best_score = score
            best_k = k
            best_labels = clustered['cluster'].tolist()

    return {'best_k': best_k, 'best_score': best_score, 'labels': best_labels, 'wcss_list': wcss_list, 'all_scores': all_scores}

