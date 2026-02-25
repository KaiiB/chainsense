import argparse
import os

import numpy as np
import pandas as pd


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def assign_block_window(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    df = df.copy()
    if "block_number" not in df.columns and "blockNumber" in df.columns:
        df = df.rename(columns={"blockNumber": "block_number"})
    if "block_number" not in df.columns:
        raise KeyError("block_number column missing from input data")
    df["window_start"] = (df["block_number"] // window_size) * window_size
    df["window_end"] = df["window_start"] + window_size - 1
    return df


def build_rep_a(transactions: pd.DataFrame, receipts: pd.DataFrame, window_size: int) -> pd.DataFrame:
    tx = assign_block_window(transactions, window_size)
    rc = assign_block_window(receipts, window_size)

    # Ensure numeric columns are numeric
    for col in ["value", "gas", "gas_price", "nonce"]:
        if col in tx.columns:
            tx[col] = pd.to_numeric(tx[col], errors="coerce").fillna(0)
    for col in ["gas_used", "effective_gas_price", "logs_count"]:
        if col in rc.columns:
            rc[col] = pd.to_numeric(rc[col], errors="coerce").fillna(0)

    tx["is_zero_value"] = (tx["value"] == 0).astype(int)

    # Activity and value flow (sender)
    sender = (
        tx.groupby(["from", "window_start", "window_end"], dropna=False)
        .agg(
            tx_out_count=("tx_hash", "count"),
            eth_sent_total=("value", "sum"),
            median_eth_value=("value", "median"),
            max_eth_value=("value", "max"),
            zero_value_txs=("is_zero_value", "sum"),
            unique_counterparties_out=("to", "nunique"),
        )
        .reset_index()
        .rename(columns={"from": "wallet"})
    )

    # Activity and value flow (receiver)
    receiver = (
        tx.groupby(["to", "window_start", "window_end"], dropna=False)
        .agg(
            tx_in_count=("tx_hash", "count"),
            eth_recv_total=("value", "sum"),
            unique_counterparties_in=("from", "nunique"),
        )
        .reset_index()
        .rename(columns={"to": "wallet"})
    )

    # Gas/execution (sender)
    rc_for_merge = rc.drop(columns=["window_start", "window_end"], errors="ignore")
    gas = (
        rc_for_merge.merge(tx[["tx_hash", "from", "window_start", "window_end"]], on="tx_hash", how="left")
        .groupby(["from", "window_start", "window_end"], dropna=False)
        .agg(
            mean_gas_used=("gas_used", "mean"),
            median_gas_used=("gas_used", "median"),
            gas_used_std=("gas_used", "std"),
            total_gas_used=("gas_used", "sum"),
        )
        .reset_index()
        .rename(columns={"from": "wallet"})
    )

    features = sender.merge(receiver, on=["wallet", "window_start", "window_end"], how="outer")
    features = features.merge(gas, on=["wallet", "window_start", "window_end"], how="left")

    # Fill NaNs for counts and totals
    for col in [
        "tx_out_count",
        "tx_in_count",
        "eth_sent_total",
        "eth_recv_total",
        "unique_counterparties_out",
        "unique_counterparties_in",
        "zero_value_txs",
        "total_gas_used",
    ]:
        if col in features.columns:
            features[col] = features[col].fillna(0)

    # Derived features
    features["tx_count"] = features["tx_out_count"] + features["tx_in_count"]
    features["eth_net_flow"] = features["eth_recv_total"] - features["eth_sent_total"]
    features["pct_zero_value_txs"] = np.where(
        features["tx_out_count"] > 0,
        features["zero_value_txs"] / features["tx_out_count"],
        0.0,
    )

    # Log1p heavy-tailed
    for col in ["tx_count", "eth_sent_total", "eth_recv_total", "total_gas_used"]:
        features[f"log1p_{col}"] = np.log1p(features[col])

    return features


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bronze-dir", default=os.path.join("data", "bronze"))
    parser.add_argument("--out-dir", default=os.path.join("data", "gold"))
    parser.add_argument("--window-size", type=int, default=10000)
    args = parser.parse_args()

    ensure_dir(args.out_dir)
    tx = pd.read_csv(os.path.join(args.bronze_dir, "transactions.csv"))
    rc = pd.read_csv(os.path.join(args.bronze_dir, "receipts.csv"))
    features = build_rep_a(tx, rc, args.window_size)
    features.to_csv(os.path.join(args.out_dir, "rep_a_wallet_features.csv"), index=False)


if __name__ == "__main__":
    main()
