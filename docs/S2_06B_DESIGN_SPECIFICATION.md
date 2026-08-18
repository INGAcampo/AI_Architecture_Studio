# Design Specification — S2.06B

`QtDockingController` es un adaptador, no el dueño del estado. La fuente canónica
continúa siendo `WorkspaceManager`. Las señales de Qt se traducen en cambios del
Workspace y los estados restaurados se aplican nuevamente a los widgets.
