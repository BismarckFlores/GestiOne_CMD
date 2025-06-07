import configuracion as config
import utilidades as util
from colorama import Fore

from src.configuracion import leer_datos


def menu_inv():
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("INVENTARIO",
                                 ['📦 Ver Productos', '➕ Agregar Producto', '✏️ Editar Producto',
                                            '🗑️ Eliminar Producto', '🔄 Restock de producto',
                                            '⚠️ Ver productos con stock bajo', '🔙 Volver al Menú Principal'],
                                 Fore.GREEN, "¡Aun no esta implementado!", Fore.YELLOW)
        print(menu)

        opcion = input("\nSeleccione una opción: ").strip()
        match opcion:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "6":
                pass
            case "7":
                break
            case _:
                util.mensaje_error("Opción inválida. Intente de nuevo.")
                util.pausa()


def reportes_avanzados():
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("REPORTES AVANZADOS",
                                 ['📊 Filtrar por ID de Producto', '📅 Filtrar por Rango de Fechas', '🔙 Volver al Menú de Ventas'],
                                 Fore.CYAN, "¡Aun no esta implementado!", Fore.YELLOW)
        print(menu)

        opcion = input("\nSeleccione una opción: ").strip()
        match opcion:
            case "1":
                pass
            case "2":
                pass
            case "3":
                break
            case _:
                util.mensaje_error("Opción inválida. Intente de nuevo.")
                util.pausa()


def menu_ventas():
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("VENTAS",
                                 ['🧾 Registrar Ticket de Venta', '📅 Ver historial de ventas',
                                            '📊 Reporte de ventas (Diario, Semanal, Mensual)', '🔝 Productos más vendidos',
                                            '📎 Reportes avanzados', '🔙 Volver al menú principal'],
                                 Fore.CYAN, "¡Aun no esta implementado!", Fore.YELLOW)
        print(menu)

        opcion = input("\nSeleccione una opción: ").strip()
        match opcion:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                reportes_avanzados()
            case "6":
                break
            case _:
                util.mensaje_error("Opción inválida. Intente de nuevo.")
                util.pausa()


def cambiar_configs_menu():
    opciones = ['🔧 Nivel minimo de stock global', '🛒 Nombre del negocio', '💵 Tipo de moneda',
                '🔙 Volver al Menú de Configuración']
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("CAMBIAR CONFIGURACIONES", opciones, Fore.LIGHTMAGENTA_EX,
                                 "Lista de configuraciones a cambiar")
        print(menu)

        opcion = util.verificar_entrada("\nSeleccione una opción", int)
        if opcion == 1:
            nuevo_valor = util.verificar_entrada(f"\nIngrese el nuevo valor para el '{opciones[0]}'", int)
        elif opcion in [2, 3]:
            nuevo_valor = input(f"Ingrese el nuevo valor para el '{opciones[opcion - 1]}': ")
        elif opcion == 4:
            break
        else:
            util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 5.")
            util.pausa()
            continue

        print(type(nuevo_valor), nuevo_valor)
        resultado, msg = config.cambiar_configuracion(opcion, nuevo_valor)
        util.reportar_resultado(msg, resultado)


def menu_config():
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("CONFIGURACIÓN",
                                 ['📃 Ver valores actuales', '⚙️ Cambiar configuraciones', '🔧 Resetear configuraciones',
                                            '🗑️ Borrar datos de ventas y productos', '🔙 Volver al Menú Principal'],
                                 Fore.MAGENTA, "Configuración General de GestiOne")
        print(menu)

        opcion = input("\nSeleccione una opción: ").strip()
        match opcion:
            case "1":
                configs = ['🔧 Nivel minimo de stock global', '🛒 Nombre del negocio', '💵 Tipo de moneda']
                _, _, valores = leer_datos()
                for indice, (_, valor) in enumerate(valores.items()):
                    print(f"{configs[indice]}: {valor}")
                util.pausa()
            case "2":
                cambiar_configs_menu()
            case "3":
                resultado, msg = config.resetear_configuracion()
                util.reportar_resultado(msg, resultado)
                util.pausa()
            case "4":
                resultado, msg = config.resetear_datos()
                util.reportar_resultado(msg, resultado)
                util.pausa()
            case "5":
                break
            case _:
                util.mensaje_error("Opción inválida. Intente de nuevo.")
                util.pausa()


def main():
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("GESTIONE",
                                 ['📦 inventario', '📝 Ventas', '⚙️ Configuración', '🚪 Salir'],
                                 Fore.CYAN, "Menú Principal")
        print(menu)

        opcion = input("\nSeleccione una opción: ").strip()
        match opcion:
            case "1":
                menu_inv()
            case "2":
                menu_ventas()
            case "3":
                menu_config()
            case "4":
                print("\n🎉 ¡Hasta luego! Gracias por usar GestiOne.\n")
                break
            case _:
                util.mensaje_error("Opción inválida. Intente de nuevo.")
                util.pausa()


if __name__ == "__main__":
    config.iniciar_archivos()
    main()