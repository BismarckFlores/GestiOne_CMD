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
    categoria: Optional[str] = None
    descripcion: Optional[str] = None

    def to_list(self):
        return [
            self.id,
            self.nombre,
            self.precio,
            self.stock,
            self.stock_minimo,
            self.categoria,
            self.descripcion
        ]

    @staticmethod
    def from_string(data: str):
        product_data = data.strip().split(',')
        if len(product_data) >= 4:
            return Producto(int(product_data[0]),
                     product_data[1],
                     float(product_data[2]),
                     int(product_data[3]),
                     int(product_data[4]),
                     product_data[5],
                     product_data[6])
        return None


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
    fecha: datetime
    items: list[ItemVenta]

    def total(self):
        return sum(item.total_item() for item in self.items)

    def to_table(self):
        return [[
            self.id,
            self.fecha.strftime("%d-%m-%Y %H:%M"),
            item.producto_id,
            item.nombre,
            item.cantidad,
            item.precio_unitario,
            item.total_item()
        ] for item in self.items]