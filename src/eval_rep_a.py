import argparse
import os

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold-dir", default=os.path.join("data", "gold"))
    parser.add_argument("--out-dir", default=os.path.join("data", "analysis"))
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    ensure_dir(args.out_dir)
    features_path = os.path.join(args.gold_dir, "rep_a_wallet_features.csv")
    df = pd.read_csv(features_path)

    id_cols = ["wallet", "window_start", "window_end"]
    feature_cols = [c for c in df.columns if c not in id_cols]
    X = df[feature_cols].fillna(0.0).values

    # Correlation matrix
    corr = pd.DataFrame(df[feature_cols]).corr()
    corr.to_csv(os.path.join(args.out_dir, "rep_a_correlation.csv"))

    # Standardize, PCA for visualization summary
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=min(5, X_scaled.shape[1]))
    X_pca = pca.fit_transform(X_scaled)

    pca_df = pd.DataFrame(X_pca, columns=[f"pc{i+1}" for i in range(X_pca.shape[1])])
    pca_df[id_cols] = df[id_cols]
    pca_df.to_csv(os.path.join(args.out_dir, "rep_a_pca.csv"), index=False)

    # KMeans clustering
    kmeans = KMeans(n_clusters=args.k, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    df_out = df[id_cols].copy()
    df_out["cluster"] = labels
    df_out.to_csv(os.path.join(args.out_dir, "rep_a_clusters.csv"), index=False)

    # Silhouette score (if > 1 cluster)
    if len(np.unique(labels)) > 1:
        score = silhouette_score(X_scaled, labels)
    else:
        score = float("nan")

    with open(os.path.join(args.out_dir, "rep_a_metrics.txt"), "w", encoding="utf-8") as f:
        f.write(f"silhouette_score: {score}\n")
        f.write(f"explained_variance_ratio: {pca.explained_variance_ratio_.tolist()}\n")


if __name__ == "__main__":
    main()
