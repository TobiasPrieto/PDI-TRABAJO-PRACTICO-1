# Procesamiento de Imágenes - Trabajo Práctico 1

Este repositorio contiene la solución a un trabajo práctico de Procesamiento de Imágenes, enfocado en dos problemas: la **ecualización de histograma local** para realzar detalles y la **validación automática de formularios**.

Para una explicación detallada de los algoritmos y métodos utilizados, por favor consulte el informe en PDF incluido en el repositorio.

---

## Ejercicio 1: Ecualización de Histograma Local

El objetivo es implementar un algoritmo de ecualización de histograma local para revelar detalles ocultos en zonas oscuras de una imagen. La función `ecualizacion_local` aplica el realce de contraste en ventanas móviles para optimizar cada región de forma independiente.

### Resultado
El script procesa la imagen `Imagen_con_detalles_escondidos.tif` con kernels de diferentes tamaños, mostrando cómo un kernel más pequeño realza más los detalles a costa de introducir ruido.


*Original vs. Resultados con kernels de 5x5, 15x15 y 35x35.*

---

## Ejercicio 2: Validación Automática de Formularios

Se desarrolló un sistema para segmentar, analizar y validar automáticamente los campos de formularios escaneados.

### Funcionalidades Principales
*   **Segmentación Automática:** Identifica y recorta renglones y columnas usando proyecciones de píxeles.
*   **Análisis de Contenido:** Cuenta caracteres y palabras en cada campo mediante componentes conexos.
*   **Validación por Reglas:** Verifica si los datos cumplen con criterios predefinidos (longitud, formato, etc.).
*   **Generación de Reportes:** Crea un informe visual (`OK`/`MAL`) y un archivo `resultados_formularios.csv` con el resumen de la validación.

### Resultados
El sistema procesa los formularios y genera las siguientes salidas:

**1. Reporte Visual:** Clasifica los formularios según si fueron completados correcta o incorrectamente.



**2. Resumen en CSV (`resultados_formularios.csv`):**

```csv
ID,Nombre y Apellido,Edad,Mail,Legajo,Pregunta 1,Pregunta 2,Pregunta 3,Comentarios
01,OK,OK,OK,OK,OK,OK,OK,OK
02,MAL,MAL,MAL,MAL,MAL,MAL,MAL,MAL
03,OK,OK,OK,OK,OK,OK,OK,OK
04,MAL,MAL,MAL,MAL,OK,MAL,MAL,MAL
05,OK,MAL,OK,OK,MAL,MAL,MAL,OK
```
---

## Tecnologías Utilizadas
*   Python 3
*   OpenCV
*   NumPy
*   Matplotlib

---

## Cómo Ejecutar

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/TobiasPrieto/PDI-TRABAJO-PRACTICO-1.git
    cd /PDI-TRABAJO-PRACTICO-1
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install opencv-python numpy matplotlib
    ```

3.  **Ejecutar los scripts:**
    ```bash
    python tp1_PDI_ejercicio1.py

    python tp1_PDI_ejercicio2.py
    ```
   Para cambiar los formularios a analizar, modifica la lista `ruta_formularios` al final del archivo.

---

## Autores
*   **Esteva Matias**
*   **Prieto Tobias**
