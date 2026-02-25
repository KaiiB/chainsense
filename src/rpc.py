import json
import os
import time
from typing import Any, Dict, Optional

import requests


def _alchemy_url() -> str:
    api_key = os.getenv("ALCHEMY_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ALCHEMY_API_KEY env var.")
    return f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"


def rpc_call(method: str, params: Optional[list] = None, timeout_s: int = 30) -> Dict[str, Any]:
    url = _alchemy_url()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or [],
    }

    for attempt in range(5):
        resp = requests.post(url, json=payload, timeout=timeout_s)
        if resp.status_code == 429:
            time.sleep(1.5 * (attempt + 1))
            continue
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(json.dumps(data["error"]))
        return data["result"]

    raise RuntimeError("Rate limited by Alchemy after retries.")
