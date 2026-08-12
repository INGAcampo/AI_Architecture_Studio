class ResultsExporter:

    @staticmethod
    def export_csv(path, data):

        with open(path, "w", encoding="utf-8") as f:

            f.write(str(data))
