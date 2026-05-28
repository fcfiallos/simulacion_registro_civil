# Simulación Registro Civil
### Generación de una API para validación de identidad del Registro Civil del Ecuador

## Objetivo

Este proyecto simula una validación de identidad con una salida mínima y determinista. No consume la API del Registro Civil ni usa huellas dactilares. La respuesta de negocio es solo un número en texto plano:

- `1` = existe
- `0` = no existe

## Estructura

- `function_app.py`: entrada HTTP de Azure Functions.
- `identity_service.py`: reglas puras y catálogo sintético.
- `synthetic_registry.json`: catálogo con `cedula`, nombre y apellido.
- `generate_synthetic_registry.py`: generador reproducible del catálogo.
- `extracted_names.json`: listado base local.
- `tests/`: pruebas unitarias.

## Cómo probar en local

1. Crea y activa un entorno virtual.
2. Instala dependencias de runtime y pruebas.
3. Ejecuta `pytest`.

Ejemplo:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Ejecutar Azure Functions en local

Necesitas Azure Functions Core Tools instalado. Luego:

1. Copia [local.settings.json.example](local.settings.json.example) a `local.settings.json`.
2. Verifica que `FUNCTIONS_WORKER_RUNTIME` quede en `python`.
3. Ejecuta `func start`.

La ruta disponible es:

- `GET /api/validar?cedula=...`
- `POST /api/validar` con `{ "cedula": "..." }`

## Contrato mínimo

La API recibe una cédula sintética de 10 dígitos y responde solo con `1` o `0`.

## Azure

Para desplegar, el proyecto está pensado como Azure Function Python con autenticación anónima. La lógica de negocio está separada del handler para facilitar pruebas, mantenimiento y trazabilidad bajo una metodología XP.

## Notas de diseño

- Las cédulas son sintéticas y se generan localmente desde el listado base.
- El catálogo final se materializa en `synthetic_registry.json`.
- No se guarda información sensible adicional.
- La validación es determinista y fácil de probar.
