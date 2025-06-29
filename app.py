from colorama import init
from dao.gestor_datos import GestorDatos
from main.menu_principal import MenuPrincipal


class App:
    def __init__(self):
        init(autoreset=True)
        self.gestor_datos = GestorDatos()
        self.menu = MenuPrincipal(self.gestor_datos)

    def run(self):
        try:
            self.menu.menu()
        except KeyboardInterrupt:
            print('\n\n⏹️ Interrupción del usuario. Saliendo de la aplicación...')
        finally:
            print("\n🎉 ¡Hasta luego! Gracias por usar la aplicación.\n")

if __name__ == "__main__":
    app = App()
    app.run()