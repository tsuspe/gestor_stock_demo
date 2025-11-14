# Gestor de Stock y Previsión — UNIFORMIDAD (DEMO)

Aplicación web hecha con **Python + Streamlit** para gestionar el stock de prendas de uniformidad, previsiones de consumo y órdenes de fabricación / corte.

Esta versión es una **demo pública** con datos inventados (`data_example/`), pensada para mostrar:

- Lógica de negocio real aplicada a inventario.
- Organización del código en modo producción.
- Flujo completo: **inventario → previsión → importaciones → exportaciones Excel**.

> ⚠️ Esta demo **no contiene datos reales de empresa**.  
> Todos los JSON y rutas son internos al proyecto.

---

## 🧩 Funcionalidades principales

La app se organiza en varias pestañas (tabs):

### 1. Stock

- Visualización del **stock actual por modelo y talla**.
- Filtros por:
  - Modelo
  - Familia / tipo de prenda
  - Color
  - Cliente / colección (según el dataset).
- Semáforo de stock:
  - 🔴 Cantidades ≤ 0
  - 🟠 Cantidades entre 1 y 10
  - 🟡 Cantidades entre 11 y 25
- Totales por modelo y totales generales.

### 2. Movimientos

- Registro de **entradas y salidas de stock**.
- Cálculo automático de **stock resultante**.
- Posibilidad de **simular** movimientos antes de aplicarlos.

### 3. Previsión

- Cálculo de **stock estimado** en función de:
  - Stock actual.
  - Pedidos pendientes.
  - Órdenes de fabricación / corte.
- Vista de **stock previsto por modelo/talla** con el mismo semáforo de colores.
- Detección rápida de **roturas de stock futuras**.

### 4. Auditoría

- Listados para revisar:
  - Inconsistencias en datos.
  - Tallas mal formateadas.
  - Modelos huérfanos, etc.
- Herramientas para **corregir y limpiar datos**.

### 5. Catálogo & Maestros

- Catálogo de modelos (descripción, familia, color...).
- Listados de:
  - Clientes.
  - Talleres.
- Pensado para mantener un **maestro unificado de datos**.

### 6. Importaciones (Excel)

- Importar **albaranes servidos** (salidas) desde Excel.
- Importar **pedidos pendientes** desde Excel.
- Opciones avanzadas:
  - Diferentes modos de tratar líneas duplicadas.
  - Fila de inicio configurable (para Excels con cabeceras largas).
  - Modo simulación (no escribe, solo muestra resumen).

En la demo, las rutas fijas apuntan a archivos dentro del propio proyecto  
(por ejemplo: `data_example/ALBARANES_SERVIDOS_DEMO.xlsx`).

### 7. Backups

- Sistema de backup de los JSON principales:
  - `datos_almacen`
  - `prevision`
  - `clientes`
  - `talleres`
- Los backups se guardan con **timestamp** para facilitar la restauración.

### 8. Exportar CSV / Excel

- Exportación completa a CSV para:
  - Stock actual.
  - Stock estimado.
  - Pedidos pendientes.
  - Órdenes de fabricación.
  - Órdenes de corte sugeridas.
- Generación automática de **Excel listos para imprimir** (`IMPRIMIR_XX_...`):
  - Cabeceras y totales en **amarillo intenso + negrita**.
  - Semáforo por stock (rojo / naranja / amarillo).
  - Pedidos pendientes coloreados por mes:
    - Verde → pasado.
    - Blanco → mes en curso.
    - Rojo → meses futuros (con gradiente de intensidad).
  - Agrupación visual por:
    - **Fecha** (en órdenes de fabricación).
    - **Modelo** (en órdenes de corte).
  - Bordes finos en todas las celdas, pensado para impresoras de taller.

---

## 🧠 Cómo está implementado por dentro

La estructura está pensada como si fuera una app “real de empresa”, separando UI de lógica de negocio.

### Capa de dominio: `GestorStock` (`src/gestor_oop.py`)

- Clase principal `GestorStock` que encapsula toda la lógica:
  - Carga y guarda los JSON:
    - Inventario (`datos_almacen`)
    - Previsión (`prevision`)
    - Clientes
    - Talleres
  - Expone métodos para:
    - Consultar stock actual y estimado.
    - Registrar entradas / salidas.
    - Importar albaranes servidos desde Excel.
    - Importar pedidos pendientes desde Excel.
    - Generar estructuras para informes (stock, pedidos, órdenes, etc.).
- Uso de **dataclasses** y tipos (`typing`) para dejar más clara la estructura interna.
- Toda la lógica de negocio vive aquí: Streamlit solo llama a métodos de `GestorStock`
  y pinta el resultado.

### Capa de datos: JSON + helpers

- Los datos se guardan en JSON, con una estructura estable:
  - Inventario indexado por `MODELO → TALLA → STOCK`.
  - Previsión con:
    - Bloque `stock` (stock previsto por modelo/talla).
    - Bloque `pedidos` (lista de pedidos con fecha, cliente, cantidad, etc.).
- Hay funciones auxiliares para:
  - Normalizar modelos (`norm_codigo`).
  - Normalizar tallas (`norm_talla`).
  - Parsear fechas (`parse_fecha_excel`).

### Capa de presentación: `Streamlit` (`src/st_app.py`)

- `st_app.py` define la interfaz por pestañas:
  - Cada tab llama a uno o varios métodos de `GestorStock`.
  - Se usan `pandas.DataFrame` + estilos para:
    - Semáforos de color.
    - Agrupaciones visuales.
- La app:
  - Mantiene una instancia de `GestorStock` en `st.session_state`.
  - Permite cambiar las rutas de los JSON desde la barra lateral.
  - Gestiona exportaciones a CSV y Excel con formato a través de `pandas + openpyxl`.

### Exportación a Excel con formato

- La generación de los Excel “IMPRIMIR*XX*...” se hace con:
  - `pandas.to_excel()` para volcar el DataFrame.
  - `openpyxl` para:
    - Pintar cabeceras y totales en amarillo.
    - Aplicar semáforo de stock.
    - Aplicar degradado de colores por mes (pasado/futuro).
    - Colorear por fecha o por modelo según el informe.
    - Añadir bordes finos a todas las celdas.

Esta separación permite que:

- La lógica de negocio se pueda testear o reutilizar sin Streamlit.
- La interfaz se pueda reemplazar (por ejemplo, por una API o un frontend React) sin tocar el core.

---

## 🏗️ Arquitectura y tecnologías

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Lógica de negocio**: Python, Programación Orientada a Objetos (`GestorStock` en `gestor_oop.py`).
- **Datos**: ficheros JSON.
- **Exportación**:
  - CSV con `pandas`.
  - Excel con `pandas` + `openpyxl`.
- **Demo data**: carpeta `data_example/` con datasets inventados.

---

## 📂 Estructura del proyecto

```text
gestor_stock_demo/
├─ src/
│  ├─ st_app.py           # Aplicación Streamlit (interfaz)
│  ├─ gestor_oop.py       # Lógica de negocio y gestión de stock
│  └─ __init__.py         # Marca el package (opcional para imports)
│
├─ data_example/
│  ├─ datos_almacen_example.json   # Inventario de ejemplo
│  ├─ prevision_example.json       # Previsión + pedidos de ejemplo
│  ├─ clientes_example.json        # Clientes de ejemplo
│  └─ talleres_example.json        # Talleres de ejemplo
│
├─ README.md
├─ requirements.txt
└─ .gitignore


🚀 Puesta en marcha

1. Clonar el repositorio
   git clone https://github.com/tsuspe/gestor_stock_demo.git
   cd gestor_stock_demo

2. Crear entorno virtual (recomendado)
    python -m venv .venv

    # Linux / macOS
    source .venv/bin/activate

    # Windows (PowerShell)
    # .venv\Scripts\Activate.ps1


3. Instalar dependencias
   pip install -r requirements.txt

4. Ejecutar la app
   streamlit run src/st_app.py

Streamlit mostrará algo como:

Local URL: http://localhost:8501

Network URL: http://<tu-ip-local>:8501

Abre la URL en tu navegador y ya puedes jugar con la demo.

⚙️ Configuración y datos

Por defecto la app apunta a los JSON de data_example/, pero en la barra lateral puedes cambiar las rutas:

Inventario JSON

Previsión JSON

Talleres JSON

Clientes JSON

Esto permite usar el mismo código con datasets propios en un entorno real.

Las exportaciones (CSV y Excel) se guardan en una carpeta interna de demo, normalmente:

    src/EXPORTAR_CSV_DEMO/

📌 Notas sobre la versión DEMO

No incluye datos reales de empresa.

No usa rutas de red ni unidades mapeadas (Z:\, Y:\, etc.).

Está pensada para:

Enseñar código y estructura.

Servir como base para otros proyectos de gestión de stock.

Poder adaptarse fácilmente a otros contextos (retail, almacén, etc.).

🧭 Posibles mejoras futuras

Autenticación básica (usuarios/roles).

Exportación directa a PDF.

API REST para integrar con otros sistemas.

Test unitarios sobre GestorStock.

Dockerfile + despliegue en servidor.

✍️ Autor

Desarrollado por Aitor Susperregui Zapata (@elvasco.x)
Tatuador, desarrollador full stack en formación y enfermo del automatismo creativo 🖤
```
