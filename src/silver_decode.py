import argparse
import csv
import json
import os
from typing import Dict, Iterable, List


ERC20_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def read_csv(path: str) -> Iterable[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield row


def _hex_to_int(value: str) -> int:
    if value is None or value == "0x":
        return 0
    return int(value, 16)


def _topic_to_address(topic: str) -> str:
    if not topic:
        return ""
    return "0x" + topic[-40:]


def decode_erc20_transfers(logs: Iterable[Dict]) -> List[Dict]:
    rows: List[Dict] = []
    for log in logs:
        topics = json.loads(log.get("topics", "[]"))
        if not topics or topics[0].lower() != ERC20_TRANSFER_TOPIC:
            continue
        from_addr = _topic_to_address(topics[1]) if len(topics) > 1 else ""
        to_addr = _topic_to_address(topics[2]) if len(topics) > 2 else ""
        amount = _hex_to_int(log.get("data"))
        rows.append(
            {
                "tx_hash": log.get("tx_hash"),
                "block_number": int(log.get("block_number")),
                "token_address": log.get("address"),
                "from": from_addr,
                "to": to_addr,
                "amount_raw": amount,
            }
        )
    return rows


def write_csv(path: str, rows: List[Dict]) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bronze-dir", default=os.path.join("data", "bronze"))
    parser.add_argument("--out-dir", default=os.path.join("data", "silver"))
    args = parser.parse_args()

    ensure_dir(args.out_dir)
    logs_path = os.path.join(args.bronze_dir, "logs.csv")
    logs = list(read_csv(logs_path))
    transfers = decode_erc20_transfers(logs)
    write_csv(os.path.join(args.out_dir, "erc20_transfers.csv"), transfers)


if __name__ == "__main__":
    main()
