"""
AI Architecture Studio
Kernel - Service Locator

Foundation 1.7
"""


class ServiceLocator:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        """
        Registra un servicio global.
        """
        self._services[name] = service

    def get(self, name):
        """
        Devuelve un servicio registrado.
        """
        return self._services.get(name)

    def exists(self, name):
        """
        Verifica si un servicio existe.
        """
        return name in self._services

    def unregister(self, name):
        """
        Elimina un servicio registrado.
        """
        if name in self._services:
            del self._services[name]

    def clear(self):
        """
        Elimina todos los servicios.
        """
        self._services.clear()