import sys
from PySide6.QtWidgets import QApplication
from .main_window import ProfessionalMainWindow

def main():
    app=QApplication.instance() or QApplication(sys.argv)
    window=ProfessionalMainWindow(); window.show()
    return app.exec()

if __name__=="__main__":
    raise SystemExit(main())
