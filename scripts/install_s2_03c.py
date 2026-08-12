from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/'src/gui/main_window.py';BACKUP=ROOT/'backups/s2_03c/main_window.py.bak'
IMPORT='from gui.inspector import BimPropertyInspector, InspectorController\n'
OLD_CREATE='''    def create_properties_panel(self):
        dock = QDockWidget(
            "Propiedades",
            self,
        )

        self.properties_list = QListWidget()

        dock.setWidget(
            self.properties_list
        )

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            dock,
        )
'''
NEW_CREATE='''    def create_properties_panel(self):
        dock = QDockWidget("Inspector BIM", self)
        property_service = None
        shared_library = None
        kernel = getattr(getattr(self, "app_core", None), "kernel", None)
        if kernel is not None:
            services = getattr(kernel, "services", None)
            if services is not None:
                try:
                    property_service = services.get("property_service")
                except Exception:
                    pass
                try:
                    shared_library = services.get("shared_parameter_library")
                except Exception:
                    pass
        self.properties_inspector = BimPropertyInspector(
            InspectorController(property_service, shared_library), self
        )
        dock.setWidget(self.properties_inspector)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
'''
OLD_CLEAR='''    def clear_properties(self):
        self.properties_list.clear()

        self.properties_list.addItems([
            "Nombre: Sin selección",
            "Tipo: -",
        ])
'''
NEW_CLEAR='''    def clear_properties(self):
        self.properties_inspector.clear()
'''
OLD_SHOW='''    def show_element_properties(self, element):
        self.properties_list.clear()

        if element is None:
            self.clear_properties()

            self.statusBar().showMessage(
                "Ningún objeto seleccionado"
            )
            return

        information = element.info()

        for key, value in information.items():
            if (
                key == "Propiedades"
                and isinstance(value, dict)
            ):
                self.properties_list.addItem(
                    "── Propiedades ──"
                )

                for (
                    property_name,
                    property_value,
                ) in value.items():
                    self.properties_list.addItem(
                        f"{property_name}: "
                        f"{property_value}"
                    )
            else:
                self.properties_list.addItem(
                    f"{key}: {value}"
                )

        self.statusBar().showMessage(
            f"Seleccionado: {element.name}"
        )
'''
NEW_SHOW='''    def show_element_properties(self, element):
        if element is None:
            self.clear_properties()
            self.statusBar().showMessage("Ningún objeto seleccionado")
            return
        self.properties_inspector.inspect(element)
        self.statusBar().showMessage(
            f"Seleccionado: {getattr(element, 'name', 'Elemento')}"
        )
'''
def repl(text,old,new,label):
    if new in text:return text
    if old not in text:raise RuntimeError('No se encontró '+label)
    return text.replace(old,new,1)
def main():
    if not TARGET.exists():print('ERROR: no existe',TARGET);return 2
    text=TARGET.read_text(encoding='utf-8')
    if IMPORT not in text:
        anchor='from gui.project_session import ProjectSessionController\n'
        if anchor not in text:print('ERROR: punto de importación no encontrado');return 3
        text=text.replace(anchor,anchor+IMPORT,1)
    try:
        text=repl(text,OLD_CREATE,NEW_CREATE,'create_properties_panel');text=repl(text,OLD_CLEAR,NEW_CLEAR,'clear_properties');text=repl(text,OLD_SHOW,NEW_SHOW,'show_element_properties')
    except RuntimeError as e:print('ERROR:',e);return 4
    BACKUP.parent.mkdir(parents=True,exist_ok=True)
    if not BACKUP.exists():shutil.copyfile(TARGET,BACKUP)
    TARGET.write_text(text,encoding='utf-8');print('RESULTADO: BIM PROPERTY INSPECTOR INSTALADO');print('Respaldo:',BACKUP);return 0
if __name__=='__main__':raise SystemExit(main())
