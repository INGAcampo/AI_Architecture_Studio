class HVACEngine:

    @staticmethod
    def calculate_airflow(room_area_m2):

        airflow_factor = 8.0

        return room_area_m2 * airflow_factor

    @staticmethod
    def size_duct(airflow_m3h):

        return {

            "width_mm": 500,
            "height_mm": 300,

        }
