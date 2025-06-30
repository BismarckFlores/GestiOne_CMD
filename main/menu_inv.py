from tabulate import tabulate as tb
import main.utilidades as util
from models.classes import Producto


class MenuInv:
    def __init__(self, gestor_datos):
        self.gestor_datos = gestor_datos


    def menu(self):
        while True:
            util.limpiar_consola()
            print(util.mostrar_menu("Inventario",
                                    ['📦 Ver Inventario', '➕ Agregar Producto', '✏️ Editar Producto',
                                    '🔄 Restock de producto', '🗑️ Borrar Producto', '🔙 Volver'], util.Fore.GREEN,
                                    "Gestión de Inventario"))

            opcion = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
            match opcion:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    break
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 5.")
                    util.pausa()