# EXP-INSTALLER-ISO-001

AIAS now has one transactional distribution core. It verifies every selected installer, builds deterministic offline media, stages deployment under an explicitly allowed root, preserves the previous release and supports recoverable rollback. Update planning blocks invalid integrity, missing publisher signature, same-version replacement and implicit downgrade.

The current artifact is an internal offline ZIP with SHA-256 integrity. It is not an ISO image and is not publisher-signed because no publisher certificate, external signing authority or ISO-generation dependency has been supplied. Those external gates remain visible rather than being simulated.
