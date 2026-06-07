# Estructura del Proyecto

```
simulacion_registro_civil/
├── src/                          # Código fuente de Azure Functions
│   ├── __init__.py
│   ├── function_app.py          # Endpoint HTTP principal
│   ├── identity_service.py      # Lógica de negocio
│   └── generate_synthetic_registry.py  # Generador de datos sintéticos
│
├── data-sources/                # Archivos de extracción
│   ├── extracted_names_pdf.py   # Script de extracción del PDF
│   ├── extracted_names.json     # Datos extraídos del PDF
│   ├── extracted_names.csv      # Datos en formato CSV
│   └── Listado-CCS-CNE.pdf      # PDF original
│
├── data/                        # Datos sintéticos
│   └── synthetic_registry.json  
│
├── tests/                       # Pruebas unitarias
│   └── test_identity_service.py
│
├── config/                      # Archivos de configuración
│   ├── host.json                # Configuración Azure Functions
│   ├── local.settings.json.example
│   └── pytest.ini
│
├── requirements.txt             # Dependencias de producción
├── requirements-dev.txt         # Dependencias de desarrollo
├── pytest.ini                   # (En config/)
├── .gitignore
└── README.md
```

## Explicación de Carpetas

### `src/` - Código Principal (Azure Functions)
Contiene todo lo necesario para ejecutar en Azure:
- `function_app.py`: Punto de entrada HTTP
- `identity_service.py`: Lógica pura sin dependencias Azure
- `generate_synthetic_registry.py`: CLI para generar datos

### `data-sources/` - Extracción de Datos
Herramientas y archivos para extraer nombres del PDF original:
- NO necesarios para Microsoft Azure Functions
- Útiles para regenerar/actualizar datos base
- Nombres y Apellidos de conocimiento público

### `data/` - Datos de Aplicación
Archivos generados que usa la aplicación:
- `synthetic_registry.json`: Se carga en memoria al iniciar

### `config/` - Configuración
Archivos de configuración del proyecto:
- Azure Functions settings
- Pytest configuration

### `tests/` - Pruebas
Suite completa de pruebas unitarias.
