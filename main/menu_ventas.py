from datetime import datetime as dt
import main.utilidades as util
from tabulate import tabulate as tb
from models.classes import ItemVenta, Venta, Producto


class MenuVentas:
    def __init__(self, gestor_datos, inventario):
        self.gestor_datos = gestor_datos
        self.inventario = inventario


    def ver_ventas(self):
        header, data = self.gestor_datos.leer_ventas()
        page_size = self.gestor_datos.leer_config()["PAGE_SIZE"]
        if not data:
            util.mensaje_error("No hay ventas registradas.")
            util.pausa()
            return

        filtros = {}
        page = 0

        def aplicar_filtros():
            ventas = data.copy()
            if 'fecha' in filtros:
                inicio, fin = filtros['fecha']
                ventas = [
                    v for v in ventas if inicio <= v.fecha.replace(hour=0, minute=0, second=0, microsecond=0) <= fin
                ]
            if 'producto_id' in filtros:
                idp = filtros['producto_id']
                ventas = [v for v in ventas if any(item.producto_id == idp for item in v.items)]
            return ventas

        while True:
            util.limpiar_consola()
            ventas_filtradas = aplicar_filtros()
            if not ventas_filtradas:
                util.mensaje_info("No hay ventas que coincidan con los filtros aplicados. Se eliminaran los filtros.")
                filtros.clear()
                page = 0
                util.pausa()
                continue

            total = len(ventas_filtradas)
            max_page = (total - 1) // page_size

            print(util.crear_banner("Ventas", util.Fore.LIGHTYELLOW_EX))

            filtros_activos = []
            if 'fecha' in filtros:
                fi, fn = filtros['fecha'][0].strftime('%d-%m-%Y'), filtros['fecha'][1].strftime('%d-%m-%Y')
                filtros_activos.append(f"Fecha: Del {fi} al {fn}")
            if 'producto_id' in filtros:
                filtros_activos.append(f"Producto ID: {filtros['producto_id']}")
            if filtros_activos:
                util.mensaje_info("Filtros activos [" + " | ".join(filtros_activos) + "]")

            start = page * page_size
            end = start + page_size

            print(f"Página {page + 1} de {max_page + 1} - Total de ventas: {total}")
            for venta in ventas_filtradas[start:end]:
                total_venta = venta.total()
                fecha = venta.fecha.strftime('%d-%m-%Y %H:%M')
                print(f'Venta ID: {venta.id} - Fecha: {fecha} - Total: {total_venta} {self.gestor_datos.leer_config()["MONEDA"]}')
                print(tb(venta.items_to_table(), header[2:], 'fancy_grid'))

            if total > page_size:
                nav_menu = [["[S]iguiente", "[A]nterior", "[I]r a", "[F]iltros", "[X] Salir"]]
            elif end < total:
                nav_menu = [["[S]iguiente", "[I]r a", "[F]iltros", "[X] Salir"]]
            elif page > 0:
                nav_menu = [["[A]nterior", "[I]r a", "[F]iltros", "[X] Salir"]]
            else:
                nav_menu = [["[F]iltros", "[X] Salir"]]
            print(tb(nav_menu, tablefmt='rounded_outline'))
            nav_options = input("Elige una opción: ").strip().lower()

            if nav_options == 's' and end < total and total > page_size:
                page += 1
            elif nav_options == 'a' and page > 0 and total > page_size:
                page -= 1
            elif nav_options == 'i' and total > page_size:
                page_num = util.verificar_entrada("Ingrese el número de página", int, "Número de página inválido.")
                if 1 <= page_num <= max_page + 1:
                    page = page_num - 1
                else:
                    util.mensaje_error(f"Error: Ingrese un número entre 1 y {max_page + 1}")
                    util.pausa()
            elif nav_options == 'f':
                util.limpiar_consola()
                print(util.mostrar_menu("Filtros Avanzados", ["📅 Filtrar por rango de fechas", "🔎 Filtrar por ID de producto",
                                        "🗑️ Quitar todos los filtros","🔙 Volver"], util.Fore.LIGHTYELLOW_EX))
                filtro_op = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
                if filtro_op == 1:
                    fecha_inicio = input("Ingrese la fecha de inicio (DD-MM-YYYY): ").strip()
                    fecha_fin = input("Ingrese la fecha de fin (DD-MM-YYYY): ").strip()
                    try:
                        dt_inicio = dt.strptime(fecha_inicio, '%d-%m-%Y')
                        dt_fin = dt.strptime(fecha_fin, '%d-%m-%Y')
                    except ValueError:
                        util.mensaje_error("Formato de fecha inválido. Use DD-MM-YYYY.")
                        util.pausa()
                        continue
                    filtros['fecha'] = (dt_inicio, dt_fin)
                    page = 0
                    util.mensaje_exito(f"Filtro aplicado: Fecha desde {dt_inicio.strftime('%d-%m-%Y')} hasta {dt_fin.strftime('%d-%m-%Y')}.")
                    util.pausa()
                elif filtro_op == 2:
                    id = util.verificar_entrada("Ingrese el ID del producto a filtrar", int, "ID inválido. Debe ser un número entero.")
                    if not self.gestor_datos.existe_id_producto(id):
                        util.mensaje_error(f"No se encontraron ventas con productos de ID {id}.")
                        util.pausa()
                        continue
                    filtros['producto_id'] = id
                    page = 0
                    util.mensaje_exito(f"Filtro aplicado: Producto ID {id}.")
                    util.pausa()
                elif filtro_op == 3:
                    filtros.clear()
                    page = 0
                    util.mensaje_exito("Filtros eliminados.")
                    util.pausa()
                elif filtro_op == 4:
                    continue
                else:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 4.")
                    util.pausa()
            elif nav_options == 'x':
                break
            else:
                util.mensaje_error("Opción inválida.")
                util.pausa()


    def agregar_venta(self):
        util.limpiar_consola()
        header, data = self.gestor_datos.leer_productos()
        inventario = [row.copy() for row in data]

        items = []
        print(util.crear_banner("Agregar productos a la venta", util.Fore.LIGHTYELLOW_EX,
                                "Seleccione los productos a agregar a la venta. Ingrese 0 para terminar."))

        while True:
            disponibles = [row for row in inventario if row[3] > 0]
            if not disponibles:
                util.mensaje_info('No hay productos disponibles para agregar a la venta.')
                util.pausa()
                break

            id = util.verificar_entrada('Ingrese el ID del producto (0 para terminar)', int, 'ID inválido. Debe ser un número entero.')
            if id == 0:
                break
            if not self.gestor_datos.existe_id_producto(id):
                util.mensaje_error('ID no encontrado.')
                util.pausa()
                continue

            producto = next((row for row in inventario if row[0] == id and row[3] > 0), None)
            if not producto:
                util.mensaje_error('Producto no disponible o sin stock.')
                util.pausa()
                continue


            nombre = producto[1]
            stock = producto[3]
            print(tb([[producto[0], nombre, stock]], [header[0], header[1], header[3]], 'fancy_grid'))

            cantidad = util.verificar_entrada('Ingrese la cantidad a vender', int, 'Cantidad inválida. Debe ser un número entero.')

            item_existente = next((item for item in items if item.producto_id == id), None)
            if item_existente:
                if item_existente.cantidad + cantidad > stock:
                    util.mensaje_info('Cantidad total supera el stock disponible.')
                    util.pausa()
                    continue
                item_existente.cantidad += cantidad
            else:
                items.append(ItemVenta(id, nombre, cantidad, producto[2]))

            producto[3] -= cantidad

        if not items:
            util.mensaje_error('No se han agregado productos a la venta.')
            return

        productos_actualizados = []
        for row in inventario:
            productos_actualizados.append(Producto(*row))
        self.gestor_datos.guardar_productos(productos_actualizados)

        _, ventas = self.gestor_datos.leer_ventas()
        next_id = 1
        if ventas:
            next_id = max(v.id for v in ventas) + 1

        venta = Venta(next_id, dt.now(), items)
        self.gestor_datos.guardar_venta(venta)
        print(f"Venta registrada con ID {venta.id} y total {venta.total()} {self.gestor_datos.leer_config()['MONEDA']}.")
        util.pausa()


    def menu(self):
        while True:
            util.limpiar_consola()
            print(util.mostrar_menu("Ventas", ['📊 Ver Ventas', '🛒 Agregar Venta', '📊 Reporte de ventas',
                                    '🔝 Productos mas vendidos', '🔙 Volver'], util.Fore.YELLOW, "Gestión de Ventas"))

            opcion = util.verificar_entrada("Seleccione una opción", int, "Opción inválida. Intente de nuevo.")
            match opcion:
                case 1:
                    self.ver_ventas()
                case 2:
                    self.agregar_venta()
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    break
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 3.")
                    util.pausa()