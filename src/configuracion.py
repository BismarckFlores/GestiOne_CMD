import os
from pathlib import Path
import pandas as pd

ALMACENAMIENTO = Path(__file__).resolve().parent / '..' / 'almacenamiento'

PRODUCTOS = ALMACENAMIENTO / 'productos.csv'
VENTAS = ALMACENAMIENTO / 'ventas.csv'
CONFIGURACION = ALMACENAMIENTO / 'configuracion.txt'


def iniciar_archivos():
    """
        Crea el directorio 'almacenamiento' y los archivos CSV/TXT de datos si no existen.

        Inicializa 'productos.csv' y 'ventas.csv' con sus encabezados, y
        'configuracion.txt' con valores predeterminados.

        Depende de las constantes globales **ALMACENAMIENTO**, **PRODUCTOS**, **VENTAS**, **CONFIGURACION**.
    """
    if not ALMACENAMIENTO.exists():
        ALMACENAMIENTO.mkdir(parents=True)
        # print(f"Directorio 'almacenamiento' creado en: {ALMACENAMIENTO}")

    if not PRODUCTOS.exists():
        df = pd.DataFrame(columns=["ID", "Nombre", "Precio", "Cantidad"])
        df.to_csv(PRODUCTOS, index=False)
        # print(f"Archivo de productos creado en: {PRODUCTOS}")

    if not VENTAS.exists():
        df = pd.DataFrame(columns=["ID Venta", "ID Producto", "Nombre Producto", "Cantidad Vendida", "Total", "Fecha"])
        df.to_csv(VENTAS, index=False)
        # print(f"Archivo de ventas creado en: {VENTAS}")

    if not CONFIGURACION.exists():
        with open(CONFIGURACION, 'w') as f:
            f.write("NIVEL_MINIMO_STOCK_GLOBAL=100\n")
            f.write("NOMBRE_NEGOCIO=Tienda GestiOne\n")
            f.write("TIPO_MONEDA=C$\n")
        # print(f"Archivo de configuración creado en: {CONFIGURACION}")


def leer_datos():
    """
        Lee datos de productos, ventas (CSV) y configuraciones (TXT).

        :returns: tuple: (**DataFrame** de productos, **DataFrame** de ventas, **dict** de configuraciones).
        :raises FileNotFoundError: Si **PRODUCTOS** o **VENTAS** no se encuentran.
    """
    df_productos = pd.read_csv(PRODUCTOS)
    df_ventas = pd.read_csv(VENTAS)

    configuraciones = {}
    if CONFIGURACION.exists():
        with open(CONFIGURACION, mode='r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if '=' in linea:
                    clave, valor = linea.split('=', 1)
                    configuraciones[clave] = valor

    return df_productos, df_ventas, configuraciones


def cambiar_configuracion(indice: int, nuevo_valor: int | str):
    """
        Actualiza el valor de una clave en el archivo de configuración.

        Reescribe el archivo con los valores actualizados.

        :param indice: int: Indice para la clave a modificar.
        :param nuevo_valor: int | str: Nuevo valor de la clave, este puede ser entero o cadena.
        :returns: tuple: (**bool**, **str**) indicando éxito y mensaje.
    """
    claves = ['NIVEL_MINIMO_STOCK_GLOBAL', 'NOMBRE_NEGOCIO', 'TIPO_MONEDA']
    clave = claves[indice - 1]
    _, _, configuraciones = leer_datos()

    if clave in configuraciones:
        configuraciones[clave] = nuevo_valor
    else:
        return False, "Clave no encontrada en la configuración."

    with open(CONFIGURACION, 'w') as archivo:
        for clave, valor in configuraciones.items():
            archivo.write(f"{clave}={valor}\n")

    return True, "Valor actualizado correctamente."

def resetear_configuracion():
    """
        Elimina y recrea el archivo **CONFIGURACION**.

        Lo restablece a un estado inicial con los valores predeterminados.
        Los archivos de datos (**PRODUCTOS**, **VENTAS**) no se ven afectados.

        :returns: tuple: (**bool**, **str**) indicando éxito y mensaje.
    """
    if CONFIGURACION.exists():
        CONFIGURACION.unlink()

    iniciar_archivos()
    return True, "Configuración fue restablecida."

def resetear_datos():
    """
        Elimina y recrea los archivos de datos (**PRODUCTOS**, **VENTAS**).

        Los restablece a un estado inicial con solo sus encabezados.
        El archivo de configuración no se ve afectado.

        :returns: tuple: (**bool**, **str**) indicando éxito y mensaje.
    """
    if PRODUCTOS.exists():
        PRODUCTOS.unlink()
    if VENTAS.exists():
        VENTAS.unlink()

    iniciar_archivos()
    return True, "Archivos reseteados correctamente."