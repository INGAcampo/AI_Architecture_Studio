"""
AI Architecture Studio
New Project Dialog

Versión: Alpha 0.2
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)


class NewProjectDialog(QDialog):

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)

        self.project_manager = project_manager

        self.setWindowTitle("Nuevo Proyecto AIAS")
        self.resize(450, 300)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.client_input = QLineEdit()
        self.location_input = QLineEdit()

        self.standard_input = QComboBox()
        self.standard_input.addItems([
            "ACI 318",
            "AISC 360",
            "ASCE 7",
            "Eurocode",
            "NSR",
            "NEC",
            "CIRSOC",
            "NTC",
        ])

        form.addRow("Nombre del proyecto:", self.name_input)
        form.addRow("Cliente:", self.client_input)
        form.addRow("Ubicación:", self.location_input)
        form.addRow("Norma:", self.standard_input)

        self.create_button = QPushButton("Crear Proyecto")
        self.create_button.clicked.connect(self.create_project)

        layout.addLayout(form)
        layout.addWidget(self.create_button)

    def create_project(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Dato faltante",
                "Debes escribir el nombre del proyecto."
            )
            return

        client = self.client_input.text().strip()
        location = self.location_input.text().strip()
        standard = self.standard_input.currentText()

        project_file = self.project_manager.create_project(
            name=name,
            client=client,
            location=location,
            standard=standard,
        )

        QMessageBox.information(
            self,
            "Proyecto creado",
            f"Proyecto creado correctamente:\n{project_file}"
        )

        self.accept()