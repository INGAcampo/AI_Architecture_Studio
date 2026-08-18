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
from aias_i18n import get_translator


class NewProjectDialog(QDialog):

    def __init__(self, project_manager, parent=None, translator=None):
        super().__init__(parent)

        self.project_manager = project_manager
        self.translator = translator or get_translator()

        self.setWindowTitle(self.translator.translate("new_project.title"))
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

        form.addRow(self.translator.translate("new_project.name"), self.name_input)
        form.addRow(self.translator.translate("new_project.client"), self.client_input)
        form.addRow(self.translator.translate("new_project.location"), self.location_input)
        form.addRow(self.translator.translate("new_project.standard"), self.standard_input)

        self.create_button = QPushButton(self.translator.translate("new_project.create"))
        self.create_button.clicked.connect(self.create_project)

        layout.addLayout(form)
        layout.addWidget(self.create_button)

    def create_project(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                self.translator.translate("new_project.missing_title"),
                self.translator.translate("new_project.missing_name")
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
            self.translator.translate("new_project.created_title"),
            self.translator.translate("new_project.created_message",project_file=project_file)
        )

        self.accept()
