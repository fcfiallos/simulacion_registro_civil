"""Genera el catálogo sintético con cédula para el proyecto."""

from __future__ import annotations

from pathlib import Path
import json

from identity_service import build_synthetic_registry, load_people


OUTPUT_FILE = Path(__file__).with_name("synthetic_registry.json")


def main() -> None:
    people = load_people()
    registry = build_synthetic_registry(people)
    OUTPUT_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(registry)} synthetic records in {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()