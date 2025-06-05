import os
from colorama import Fore, init


init(autoreset=True)

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input("\n🔄 Presiona Enter para continuar...")

def crear_banner(titulo, sub_titulo=None,  color=Fore.CYAN):
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
    """Test"""
    baner = crear_banner(titulo, sub_titulo, color)

    menu_opciones = ""
    for i, opcione in enumerate(opciones, 1):
        menu_opciones += f"{i}. {opcione}\n"

    return baner + Fore.WHITE + menu_opciones


def mensaje_exito(mensaje):
    print(Fore.GREEN + f"\n✅ {mensaje}\n")

def mensaje_error(mensaje):
    print(Fore.RED + f"\n❌ {mensaje}\n")
