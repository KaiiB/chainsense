import argparse
import json
import os
from typing import Dict, Iterable, List

from rpc import rpc_call


def _hex_block(num: int) -> str:
    return hex(num)


def fetch_block(number: int) -> Dict:
    return rpc_call("eth_getBlockByNumber", [_hex_block(number), True])


def fetch_receipt(tx_hash: str) -> Dict:
    return rpc_call("eth_getTransactionReceipt", [tx_hash])


def iter_blocks(start: int, end: int) -> Iterable[Dict]:
    for num in range(start, end + 1):
        block = fetch_block(num)
        if block is None:
            continue
        yield block


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_jsonl(path: str, items: Iterable[Dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item))
            f.write("\n")


def fetch_and_store(start: int, end: int, raw_dir: str) -> None:
    ensure_dir(raw_dir)
    blocks_path = os.path.join(raw_dir, "blocks.jsonl")
    receipts_path = os.path.join(raw_dir, "receipts.jsonl")

    blocks: List[Dict] = []
    receipts: List[Dict] = []

    for block in iter_blocks(start, end):
        blocks.append(block)
        for tx in block.get("transactions", []):
            tx_hash = tx.get("hash")
            if not tx_hash:
                continue
            receipt = fetch_receipt(tx_hash)
            if receipt:
                receipts.append(receipt)

    write_jsonl(blocks_path, blocks)
    write_jsonl(receipts_path, receipts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--raw-dir", default=os.path.join("data", "raw"))
    args = parser.parse_args()

    fetch_and_store(args.start, args.end, args.raw_dir)


if __name__ == "__main__":
    main()
