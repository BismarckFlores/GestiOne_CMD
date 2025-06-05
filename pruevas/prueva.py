import src.configuracion as config
import src.utilidades as util
from colorama import Fore


def main():
    config.iniciar_archivos()
    while True:
        util.limpiar_consola()
        menu = util.mostrar_menu("GESTIONE", ['📦 inventario', '📝 Ventas', '⚙️ Configuración', '🚪 Salir'], "Menú Principal", Fore.CYAN)
        print(menu)



if __name__ == "__main__":
    main()