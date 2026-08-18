"""Public module supporting the coordinated multi-studio desktop shell."""
import sys
from PySide6.QtWidgets import QApplication
from .shell_window import MultiStudioShellWindow

def main() -> int:
    """Execute the public main operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    app = QApplication.instance() or QApplication(sys.argv)
    window = MultiStudioShellWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
