"""
AI Architecture Studio
Workspace Profesional

Versión: Foundation 1.1
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from engines.cad.canvas import CadCanvas


class Workspace(QWidget):

    def __init__(self, scene=None, parent=None):
        super().__init__(parent)

        self.scene = scene

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        layout.addWidget(self.tabs)

        self.add_home_tab()

    def add_home_tab(self):
        canvas = CadCanvas(scene=self.scene)
        self.tabs.addTab(canvas, "Inicio")

    def add_document_tab(self, title):
        canvas = CadCanvas(scene=self.scene)
        self.tabs.addTab(canvas, title)
        self.tabs.setCurrentWidget(canvas)

    def close_tab(self, index):
        if index > 0:
            self.tabs.removeTab(index)

    def current_canvas(self):
        return self.tabs.currentWidget()