import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    stock: int
    stock_minimo: Optional[int] = None

    def to_list(self):
        return [
            self.id,
            self.nombre,
            self.precio,
            self.stock,
            self.stock_minimo
        ]


@dataclass
class ItemVenta:
    producto_id: int
    nombre: str
    cantidad: int
    precio_unitario: float

    def total_item(self):
        return self.cantidad * self.precio_unitario


@dataclass
class Venta:
    id: int
    fecha: datetime.datetime
    items: list[ItemVenta]

    def total(self):
        return sum(item.total_item() for item in self.items)

    def items_to_table(self):
        return [[
            item.producto_id,
            item.nombre,
            item.cantidad,
            item.precio_unitario,
            item.total_item()
        ] for item in self.items]