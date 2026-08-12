from __future__ import annotations

from typing import Any

from .controller import BimWorkspaceController
from .entities import BimWorkspaceNodeKind

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QComboBox,
        QHBoxLayout,
        QLineEdit,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    Qt = None
    QAbstractItemView = QComboBox = QHBoxLayout = QLineEdit = None
    QTreeWidget = QTreeWidgetItem = QVBoxLayout = QWidget = None


class QtUnavailableError(RuntimeError):
    pass


def require_qt() -> None:
    if QWidget is None:
        raise QtUnavailableError("PySide6 no está disponible para BIM Workspace Suite.")


class BimWorkspaceWidget(QWidget if QWidget is not None else object):
    ROLE_NODE_ID = 0x0100

    FILTERS = (
        ("Todos", None),
        ("Niveles", BimWorkspaceNodeKind.LEVEL),
        ("Familias", BimWorkspaceNodeKind.FAMILY),
        ("Tipos", BimWorkspaceNodeKind.TYPE),
        ("Instancias", BimWorkspaceNodeKind.INSTANCE),
        ("Materiales", BimWorkspaceNodeKind.MATERIAL),
        ("Fases", BimWorkspaceNodeKind.PHASE),
    )

    def __init__(self, controller: BimWorkspaceController, parent: Any = None) -> None:
        require_qt()
        super().__init__(parent)
        self.controller = controller
        self._items: dict[str, QTreeWidgetItem] = {}
        self._syncing = False

        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Buscar en el modelo BIM…")
        self.kind_filter = QComboBox(self)
        for label, kind in self.FILTERS:
            self.kind_filter.addItem(label, kind.value if kind else "")

        controls = QHBoxLayout()
        controls.addWidget(self.search)
        controls.addWidget(self.kind_filter)

        self.tree = QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(controls)
        layout.addWidget(self.tree)

        self.search.textChanged.connect(self.apply_filter)
        self.kind_filter.currentIndexChanged.connect(
            lambda _index: self.apply_filter(self.search.text())
        )
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemExpanded.connect(
            lambda item: self._on_expanded_changed(item, True)
        )
        self.tree.itemCollapsed.connect(
            lambda item: self._on_expanded_changed(item, False)
        )
        self.rebuild()

    def rebuild(self) -> None:
        self._syncing = True
        try:
            self.tree.clear()
            self._items.clear()
            root = self.controller.tree.require(self.controller.tree.ROOT_ID)
            root_item = self._create_item(root)
            self.tree.addTopLevelItem(root_item)
            self._append_children(root.node_id, root_item)
            root_item.setExpanded(True)
            self.restore_state()
        finally:
            self._syncing = False

    def _append_children(self, node_id: str, parent_item: QTreeWidgetItem) -> None:
        for node in self.controller.tree.children_of(node_id):
            item = self._create_item(node)
            parent_item.addChild(item)
            self._append_children(node.node_id, item)

    def _create_item(self, node) -> QTreeWidgetItem:
        item = QTreeWidgetItem([node.title])
        item.setData(0, self.ROLE_NODE_ID, node.node_id)
        item.setToolTip(0, node.kind.value)
        self._items[node.node_id] = item
        return item

    def apply_filter(self, text: str) -> None:
        raw_kind = self.kind_filter.currentData()
        kinds = {BimWorkspaceNodeKind(raw_kind)} if raw_kind else set()
        matches = {
            node.node_id
            for node in self.controller.set_filter(text, kinds)
        }
        active = bool(text.strip() or kinds)

        for node_id, item in self._items.items():
            visible = not active or node_id in matches or self._has_visible_descendant(
                item, matches
            )
            item.setHidden(not visible)

        if active:
            self.tree.expandAll()

    def _has_visible_descendant(self, item: QTreeWidgetItem, matches: set[str]) -> bool:
        for index in range(item.childCount()):
            child = item.child(index)
            node_id = child.data(0, self.ROLE_NODE_ID)
            if node_id in matches or self._has_visible_descendant(child, matches):
                return True
        return False

    def restore_state(self) -> None:
        for node_id, item in self._items.items():
            item.setExpanded(node_id in self.controller.state.expanded_node_ids)
        selected = self.controller.state.selected_node_id
        if selected and selected in self._items:
            self.tree.setCurrentItem(self._items[selected])

    def select_object(self, object_id: str) -> bool:
        node_id = self.controller.select_object(object_id)
        if node_id is None or node_id not in self._items:
            return False
        self._syncing = True
        try:
            item = self._items[node_id]
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)
        finally:
            self._syncing = False
        return True

    def _on_selection_changed(self) -> None:
        if self._syncing:
            return
        selected = self.tree.selectedItems()
        if not selected:
            self.controller.select_node(None)
            return
        self.controller.select_node(
            selected[0].data(0, self.ROLE_NODE_ID)
        )

    def _on_expanded_changed(self, item: QTreeWidgetItem, expanded: bool) -> None:
        if self._syncing:
            return
        self.controller.set_expanded(
            item.data(0, self.ROLE_NODE_ID),
            expanded,
        )
