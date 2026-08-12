from PySide6.QtCore import Qt,Signal
from PySide6.QtWidgets import QComboBox,QHBoxLayout,QLabel,QLineEdit,QScrollArea,QToolButton,QVBoxLayout,QWidget
from .controller import InspectorController,InspectorFilter
from .editor_factory import PropertyEditorFactory
from aias_i18n import tr
class BimPropertyInspector(QWidget):
    property_changed=Signal(str,object);inspection_changed=Signal(object)
    FILTERS={'Todos':InspectorFilter.ALL,'Editables':InspectorFilter.EDITABLE,'Compartidos':InspectorFilter.SHARED,'Calculados':InspectorFilter.CALCULATED,'IFC':InspectorFilter.IFC,'Modificados':InspectorFilter.MODIFIED}
    def __init__(self,controller=None,parent=None):super().__init__(parent);self.controller=controller or InspectorController();self._ui();self.clear()
    def _ui(self):
        r=QVBoxLayout(self);r.setContentsMargins(6,6,6,6);self.title=QLabel(tr("inspector.none"));r.addWidget(self.title)
        h=QHBoxLayout();self.search=QLineEdit();self.search.setPlaceholderText(tr("inspector.search"));self.search.setClearButtonEnabled(True);self.search.textChanged.connect(self.refresh);h.addWidget(self.search,1)
        self.filters=QComboBox();self.filters.addItems(self.FILTERS);self.filters.currentTextChanged.connect(self.refresh);h.addWidget(self.filters);r.addLayout(h)
        self.scroll=QScrollArea();self.scroll.setWidgetResizable(True);self.content=QWidget();self.layout=QVBoxLayout(self.content);self.layout.addStretch(1);self.scroll.setWidget(self.content);r.addWidget(self.scroll,1)
    def inspect(self,e):self.controller.inspect(e);self.title.setText(str(getattr(e,'name',tr("element.default")) if e else tr("inspector.none")));self.refresh();self.inspection_changed.emit(e)
    def clear(self):self.controller.clear();self.title.setText(tr("inspector.none"));self.refresh()
    def refresh(self,*_):
        while self.layout.count()>1:
            it=self.layout.takeAt(0);w=it.widget();w.deleteLater() if w else None
        groups=self.controller.grouped(self.search.text(),self.FILTERS[self.filters.currentText()])
        if not groups:
            l=QLabel(tr("inspector.empty"));l.setAlignment(Qt.AlignCenter);l.setEnabled(False);self.layout.insertWidget(0,l);return
        idx=0
        for group,items in groups.items():
            box=QWidget();bl=QVBoxLayout(box);bl.setContentsMargins(0,0,0,0);toggle=QToolButton();toggle.setText('▾  '+group);toggle.setCheckable(True);toggle.setChecked(True);bl.addWidget(toggle)
            body=QWidget();body_l=QVBoxLayout(body);body_l.setContentsMargins(12,2,2,6)
            for p in items:
                row=QWidget();rl=QHBoxLayout(row);rl.setContentsMargins(0,0,0,0);marks=[]
                if p.shared:marks.append('S')
                if p.calculated:marks.append('ƒ')
                if p.ifc:marks.append('IFC')
                if not p.editable:marks.append('🔒')
                label=QLabel(p.display_name+('  ['+' · '.join(marks)+']' if marks else ''));label.setMinimumWidth(125);rl.addWidget(label,1)
                if p.editable and p.setter:
                    try:editor=PropertyEditorFactory.create(p,row);rl.addWidget(editor,1)
                    except Exception:rl.addWidget(QLabel(str(p.value)),1)
                else:rl.addWidget(QLabel(str(p.value)),1)
                body_l.addWidget(row)
            toggle.toggled.connect(body.setVisible);bl.addWidget(body);self.layout.insertWidget(idx,box);idx+=1
