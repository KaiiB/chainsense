# Chainsense Dashboard Backend

Python FastAPI server for serving Chainsense analysis data.

## Setup

```bash
pip install fastapi uvicorn pandas pyarrow numpy
```

## Running

```bash
python server.py
```

Server runs on `http://localhost:8000`

## Endpoints

- `GET /api/analysis` - Fetch full analysis data
- `GET /health` - Health check
