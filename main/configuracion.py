from pathlib import Path
import pandas as pd


class Configuracion:
    def __init__(self):
        self.STORAGE = Path(__file__).resolve().parent.parent / "storage"
        self.iniciar_archivos()

    def iniciar_archivos(self):
        self.STORAGE.mkdir(exist_ok=True)

        # Productos
        if not (self.STORAGE / "productos.csv").exists():
            pd.DataFrame(columns=["ID", "Nombre", "Precio", "Cantidad", "Stock Mínimo"]).to_csv(
                self.STORAGE / "productos.csv", index=False
            )

        # Ventas
        if not (self.STORAGE / "ventas.csv").exists():
            pd.DataFrame(columns=["ID Venta", "ID Producto", "Nombre Producto", "Cantidad Vendida", "Total", "Fecha"]).to_csv(
                self.STORAGE / "ventas.csv", index=False
            )

        # Configuración
        if not (self.STORAGE / "configuracion.txt").exists():
            with open(self.STORAGE / "configuracion.txt", 'w') as f:
                f.write("NIVEL_MINIMO_STOCK_GLOBAL=100\nNOMBRE_NEGOCIO=Mi Tienda\nTIPO_MONEDA=C$\n")

    # -- Productos --
    def obtener_productos(self):
        return pd.read_csv(self.STORAGE / "productos.csv")

    def guardar_productos(self, df: pd.DataFrame) -> tuple[bool, str]:
        try:
            df.to_csv(self.STORAGE / 'productos.csv', index=False)
            return True, "Productos guardados correctamente"
        except Exception as e:
            return False, f"Error al guardar productos: {str(e)}"

    # -- Ventas --
    def obtener_ventas(self):
        return pd.read_csv(self.STORAGE / "ventas.csv")

    def registrar_ventas(self, datos_venta: dict) -> tuple[bool, str]:
        try:
            df = self.obtener_ventas()
            nueva_venta = pd.DataFrame([datos_venta])
            df = pd.concat([df, nueva_venta], ignore_index=True)
            df.to_csv(self.STORAGE / 'ventas.csv', index=False)
            return True, "Venta registrada correctamente"
        except Exception as e:
            return False, f"Error al registrar venta: {str(e)}"

    # -- Configuración --
    def obtener_configuracion(self) -> dict[str, str]:
        config = {}
        with open(self.STORAGE / "configuracion.txt", mode='r') as archivo:
            for linea in archivo:
                if '=' in linea:
                    clave, valor = linea.split('=', 1)
                    config[clave] = valor
        return config

    def cambiar_config(self, clave: str, valor: int | str) -> tuple[bool, str]:
        try:
            config = self.obtener_configuracion()
            config[clave] = str(valor)
            with open(self.STORAGE / "configuracion.txt", 'w') as archivo:
                for k, v in config.items():
                    archivo.write(f"{k}={v}\n")
            return True, "Configuración actualizada correctamente"
        except Exception as e:
            return False, f"Error al actualizar configuración: {str(e)}"

    def resetear_datos(self, tipo: str) -> tuple[bool, str]:
        """
            Restablece archivos del sistema según el tipo especificado.

            :param tipo: str: Tipo de reset:
                          - 'C': Solo configuración
                          - 'D': Solo datos (productos y ventas)
                          - 'T': Todos los archivos
            :returns: tuple (éxito: bool, mensaje: str)
            :raises ValueError: Si el tipo no es válido
        """
        try:
            if tipo not in ['C', 'D', 'T']:
                return False, "Tipo de reset inválido. Use 'C' para configuraciones, 'D' para datos o 'T' para todo"

            if tipo in ['C', 'T']:
                config_file = self.STORAGE / 'configuracion.txt'
                config_file.unlink(missing_ok=True)
            if tipo in ['D', 'T']:
                productos_file = self.STORAGE / 'productos.csv'
                ventas_file = self.STORAGE / 'ventas.csv'
                productos_file.unlink(missing_ok=True)
                ventas_file.unlink(missing_ok=True)

            self.iniciar_archivos()

            mensajes = {
                'C': "Configuración ha sido restablecida.",
                'D': "Datos de productos y ventas han sido eliminados.",
                'T': "Todo ha sido restablecido a su estado inicial."
            }

            return True, mensajes[tipo]
        except Exception as e:
            return False, f"Error al restablecer datos: {str(e)}"