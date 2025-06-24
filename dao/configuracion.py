import pickle as pkl
from pathlib import Path
from typing import Literal
from pruevas.GestiOne_v2_2.models.classes import *


class Configuracion:
    def __init__(self):
        self.STORAGE_PATH = Path(__file__).resolve().parent.parent / "storage"
        self.iniciar_archivos()

    def iniciar_archivos(self):
        self.STORAGE_PATH.mkdir(exist_ok=True)
        self.productos_file = self.STORAGE_PATH / "productos.bin"
        self.ventas_file = self.STORAGE_PATH / "ventas.bin"
        self.config_file = self.STORAGE_PATH / "configuracion.bin"

        if not self.productos_file.exists():
            with open(self.productos_file, 'wb') as f:
                pkl.dump([], f)

        if not self.ventas_file.exists():
            with open(self.ventas_file, 'wb') as f:
                pkl.dump([], f)

        if not self.config_file.exists():
            with open(self.config_file, 'wb') as f:
                config_data = {
                    "STOCK_MIN_GLOBAL": 200,
                    "NOMBRE_NEGOCIO": "GestiOne",
                    "MONEDA": "C$"
                }
                pkl.dump(config_data, f)


    # Productos
    def leer_productos(self):
        with open(self.productos_file, 'rb') as f:
            productos = pkl.load(f)
        header = ["ID", "Nombre", "Precio", "Stock", "Stock Mínimo", "Categoría", "Descripción"]
        return header, [p.to_list() for p in productos]

    def existe_id_producto(self, id_buscar):
        with open(self.productos_file, 'rb') as f:
            productos = pkl.load(f)
        return any(p.id == id_buscar for p in productos)

    def guardar_producto(self, producto: Producto):
        productos = []
        if self.productos_file.exists():
            with open(self.productos_file, 'rb') as f:
                productos = pkl.load(f)
        productos.append(producto)
        with open(self.productos_file, 'wb') as f:
            pkl.dump(productos, f)


    # Ventas
    def leer_ventas(self):
        with open(self.ventas_file, 'rb') as f:
            ventas = pkl.load(f)
        header = ["ID Venta", "Fecha", "ID Producto","Producto",
                  "Cantidad", "Precio Unitario","Subtotal Producto"]
        rows = []
        for venta in ventas:
            rows.extend(venta.to_table())
        return header, rows

    def guardar_venta(self, venta: Venta):
        ventas = []
        if self.ventas_file.exists():
            with open(self.ventas_file, 'rb') as f:
                ventas = pkl.load(f)
        ventas.append(venta)
        with open(self.ventas_file, 'wb') as f:
            pkl.dump(ventas, f)


    # Configuración
    def leer_config(self):
        with open(self.config_file, 'rb') as f:
            config = pkl.load(f)
        return config

    def actializar_config(self, config_data: dict):
        with open(self.config_file, 'wb') as f:
            pkl.dump(config_data, f)
        return True


    def borrar_datos(self, tipo: Literal["Todo", "Datos", "Configuración"] = 'Todo'):
        if tipo == 'Todo':
            with open(self.productos_file, 'wb') as f:
                pkl.dump([], f)
            with open(self.ventas_file, 'wb') as f:
                pkl.dump([], f)
            with open(self.config_file, 'wb') as f:
                config_data = {
                    "STOCK_MIN_GLOBAL": 200,
                    "NOMBRE_NEGOCIO": "GestiOne",
                    "MONEDA": "C$"
                }
                pkl.dump(config_data, f)

        elif tipo == 'Datos':
            with open(self.productos_file, 'wb') as f:
                pkl.dump([], f)
            with open(self.ventas_file, 'wb') as f:
                pkl.dump([], f)

        elif tipo == 'Configuración':
            with open(self.config_file, 'wb') as f:
                config_data = {
                    "STOCK_MIN_GLOBAL": 200,
                    "NOMBRE_NEGOCIO": "GestiOne",
                    "MONEDA": "C$"
                }
                pkl.dump(config_data, f)

        else:
            raise ValueError("Tipo de datos no reconocido.")