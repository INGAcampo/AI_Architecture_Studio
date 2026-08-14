from __future__ import annotations

from dataclasses import dataclass

from .policy import OperationPolicy


@dataclass(frozen=True)
class CapabilityToken:
    application: str
    operations: tuple[str,...]
    allow_destructive: bool = False
    allow_publish: bool = False


@dataclass(frozen=True)
class CapabilityDecision:
    authorized: bool
    reason: str


def authorize_operation(
    token: CapabilityToken,
    policy: OperationPolicy,
    operation: str,
) -> CapabilityDecision:
    policy.validate()

    if token.application != policy.application:
        return CapabilityDecision(False,"application_mismatch")

    if operation not in policy.allowed_operations:
        return CapabilityDecision(False,"operation_not_allowed_by_policy")

    if operation not in token.operations:
        return CapabilityDecision(False,"operation_not_granted_by_token")

    if operation in policy.destructive_operations and not token.allow_destructive:
        return CapabilityDecision(False,"destructive_authorization_required")

    if operation in policy.publish_operations and not token.allow_publish:
        return CapabilityDecision(False,"publish_authorization_required")

    return CapabilityDecision(True,"authorized")
