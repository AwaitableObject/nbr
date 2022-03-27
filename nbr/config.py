class Config:
    host: str = "127.0.0.1"
    port: int = 8888

    @property
    def api_url(self) -> str:
        return f"http://{Config.host}:{Config.port}/api"

    @property
    def ws_url(self) -> str:
        return f"ws://{Config.host}:{Config.port}/api"

    @staticmethod
    def configure(host: str, port: int) -> None:
        Config.host = host
        Config.port = port


config = Config()
