from nbformat import NotebookNode


class NotebookExecutor:
    host: str
    port: int

    def __init__(
        self, *, notebook: NotebookNode, host: str = "127.0.0.1", port=8888
    ) -> None:
        self.notebook: NotebookNode = notebook
        self.host: str = host
        self.port: int = port

    async def execute(self) -> NotebookNode:
        pass
