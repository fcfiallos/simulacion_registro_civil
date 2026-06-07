"""Reglas puras para la simulación de validación de identidad.

Este módulo no conoce Azure Functions ni HTTP. Solo carga el listado local,
genera cédulas sintéticas y valida si una cédula existe en el catálogo.
"""

from __future__ import annotations

from pathlib import Path
import json


# Rutas relativas al directorio src
DEFAULT_DATA_FILE = Path(__file__).parent.parent / "data-sources" / "extracted_names.json"
DEFAULT_REGISTRY_FILE = Path(__file__).parent.parent / "data" / "synthetic_registry.json"
CEDULA_PREFIX = "99"
CEDULA_LENGTH = 10


def load_people(file_path: Path | None = None) -> list[dict[str, str]]:
    """Carga el catálogo local de nombres y apellidos.

    Args:
        file_path: Ruta al archivo JSON con el listado base.

    Returns:
        Lista de diccionarios con las claves ``name`` y ``surname``.
    """

    source_file = file_path or DEFAULT_DATA_FILE
    return json.loads(source_file.read_text(encoding="utf-8"))


def build_synthetic_cedulas(people: list[dict[str, str]]) -> set[str]:
    """Construye cédulas sintéticas deterministas a partir del listado local."""

    return {f"{CEDULA_PREFIX}{index:08d}" for index, _ in enumerate(people, start=1)}


def build_synthetic_registry(people: list[dict[str, str]]) -> list[dict[str, str]]:
    """Construye un catálogo sintético con nombre, apellido y cédula."""

    return [
        {
            "cedula": f"{CEDULA_PREFIX}{index:08d}",
            "name": person["name"],
            "surname": person["surname"],
        }
        for index, person in enumerate(people, start=1)
    ]


def load_registry(file_path: Path | None = None) -> list[dict[str, str]]:
    """Carga el catálogo sintético si existe; si no, lo deriva del listado base."""

    registry_file = file_path or DEFAULT_REGISTRY_FILE

    if registry_file.exists():
        return json.loads(registry_file.read_text(encoding="utf-8"))

    return build_synthetic_registry(load_people())


def build_valid_cedulas(registry: list[dict[str, str]]) -> set[str]:
    """Extrae el conjunto de cédulas válidas desde el catálogo sintético."""

    return {person["cedula"] for person in registry}


def normalize_cedula(value: str | None) -> str:
    """Normaliza el valor recibido para evitar espacios accidentales."""

    return (value or "").strip()


def is_valid_cedula_format(cedula: str) -> bool:
    """Valida el formato mínimo esperado para la cédula sintética.

    La simulación usa exactamente 10 dígitos.
    """

    return len(cedula) == CEDULA_LENGTH and cedula.isdigit()


def exists_in_registry(cedula: str, valid_cedulas: set[str]) -> bool:
    """Indica si la cédula existe en el catálogo sintético local."""

    return is_valid_cedula_format(cedula) and cedula in valid_cedulas


SYNTHETIC_REGISTRY = load_registry()
VALID_CEDULAS = build_valid_cedulas(SYNTHETIC_REGISTRY)
