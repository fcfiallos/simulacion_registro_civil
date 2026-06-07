# Simulación Registro Civil
### Generación de una API para validación de identidad del Registro Civil del Ecuador

## Objetivo

Este proyecto simula una validación de identidad con una salida mínima y determinista. No consume la API del Registro Civil ni usa huellas dactilares. La respuesta de negocio es solo un número en texto plano:

- `1` = existe
- `0` = no existe

## Estructura

Ver [ESTRUCTURA](ESTRUCTURA.md) para la documentación completa de carpetas y organización del proyecto.

**Componentes principales:**

- `src/function_app.py`: Endpoint HTTP de Azure Functions
- `src/identity_service.py`: Lógica pura de validación
- `src/generate_synthetic_registry.py`: Generador de catálogo sintético
- `data/synthetic_registry.json`: Catálogo con cédula, nombre y apellido
- `data-sources/extracted_names.json`: Listado base de datos
- `tests/test_identity_service.py`: Pruebas unitarias

## API - Contrato de Datos

La API recibe una cédula sintética de 10 dígitos y responde con:
- `1` = cédula válida (existe en registro)
- `0` = cédula inválida (no existe en registro)

**Endpoints disponibles:**

- `GET /api/validar?cedula=9900000001`
- `POST /api/validar` con body `{ "cedula": "9900000001" }`

## Despliegue en Azure

El proyecto está diseñado para ejecutarse como **Azure Function Python** con:
- Autenticación: Anónima
- Runtime: Python 3.x
- Trigger: HTTP
- Dependencias: Azure Functions SDK + librerías estándar

La separación entre lógica de negocio (`identity_service.py`) y handler HTTP (`function_app.py`) facilita pruebas, mantenimiento y trazabilidad.

## Notas de diseño

- Las cédulas son sintéticas y se generan localmente desde el listado base.
- El catálogo final se materializa en `synthetic_registry.json`.
- No se guarda información sensible adicional.
- La validación es determinista y fácil de probar.
