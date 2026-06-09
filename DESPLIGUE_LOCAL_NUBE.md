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
5. Pruebas de EndPoint local
***GET***  
```
http://localhost:7071/api/validar-persona?cedula=9900000001&name=ANA&surname=PEREZ
```
***POST***
```
POST http://localhost:7071/api/validar-persona
Content-Type: application/json

{ "cedula": "9900000001", "name": "ANA", "surname": "PEREZ" }
```
6. Despliegue en Azure Functions

Para ejecutar este servicio en la nube con Azure Functions, siga estos pasos básicos:

1. Inicie sesión en Azure:
```powershell
az login
```
2. Cree (si aún no existe) un recurso de Function App en Azure. Por ejemplo:
```powershell
az functionapp create --resource-group <NOMBRE_DEL_GRUPO> --consumption-plan-location <REGION> --runtime python --runtime-version 3.11 --functions-version 4 --name <NOMBRE_APP> --storage-account <NOMBRE_STORAGE>
```
3. Publique el proyecto en la Function App:
```powershell
func azure functionapp publish <NOMBRE_APP> --python
```

Después del despliegue, la URL del servicio será similar a:
```
https://<NOMBRE_APP>.azurewebsites.net/api/validar-persona?cedula=9900000001&name=ANA&surname=PEREZ
```

Para un `POST` en la nube:
```
POST https://<NOMBRE_APP>.azurewebsites.net/api/validar-persona
Content-Type: application/json

{ "cedula": "9900000001", "name": "ANA", "surname": "PEREZ" }
```

> Importante: la configuración local de `local.settings.json` no se publica automáticamente a Azure. Use el portal de Azure o `az functionapp config appsettings set` para definir variables de configuración en la nube.
