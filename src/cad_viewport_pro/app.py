import sys
from PySide6.QtWidgets import QApplication
from .main_window import CadViewportMainWindow

def main():
    app=QApplication.instance() or QApplication(sys.argv)
    window=CadViewportMainWindow(); window.show()
    return app.exec()

if __name__=="__main__":
    raise SystemExit(main())
