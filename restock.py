import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')
#Esto lo pongo para mientras porque no tengo la otra parte del código que establece el inventario 
def definir_inventario():
    inventario = {}
    print("=== Definir inventario inicial ===")
    while True:
        producto = input("Nombre del producto (o escribe 'fin' para terminar inventario): ").strip()
        if producto.lower() == 'fin':
            break
        try:
            cantidad = int(input(f"Cantidad de '{producto}': "))
            inventario[producto] = cantidad
        except ValueError:
            print("Por favor, ingresa un número válido.")
    return inventario

def hacer_restock(inventario):
    limpiar_consola()
    print("=== Hacer restock de productos ===")
    while True:
        producto = input("Producto a reabastecer (Escribe 'fin' para terminar): ").strip()
        if producto.lower() == 'fin':
            break
        try:
            cantidad = int(input(f"Cantidad a agregar de '{producto}': "))
            if producto in inventario:
                inventario[producto] += cantidad
                print(f"Se añadieron {cantidad} unidades a '{producto}'. Total: {inventario[producto]}")
            else:
                inventario[producto] = cantidad
                print(f"Producto nuevo '{producto}' añadido con {cantidad} unidades.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def mostrar_inventario(inventario):
    limpiar_consola()
    print("=== Inventario final ===")
    for producto, cantidad in inventario.items():
        print(f"{producto}: {cantidad}")

# Programa principal
limpiar_consola()
inventario = definir_inventario()
hacer_restock(inventario)
mostrar_inventario(inventario)
