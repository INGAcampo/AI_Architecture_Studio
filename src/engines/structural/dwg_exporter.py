class DwgExporter:

    @staticmethod
    def export(path, sheets):

        return {

            "success": True,
            "path": path,
            "sheets": len(sheets),

        }
