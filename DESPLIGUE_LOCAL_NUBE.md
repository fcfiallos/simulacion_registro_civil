# Guía de Prueba Local

## Objetivo

Este documento explica cómo instalar, ejecutar y probar el proyecto localmente antes de desplegarlo a Azure.

## Requisitos

- Python 3.11 recomendado
- Azure Functions Core Tools instalado
- `pip` disponible

Documentación oficial de instalación:
https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local

## Comandos de Ejecución Local

1. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Instalar Dependencias
```powershell
pip install -r requirements.txt -r requirements-dev.txt
```
3. Ejecutar pruebas unitarias
```powershell
pytest
```
4. Ejecutar Azure Functions local
```powershell
func start --script-root src --verbose
```
5. Pruebas de EndPoint
***GET***  
```
http://localhost:7071/api/validar?cedula=9900000001 
```
***POST***
```
http://localhost:7071/api/validar con body { "cedula": "9900000001}
```
