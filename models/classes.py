import datetime
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    cantidad: int
    stock_minimo: int = None

    def actualizar_stock(self, cantidad: int) -> bool:
        nuevo_stock = self.cantidad + cantidad
        if nuevo_stock < 0:
            raise ValueError("No hay stock suficiente")
        self.cantidad = nuevo_stock
        return True


@dataclass
class Ventas:
    id: int
    nombre: str
    cantidad: int
    total: float
    fecha: str = datetime.now().strftime("%d-%m-%Y %H:%M")