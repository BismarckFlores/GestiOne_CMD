import main.utilidades as util
from main.menu_ventas import MenuVentas
from main.menu_inv import MenuInv
from dao.configuracion import Configuracion


class MenuPrincipal:
    def __init__(self, config: Configuracion):
        self.config = config
        self.menu_inv = MenuInv(self.config)
        self.menu_ventas = MenuVentas(self.config, self.menu_inv)


    def menu_config(self):
        while True:
            config = self.config.leer_config()

            util.limpiar_consola()
            print(util.mostrar_menu("Configuración",
                                    ['📝 Ver Configuración', '✏️ Editar Configuración', '🗑️ Borrar datos', '🔙 Volver'],
                                    util.Fore.LIGHTBLUE_EX, "Configuración de GestiOne"))

            opcion = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
            match opcion:
                case 1:
                    print(f"Nombre del negocio: {config['NOMBRE_NEGOCIO']}")
                    print(f"Moneda: {config['MONEDA']}")
                    print(f"Stock mínimo global: {config['STOCK_MIN_GLOBAL']}")
                    util.pausa()
                case 2:
                    while True:
                        util.limpiar_consola()
                        print(util.mostrar_menu("Editar Configuración",
                                          ['✏️ Cambiar Nombre del Negocio', "💱 Cambiar Moneda",
                                           '📦 Cambiar Stock Mínimo Global', '🔙 Volver'],))
                        opcion_editar = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
                        match opcion_editar:
                            case 1:
                                config['NOMBRE_NEGOCIO'] = input("Nuevo nombre del negocio: ").strip()
                                self.config.actializar_config(config)
                                util.mensaje_exito("Configuración actualizada correctamente.")
                                util.pausa()
                            case 2:
                                config['MONEDA'] = input("Nueva moneda: ").strip()
                                self.config.actializar_config(config)
                                util.mensaje_exito("Configuración actualizada correctamente.")
                                util.pausa()
                            case 3:
                                config['STOCK_MIN_GLOBAL'] = util.verificar_entrada("Nuevo stock mínimo global", int, "Debe ser un número entero positivo.")
                                self.config.actializar_config(config)
                                util.mensaje_exito("Configuración actualizada correctamente.")
                                util.pausa()
                            case 4:
                                break
                            case _:
                                util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 4.")
                                util.pausa()
                case 3:
                    while True:
                        util.limpiar_consola()
                        print(util.mostrar_menu("Elige una opción para borrar",
                                                ['🗑️ Borrar Datos', '🗑️ Borrar Configuración', '🗑️ Borrar Todo', '🔙 Volver'],
                                                util.Fore.LIGHTBLUE_EX, "Advertencia: Esta acción no se puede deshacer.", util.Fore.LIGHTRED_EX))
                        opcion_borrar = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
                        match opcion_borrar:
                            case 1:
                                confirmacion = input("¿Está seguro de que desea borrar los datos? (s/n): ").strip().lower()
                                if confirmacion != 's':
                                    util.mensaje_info("Operación cancelada.")
                                    util.pausa()
                                    continue
                                self.config.borrar_datos('Datos')
                                util.mensaje_exito("Datos borrados correctamente.")
                                util.pausa()
                            case 2:
                                confirmacion = input("¿Está seguro de que desea borrar la configuración? (s/n): ").strip().lower()
                                if confirmacion != 's':
                                    util.mensaje_info("Operación cancelada.")
                                    util.pausa()
                                    continue
                                self.config.borrar_datos('Configuración')
                                util.mensaje_exito("Configuración borrada correctamente.")
                                util.pausa()
                            case 3:
                                confirmacion = input("¿Está seguro de que desea borrar todos los datos y configuración? (s/n): ").strip().lower()
                                if confirmacion != 's':
                                    util.mensaje_info("Operación cancelada.")
                                    util.pausa()
                                    continue
                                self.config.borrar_datos()
                                util.mensaje_exito("Todos los datos y configuración han sido borrados.")
                                util.pausa()
                            case 4:
                                break
                            case _:
                                util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 4.")
                                util.pausa()
                case 4:
                    return
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 3.")
                    util.pausa()


    def menu(self):
        while True:
            util.limpiar_consola()
            print(util.mostrar_menu("MENÚ PRINCIPAL",
                                    ['📦 Inventario', '💰 Ventas', '⚙️ Configuración', '🔙 Salir'],
                                    util.Fore.BLUE, "Bienvenido a GestiOne"))

            opcion = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
            match opcion:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    self.menu_config()
                case 4:
                    return
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 5.")
                    util.pausa()