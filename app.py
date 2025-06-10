from colorama import init
from main.menu import Menu
from main.configuracion import Configuracion


class App:
    def __init__(self):
        init(autoreset=True)

        self.confing = Configuracion()
        self.menu = Menu(self)

    def run(self):
        try:
            self.menu.main()
        finally:
            print("\n🎉 ¡Hasta luego! Gracias por usar GestiOne.\n")


if __name__ == "__main__":
    app = App()
    app.run()