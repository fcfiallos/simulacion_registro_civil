# !pip install pdfplumber
"""
Módulo de Extracción de Datos desde PDF

Este módulo proporciona funcionalidades para:
1. Extraer texto de documentos PDF
2. Parsear nombres y apellidos usando expresiones regulares
3. Exportar datos en formatos JSON y CSV

El módulo está diseñado específicamente para procesar el listado de nombres
del "Listado-CCS-CNE.pdf" (Registro de Candidatos del CNE de Ecuador).

Uso:
    python extracted_names_pdf.py

Resultado:
    - extracted_names.json: Datos en formato JSON
    - extracted_names.csv: Datos en formato CSV
"""

import pdfplumber
import re
import json
import csv
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    Extrae el texto completo de un documento PDF página por página.
    
    Este método abre el archivo PDF especificado y extrae todo el texto
    disponible, concatenando el contenido de todas las páginas.
    
    Args:
        pdf_path (str | Path): Ruta al archivo PDF a procesar.
                               Puede ser string o Path object.
    
    Returns:
        str: Texto completo extraído del PDF con saltos de línea entre páginas.
        None: Si ocurre un error al leer o procesar el PDF.
    
    Raises (implícito):
        Cualquier excepción se captura y se imprime un mensaje descriptivo.
    
    Métodos internos utilizados:
        - pdfplumber.open(pdf_path): Abre el PDF en modo lectura
        - pdf.pages: Itera sobre todas las páginas del documento
        - page.extract_text(): Extrae texto de cada página
    
    Ejemplo:
        >>> texto = extract_text_from_pdf("documento.pdf")
        >>> print(len(texto))  # Muestra cantidad de caracteres
        45230
    """
    all_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Itera sobre cada página del PDF
            for page in pdf.pages:
                # Extrae el texto de la página y lo añade al texto completo
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None
    return all_text

def extract_names_and_surnames(text):
    """
    Extrae nombres y apellidos del texto usando procesamiento de líneas y regex.
    
    Este método analiza el texto línea por línea buscando patrones que coincidan
    con el formato de registro del documento (NÚMERO PROVINCIA NOMBRES APELLIDOS GÉNERO).
    
    La estrategia es:
    1. Dividir el texto en líneas individuales
    2. Descartar líneas vacías y sin números iniciales
    3. Aplicar expresión regular para identificar líneas de datos válidas
    4. Parsear la sección de nombres y apellidos
    5. Separar inteligentemente nombre(s) de apellido(s)
    
    Args:
        text (str): Texto completo extraído del PDF, típicamente resultado
                   de extract_text_from_pdf().
    
    Returns:
        list[dict]: Lista de diccionarios con estructura:
                   [{"name": "NOMBRE(S)", "surname": "APELLIDO(S)"}, ...]
                   Lista vacía si no se encuentran registros válidos.
    
    Métodos internos utilizados:
        - str.split('\n'): Divide texto en líneas
        - str.strip(): Elimina espacios en blanco al inicio/final
        - re.compile(): Compila patrón regex
        - re.match(): Intenta coincidir patrón desde inicio de línea
        - str.split(): Divide la sección de nombre en palabras
        - str.join(): Reconstruye strings con espacios
    
    Notas sobre el patrón Regex:
        Pattern: r'^\s*\d+\s+([A-ZÁÉÍÓÚÜÑ]+)\s+([A-ZÁÉÍÓÚÜÑ ]+)\s+([A-ZÁÉÍÓÚÜÑ]+)\s*$'
        
        ^\s*     : Inicio de línea con espacios opcionales
        \d+      : Uno o más dígitos (número de registro)
        \s+      : Espacios en blanco separadores
        Group 1  : Provincia (palabra única con caracteres latinos y acentos)
        Group 2  : Nombres y Apellidos (múltiples palabras con espacios)
        Group 3  : Género (M/F, palabra única)
        \s*$     : Espacios opcionales y fin de línea
        
        Soporta caracteres latinos con acentos: ÁÉÍÓÚÜÑ
    
    Lógica de separación Nombre/Apellido:
        - 3+ palabras: últimas 2 son apellidos, resto es nombre
        - 2 palabras: primera es nombre, segunda es apellido
        - 1 palabra: se asume que es nombre, apellido vacío
        - 0 palabras: se descarta (no se añade a resultados)
    
    Limitaciones (heurísticas):
        Este enfoque heurístico puede fallar con:
        - Nombres compuestos con preposiciones (ej: "María de los Ángeles")
        - Apellidos con prefijos (ej: "de la Cruz")
        Para mayor precisión, considerar usar NLP (spaCy, NLTK, Transformers)
    
    Ejemplo:
        >>> texto = "1 PICHINCHA JUAN CARLOS MORA GARCÍA M"
        >>> resultado = extract_names_and_surnames(texto)
        >>> resultado
        [{'name': 'JUAN CARLOS', 'surname': 'MORA GARCÍA'}]
    """
    names_found = []
    # Dividir el texto en líneas individuales para procesamiento
    lines = text.split('\n')

    # Expresión regular compilada una sola vez por eficiencia
    # Patrón diseñado para el formato: NÚMERO | PROVINCIA | NOMBRES APELLIDOS | GÉNERO
    data_line_pattern = re.compile(
        r'^\s*\d+\s+([A-ZÁÉÍÓÚÜÑ]+)\s+([A-ZÁÉÍÓÚÜÑ ]+)\s+([A-ZÁÉÍÓÚÜÑ]+)\s*$'
    )

    for line in lines:
        # Limpiar espacios en blanco al inicio y final
        line = line.strip()
        
        # Saltar líneas vacías
        if not line:
            continue

        # Saltar líneas que no comienzan con un dígito (encabezados, etc.)
        if not line[0].isdigit():
            continue

        # Intentar coincidencia del patrón regex
        match = data_line_pattern.match(line)
        if match:
            # Group 2 contiene: NOMBRES Y APELLIDOS (sin provincia ni género)
            full_name_part = match.group(2).strip()
            
            # Dividir en palabras individuales para procesamiento
            parts = full_name_part.split()
            
            # Variables para almacenar resultado
            nombre = ""
            apellido = ""
            num_words = len(parts)

            # Lógica heurística: últimas palabras son apellidos, resto es nombre
            if num_words >= 3:
                # 3 o más palabras: últimas 2 son apellidos
                nombre = " ".join(parts[:-2])
                apellido = " ".join(parts[-2:])
            elif num_words == 2:
                # Exactamente 2 palabras: primera es nombre, segunda es apellido
                nombre = parts[0]
                apellido = parts[1]
            elif num_words == 1:
                # Solo 1 palabra: se asume que es nombre, apellido vacío
                nombre = parts[0]
                apellido = ""

            # Solo añadir si hay al menos nombre o apellido (no líneas corruptas)
            if nombre or apellido:
                names_found.append({
                    "name": nombre.strip(),
                    "surname": apellido.strip()
                })
    
    return names_found

def save_to_json(data, json_path):
    """
    Exporta una lista de registros a formato JSON con codificación UTF-8.
    
    Guarda los datos con formato legible (indentación de 4 espacios) para
    facilitar debugging e inspección manual del archivo.
    
    Args:
        data (list[dict]): Lista de diccionarios con estructura:
                          [{"name": "...", "surname": "..."}, ...]
        json_path (str | Path): Ruta donde guardar el archivo JSON.
                               Se crea si no existe, se sobrescribe si existe.
    
    Exporta una lista de registros a formato CSV con codificación UTF-8.
    
    Crea un archivo CSV con encabezados basados en las claves del primer
    diccionario de la lista. Utiliza DictWriter para manejar automáticamente
    la estructura de columnas.
    
    Args:
        data (list[dict]): Lista de diccionarios con estructura:
                          [{"name": "...", "surname": "..."}, ...]
                          Debe contener al menos un elemento.
        csv_path (str | Path): Ruta donde guardar el archivo CSV.
                              Se crea si no existe, se sobrescribe si existe.
    
    Returns:
        None
    
    Side Effects:
        - Crea o sobrescribe el archivo en csv_path
        - Imprime mensaje de estado (éxito, lista vacía, o error)
    
    Métodos internos utilizados:
        - open(path, 'w', newline='', encoding='utf-8'):
            * newline='': Asegura manejo correcto de saltos de línea en Windows
            * encoding='utf-8': Soporta caracteres acentuados
        - csv.DictWriter(file, fieldnames):
            * fieldnames: Nombres de columnas basadas en claves de diccionarios
        - writer.writeheader(): Escribe la fila de encabezados
        - writer.writerows(data): Escribe todas las filas de datos
    
    Flujo de validación:
        1. Verifica que data no esté vacía
        2. Extrae fieldnames del primer diccionario
        3. Intenta escribir archivo
        4. Captura y reporta excepciones
    
    Excepciones manejadas:
        - ValueError: data está vacía
        - FileNotFoundError: Ruta inválida
        - IOError: Error de permisos o escritura
        - Exception: Otros errores durante la escritura
    
    Ejemplo:
        >>> data = [
        ...     {"name": "JUAN", "surname": "PÉREZ"},
        ...     {"name": "MARÍA", "surname": "GARCÍA"}
        ... ]
        >>> save_to_csv(data, "nombres.csv")
        ✓ Datos guardados exitosamente en nombres.csv
        
    Resultado CSV:
        name,surname
        JUAN,PÉREZ
        """
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✓ Datos guardados exitosamente en {json_path}")
    except FileNotFoundError:
        print(f"✗ Error: El directorio no existe para {json_path}")
    except IOError as e:
        print(f"✗ Error de I/O al guardar JSON: {e}")
    except Exception as e:
        print(f"✗ Error al guardar en JSON: {e}")

def main() -> None:
    """
    Función principal de orquestación del proceso de extracción.
    
    Ejecuta el pipeline completo:
    1. Extrae texto del PDF
    2. Parsea nombres y apellidos
    3. Exporta resultados a JSON y CSV
    
    El flujo es lineal y cada paso valida su entrada para asegurar
    que los datos sean válidos antes de continuar.
    
    Archivos de entrada (esperados):
        - Listado-CCS-CNE.pdf: PDF con listado de nombres
    
    Archivos de salida (generados):
        - extracted_names.json: Datos en formato JSON
        - extracted_names.csv: Datos en formato CSV
    
    Retorna:
        None (lado efectos: crea archivos de salida)
    
    Flujo de ejecución:
        1. Extrae texto PDF → print de progreso o error
        2. Si OK: parsea nombres → print de cantidad encontrada
        3. Si OK: exporta a JSON → print de éxito/error
        4. Si OK: exporta a CSV → print de éxito/error
        5. En cualquier paso, si falla: imprime error y termina
    
    Ejemplo:
        >>> python extracted_names_pdf.py
        Extrayendo texto del PDF...
        Texto extraído del PDF. Intentando extraer nombres...
        Se encontraron 987 posibles nombres.
        ✓ Datos guardados exitosamente en extracted_names.json
        ✓ Datos guardados exitosamente en extracted_names.csv
    """
    # Obtener rutas relativas al directorio del script
    script_dir = Path(__file__).parent
    pdf_file_path = script_dir / "Listado-CCS-CNE.pdf"
    json_output_path = script_dir / "extracted_names.json"
    csv_output_path = script_dir / "extracted_names.csv"
    
    print("\n" + "="*60)
    print("EXTRACTOR DE NOMBRES DESDE PDF - Registro Civil Ecuador")
    print("="*60 + "\n")
    
    # Paso 1: Extraer texto del PDF
    print(f"1️⃣  Extrayendo texto de: {pdf_file_path.name}")
    print("-" * 60)
    pdf_text = extract_text_from_pdf(pdf_file_path)

    if pdf_text:
        print(f"✓ Extracción completada ({len(pdf_text)} caracteres)\n")
        
        # Paso 2: Extraer nombres y apellidos
        print("2️⃣  Parseando nombres y apellidos...")
        print("-" * 60)
        extracted_people = extract_names_and_surnames(pdf_text)

        if extracted_people:
            print(f"✓ Se encontraron {len(extracted_people)} registros\n")
            
            # Paso 3: Guardar en JSON
            print("3️⃣  Guardando resultados...")
            print("-" * 60)
            save_to_json(extracted_people, json_output_path)
            
            # Paso 4: Guardar en CSV
            save_to_csv(extracted_people, csv_output_path)
            
            print("\n" + "="*60)
            print("✅ PROCESO COMPLETADO EXITOSAMENTE")
            print("="*60 + "\n")
        else:
            print("✗ Error: No se encontraron o extrajeron nombres válidos.")
    else:
        print("✗ Error: No se pudo extraer texto del PDF.")
        print(f"   Por favor verifica: {pdf_file_path}")

def save_to_csv(data, csv_path):
    """
    Guarda una lista de diccionarios en un archivo CSV.
    """
    if not data:
        print("No hay datos para guardar en CSV.")
        return

    try:
        fieldnames = data[0].keys()
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Datos guardados exitosamente en {csv_path}")
    except Exception as e:
        print(f"Error al guardar en CSV: {e}")
   
   
   
   
    """
    main(
        print(f"✗ tFoundError: Ruta inválida
        - IOError: Error de permisos o escritura
        - TypeError: Datos no serializables a JSON
    
    Ejemplo:
        >>> data = [{"name": "JUAN", "surname": "PÉREZ"}]
        >>> save_to_json(data, "nombres.json")
        Datos guardados exitosamente en nombres.json
    """
# --- Ejecución principal ---
if __name__ == "__main__":
    pdf_file_path = "Listado-CCS-CNE.pdf" 
    json_output_path = "extracted_names.json"
    csv_output_path = "extracted_names.csv"

    # 1. Extraer texto del PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    if pdf_text:
        print("Texto extraído del PDF. Intentando extraer nombres...")
        # 2. Extraer nombres y apellidos
        extracted_people = extract_names_and_surnames(pdf_text)

        if extracted_people:
            print(f"Se encontraron {len(extracted_people)} posibles nombres.")
            # 3. Guardar en JSON
            save_to_json(extracted_people, json_output_path)
            # 4. Guardar en CSV
            save_to_csv(extracted_people, csv_output_path)
        else:
            print("No se encontraron o extrajeron nombres.")
    else:
        print("No se pudo extraer texto del PDF. Por favor, verifica la ruta del archivo y su contenido.")