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


@dataclass
class Ventas:
    id: int
    nombre: str
    cantidad: int
    total: float
    fecha: str = datetime.now().strftime("%d-%m-%Y %H:%M")