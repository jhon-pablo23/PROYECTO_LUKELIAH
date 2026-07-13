from config.logger import Logger


class SistemaConfig:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)

            cls._instancia.nombre = "LUKELIAH"
            cls._instancia.version = "1.0"
            cls._instancia.empresa = "IESTP Argentina"
            cls._instancia.autor = "JHON Y PATRICIA"

            Logger().info(
                f"Sistema iniciado: {cls._instancia.nombre} "
                f"Version: {cls._instancia.version}"
            )

        return cls._instancia