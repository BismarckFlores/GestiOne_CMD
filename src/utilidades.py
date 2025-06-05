import os
from colorama import Fore, init


init(autoreset=True)

def limpiar_consola():
    """
        Limpia la pantalla de la consola.

        Detecta el sistema operativo para usar 'cls' (Windows) o 'clear' (Unix/macOS).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    """
        Pausa la ejecución del programa hasta que el usuario presione Enter.
    """
    input("\n🔄 Presiona Enter para continuar...")

def crear_banner(titulo: str, sub_titulo: str = None, color = Fore.CYAN):
    """
        Crea un banner ASCII decorativo para la consola.

        Genera un marco con el título y opcionalmente un subtítulo, usando un color.

        :param titulo: str: Texto principal del banner.
        :param sub_titulo: Optional[str]: Texto secundario debajo del título. Por defecto es None.
        :param color: colorama.Fore: Color del banner (e.g., Fore.CYAN). Por defecto es cian.
        :returns: str: La cadena de texto del banner con formato y color.
    """
    if sub_titulo:
        max_len = max(len(titulo), len(sub_titulo))
    else:
        max_len = len(titulo)

    borde = "═" * (max_len + 8)

    if sub_titulo:
        banner = (
                color + f"\n╔{borde}╗\n"
                + f"║    {titulo.center(max_len)}    ║\n"
                + f"║    {sub_titulo.center(max_len)}    ║\n"
                + f"╚{borde}╝\n"
        )
    else:
        banner = (
                color + f"\n╔{borde}╗\n"
                + f"║    {titulo.center(max_len)}    ║\n"
                + f"╚{borde}╝\n"
        )

    return banner

def mostrar_menu(titulo: str, opciones: list, sub_titulo: str = None, color=Fore.CYAN):
    """
        Muestra un menú en la consola con un banner y una lista numerada de opciones.

        Utiliza `crear_banner()` para el encabezado y lista las opciones dadas.

        :param titulo: str: Título principal del menú.
        :param opciones: list: Lista de cadenas con las opciones del menú.
        :param sub_titulo: Optional[str]: Subtítulo opcional para el banner del menú. Por defecto es None.
        :param color: colorama.Fore: Color del banner del menú. Por defecto es cian.
        :returns: str: La cadena de texto completa del menú con formato.
    """
    baner = crear_banner(titulo, sub_titulo, color)

    menu_opciones = ""
    for i, opcione in enumerate(opciones, 1):
        menu_opciones += f"{i}. {opcione}\n"

    return baner + Fore.WHITE + menu_opciones


def mensaje_exito(mensaje):
    """
        Muestra un mensaje de éxito en color verde.

        :param mensaje: str: El mensaje a mostrar.
    """
    print(Fore.GREEN + f"\n✅ {mensaje}\n")

def mensaje_error(mensaje):
    """
        Muestra un mensaje de error en color rojo.

        :param mensaje: str: El mensaje a mostrar.
    """
    print(Fore.RED + f"\n❌ {mensaje}\n")