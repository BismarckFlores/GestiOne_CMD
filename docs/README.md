## 🌟 **GestiOne_CMD: Sistema de Gestión para Inventario y Ventas** 🌟

### Descripción

**GestiOne_CMD** es una *aplicación* diseñada para la **automatización** del control de inventarios y ventas en pequeños negocios, como bares y cocinas. En estos contextos, la gestión manual con hojas de cálculo o registros escritos puede ser propensa a errores, pérdida de información y dificultad para generar reportes precisos. **GestiOne_CMD** proporciona una **solución práctica**, eficiente y automatizada que permite gestionar de manera sencilla el inventario, realizar ventas y generar reportes detallados.

---

### ⚠️ **Problema o Necesidad**

En muchos pequeños negocios, la gestión del inventario y las ventas se realiza de manera **manual**, lo que genera problemas como:

- ❌ **Errores humanos** en el registro de datos.
- ❌ **Dificultad** para obtener reportes confiables sobre ventas e inventario.
- ❌ Imposibilidad de tomar decisiones informadas debido a la falta de un sistema **automatizado**.

**GestiOne** soluciona estos problemas al automatizar la creación de reportes, la actualización de inventarios y las ventas.

---

### 💡 **Características**

Las funcionalidades clave de **GestiOne_CMD** incluyen:

- 🗃️ **Gestión de Inventario**: Permite agregar, editar, eliminar y actualizar productos en el inventario.
- 🛍️ **Ventas Automatizadas**: Realiza el registro de ventas y actualiza automáticamente el inventario, generando reportes con los datos relevantes.
- 🚨 **Alertas por Bajo Stock**: Muestra los productos con bajo stock para facilitar el reabastecimiento.
- 📊 **Reportes Detallados**: Genera reportes de ventas diarias, semanales y mensuales, permitiendo un análisis detallado de los productos más vendidos.

---

### 📝 **Requerimientos Funcionales**

A continuación, se presentan los principales requerimientos funcionales del sistema:

1. **RF-01**: Inicialización de archivos del sistema (productos, ventas, configuración).
2. **RF-02**: Agregar productos al inventario con validaciones de ID único, nombre, precio y cantidad.
3. **RF-07**: Registrar tickets de venta y actualizar el inventario automáticamente.
4. **RF-09**: Generar reportes de ventas por período (diario, semanal, mensual).

[Más detalles en los Requerimientos Funcionales](https://docs.google.com/spreadsheets/d/16aMvolZCGdlaI4Yilng2JjtxPprdYdvrzQ3ZGAainnQ/edit?usp=sharing)

---

### 🎯 **Objetivo del Proyecto**

El objetivo de **GestiOne** es proporcionar una herramienta sencilla, eficaz y automatizada para la gestión de inventarios y ventas en pequeños negocios, lo cual permitirá a los propietarios tener un control más preciso y eficiente de su negocio, mejorando la toma de decisiones y reduciendo los errores humanos en los registros.

---

### 👥 **Integrantes**

| **Nombre**            | **Rol**                                 |
|-----------------------|-----------------------------------------|
| **Bismarck Flores**   | Líder del grupo y programador principal |
| **Andrés Mejía**      | Programador de menú y lógica            |
| **Caleb Tardencilla** | Programador y tester                    |
| **Rommel Muñoz**      | Programador de entradas/salidas y datos |

---
### 📦 **Instalación y Uso**
```bash
git clone <repository>
cd <repository name>
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requerimientos.txt
```
```bash
python app.py
```