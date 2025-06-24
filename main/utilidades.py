import os
from colorama import Fore


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

def crear_banner(titulo: str, color = Fore.CYAN, sub_titulo: str = None, color_sub_titulo = None):
    """
        Crea un banner decorativo para la consola.

        Genera un marco con el título y opcionalmente un subtítulo, usando un color.

        :param titulo: str: Texto principal del banner.
        :param color: colorama.Fore: Color del banner (e.g., Fore.CYAN). Por defecto es cian.
        :param sub_titulo: Optional[str]: Texto secundario debajo del título. Por defecto es None.
        :param color_sub_titulo: Optional[colorama.Fore]: Color específico para el texto del subtítulo. Si es None, usa el 'color' principal.
        :returns: str: La cadena de texto del banner con formato y color.
    """
    max_len = max(len(titulo), len(sub_titulo)) if sub_titulo else len(titulo)
    sub_titulo_color = color_sub_titulo if color_sub_titulo is not None else color

    borde = "═" * (max_len + 8)

    if sub_titulo:
        banner = (
                color + f"\n╔{borde}╗\n"
                + f"║    {titulo.center(max_len)}    ║\n"
                + "║" + sub_titulo_color + f"    {sub_titulo.center(max_len)}    " + color +"║\n"
                + f"╚{borde}╝\n\n"
        )
    else:
        banner = (
                color + f"\n╔{borde}╗\n"
                + f"║    {titulo.center(max_len)}    ║\n"
                + f"╚{borde}╝\n\n"
        )

    return banner

def mostrar_menu(titulo: str, opciones: list, color = Fore.CYAN, sub_titulo: str = None, color_sub_titulo = None):
    """
        Muestra un menú en la consola con un banner y una lista numerada de opciones.

        Utiliza `crear_banner()` para el encabezado y lista las opciones dadas.
        Permite personalizar el color del título y opcionalmente el del subtítulo.

        :param titulo: str: Título principal del menú.
        :param opciones: list: Lista de cadenas con las opciones del menú.
        :param color: colorama.Fore: Color del banner del menú. Por defecto es cian.
        :param sub_titulo: Optional[str]: Subtítulo opcional para el banner del menú. Por defecto es None.
        :param color_sub_titulo: Optional[colorama.Fore]: Color específico para el texto del subtítulo. Si es None, usa el 'color' principal.
        :returns: str: La cadena de texto completa del menú con formato.
    """
    baner = crear_banner(titulo, color, sub_titulo, color_sub_titulo)

    menu_opciones = ""
    for i, opcione in enumerate(opciones, 1):
        menu_opciones += f"{i}. {opcione}\n"

    return baner + Fore.WHITE + menu_opciones


def mensaje_exito(mensaje: str):
    """
        Muestra un mensaje de éxito en color verde.

        :param mensaje: str: El mensaje a mostrar.
    """
    print(Fore.GREEN + f"\n✅ {mensaje}\n")

def mensaje_error(mensaje: str):
    """
        Muestra un mensaje de error en color rojo.

        :param mensaje: str: El mensaje a mostrar.
    """
    print(Fore.RED + f"\n❌ {mensaje}\n")

def mensaje_info(mensaje: str):
    """
        Muestra un mensaje informativo en color amarillo.

        :param mensaje: str: El mensaje a mostrar.
    """
    print(Fore.YELLOW + f"\nℹ️ {mensaje}\n")

def reportar_resultado(mensaje: str, exito: bool = True):
    """
        Muestra un mensaje de éxito o error según el valor de `exito`.

        :param mensaje: str: El mensaje a mostrar.
        :param exito: bool: Si es True, muestra el mensaje como éxito; si es False, como error.
    """
    if exito:
        mensaje_exito(mensaje)
    else:
        mensaje_error(mensaje)

def verificar_entrada(mensaje_entrada: str, tipo_dato: type[int | float], error: str = "Entrada inválida."):
    """
        Solicita al usuario un número (entero o flotante) y valida la entrada.

        Continúa solicitando hasta que se ingrese un número válido del tipo especificado.

        :param mensaje_entrada: str: El mensaje que se muestra al usuario para solicitar la entrada.
        :param tipo_dato: type[int | float]: El tipo de número esperado (int para enteros, float para decimales).
        :param error: str: El mensaje de error que se muestra si la entrada no es un número válido. (Por defecto: "Entrada inválida.").
        :returns: int | float: El número válido ingresado por el usuario, del tipo especificado.
    """

    if not mensaje_entrada.endswith(": "):
        mensaje_entrada += ": "

    while True:
        try:
            entrada = tipo_dato(input(mensaje_entrada))
            return entrada
        except ValueError:
            if error == "Entrada inválida.":
                if tipo_dato == int:
                    error = "Entrada inválida. Debe ser un número entero."
                else:
                    error = "Entrada inválida. Debe ser un número decimal."
            mensaje_error(error)