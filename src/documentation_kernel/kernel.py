from .views import ViewManager
from .sheets import SheetManager
from .styles import StyleRegistry
from .sync import DocumentationSynchronizer
from .publisher import Publisher
from .validator import DocumentationValidator

class DocumentationKernel:
    def __init__(self):
        self.views = ViewManager()
        self.sheets = SheetManager()
        self.styles = StyleRegistry()
        self.synchronizer = DocumentationSynchronizer()
        self.publisher = Publisher()
        self.validator = DocumentationValidator()

    def synchronize(self, model_revision):
        return self.synchronizer.synchronize(self.views, model_revision)

    def validate(self):
        return self.validator.validate(self.views, self.sheets, self.styles)
