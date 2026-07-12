"""
AI Architecture Studio
Punto de entrada principal

Versión: Alpha 0.2
"""

import sys

from PySide6.QtWidgets import QApplication

from core.app import AIASApplication
from gui.main_window import MainWindow


def main():

    # Crear aplicación Qt
    app = QApplication(sys.argv)

    # Inicializar el núcleo de AIAS
    aias = AIASApplication()
    aias.start()

    # Crear ventana principal y pasar el núcleo
    window = MainWindow(app_core=aias)
    window.show()

    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()