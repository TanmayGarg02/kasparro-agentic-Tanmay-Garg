# core/writer.py
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _meta():
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "version": "1.0"
    }


def write_json(obj: Dict[str, Any], filename: str) -> Path:
    path = OUTPUT_DIR / filename
    # attach metadata without overwriting existing keys
    if isinstance(obj, dict):
        meta = obj.get("_meta", {})
        meta.update(_meta())
        obj["_meta"] = meta
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def write_all(faq_obj: Dict, product_obj: Dict, comparison_obj: Dict) -> Dict[str, str]:
    p1 = write_json(faq_obj, "faq.json")
    p2 = write_json(product_obj, "product_page.json")
    p3 = write_json(comparison_obj, "comparison_page.json")
    return {
        "faq": str(p1),
        "product_page": str(p2),
        "comparison_page": str(p3)
    }
