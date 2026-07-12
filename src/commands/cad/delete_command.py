"""
AI Architecture Studio
Delete Command

Foundation 3.2
"""

from core.history.delete_action import DeleteAction


class DeleteCommand:

    def __init__(self, app_core=None):
        self.app_core = app_core

    def get_history_manager(self, canvas):
        if self.app_core is not None:
            return self.app_core.history

        kernel = getattr(canvas.scene, "kernel", None)

        if kernel is not None:
            return kernel.services.get("history_manager")

        return None

    def execute(self, canvas):
        selected = canvas.selection_manager.selected_elements()

        if not selected:
            print("DELETE: No hay objetos seleccionados")
            return

        history = self.get_history_manager(canvas)
        removed = 0

        for element in selected:
            if canvas.scene.remove_element(element):
                removed += 1

                if history is not None:
                    history.push(
                        DeleteAction(canvas.scene, element)
                    )

        canvas.selection_manager.clear()
        canvas.highlight.clear()
        canvas.update()

        print(f"DELETE: {removed} objeto(s) eliminados")