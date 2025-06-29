"""
    Módulo de menú de ventas para GestiOne.

    Permite gestionar las operaciones relacionadas con ventas: ver, agregar, filtrar, reportar y analizar productos más vendidos.
    Utiliza utilidades y gestor de datos para la interacción y persistencia.
"""
import main.utilidades as util


class MenuVentas:
    def __init__(self, config, inventario):
        self.config = config
        self.inventario = inventario


    def menu(self):
        while True:
            util.limpiar_consola()
            print(util.mostrar_menu("Ventas", ['📊 Ver Ventas', '🛒 Agregar Venta', '📊 Reporte de ventas',
                                    '🔝 Productos mas vendidos', '🔙 Volver'], util.Fore.YELLOW, "Gestión de Ventas"))

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
                    break
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 3.")
                    util.pausa()