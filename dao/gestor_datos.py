import pickle as pkl
import hashlib as hl
from collections import defaultdict
from typing import Literal
from models.classes import *


class GestorDatos:
    def __init__(self):
        from pathlib import Path
        self.STORAGE_PATH = Path(__file__).resolve().parent.parent / "storage"
        self.iniciar_archivos()

    def iniciar_archivos(self):
        self.STORAGE_PATH.mkdir(exist_ok=True)
        self.data_file = self.STORAGE_PATH / "almacenamiento.bin"

        if not self.data_file.exists():
            data = {
                "productos": [],
                "ventas": [],
                "usuarios": [
                    {"username": "Admin", "password": self.hash_password('Admin123!'), "is_admin": True},
                    {"username": "User", "password": self.hash_password('User123!'), "is_admin": False}
                ],
                "config": {
                    "STOCK_MIN_GLOBAL": 200,
                    "PAGE_SIZE": 5,
                    "NOMBRE_NEGOCIO": "GestiOne",
                    "MONEDA": "C$",
                }
            }
            with open(self.data_file, 'wb') as f:
                pkl.dump(data, f)


    # Acceso a los datos
    def leer_datos(self) -> dict:
        with open(self.data_file, 'rb') as f:
            return pkl.load(f)

    def guardar_datos(self, datos: dict):
        with open(self.data_file, 'wb') as f:
            pkl.dump(datos, f)


    # Productos
    def leer_productos(self):
        productos = self.leer_datos()["productos"]
        productos.sort(key=lambda p: p.id)
        header = ["ID", "Nombre", f"Precio ({self.leer_config()["MONEDA"]})", "Stock", "Stock Mínimo"]
        return header, [p.to_list() for p in productos]

    def existe_id_producto(self, id_buscar):
        productos = self.leer_datos()["productos"]
        return any(p.id == id_buscar for p in productos)

    def buscar_producto(self, id_buscar: int) -> Producto | None:
        productos = self.leer_datos()["productos"]
        for producto in productos:
            if producto.id == id_buscar:
                return producto
        return None

    def actualizar_producto(self, producto: Producto):
        data = self.leer_datos()
        for i, p in enumerate(data["productos"]):
            if p.id == producto.id:
                data["productos"][i] = producto
                break
        self.guardar_datos(data)

    def guardar_producto(self, producto: Producto):
        data = self.leer_datos()
        data["productos"].append(producto)
        self.guardar_datos(data)

    def eliminar_producto(self, id_producto: int):
        data = self.leer_datos()
        data["productos"] = [p for p in data["productos"] if p.id != id_producto]
        self.guardar_datos(data)

    def guardar_productos(self, productos: list[Producto]):
        data = self.leer_datos()
        data["productos"] = productos
        self.guardar_datos(data)


    # Ventas
    def leer_ventas(self) -> tuple[list[str], list[Venta]]:
        ventas = self.leer_datos()["ventas"]
        header = ["ID Venta", "Fecha", "ID Producto","Producto",
                  "Cantidad", f"Precio Unitario ({self.leer_config()["MONEDA"]})",
                  f"Subtotal Producto ({self.leer_config()["MONEDA"]})"]
        return header, ventas

    def filtrar_ventas_por_fecha(self, fecha, tipo: Literal["dia", "mes", "anio"]):
        from datetime import datetime as dt
        ventas = self.leer_datos()["ventas"]
        resultado = []
        for venta in ventas:
            fecha_venta: dt = venta.fecha
            if tipo == 'dia' and fecha_venta.strftime('%d-%m-%Y') == fecha:
                resultado.append(venta)
            elif tipo == 'mes' and fecha_venta.strftime('%m-%Y') == fecha:
                resultado.append(venta)
            elif tipo == 'anio' and fecha_venta.strftime('%Y') == fecha:
                resultado.append(venta)
        return resultado

    def resumen_ventas(self, ventas):
        total_ticket = len(ventas)
        productos_vendidos = defaultdict(int)
        total_ventas = 0.0
        for venta in ventas:
            total_ventas += venta.total()
            for item in venta.items:
                productos_vendidos[(item.producto_id, item.nombre)] += item.cantidad
        productos_vendidos_lista = [
            (id_producto, nombre, cantidad) for (id_producto, nombre), cantidad in productos_vendidos.items()
        ]
        return total_ticket, productos_vendidos_lista, total_ventas

    def guardar_venta(self, venta: Venta):
        data = self.leer_datos()
        data["ventas"].append(venta)
        self.guardar_datos(data)


    # Configuración
    def leer_config(self) -> dict:
        data = self.leer_datos()
        return data["config"]

    def actualizar_config(self, config_data: dict):
        data = self.leer_datos()
        data["config"] = config_data
        self.guardar_datos(data)


    # Usuarios
    def listar_usuarios(self) -> list[dict[str, str]]:
        return [user["username"] for user in self.leer_datos()["usuarios"]]

    @staticmethod
    def hash_password(password: str):
        return hl.sha256(password.encode("utf-8")).hexdigest()

    def verificar_usuario(self, username: str, password: str) -> bool:
        users = self.leer_datos()["usuarios"]
        password_hash = self.hash_password(password)
        return any(user["username"] == username and user["password"] == password_hash for user in users)

    def is_admin(self, username: str):
        users = self.leer_datos()["usuarios"]
        return any(user["username"] == username and user['is_admin'] for user in users)

    def ver_usuario(self, username: str):
        users = self.leer_datos()["usuarios"]
        for user in users:
            if user["username"] == username:
                return {
                    "username": user["username"],
                    "is_admin": user["is_admin"]
                }
        return None

    def agregar_usuario(self, username: str, password: str, current_user: str, is_admin: bool = False):
        data = self.leer_datos()
        users = data["usuarios"]
        if not self.is_admin(current_user):
            return False
        if any(user["username"] == username for user in users):
            return False
        users.append({'username': username, 'password': self.hash_password(password), 'is_admin': is_admin})
        self.guardar_datos(data)
        return True

    def cambiar_contrasenia(self, current_user: str, old_password: str, new_password: str):
        data = self.leer_datos()
        users = data["usuarios"]
        old_password_hash = self.hash_password(old_password)
        new_password_hash = self.hash_password(new_password)

        for user in users:
            if user["username"] == current_user and user["password"] == old_password_hash:
                user["password"] = new_password_hash
                self.guardar_datos(data)
                return True
        return False

    def eliminar_usuario(self, username: str, current_user: str):
        data = self.leer_datos()
        users = data["usuarios"]
        if not self.is_admin(current_user):
            return False
        data["usuarios"] = [user for user in users if user["username"] != username]
        self.guardar_datos(data)
        return True


    # Helpers
    def borrar_datos(self, tipo: Literal["Todo", "Datos", "Configuración"] = 'Todo'):
        data = self.leer_datos()
        if tipo in ['Datos', 'Todo']:
            data["productos"] = []
            data["ventas"] = []
        elif tipo in ['Configuración', 'Todo']:
            data['config'] = {
                "STOCK_MIN_GLOBAL": 200,
                "PAGE_SIZE": 5,
                "NOMBRE_NEGOCIO": "GestiOne",
                "MONEDA": "C$",
            }
        else:
            raise ValueError("Tipo de datos no reconocido.")
        self.guardar_datos(data)

    def exportar_reporte(self, nombre_archivo: str, tipo: str, periodo: str,
                         total_tickets: int, productos_vendidos: list, total_periodo: float):
        import csv
        ruta_archivo = self.STORAGE_PATH / nombre_archivo
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Reporte de Ventas", tipo, periodo])
            writer.writerow(["Total Tickets", total_tickets])
            writer.writerow(["Total Ventas", f"{total_periodo:,.2f} {self.leer_config()["MONEDA"]}"])
            writer.writerow([])
            writer.writerow(["ID Producto", "Nombre Producto", "Cantidad Vendida"])
            for id_producto, nombre, cantidad in productos_vendidos:
                writer.writerow([id_producto, nombre, cantidad])