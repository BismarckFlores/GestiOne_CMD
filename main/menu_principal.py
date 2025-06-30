"""
    Módulo de menú principal de GestiOne.

    Gestiona la navegación principal de la aplicación, permitiendo el acceso a los módulos de inventario, ventas y configuración.
    Incluye menús interactivos y opciones avanzadas para administradores.
"""
import main.utilidades as util
from tabulate import tabulate as tb
from main.menu_inv import MenuInv
from main.menu_ventas import MenuVentas


class MenuPrincipal:
    def __init__(self, gestor_datos, user):
        self.gestor_datos = gestor_datos
        self.user = user
        self.is_admin = gestor_datos.is_admin(user)
        self.menu_inv = MenuInv(self.gestor_datos)
        self.menu_ventas = MenuVentas(self.gestor_datos, self.menu_inv)


    def menu_config(self):
        while True:
            config = self.gestor_datos.leer_config()

            opciones = ['📝 Ver Configuración', '👤 Panel de Usuario']
            admin = f'{util.Fore.LIGHTRED_EX}ADMIN{util.Fore.RESET}'
            if self.is_admin:
                opciones.extend([f'✏️ Modificar Ajustes [{admin}]', f'🚨 Gestión de Datos y Resets [{admin}]'])
            opciones.append('🔙 Volver')

            util.limpiar_consola()
            print(util.mostrar_menu("Configuración", opciones, util.Fore.MAGENTA, "Configuración de GestiOne"))

            opcion = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
            if opcion == 1:
                util.limpiar_consola()
                print(util.crear_banner("Configuración Actual", util.Fore.LIGHTMAGENTA_EX))
                print(f"🏢 Nombre del negocio: {config['NOMBRE_NEGOCIO']}")
                print(f"💵 Moneda: {config['MONEDA']}")
                print(f"📃 Tamaño de pagina: {config['PAGE_SIZE']}")
                print(f"📦 Stock mínimo global: {config['STOCK_MIN_GLOBAL']}")
                util.pausa()
            elif opcion == 2:
                while True:
                    opciones_pu = ['👤 Ver Información de Usuario', '🔐 Cambiar Contraseña']
                    if self.is_admin:
                        opciones_pu.extend([f'➕ Agregar Usuario [{admin}]',
                                            f'🗑️ Borrar Cuenta (Irreversible) [{admin}]'])
                    opciones_pu.append("🔙 Volver")
                    util.limpiar_consola()
                    print(util.mostrar_menu("Panel de Usuario", opciones_pu, util.Fore.LIGHTMAGENTA_EX))
                    opcion_pu = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
                    if opcion_pu == 1:
                        util.limpiar_consola()
                        print(util.crear_banner("Información de Usuario", util.Fore.LIGHTMAGENTA_EX))
                        print(f"👤 Usuario: {self.user}")
                        print(f"🔑 Rol: {'Administrador' if self.is_admin else 'Usuario Regular'}")
                        util.pausa()
                    elif opcion_pu == 2:
                        while True:
                            util.limpiar_consola()
                            print(util.crear_banner("Cambiar Contraseña", util.Fore.LIGHTMAGENTA_EX))
                            old_password = util.pedir_contrasenia("Ingrese su contraseña actual (0 para cancelar): ")
                            if old_password == '0':
                                util.mensaje_info("Operación de cambio de contraseña cancelada.")
                                break
                            new_password = util.pedir_contrasenia("Ingrese su nueva contraseña: ")
                            confirm_password = util.pedir_contrasenia("Confirme su nueva contraseña: ")

                            if new_password != confirm_password:
                                util.mensaje_error("Las contraseñas no coinciden. Intente de nuevo.")
                                continue

                            if self.gestor_datos.cambiar_contrasenia(self.user, old_password, new_password):
                                util.mensaje_exito("Contraseña cambiada exitosamente.")
                                break
                            else:
                                util.mensaje_error("Error al cambiar la contraseña. Verifique sus datos e intente de nuevo.")
                                util.pausa()
                    elif opcion_pu == 3 and self.is_admin:
                        while True:
                            util.limpiar_consola()
                            print(util.crear_banner("Agregar Usuario", util.Fore.LIGHTMAGENTA_EX))
                            new_username = input("Ingrese el nombre de usuario del nuevo usuario (0 para cancelar): ").strip()
                            if new_username == '0':
                                util.mensaje_info("Operación de agregar usuario cancelada.")
                                break
                            if not new_username:
                                util.mensaje_error("El nombre de usuario no puede estar vacío. Intente de nuevo.")
                                continue
                            new_password = util.pedir_contrasenia("Ingrese la contraseña del nuevo usuario: ")
                            is_admin = input("¿Es administrador? (s/n): ").strip().lower() == 's'

                            if self.gestor_datos.agregar_usuario(new_username, new_password, self.user, is_admin):
                                util.mensaje_exito(f"Usuario '{new_username}' agregado exitosamente.")
                                break
                            else:
                                util.mensaje_error(f"Error al agregar el usuario '{new_username}'. Verifique los datos e intente de nuevo.")
                                util.pausa()
                    elif opcion_pu == 3 and not self.is_admin:
                        break
                    elif opcion_pu == 4 and self.is_admin:
                        users = sorted(self.gestor_datos.leer_datos()['usuarios'], key=lambda x: not x['is_admin'])



                        page_size = config['PAGE_SIZE']
                        total = len(users)
                        max_page = (total - 1) // page_size
                        page = 0
                        while True:
                            util.limpiar_consola()
                            print(util.crear_banner("Eliminar usuarios", util.Fore.LIGHTMAGENTA_EX,
                                                "Advertencia: Esta acción es irreversible"), util.Fore.LIGHTRED_EX)

                            start = page * page_size
                            end = start + page_size
                            table = []
                            for idx, user in enumerate(users[start:end], start=1 + start):
                                table.append([idx, user['username'], "Administrador" if user['is_admin'] else "Usuario Regular"])
                            print(f'Página {page + 1} de {max_page + 1} | Total de usuarios: {total}')
                            print(tb(table, ["#", "Usuario", "Rol"], "fancy_grid"))

                            if total > page_size:
                                nav_menu = [["[S]iguiente", "[A]nterior", "[I]r a", "[E]liminar usuario", "[X] Salir"]]
                            elif end < total:
                                nav_menu = [["[S]iguiente", "[I]r a", "[E]liminar usuario", "[X] Salir"]]
                            elif page > 0:
                                nav_menu = [["[A]nterior", "[I]r a", "[E]liminar usuario", "[X] Salir"]]
                            else:
                                nav_menu = [["[E]liminar usuario", "[X] Salir"]]
                            print(tb(nav_menu, tablefmt='rounded_outline'))
                            nav_options = input("Seleccione una opción: ").strip().lower()

                            if nav_options == 's' and end < total and total > page_size:
                                page += 1
                            elif nav_options == 'a' and page > 0 and total > page_size:
                                page -= 1
                            elif nav_options == 'i' and total > page_size:
                                page_num = util.verificar_entrada("Ingrese el número de página", int,
                                                                  "Número de página inválido.")
                                if 1 <= page_num <= max_page + 1:
                                    page = page_num - 1
                                else:
                                    util.mensaje_error(f"Error: Ingrese un número entre 1 y {max_page + 1}")
                                    util.pausa()
                            elif nav_options == 'e':
                                user_num = util.verificar_entrada("Ingrese el número del usuario a eliminar",
                                                                  int, "Número inválido. Intente de nuevo.")
                                if 1 <= user_num <= total:
                                    username = users[user_num - 1]['username']
                                    self.gestor_datos.eliminar_usuario(username, self.user)
                                    util.mensaje_exito(f"Usuario '{username}' eliminado exitosamente.")
                                    util.pausa()
                                    break
                                else:
                                    util.mensaje_error(f"Error: Ingrese un número entre 1 y {total}")
                                    util.pausa()
                                    continue
                            elif nav_options == 'x':
                                break
                            else:
                                util.mensaje_error("Opción inválida.")
                                util.pausa()
                                continue
                    elif opcion_pu == 5 and self.is_admin:
                        break
            elif opcion == 3 and self.is_admin:
                while True:
                    util.limpiar_consola()
                    print(util.mostrar_menu("Editar Configuración",
                                            ['✏️ Cambiar Nombre del Negocio', "💱 Cambiar Moneda",
                                            '📦 Cambiar Stock Mínimo Global', '📃 Cambiar Tamaño de Página','🔙 Volver'],
                                            util.Fore.LIGHTMAGENTA_EX, "Sección de solo ADMIN", util.Fore.LIGHTRED_EX))
                    opcion_editar = util.verificar_entrada("Seleccione una opción (Deja en blanco para conservar los valores actuales)",
                                                           int, "Opción inválida. Intente de nuevo.")
                    match opcion_editar:
                        case 1:
                            nombre_negocio = config['NOMBRE_NEGOCIO']
                            config['NOMBRE_NEGOCIO'] = input(f"📝 Nuevo nombre del negocio [{nombre_negocio}]: ").strip() or nombre_negocio
                            self.gestor_datos.actualizar_config(config)
                            util.mensaje_exito("🎉 Nombre del negocio actualizado correctamente.")
                            util.pausa()
                        case 2:
                            moneda = config['MONEDA']
                            config['MONEDA'] = input(f"💱 Nueva moneda (ej. $, C$, €) [{moneda}]: ").strip() or moneda
                            self.gestor_datos.actualizar_config(config)
                            util.mensaje_exito("Moneda actualizada correctamente.")
                            util.pausa()
                        case 3:
                            stock_min_global = config['STOCK_MIN_GLOBAL']
                            config['STOCK_MIN_GLOBAL'] = util.verificar_entrada(f"📦 Nuevo stock mínimo global [{stock_min_global}]",
                                                                                int) or stock_min_global
                            if config['STOCK_MIN_GLOBAL'] <= 0:
                                util.mensaje_error("El stock mínimo global debe ser un número entero positivo.")
                                continue
                            self.gestor_datos.actualizar_config(config)
                            util.mensaje_exito("Configuración actualizada correctamente.")
                            util.pausa()
                        case 4:
                            page_size = config['PAGE_SIZE']
                            config['PAGE_SIZE'] = util.verificar_entrada(f"📃 Nuevo tamaño de página [{page_size}]",
                                                                         int) or page_size
                            if config['PAGE_SIZE'] <= 0:
                                util.mensaje_error("El tamaño de página debe ser un número entero positivo.")
                                continue
                            self.gestor_datos.actualizar_config(config)
                            util.mensaje_exito("Configuración actualizada correctamente.")
                            util.pausa()
                        case 5:
                            break
                        case _:
                            util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 4.")
                            util.pausa()
            elif opcion == 3:
                break
            elif opcion == 4 and self.is_admin:
                while True:
                    util.limpiar_consola()
                    print(util.mostrar_menu("Elige una opción para borrar",
                                            ['🗑️ Borrar Productos y Ventas', '⚙️ Restablecer Configuración', '💥 Borrar Todo (Fábrica)', '🔙 Volver'],
                                            util.Fore.LIGHTMAGENTA_EX, "Advertencia: Esta acción no se puede deshacer - Sección de solo ADMIN", util.Fore.LIGHTRED_EX))
                    opcion_borrar = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
                    match opcion_borrar:
                        case 1:
                            confirmacion = input("⚠️ ¿Confirmas que quieres borrar TODOS los productos y ventas? (s/n): ").strip().lower()
                            if confirmacion != 's':
                                util.mensaje_info("✅ Borrado de productos y ventas cancelado. Tus datos están a salvo.")
                                util.pausa()
                                continue
                            self.gestor_datos.borrar_datos('datos')
                            util.mensaje_exito("🗑️ Todos los productos y registros de ventas han sido eliminados permanentemente.")
                            util.pausa()
                        case 2:
                            confirmacion = input("⚙️ ¿Confirmas que quieres restablecer la configuración a los valores predeterminados? (s/n): ").strip().lower()
                            if confirmacion != 's':
                                util.mensaje_info("✅ Restablecimiento de configuración cancelado.")
                                util.pausa()
                                continue
                            self.gestor_datos.borrar_datos('configuración')
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
                            self.gestor_datos.borrar_datos()
                            util.mensaje_exito("🎉 ¡Sistema restablecido a valores de fábrica! Todos los datos han sido eliminados.")
                            util.pausa()
                        case 4:
                            break
                        case _:
                            util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 4.")
                            util.pausa()
            elif opcion == 5 and self.is_admin:
                return
            else:
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