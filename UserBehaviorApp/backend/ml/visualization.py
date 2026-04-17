import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
from io import BytesIO
import base64

def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def generate_plots(df_clustered, features):
    plots = {}
    
    # Elbow would need wcss_list from opt
    # PCA 2D
    X = df_clustered[features].select_dtypes(include=[np.number]).fillna(0)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    fig_pca = plt.figure(figsize=(8,6))
    scatter = plt.scatter(X_pca[:,0], X_pca[:,1], c=df_clustered['cluster'], cmap='viridis', alpha=0.6)
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
    plt.title('PCA 2D Clusters')
    plt.colorbar(scatter, label='Cluster')
    plots['pca_2d'] = plot_to_base64(fig_pca)
    plt.close(fig_pca)
    
    return plots

