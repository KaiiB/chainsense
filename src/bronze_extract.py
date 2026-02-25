import argparse
import csv
import json
import os
from typing import Dict, Iterable, List


def read_jsonl(path: str) -> Iterable[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _hex_to_int(value: str) -> int:
    if value is None:
        return 0
    return int(value, 16)


def write_csv(path: str, rows: List[Dict]) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def extract_blocks(blocks: Iterable[Dict]) -> List[Dict]:
    rows: List[Dict] = []
    for b in blocks:
        rows.append(
            {
                "block_number": _hex_to_int(b.get("number")),
                "timestamp": _hex_to_int(b.get("timestamp")),
                "hash": b.get("hash"),
                "parent_hash": b.get("parentHash"),
                "miner": b.get("miner"),
                "gas_limit": _hex_to_int(b.get("gasLimit")),
                "gas_used": _hex_to_int(b.get("gasUsed")),
            }
        )
    return rows


def extract_transactions(blocks: Iterable[Dict]) -> List[Dict]:
    rows: List[Dict] = []
    for b in blocks:
        block_number = _hex_to_int(b.get("number"))
        for tx in b.get("transactions", []):
            rows.append(
                {
                    "tx_hash": tx.get("hash"),
                    "block_number": block_number,
                    "from": tx.get("from"),
                    "to": tx.get("to"),
                    "value": _hex_to_int(tx.get("value")),
                    "gas": _hex_to_int(tx.get("gas")),
                    "gas_price": _hex_to_int(tx.get("gasPrice")),
                    "nonce": _hex_to_int(tx.get("nonce")),
                    "input": tx.get("input"),
                }
            )
    return rows


def extract_receipts(receipts: Iterable[Dict]) -> List[Dict]:
    rows: List[Dict] = []
    for r in receipts:
        rows.append(
            {
                "tx_hash": r.get("transactionHash"),
                "block_number": _hex_to_int(r.get("blockNumber")),
                "status": _hex_to_int(r.get("status")),
                "gas_used": _hex_to_int(r.get("gasUsed")),
                "effective_gas_price": _hex_to_int(r.get("effectiveGasPrice")),
                "contract_address": r.get("contractAddress"),
                "logs_count": len(r.get("logs", [])),
            }
        )
    return rows


def extract_logs(receipts: Iterable[Dict]) -> List[Dict]:
    rows: List[Dict] = []
    for r in receipts:
        for log in r.get("logs", []):
            rows.append(
                {
                    "tx_hash": log.get("transactionHash"),
                    "block_number": _hex_to_int(log.get("blockNumber")),
                    "log_index": _hex_to_int(log.get("logIndex")),
                    "address": log.get("address"),
                    "topics": json.dumps(log.get("topics", [])),
                    "data": log.get("data"),
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default=os.path.join("data", "raw"))
    parser.add_argument("--out-dir", default=os.path.join("data", "bronze"))
    args = parser.parse_args()

    ensure_dir(args.out_dir)
    blocks_path = os.path.join(args.raw_dir, "blocks.jsonl")
    receipts_path = os.path.join(args.raw_dir, "receipts.jsonl")

    blocks = list(read_jsonl(blocks_path))
    receipts = list(read_jsonl(receipts_path))

    write_csv(os.path.join(args.out_dir, "blocks.csv"), extract_blocks(blocks))
    write_csv(os.path.join(args.out_dir, "transactions.csv"), extract_transactions(blocks))
    write_csv(os.path.join(args.out_dir, "receipts.csv"), extract_receipts(receipts))
    write_csv(os.path.join(args.out_dir, "logs.csv"), extract_logs(receipts))


if __name__ == "__main__":
    main()
