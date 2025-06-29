# ✨🌟✨ **GestiOne_CMD: Documentación Técnica Detallada** ✨🌟✨

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/CLI-Consola-informational">
</p>

---

## 🏢 Introducción

**GestiOne_CMD** es una aplicación de consola para la gestión de inventario y ventas, orientada a pequeños negocios.
Este documento complementa el [README.md](../docs/README.md) y describe en profundidad la arquitectura, lógica interna, decisiones de diseño y detalles técnicos de los módulos principales.

---

## 🏗️ Arquitectura General

| Característica   | Descripción                                                                  |
|------------------|------------------------------------------------------------------------------|
| **Modularidad**  | Módulos independientes para fácil mantenimiento y escalabilidad.             |
| **Persistencia** | Archivos binarios (pickle) para productos, ventas, usuarios y configuración. |
| **Interfaz**     | 100% consola, con menús, banners y validaciones amigables.                   |

---

## 🧩 Módulos Clave

| Módulo                     | Propósito / Lógica Principal                                                                |
|----------------------------|---------------------------------------------------------------------------------------------|
| **app.py**                 | Punto de entrada. Login, ciclo de vida, delega a menús principales.                         |
| **main/utilidades.py**     | Utilidades para interacción: limpiar consola, banners, menús, validaciones, mensajes.       |
| **dao/gestor_datos.py**    | Acceso y manipulación de datos persistentes. CRUD, filtrado, reportes, hash de contraseñas. |
| **main/menu_principal.py** | Menú principal y configuración. Navegación, gestión de usuarios, reseteo de datos.          |
| **main/menu_inv.py**       | Gestión de inventario: ver, agregar, editar, restock, eliminar, alertas de stock.           |
| **main/menu_ventas.py**    | Gestión de ventas y reportes: registrar, filtrar, exportar, top productos.                  |
| **models/classes.py**      | Definición de entidades principales (Producto, ItemVenta, Venta) con dataclasses.           |

---

## 🛠️ Buenas Prácticas y Decisiones de Diseño

- **Validaciones exhaustivas** en entradas de usuario para evitar errores y datos corruptos.
- **Separación de responsabilidades**: cada módulo tiene un propósito claro.
- **Mensajes y menús centralizados** para facilitar la traducción o personalización.
- **Soporte para múltiples usuarios y roles (admin/usuario regular)**.
- **Exportación de reportes** en formato CSV para interoperabilidad.

---

## 🔄 Flujo Interno de una Venta

| Paso | Descripción                                                  |
|------|--------------------------------------------------------------|
| 1    | Usuario accede a "Agregar Venta".                            |
| 2    | Se muestra inventario y se seleccionan productos/cantidades. |
| 3    | Se valida stock y se actualiza inventario.                   |
| 4    | Se crea un objeto Venta y se almacena.                       |
| 5    | Se actualizan los archivos binarios.                         |
| 6    | Se puede generar y exportar un reporte de ventas.            |

---

## 💻 Ejemplos de Uso

**Ejemplo 1: Agregar un producto**
```bash
$ python app.py
# Menú principal > Inventario > Agregar Producto
Ingrese el ID del producto: 101
Nombre del producto: Coca-Cola
Precio del producto: 25
Stock inicial: 50
Stock mínimo (opcional, deje en blanco para usar el global):
Producto Coca-Cola agregado correctamente con ID 101.
```

**Ejemplo 2: Registrar una venta**
```bash
# Menú principal > Ventas > Agregar Venta
Ingrese el ID del producto (0 para terminar): 101
Producto seleccionado: Coca-Cola (ID: 101, Stock: 50)
Ingrese la cantidad a vender: 3
Ingrese el ID del producto (0 para terminar): 0
Venta registrada con ID 1 y total 75 C$.
```

**Ejemplo 3: Generar y exportar reporte de ventas**
```bash
# Menú principal > Ventas > Reporte de ventas > Día
Ingrese la fecha (DD-MM-YYYY): 29-06-2025
Total de tickets: 1
Total de ventas: 75 C$
¿Desea exportar el reporte a un archivo? (s/n): s
Reporte exportado como reporte_ventas_Dia_29_06_2025.csv a storage.
```

---

## ⚠️ Consideraciones y Limitaciones

- Pensado para volúmenes pequeños/medios de datos.
- No es multiusuario concurrente (no soporta acceso simultáneo desde varias terminales).
- Seguridad básica de contraseñas (hash SHA-256, sin sal).
- No hay control de acceso por sesión, solo por rol.

---

## 🚀 Sugerencias para Futuras Versiones

| Mejora                                   | Descripción breve                          |
|------------------------------------------|--------------------------------------------|
| Base de datos relacional o NoSQL         | Persistencia más robusta y escalable.      |
| Interfaz gráfica (GUI) o web             | Mejor experiencia de usuario.              |
| Seguridad avanzada de contraseñas        | Hashing con sal, autenticación por tokens. |
| Soporte multiusuario concurrente         | Acceso simultáneo desde varias terminales. |
| Integración con facturación/contabilidad | Exportar datos a sistemas externos.        |

---

**Ver [README.md](../docs/README.md) para más detalles de instalación y créditos.**  
**Para detalles de cada función, consulta los docstrings en el código fuente.**
