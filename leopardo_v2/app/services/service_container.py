class ServiceContainer:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services.get(name)

# Create a global instance of the service container
container = ServiceContainer()
