import json
from pathlib import Path
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/api/tariff-engine", tags=["tariff-engine"])
@router.get("/_ping")
def ping():
    return {"ok": True}


DATA_DIR = Path("tariff_engine/normalized")
_cache = {}

def load_bloc(bloc: str):
    b = bloc.upper().strip()
    candidates = [
        DATA_DIR / f"{b}_MASTER_indexed.json",
        DATA_DIR / f"{b}_MASTER_14_80_indexed.json",
    ]
    for p in candidates:
        if p.exists():
            if b not in _cache:
                _cache[b] = json.loads(p.read_text(encoding="utf-8"))
            return _cache[b], str(p)
    raise FileNotFoundError(f"No indexed JSON for bloc={b}. Expected: {candidates}")

@router.get("/{bloc}")
def get_tariff(bloc: str, hs: str):
    try:
        data, src = load_bloc(bloc)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    key = hs.replace(".", "").strip()
    row = data.get(key)
    if not row:
        raise HTTPException(status_code=404, detail={"error": "not found", "bloc": bloc.upper(), "hs": key, "dataset": src})

    out = dict(row)
    out["_bloc"] = bloc.upper()
    out["_dataset"] = src
    return out

@router.get("/{bloc}/meta")
def meta(bloc: str):
    data, src = load_bloc(bloc)
    keys = list(data.keys())
    # stats rapides
    rate_ok = sum(1 for k in keys if data[k].get("duty_rate_pct") is not None)
    unit_ok = sum(1 for k in keys if str(data[k].get("unit","")).strip() != "")
    return {
        "bloc": bloc.upper(),
        "dataset": src,
        "keys": len(keys),
        "rate_non_null": rate_ok,
        "unit_non_empty": unit_ok,
        "sample_keys": keys[:10],
    }

