# Design Specification — S2.06A

El Workspace es una capa de aplicación independiente de PySide6. Mantiene documentos,
paneles, selección, herramienta activa y layouts persistentes. La GUI consume esta API,
pero el núcleo puede probarse sin crear `QApplication`.
