"""
    Módulo principal de la aplicación GestiOne.

    Este módulo inicializa la aplicación, gestiona el ciclo de vida principal y el flujo de autenticación de usuarios.
    Permite el acceso a las funcionalidades de inventario, ventas y configuración a través de menús interactivos.
    Utiliza los módulos de utilidades, gestor de datos y menús para la interacción con el usuario y la gestión de datos.
"""
from colorama import init
from time import sleep as sp
from main.utilidades import *
from dao.gestor_datos import GestorDatos
from main.menu_principal import MenuPrincipal


class App:
    def __init__(self):
        init(autoreset=True)
        self.gestor_datos = GestorDatos()
        self.current_user = None
        self.menu = None


    def login(self):
        for i in range(3, 0, -1):
            limpiar_consola()
            print(crear_banner('Bienvenido a GestiOne', Fore.CYAN, f'Iniciar Sesión en {self.gestor_datos.leer_config()['NOMBRE_NEGOCIO']}'))
            username = input("Ingrese su nombre de usuario: ").strip()
            # if username == 'app.admin.test':
            #     self.current_user = 'Admin'
            #     print('\n 🔑 Has accedido como usuario de prueba "app.admin.test".')
            #     sp(3)
            #     return True
            # if username == 'app.user.test':
            #     self.current_user = 'User'
            #     print('\n 🔑 Has accedido como usuario de prueba "app.user.test".')
            #     sp(3)
            #     return True
            password = pedir_contrasenia("Ingrese su contraseña")
            if self.gestor_datos.verificar_usuario(username, password):
                self.current_user = username
                print(f"\n🔑 Bienvenido, {username}!")
                sp(3)
                return True
            else:
                mensaje_error(f'Credenciales incorrectas. Intentos restantes {i - 2}.')
                pausa()
        mensaje_error('Demasiados intentos fallidos. Saliendo de la aplicación...')
        return False


    def run(self):
        try:
            if self.login():
                self.menu = MenuPrincipal(self.gestor_datos, self.current_user)
                self.menu.menu()
        except KeyboardInterrupt:
            print('\n\n⏹️ Interrupción del usuario. Saliendo de la aplicación...')
        finally:
            print("\n🎉 ¡Hasta luego! Gracias por usar la aplicación.\n")

if __name__ == "__main__":
    app = App()
    app.run()