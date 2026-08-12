"""Desktop application entrypoint for the S1 CAD foundation program."""
import sys
from PySide6.QtWidgets import QApplication
from .workspace import CadProgramS1Window

def main():
    """Create the Qt application, show the CAD workspace and enter its event loop."""
    app=QApplication.instance() or QApplication(sys.argv)
    window=CadProgramS1Window(); window.show()
    return app.exec()

if __name__=="__main__":
    raise SystemExit(main())
