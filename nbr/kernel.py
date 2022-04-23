from typing import Dict, List

from nbr.schemas.result import RunResult


class Kernel:
    def send(self, data: List[Dict]) -> RunResult:
        pass
