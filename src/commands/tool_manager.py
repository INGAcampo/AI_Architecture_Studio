"""
AI Architecture Studio
Tool Manager

Foundation 2.4
"""


class ToolManager:
    def __init__(self):
        self.current_tool = None
        self.previous_tool = None

    def activate(self, tool):
        """
        Activa una nueva herramienta.
        """

        if self.current_tool is not None:
            self.current_tool.deactivate()

        self.previous_tool = self.current_tool
        self.current_tool = tool

        if self.current_tool:
            self.current_tool.activate()

    def cancel(self, canvas=None):
        """
        Cancela la herramienta actual.
        """

        if self.current_tool:
            self.current_tool.cancel(canvas)

        self.current_tool = None

    def tool_name(self):
        if self.current_tool:
            return self.current_tool.name

        return "NONE"

    def has_active_tool(self):
        return self.current_tool is not None