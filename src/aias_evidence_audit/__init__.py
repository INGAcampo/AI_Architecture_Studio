"""Tamper-evident synchronization for external evidence records."""
from .audit import AuditTrail, AuditEvent
__all__ = ["AuditTrail", "AuditEvent"]
