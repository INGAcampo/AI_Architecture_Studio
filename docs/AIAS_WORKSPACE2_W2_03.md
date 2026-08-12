# AIAS Workspace 2.0 — W2-03

W2-03 establishes a single selection path among the project/BIM browser, graphical canvas and typed property inspector. Stable engineering-object identifiers are mandatory and duplicates fail closed. Selection state is retained in `WorkspaceManager`, while the coordinator resolves identifiers to real model objects before exposing properties.

Selections that refer to absent objects remain explicit in synchronization evidence and never generate invented property values. Selecting a grouping node clears object properties. Existing property validation and undo mechanisms remain authoritative.

The integration is framework-neutral and testable without a display server. Qt layout composition and visual usability remain separate rendered gates.
