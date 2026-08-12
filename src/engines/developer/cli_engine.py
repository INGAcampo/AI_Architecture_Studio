class CLIEngine:

    @staticmethod
    def run_command(command):

        return {"command": command, "status": "ok"}

    @staticmethod
    def generate_template(name):

        return {"template": name}
