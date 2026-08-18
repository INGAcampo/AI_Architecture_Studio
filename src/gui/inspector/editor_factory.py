from datetime import date
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QCheckBox,QDateEdit,QDoubleSpinBox,QLineEdit,QSpinBox
class PropertyEditorFactory:
    @staticmethod
    def create(item,parent=None):
        t=str(item.property_type).casefold()
        if t=='boolean':
            w=QCheckBox(parent);w.setChecked(bool(item.value));w.stateChanged.connect(lambda _s:item.set_value(w.isChecked()));return w
        if t=='integer':
            w=QSpinBox(parent);w.setRange(-2147483648,2147483647);w.setValue(int(item.value or 0));w.valueChanged.connect(item.set_value);return w
        if t in {'decimal','length','area','volume','angle','force','pressure','temperature'}:
            w=QDoubleSpinBox(parent);w.setDecimals(6);w.setRange(-1e12,1e12);w.setValue(float(item.value or 0));
            if item.unit:w.setSuffix(' '+item.unit)
            w.valueChanged.connect(item.set_value);return w
        if t=='date':
            w=QDateEdit(parent);w.setCalendarPopup(True)
            if isinstance(item.value,date):w.setDate(QDate(item.value.year,item.value.month,item.value.day))
            w.dateChanged.connect(lambda d:item.set_value(date(d.year(),d.month(),d.day())));return w
        w=QLineEdit(parent);w.setText('' if item.value is None else str(item.value));w.editingFinished.connect(lambda:item.set_value(w.text()));return w
