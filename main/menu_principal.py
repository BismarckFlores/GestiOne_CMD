import main.utilidades as util
from main.menu_ventas import MenuVentas
from main.menu_inv import MenuInv


class MenuPrincipal:
    def __init__(self, config):
        self.config = config
        self.menu_inv = MenuInv(self.config)
        self.menu_ventas = MenuVentas(self.config, self.menu_inv)


    def menu_config(self):
        while True:
            config = self.config.leer_config()

            util.limpiar_consola()
            print(util.mostrar_menu("Configuración",
                                    ['📝 Ver Configuración', '✏️ Modificar Ajustes', '🚨 Gestión de Datos y Resets', '🔙 Volver'],
                                    util.Fore.MAGENTA, "Configuración de GestiOne"))

            opcion = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
            match opcion:
                case 1:
                    print(f"\n🏢 Nombre del negocio: {config['NOMBRE_NEGOCIO']}")
                    print(f"💵 Moneda: {config['MONEDA']}")
                    print(f"📃 Tamaño de pagina: {config['PAGE_SIZE']}")
                    print(f"📦 Stock mínimo global: {config['STOCK_MIN_GLOBAL']}")
                    util.pausa()
                case 2:
                    while True:
                        util.limpiar_consola()
                        print(util.mostrar_menu("Editar Configuración",
                                                ['✏️ Cambiar Nombre del Negocio', "💱 Cambiar Moneda",
                                                '📦 Cambiar Stock Mínimo Global', '📃 Cambiar Tamaño de Página','🔙 Volver'],
                                                util.Fore.LIGHTMAGENTA_EX))
                        opcion_editar = util.verificar_entrada("Seleccione una opción (Deja en blanco para conservar los valores actuales)",
                                                               int, "Opción inválida. Intente de nuevo.")
                        match opcion_editar:
                            case 1:
                                config['NOMBRE_NEGOCIO'] = input(f"📝 Nuevo nombre del negocio [{config["NOMBRE_NEGOCIO"]}]: ").strip() or config['NOMBRE_NEGOCIO']
                                self.config.actualizar_config(config)
                                util.mensaje_exito("🎉 Nombre del negocio actualizado correctamente.")
                                util.pausa()
                            case 2:
                                config['MONEDA'] = input(f"💱 Nueva moneda (ej. $, C$, €) [{config["MONEDA"]}]: ").strip() or config['MONEDA']
                                self.config.actualizar_config(config)
                                util.mensaje_exito("Moneda actualizada correctamente.")
                                util.pausa()
                            case 3:
                                config['STOCK_MIN_GLOBAL'] = util.verificar_entrada(f"📦 Nuevo stock mínimo global [{config["STOCK_MIN_GLOBAL"]}]",
                                                                                    int) or config['STOCK_MIN_GLOBAL']
                                if config['STOCK_MIN_GLOBAL'] <= 0:
                                    util.mensaje_error("El stock mínimo global debe ser un número entero positivo.")
                                    continue
                                self.config.actualizar_config(config)
                                util.mensaje_exito("Configuración actualizada correctamente.")
                                util.pausa()
                            case 4:
                                config['PAGE_SIZE'] = util.verificar_entrada(f"📃 Nuevo tamaño de página [{config["PAGE_SIZE"]}]",
                                                                             int) or config['PAGE_SIZE']
                                if config['PAGE_SIZE'] <= 0:
                                    util.mensaje_error("El tamaño de página debe ser un número entero positivo.")
                                    continue
                                self.config.actualizar_config(config)
                                util.mensaje_exito("Configuración actualizada correctamente.")
                                util.pausa()
                            case 5:
                                break
                            case _:
                                util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 4.")
                                util.pausa()
                case 3:
                    while True:
                        util.limpiar_consola()
                        print(util.mostrar_menu("Elige una opción para borrar",
                                                ['🗑️ Borrar Productos y Ventas', '⚙️ Restablecer Configuración', '💥 Borrar Todo (Fábrica)', '🔙 Volver'],
                                                util.Fore.LIGHTMAGENTA_EX, "⚠️ Advertencia: Esta acción no se puede deshacer ⚠️", util.Fore.LIGHTRED_EX))
                        opcion_borrar = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
                        match opcion_borrar:
                            case 1:
                                confirmacion = input("⚠️ ¿Confirmas que quieres borrar TODOS los productos y ventas? (s/n): ").strip().lower()
                                if confirmacion != 's':
                                    util.mensaje_info("✅ Borrado de productos y ventas cancelado. Tus datos están a salvo.")
                                    util.pausa()
                                    continue
                                self.config.borrar_datos('Datos')
                                util.mensaje_exito("🗑️ Todos los productos y registros de ventas han sido eliminados permanentemente.")
                                util.pausa()
                            case 2:
                                confirmacion = input("⚙️ ¿Confirmas que quieres restablecer la configuración a los valores predeterminados? (s/n): ").strip().lower()
                                if confirmacion != 's':
                                    util.mensaje_info("✅ Restablecimiento de configuración cancelado.")
                                    util.pausa()
                                    continue
                                self.config.borrar_datos('Configuración')
                                util.mensaje_exito("✅ La configuración ha sido restablecida a sus valores predeterminados.")
                                util.pausa()
                            case 3:
                                confirmacion = input("🔥 ADVERTENCIA CRÍTICA: ¿Estás ABSOLUTAMENTE seguro de borrar TODOS los datos "
                                                     "y restablecer la configuración de fábrica? Esta acción es IRREVERSIBLE.\n"
                                                     "Escribe 'SI' para confirmar: ").strip()
                                if confirmacion != 'SI':
                                    util.mensaje_info("✅ Operación de borrado total cancelada. Nada ha sido modificado.")
                                    util.pausa()
                                    continue
                                self.config.borrar_datos()
                                util.mensaje_exito("🎉 ¡Sistema restablecido a valores de fábrica! Todos los datos han sido eliminados.")
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
                    self.menu_inv.menu()
                case 2:
                    self.menu_ventas.menu()
                case 3:
                    self.menu_config()
                case 4:
                    return
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 5.")
                    util.pausa()