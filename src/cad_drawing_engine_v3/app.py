import sys
from PySide6.QtWidgets import QApplication
from .main_window import DrawingMainWindow

def main():
    app=QApplication.instance() or QApplication(sys.argv)
    window=DrawingMainWindow(); window.show()
    return app.exec()

if __name__=="__main__":
    raise SystemExit(main())
