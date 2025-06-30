from tabulate import tabulate as tb
import pruevas.GestiOne_v2_2.main.utilidades as util
from pruevas.GestiOne_v2_2.models.classes import Producto


class MenuInv:
    def __init__(self, gestor_datos):
        self.gestor_datos = gestor_datos


    def ver_inv(self, header = None, data = None):
        config = self.gestor_datos.leer_config()
        if header is None or data is None:
            header_fetched, data_fetched = self.gestor_datos.leer_productos()
            if header is None:
                header = header_fetched
            if data is None:
                data = data_fetched
        global_stock_minimo = config["STOCK_MIN_GLOBAL"]
        page_size = config["PAGE_SIZE"]

        if data is None or len(data) == 0:
            util.mensaje_error('No hay productos registrados en el inventario.')
            util.pausa()
            return

        idx_stock_min = header.index("Stock Mínimo")
        idx_id = header.index("ID")

        new_data = []
        for row in data:
            stock_minimo = row[idx_stock_min]
            if stock_minimo is None or stock_minimo == "" or stock_minimo == 0:
                row[idx_stock_min] = f"{global_stock_minimo} (Global)"
            else:
                row[idx_stock_min] = f"{stock_minimo} (Personalizado)"
            new_data.append(row)

        total = len(new_data)
        max_page = (total - 1) // page_size
        page = 0
        while True:
            util.limpiar_consola()
            print(util.crear_banner("Inventario", util.Fore.LIGHTGREEN_EX))
            start = page * page_size
            end = start + page_size
            print(f"Página {page + 1} de {max_page + 1} | Total productos: {total}")
            print(tb(new_data[start:end], header, 'fancy_grid'))
            if total > page_size:
                print(tb([["[S]iguiente", "[A]nterior", "[I]r a", "[B]uscar ID", "[X] Salir"]], tablefmt='rounded_outline'))
                choice = input("Elige una opción: ").strip().lower()
                if choice == 's' and end < total:
                    page += 1
                elif choice == 'a' and page > 0:
                    page -= 1
                elif choice == 'i':
                    page_num = util.verificar_entrada("Ingrese el número de página", int, "Número de página inválido.")
                    if 1 <= page_num <= max_page + 1:
                        page = page_num - 1
                    else:
                        util.mensaje_error(f"Error: Ingrese un número entre 1 y {max_page + 1}")
                        util.pausa()
                elif choice == 'b':
                    id = util.verificar_entrada("Ingrese el ID del producto a buscar", int, "ID inválido. Debe ser un número entero.")
                    for i, row in enumerate(new_data):
                        if row[idx_id] == id:
                            page = i // page_size
                            break
                    else:
                        util.mensaje_error(f"No se encontró un producto con ID {id}.")
                        util.pausa()
                elif choice == 'x':
                    break
            else:
                print(tb([["[X] Salir"]], tablefmt='rounded_outline'))
                choice = input("Elige una opción: ").strip().lower()
                if choice == 'x':
                    break


    def agregar_producto(self):
        util.limpiar_consola()
        print(util.crear_banner("Agregar Producto", util.Fore.LIGHTGREEN_EX))

        id = util.verificar_entrada("Ingrese el ID del producto", int, "ID inválido. Debe ser un número entero.")
        while self.gestor_datos.existe_id_producto(id) or id <= 0:
            if id <= 0:
                util.mensaje_error("El ID debe ser un número entero mayor a 0.")
            else:
                util.mensaje_error(f"El ID {id} ya existe. Por favor, ingrese un ID único.")
            id = util.verificar_entrada("Ingrese el ID del producto", int, "ID inválido. Debe ser un número entero.")

        nombre = input("Nombre del producto: ").strip()
        while not nombre:
            util.mensaje_error("El nombre del producto no puede estar vacío.")
            nombre = input("Nombre del producto: ").strip()

        precio = util.verificar_entrada("Precio del producto", float)
        while precio <= 0:
            util.mensaje_error("El precio debe ser un número positivo.")
            precio = util.verificar_entrada("Precio del producto", float)

        stock = util.verificar_entrada("Stock inicial", int)
        while stock < 0:
            util.mensaje_error("El stock no puede ser negativo.")
            stock = util.verificar_entrada("Stock inicial", int)

        while True:
            stock_minimo_str = input("Stock mínimo (opcional, deje en blanco para usar el global): ").strip()
            if not stock_minimo_str:
                stock_min = None
                break
            try:
                stock_min = int(stock_minimo_str)
                if stock_min <= 0:
                    util.mensaje_error("El stock mínimo no puede ser negativo o cero. Intente de nuevo.")
                else:
                    break
            except ValueError:
                util.mensaje_error("Entrada inválida. Ingrese un número entero o '0'.")

        producto = Producto(id, nombre, precio, stock, stock_min)
        self.gestor_datos.guardar_producto(producto)
        util.mensaje_exito(f"Producto {nombre} agregado correctamente con ID {id}.")
        util.pausa()


    def editar_producto(self):
        util.limpiar_consola()
        print(util.crear_banner("Editar Producto", util.Fore.LIGHTGREEN_EX))

        id = util.verificar_entrada("Ingrese el ID del producto a editar (0 para cancelar)",
                                    int, "ID inválido. Debe ser un número entero.")
        if id == 0:
            util.mensaje_info("Operación cancelada.")
            util.pausa()
            return
        producto = self.gestor_datos.buscar_producto(id)
        if not producto:
            util.mensaje_error(f"No se encontró un producto con ID {id}.")
            util.pausa()
            return

        stock_min_global = self.gestor_datos.leer_config()["STOCK_MIN_GLOBAL"]
        header = self.gestor_datos.leer_productos()[0]
        data = producto.to_list()
        idx = header.index("Stock Mínimo")

        if producto.stock_minimo is None or producto.stock_minimo == '' or producto.stock_minimo == 0:
            data[idx] = f"{stock_min_global} (Global)"
        else:
            data[idx] = f"{producto.stock_minimo} (Personalizado)"

        print(tb([data], header, 'fancy_grid'))

        print("\nIngrese los nuevos valores para el producto (deje en blanco para mantener el valor actual)\n")
        nombre = input(f'Nuevo nombre [{producto.nombre}]: ').strip() or producto.nombre

        while True:
            precio = input(f"Nuevo precio [{producto.precio}]: ").strip()
            if not precio:
                precio = producto.precio
                break
            try:
                precio = float(precio)
                if precio <= 0:
                    util.mensaje_error("El precio debe ser un número mayor a 0.")
                else:
                    break
            except ValueError:
                util.mensaje_error("Entrada inválida. Ingrese un número decimal.")

        while True:
            stock = input(f"Nuevo stock [{producto.stock}]: ").strip()
            if not stock:
                stock = producto.stock
                break
            try:
                stock = int(stock)
                if stock < 0:
                    util.mensaje_error("El stock no puede ser negativo.")
                else:
                    break
            except ValueError:
                util.mensaje_error("Entrada inválida. Ingrese un número entero.")

        while True:
            stock_min = input(f"Nuevo stock mínimo [{data[idx]}] (0 para usar global): ").strip()
            if not stock_min:
                stock_min = producto.stock_minimo
                break
            try:
                stock_min = int(stock_min)
                if stock_min == 0:
                    stock_min = None
                    break
                elif stock_min > 0:
                    break
                else:
                    util.mensaje_error("El stock mínimo debe ser un número mayor a 0 o 0 para usar el global.")
            except ValueError:
                util.mensaje_error("Entrada inválida. Ingrese un número entero o '0'.")

        if stock_min is None or stock_min == '' or stock_min == 0:
            stock_min_display = f'{stock_min_global} (Global)'
        else:
            stock_min_display = f'{stock_min} (Personalizado)'

        new_data = [data[1:], [nombre, precio, stock, stock_min_display]]

        print("\nResumen de cambios:")
        print(tb(new_data, header[1:], 'fancy_grid'))
        confirmacion = input("¿Desea confirmar los cambios? (s/n): ").strip().lower()
        if confirmacion != 's':
            util.mensaje_info("Cambios cancelados.")
            util.pausa()
            return

        producto.nombre, producto.precio, producto.stock, producto.stock_minimo = nombre, precio, stock, stock_min
        self.gestor_datos.actualizar_producto(producto)
        util.mensaje_exito(f"Producto [ID: {producto.id}, Nombre: {producto.nombre}] actualizado correctamente.")
        util.pausa()


    def mostrar_bajo_stock(self):
        global_stock_min = self.gestor_datos.leer_config()["STOCK_MIN_GLOBAL"]
        header, data = self.gestor_datos.leer_productos()
        if not data:
            util.mensaje_error("No hay productos registrados en el inventario.")
            return

        idx_stock_min = header.index("Stock Mínimo")
        idx_stock = header.index("Stock")

        bajo_stock = []
        for row in data:

            stock = row[idx_stock]
            stock_minimo = row[idx_stock_min]

            if stock_minimo is None or stock_minimo == "" or stock_minimo == 0:
                stock_minimo = global_stock_min
            if stock < stock_minimo:
                if stock_minimo == global_stock_min:
                    row[idx_stock_min] = f"{stock_minimo} (Global)"
                else:
                    row[idx_stock_min] = f"{stock_minimo} (Personalizado)"
                bajo_stock.append(row)

        if not bajo_stock:
            util.mensaje_info("No hay productos con stock por debajo del mínimo.")
            return

        header_display = [col for i, col in enumerate(header) if i != 2] # Exclude "Precio"
        bajo_stock = [[col for i, col in enumerate(row) if i != 2] for row in bajo_stock] # Exclude "Precio" from each row

        print('\nProductos con stock por debajo del mínimo:\n')
        print(tb(bajo_stock, header_display, 'fancy_grid'), '\n')


    def restock_producto(self):
        global_stock_minimo = self.gestor_datos.leer_config()["STOCK_MIN_GLOBAL"]
        util.limpiar_consola()
        print(util.crear_banner("Restock de Producto", util.Fore.LIGHTGREEN_EX))

        self.mostrar_bajo_stock()

        id = util.verificar_entrada("Ingrese el ID del producto a restockear (0 para cancelar)",
                                    int, "ID inválido. Debe ser un número entero.")
        if id == 0:
            util.mensaje_info("Operación cancelada.")
            util.pausa()
            return
        producto = self.gestor_datos.buscar_producto(id)
        if not producto:
            util.mensaje_error(f"No se encontró un producto con ID {id}.")
            util.pausa()
            return
        header, data = self.gestor_datos.leer_productos()[0], producto.to_list()
        header, data = header[:2] + header[3:], data[:2] + data[3:]

        idx_stock_min = header.index("Stock Mínimo")
        stock_minimo = data[idx_stock_min]
        if stock_minimo is None or stock_minimo == "" or stock_minimo == 0:
            data[idx_stock_min] = f"{global_stock_minimo} (Global)"
        else:
            data[idx_stock_min] = f"{stock_minimo} (Personalizado)"
        print(tb([data], header, 'fancy_grid'))

        stock = util.verificar_entrada("Ingrese la cantidad a restockear", int, "Cantidad inválida. Debe ser un número entero.")
        while stock <= 0:
            util.mensaje_error("La cantidad a restockear debe ser un número entero positivo.")
            stock = util.verificar_entrada("Ingrese la cantidad a restockear", int, "Cantidad inválida. Debe ser un número entero.")

        producto.stock += stock
        self.gestor_datos.actualizar_producto(producto)
        util.mensaje_exito(f"Producto [ID: {producto.id}, Nombre: {producto.nombre}] restockeado correctamente. Nuevo stock: {producto.stock}.")
        util.pausa()


    def eliminar_producto(self):
        util.limpiar_consola()
        print(util.crear_banner("Eliminar producto", util.Fore.LIGHTGREEN_EX,
                                "Advertencia: Esta acción no se puede deshacer.", util.Fore.LIGHTRED_EX))

        id = util.verificar_entrada("Ingrese el id del producto a eliminar (0 para cancelar)",
                                    int, "ID no valido. Intente otra vez")
        if id == 0:
            util.mensaje_info("Operación cancelada.")
            util.pausa()
            return
        producto = self.gestor_datos.buscar_producto(id)
        if not producto:
            util.mensaje_error(f"No se encontró un producto con ID {id}.")
            util.pausa()
            return

        print(util.Fore.LIGHTRED_EX + "Estas por eliminar el siguiente producto:")
        header, data = self.gestor_datos.leer_productos()[0], producto.to_list()
        print(tb([data[:2]], header[:2], 'fancy_grid'))
        confirmacion = input(util.Fore.LIGHTRED_EX + "Estas seguro de que quieres eliminar este producto? (s/n): ")
        if confirmacion.lower() != 's':
            util.mensaje_info("Operación cancelada.")
            util.pausa()
            return
        self.gestor_datos.eliminar_producto(id)
        util.mensaje_exito(f"Producto [ID: {producto.id}, Nombre: {producto.nombre}] eliminado correctamente.")
        util.pausa()


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
                    self.ver_inv()
                case 2:
                    self.agregar_producto()
                case 3:
                    self.editar_producto()
                case 4:
                    self.restock_producto()
                case 5:
                    self.eliminar_producto()
                case 6:
                    break
                case _:
                    util.mensaje_error("Opción inválida. Intente de nuevo con un valor del 1 al 5.")
                    util.pausa()