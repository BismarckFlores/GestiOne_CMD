"""
    Módulo de gestión de datos para GestiOne.

    Proporciona funciones para el almacenamiento, recuperación y manipulación de datos de productos, ventas, usuarios y configuración.
    Utiliza archivos binarios para persistencia y asegura la integridad de los datos.
"""
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
        """
            Inicializa los archivos de almacenamiento de datos.

            Crea la carpeta de almacenamiento y el archivo binario principal si no existen.
            Si es la primera vez, inicializa con datos de ejemplo y configuración por defecto.
        """
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
        """
            Lee todos los datos almacenados en el archivo binario principal.

            :returns: dict: Diccionario con listas de productos, ventas, usuarios y configuración.
        """
        with open(self.data_file, 'rb') as f:
            return pkl.load(f)

    def guardar_datos(self, datos: dict):
        """
            Guarda el diccionario de datos en el archivo binario principal.

            :param datos: dict: Diccionario con los datos a almacenar.
        """
        with open(self.data_file, 'wb') as f:
            pkl.dump(datos, f)

    def leer_productos(self):
        """
            Obtiene la lista de productos almacenados.

            :returns: tuple: Encabezados y lista de productos en formato lista.
        """
        productos = self.leer_datos()["productos"]
        productos.sort(key=lambda p: p.id)
        moneda = self.leer_config()["MONEDA"]
        header = ["ID", "Nombre", f"Precio ({moneda})", "Stock", "Stock Mínimo"]
        return header, [p.to_list() for p in productos]

    def existe_id_producto(self, id_buscar):
        """
            Verifica si existe un producto con el ID dado.

            :param id_buscar: int: ID a buscar.
            :returns: bool: True si existe, False si no.
        """
        productos = self.leer_datos()["productos"]
        return any(p.id == id_buscar for p in productos)

    def buscar_producto(self, id_buscar: int) -> Producto | None:
        """
            Busca y retorna un producto por su ID.

            :param id_buscar: int: ID del producto a buscar.
            :returns: Producto | None: El producto si existe, None si no.
        """
        productos = self.leer_datos()["productos"]
        for producto in productos:
            if producto.id == id_buscar:
                return producto
        return None

    def actualizar_producto(self, producto: Producto):
        """
            Actualiza los datos de un producto existente.

            :param producto: Producto: Instancia de producto con los nuevos datos.
        """
        data = self.leer_datos()
        for i, p in enumerate(data["productos"]):
            if p.id == producto.id:
                data["productos"][i] = producto
                break
        self.guardar_datos(data)

    def guardar_producto(self, producto: Producto):
        """
            Agrega un nuevo producto al almacenamiento.

            :param producto: Producto: Instancia del producto a guardar.
        """
        data = self.leer_datos()
        data["productos"].append(producto)
        self.guardar_datos(data)

    def eliminar_producto(self, id_producto: int):
        """
            Elimina un producto por su ID.

            :param id_producto: int: ID del producto a eliminar.
        """
        data = self.leer_datos()
        data["productos"] = [p for p in data["productos"] if p.id != id_producto]
        self.guardar_datos(data)

    def guardar_productos(self, productos: list[Producto]):
        """
            Reemplaza la lista de productos almacenados por una nueva lista.

            :param productos: list[Producto]: Lista de productos a guardar.
        """
        data = self.leer_datos()
        data["productos"] = productos
        self.guardar_datos(data)

    def leer_ventas(self) -> tuple[list[str], list[Venta]]:
        """
            Obtiene la lista de ventas almacenadas.

            :returns: tuple: Encabezados y lista de ventas.
        """
        ventas = self.leer_datos()["ventas"]
        header = ["ID Venta", "Fecha", "ID Producto","Producto",
                  "Cantidad", f"Precio Unitario ({self.leer_config()["MONEDA"]})",
                  f"Subtotal Producto ({self.leer_config()["MONEDA"]})"]
        return header, ventas

    def filtrar_ventas_por_fecha(self, fecha, tipo: Literal["dia", "mes", "anio"]):
        """
            Filtra las ventas por día, mes o año.

            :param fecha: str: Fecha a filtrar (formato depende del tipo).
            :param tipo: Literal['dia', 'mes', 'anio']: Tipo de filtro.
            :returns: list: Lista de ventas filtradas.
        """
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
        """
            Genera un resumen de ventas: total de tickets, productos vendidos y total de ventas.

            :param ventas: list: Lista de ventas a resumir.
            :returns: tuple: (total tickets, lista de productos vendidos, total de ventas).
        """
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
        """
            Agrega una nueva venta al almacenamiento.

            :param venta: Venta: Instancia de la venta a guardar.
        """
        data = self.leer_datos()
        data["ventas"].append(venta)
        self.guardar_datos(data)

    def leer_config(self) -> dict:
        """
            Obtiene la configuración actual del sistema.

            :returns: dict: Diccionario con la configuración.
        """
        data = self.leer_datos()
        return data["config"]

    def actualizar_config(self, config_data: dict):
        """
            Actualiza la configuración del sistema.

            :param config_data: dict: Nueva configuración a guardar.
        """
        data = self.leer_datos()
        data["config"] = config_data
        self.guardar_datos(data)

    def listar_usuarios(self) -> list[dict[str, str]]:
        """
            Lista los nombres de usuario registrados.

            :returns: list: Lista de nombres de usuario.
        """
        return [user["username"] for user in self.leer_datos()["usuarios"]]

    @staticmethod
    def hash_password(password: str):
        """
            Genera el hash SHA-256 de una contraseña.

            :param password: str: Contraseña en texto plano.
            :returns: str: Hash de la contraseña.
        """
        return hl.sha256(password.encode("utf-8")).hexdigest()

    def verificar_usuario(self, username: str, password: str) -> bool:
        """
            Verifica si un usuario y contraseña son válidos.

            :param username: str: Nombre de usuario.
            :param password: str: Contraseña en texto plano.
            :returns: bool: True si las credenciales son correctas, False si no.
        """
        users = self.leer_datos()["usuarios"]
        password_hash = self.hash_password(password)
        return any(user["username"] == username and user["password"] == password_hash for user in users)

    def is_admin(self, username: str):
        """
            Verifica si un usuario es administrador.

            :param username: str: Nombre de usuario.
            :returns: bool: True si es admin, False si no.
        """
        users = self.leer_datos()["usuarios"]
        return any(user["username"] == username and user['is_admin'] for user in users)

    def ver_usuario(self, username: str):
        """
            Obtiene la información de un usuario.

            :param username: str: Nombre de usuario.
            :returns: dict | None: Diccionario con info del usuario o None si no existe.
        """
        users = self.leer_datos()["usuarios"]
        for user in users:
            if user["username"] == username:
                return {
                    "username": user["username"],
                    "is_admin": user["is_admin"]
                }
        return None

    def agregar_usuario(self, username: str, password: str, current_user: str, is_admin: bool = False):
        """
            Agrega un nuevo usuario al sistema (solo admin).

            :param username: str: Nombre de usuario.
            :param password: str: Contraseña en texto plano.
            :param current_user: str: Usuario actual (debe ser admin).
            :param is_admin: bool: Si el nuevo usuario será admin.
            :returns: bool: True si se agregó, False si no.
        """
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
        """
            Cambia la contraseña de un usuario.

            :param current_user: str: Usuario actual.
            :param old_password: str: Contraseña actual.
            :param new_password: str: Nueva contraseña.
            :returns: bool: True si se cambió, False si no.
        """
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
        """
            Elimina un usuario del sistema (solo admin).

            :param username: str: Usuario a eliminar.
            :param current_user: str: Usuario actual (debe ser admin).
            :returns: bool: True si se eliminó, False si no.
        """
        data = self.leer_datos()
        users = data["usuarios"]
        if not self.is_admin(current_user):
            return False
        data["usuarios"] = [user for user in users if user["username"] != username]
        self.guardar_datos(data)
        return True

    def borrar_datos(self, tipo: Literal["todos", "datos", "configuración"] = 'todos'):
        """
            Borra datos del sistema según el tipo especificado.

            :param tipo: Literal['todos', 'datos', 'configuración']: Qué borrar.
        """
        data = self.leer_datos()
        if tipo in ['datos', 'todos']:
            data["productos"] = []
            data["ventas"] = []
        elif tipo in ['configuración', 'todos']:
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
        """
            Exporta un reporte de ventas a un archivo CSV en la carpeta de almacenamiento.

            :param nombre_archivo: str: Nombre del archivo a crear.
            :param tipo: str: Tipo de reporte (Día, Mes, Año).
            :param periodo: str: Periodo del reporte.
            :param total_tickets: int: Total de tickets en el periodo.
            :param productos_vendidos: list: Lista de productos vendidos.
            :param total_periodo: float: Total de ventas en el periodo.
        """
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