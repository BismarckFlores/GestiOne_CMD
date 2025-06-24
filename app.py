from colorama import init
from pruevas.GestiOne_v2_2.dao.configuracion import Configuracion
from pruevas.GestiOne_v2_2.main.menu_principal import MenuPrincipal


class App:
    def __init__(self):
        init(autoreset=True)
        self.config = Configuracion()
        self.menu = MenuPrincipal(self.config)

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