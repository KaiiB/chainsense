import argparse
import os

import numpy as np
import pandas as pd


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def build_profiles(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = [
        c
        for c in df.columns
        if c not in ["wallet", "window_start", "window_end", "cluster"]
        and np.issubdtype(df[c].dtype, np.number)
    ]
    return df.groupby("cluster")[num_cols].median().reset_index()


def label_clusters(profile: pd.DataFrame) -> pd.DataFrame:
    q_tx = profile["tx_count"].quantile([0.33, 0.67]).values
    q_cp = profile["unique_counterparties_out"].quantile([0.33, 0.67]).values
    q_gas = profile["total_gas_used"].quantile([0.33, 0.67]).values
    q_net = profile["eth_net_flow"].quantile([0.33, 0.67]).values

    labels = []
    for _, row in profile.iterrows():
        tx = row.get("tx_count", 0.0)
        cp = row.get("unique_counterparties_out", 0.0)
        gas = row.get("total_gas_used", 0.0)
        net = row.get("eth_net_flow", 0.0)
        pz = row.get("pct_zero_value_txs", 0.0)

        if tx >= q_tx[1] and cp >= q_cp[1] and gas >= q_gas[1]:
            label = "High-activity contract users (trader/bot-like)"
        elif net >= q_net[1] and tx <= q_tx[0]:
            label = "Net accumulators (holder-like)"
        elif net <= q_net[0] and tx >= q_tx[1]:
            label = "Net distributors (active senders)"
        elif pz > 0.5 and gas >= q_gas[0]:
            label = "Contract-interaction heavy users"
        else:
            label = "General/retail mixed behavior"

        labels.append({"cluster": int(row["cluster"]), "provisional_label": label})

    return pd.DataFrame(labels).sort_values("cluster").reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold-dir", default=os.path.join("data", "gold"))
    parser.add_argument("--analysis-dir", default=os.path.join("data", "analysis"))
    args = parser.parse_args()

    ensure_dir(args.analysis_dir)

    features = pd.read_csv(os.path.join(args.gold_dir, "rep_a_wallet_features.csv"))
    clusters = pd.read_csv(os.path.join(args.analysis_dir, "rep_a_clusters.csv"))

    df = features.merge(clusters, on=["wallet", "window_start", "window_end"], how="inner")

    cluster_sizes = (
        df["cluster"].value_counts().sort_index().rename_axis("cluster").reset_index(name="count")
    )
    profile = build_profiles(df)
    labels = label_clusters(profile)

    cluster_sizes.to_csv(os.path.join(args.analysis_dir, "rep_a_cluster_sizes.csv"), index=False)
    profile.to_csv(os.path.join(args.analysis_dir, "rep_a_cluster_profile_median.csv"), index=False)
    labels.to_csv(os.path.join(args.analysis_dir, "rep_a_cluster_labels.csv"), index=False)

    print("Wrote:")
    print("- data/analysis/rep_a_cluster_sizes.csv")
    print("- data/analysis/rep_a_cluster_profile_median.csv")
    print("- data/analysis/rep_a_cluster_labels.csv")


if __name__ == "__main__":
    main()
