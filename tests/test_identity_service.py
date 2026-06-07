from pathlib import Path
import sys

# Agregar el directorio src al path para poder importar identity_service
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from identity_service import (
    build_synthetic_cedulas,
    build_synthetic_registry,
    build_valid_cedulas,
    exists_in_registry,
    is_valid_cedula_format,
    load_people,
    load_registry,
    normalize_cedula,
)


def test_load_people_reads_json(tmp_path: Path) -> None:
    data_file = tmp_path / "people.json"
    data_file.write_text(
        '[{"name": "ANA", "surname": "PEREZ"}, {"name": "LUIS", "surname": "GOMEZ"}]',
        encoding="utf-8",
    )

    people = load_people(data_file)

    assert len(people) == 2
    assert people[0]["name"] == "ANA"


def test_build_synthetic_cedulas_is_deterministic() -> None:
    people = [{"name": "ANA", "surname": "PEREZ"}, {"name": "LUIS", "surname": "GOMEZ"}]

    cedulas = build_synthetic_cedulas(people)

    assert cedulas == {"9900000001", "9900000002"}


def test_build_synthetic_registry_includes_cedula() -> None:
    people = [{"name": "ANA", "surname": "PEREZ"}, {"name": "LUIS", "surname": "GOMEZ"}]

    registry = build_synthetic_registry(people)

    assert registry == [
        {"cedula": "9900000001", "name": "ANA", "surname": "PEREZ"},
        {"cedula": "9900000002", "name": "LUIS", "surname": "GOMEZ"},
    ]


def test_build_valid_cedulas_extracts_from_registry() -> None:
    registry = [
        {"cedula": "9900000001", "name": "ANA", "surname": "PEREZ"},
        {"cedula": "9900000002", "name": "LUIS", "surname": "GOMEZ"},
    ]

    assert build_valid_cedulas(registry) == {"9900000001", "9900000002"}


def test_normalize_and_validate_format() -> None:
    assert normalize_cedula(" 9900000001 ") == "9900000001"
    assert is_valid_cedula_format("9900000001") is True
    assert is_valid_cedula_format("990000001") is False
    assert is_valid_cedula_format("99A0000001") is False


def test_exists_in_registry_only_accepts_catalog_values() -> None:
    valid_cedulas = {"9900000001"}

    assert exists_in_registry("9900000001", valid_cedulas) is True
    assert exists_in_registry("9900000002", valid_cedulas) is False
    assert exists_in_registry(" 9900000001 ", valid_cedulas) is False


def test_load_registry_falls_back_to_generated_catalog(tmp_path: Path, monkeypatch) -> None:
    data_file = tmp_path / "people.json"
    data_file.write_text(
        '[{"name": "ANA", "surname": "PEREZ"}]',
        encoding="utf-8",
    )
    registry_file = tmp_path / "synthetic_registry.json"

    monkeypatch.setattr("identity_service.DEFAULT_DATA_FILE", data_file)
    monkeypatch.setattr("identity_service.DEFAULT_REGISTRY_FILE", registry_file)

    registry = load_registry(registry_file)

    assert registry == [{"cedula": "9900000001", "name": "ANA", "surname": "PEREZ"}]