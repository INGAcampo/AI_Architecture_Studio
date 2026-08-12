"""Dependency-aware AEOS service catalog and health evaluation."""
from __future__ import annotations
from .models import ServiceDescriptor
class ServiceRegistry:
    """Register unique services and verify dependency-ready platform health."""
    def __init__(self):self.services={}
    def register(self,service:ServiceDescriptor):
        """Register a service idempotently while rejecting contract drift."""
        service.validate();row=service.to_dict();old=self.services.get(service.service_id)
        if old and old!=row:raise ValueError("service_descriptor_conflict")
        self.services[service.service_id]=row
    def readiness(self,service_id:str)->dict:
        """Return transitive direct-dependency readiness and concrete issues."""
        if service_id not in self.services:raise ValueError("unknown_service")
        service=self.services[service_id];issues=[]
        if service["health"]!="READY":issues.append(f"service_health:{service_id}:{service['health']}")
        for dep in service["dependencies"]:
            if dep not in self.services:issues.append(f"missing_dependency:{dep}")
            elif self.services[dep]["health"]!="READY":issues.append(f"dependency_health:{dep}:{self.services[dep]['health']}")
        return {"ready":not issues,"issues":issues}
    def platform_health(self):
        """Summarize all registered service readiness without concealing degradation."""
        rows={sid:self.readiness(sid) for sid in sorted(self.services)};return {"ready":all(x["ready"] for x in rows.values()),"services":rows}
