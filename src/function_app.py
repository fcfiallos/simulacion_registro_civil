"""Punto de entrada de Azure Functions para la simulación."""

from __future__ import annotations

import azure.functions as func

from identity_service import VALID_CEDULAS, exists_in_registry, normalize_cedula, normalize_text, matches_full_name, SYNTHETIC_REGISTRY


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _extract_cedula(req: func.HttpRequest) -> str:
    """Extrae la cédula de query string o body JSON."""

    try:
        body = req.get_json()
    except ValueError:
        body = {}

    cedula = req.params.get("cedula") or body.get("cedula") or ""
    return normalize_cedula(cedula)


@app.route(route="validar", methods=["GET", "POST"])
def validar(req: func.HttpRequest) -> func.HttpResponse:
    """Devuelve 1 si la cédula sintética existe, 0 en caso contrario."""

    cedula = _extract_cedula(req)
    result = "1" if exists_in_registry(cedula, VALID_CEDULAS) else "0"

    return func.HttpResponse(result, status_code=200, mimetype="text/plain")

def _extract_person_data(req: func.HttpRequest) -> tuple[str, str, str]:
    try:
        body = req.get_json()
    except ValueError:
        body = {}

    cedula = normalize_cedula(req.params.get("cedula") or body.get("cedula") or "")
    name = req.params.get("name") or body.get("name") or ""
    surname = req.params.get("surname") or body.get("surname") or ""

    return cedula, name, surname


@app.route(route="validar-persona", methods=["GET", "POST"])
def validar(req: func.HttpRequest) -> func.HttpResponse:
    cedula, name, surname = _extract_person_data(req)

    result = "1" if matches_full_name(cedula, name, surname, SYNTHETIC_REGISTRY) else "0"

    return func.HttpResponse(result, status_code=200, mimetype="text/plain")
