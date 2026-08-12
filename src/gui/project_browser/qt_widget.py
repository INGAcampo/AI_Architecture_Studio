from __future__ import annotations

from typing import Any

from .controller import ProjectBrowserController
from .model import BrowserNodeKind
from aias_i18n import get_translator

try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QLineEdit,
        QMenu,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    Qt = QAction = QAbstractItemView = QLineEdit = QMenu = None
    QTreeWidget = QTreeWidgetItem = QVBoxLayout = QWidget = None


class QtUnavailableError(RuntimeError):
    pass


def require_qt(translator=None) -> None:
    if QWidget is None:
        raise QtUnavailableError((translator or get_translator()).translate("error.qt_project_browser"))


class ProjectBrowserWidget(QWidget if QWidget is not None else object):
    ROLE_NODE_ID = 0x0100

    def __init__(
        self,
        controller: ProjectBrowserController,
        parent: Any = None,
    ) -> None:
        self.translator = get_translator()
        require_qt(self.translator)
        super().__init__(parent)
        self.controller = controller
        self._items: dict[str, QTreeWidgetItem] = {}
        self._syncing = False

        self.search = QLineEdit(self)
        self.search.setPlaceholderText(self.translator.translate("browser.search"))
        self.tree = QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.search)
        layout.addWidget(self.tree)

        self.search.textChanged.connect(self.apply_filter)
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree.itemExpanded.connect(
            lambda item: self._on_expanded_changed(item, True)
        )
        self.tree.itemCollapsed.connect(
            lambda item: self._on_expanded_changed(item, False)
        )
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.rebuild()

    def rebuild(self) -> None:
        self._syncing = True
        try:
            self.tree.clear()
            self._items.clear()
            root_node = self.controller.model.require(
                self.controller.model.ROOT_ID
            )
            root_item = self._create_item(root_node)
            self.tree.addTopLevelItem(root_item)
            self._append_children(root_node.node_id, root_item)
            root_item.setExpanded(True)
            self.restore_state()
        finally:
            self._syncing = False

    def _append_children(
        self,
        node_id: str,
        parent_item: QTreeWidgetItem,
    ) -> None:
        for node in self.controller.model.children_of(node_id):
            item = self._create_item(node)
            parent_item.addChild(item)
            self._append_children(node.node_id, item)

    def _create_item(self, node) -> QTreeWidgetItem:
        item = QTreeWidgetItem([node.title])
        item.setData(0, self.ROLE_NODE_ID, node.node_id)
        if node.kind is BrowserNodeKind.OBJECT:
            item.setToolTip(
                0,
                f"{node.metadata.get('category', '')} · "
                f"{node.metadata.get('level', '')}",
            )
        self._items[node.node_id] = item
        return item

    def apply_filter(self, text: str) -> None:
        matches = {
            node.node_id for node in self.controller.set_filter(text)
        }
        active = bool(text.strip())

        for node_id, item in self._items.items():
            visible = not active or node_id in matches or self._has_match_descendant(
                item, matches
            )
            item.setHidden(not visible)

        if active:
            self.tree.expandAll()

    def _has_match_descendant(
        self,
        item: QTreeWidgetItem,
        matches: set[str],
    ) -> bool:
        for index in range(item.childCount()):
            child = item.child(index)
            node_id = child.data(0, self.ROLE_NODE_ID)
            if node_id in matches or self._has_match_descendant(child, matches):
                return True
        return False

    def restore_state(self) -> None:
        for node_id, item in self._items.items():
            item.setExpanded(
                node_id in self.controller.state.expanded_node_ids
            )

        selected = self.controller.state.selected_node_id
        if selected and selected in self._items:
            self.tree.setCurrentItem(self._items[selected])

        if self.search.text() != self.controller.state.filter_text:
            self.search.setText(self.controller.state.filter_text)

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
        items = self.tree.selectedItems()
        if not items:
            self.controller.select_node(None)
            return
        node_id = items[0].data(0, self.ROLE_NODE_ID)
        self.controller.select_node(node_id)

    def _on_expanded_changed(
        self,
        item: QTreeWidgetItem,
        expanded: bool,
    ) -> None:
        if self._syncing:
            return
        node_id = item.data(0, self.ROLE_NODE_ID)
        self.controller.set_expanded(node_id, expanded)

    def _show_context_menu(self, position) -> None:
        item = self.tree.itemAt(position)
        if item is None:
            return

        node_id = item.data(0, self.ROLE_NODE_ID)
        node = self.controller.model.require(node_id)
        menu = QMenu(self)

        select_action = QAction(self.translator.translate("browser.select"), self)
        select_action.setEnabled(node.object_id is not None)
        select_action.triggered.connect(
            lambda: self.controller.select_node(node_id)
        )
        menu.addAction(select_action)

        expand_action = QAction(self.translator.translate("browser.expand"), self)
        expand_action.triggered.connect(item.setExpanded)
        menu.addAction(expand_action)

        collapse_action = QAction(self.translator.translate("browser.collapse"), self)
        collapse_action.triggered.connect(lambda: item.setExpanded(False))
        menu.addAction(collapse_action)

        menu.exec(self.tree.viewport().mapToGlobal(position))
