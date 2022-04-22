from enum import Enum
from typing import Dict, List

from pydantic import BaseModel


class ExecutionStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"


class RunResult(BaseModel):
    status: ExecutionStatus
    executed_cells: List[Dict]
