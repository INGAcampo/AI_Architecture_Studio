# AIAS Workspace 2.0 — W2-02

W2-02 establishes one recoverable authority for the professional desktop session. It composes the proven `WorkspaceManager` rather than duplicating document, panel, docking or event behavior.

A session now binds open documents, active document, selection, tool, panel descriptors, panel geometry and visibility to the active professional profile, semantic theme, jurisdiction and review state. Recovery files are written atomically and contain a canonical SHA-256 digest. Restoration is transactional: all fields and the checksum are validated before the active session changes.

This provides the continuity foundation required for interrupted engineering work. It does not imply that an unsaved engineering model has been persisted internally; individual document storage remains responsible for model contents.
