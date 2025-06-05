import os
from pathlib import Path
import pandas as pd

ALMACENAMIENTO = Path(__file__).resolve().parent / '..' / 'almacenamiento'

PRODUCTOS = ALMACENAMIENTO / 'productos.csv'
VENTAS = ALMACENAMIENTO / 'ventas.csv'
CONFIGURACION = ALMACENAMIENTO / 'configuracion.txt'


def iniciar_archivos():
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
            f.write("NIVEL_MINIMO_STOCK_GLOBAL=10\n")
            f.write("TEST=10\n")
            f.write("TEST2=10\n")
        # print(f"Archivo de configuración creado en: {CONFIGURACION}")


def leer_datos():
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


def cambiar_configuracion(clave, nuevo_valor):
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
    configuraciones_predeterminadas = {
        'NIVEL_MINIMO_STOCK': '10',
        'TEST': '100',
        'TEST2': 'False'
    }

    with open(CONFIGURACION, mode='w') as archivo:
        for clave, valor in configuraciones_predeterminadas.items():
            archivo.write(f"{clave}={valor}\n")

    return True, "Configuración restablecida a los valores predeterminados."

def resetear_datos():
    if PRODUCTOS.exists():
        PRODUCTOS.unlink()
    if VENTAS.exists():
        VENTAS.unlink()

    iniciar_archivos()

    return True, "Archivos reseteados correctamente."