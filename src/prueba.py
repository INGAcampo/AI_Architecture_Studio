import sys

from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

ventana = QWidget()
ventana.setWindowTitle("PRUEBA")
ventana.resize(500, 300)

print("Antes de show()")

ventana.show()

print("Después de show()")
print("¿Visible?:", ventana.isVisible())
print("Geometría:", ventana.geometry())

sys.exit(app.exec())