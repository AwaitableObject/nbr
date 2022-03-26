from dataclasses import dataclass
from typing import List, Optional


@dataclass()
class Cell:
    id: str
    outputs: List[str]
    source: str
    execution_count: Optional[int] = None
    cell_type: str = "code"

    def __str__(self) -> str:
        return f"<Cell {self.id}>"
