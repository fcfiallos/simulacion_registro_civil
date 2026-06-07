"""Punto de entrada de Azure Functions para la simulación."""

from __future__ import annotations

import azure.functions as func

from identity_service import VALID_CEDULAS, exists_in_registry, normalize_cedula


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
