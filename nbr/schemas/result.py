from enum import Enum

from pydantic import BaseModel

# from typing import Dict, List


class ExecutionStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"


class RunResult(BaseModel):
    status: ExecutionStatus
    # executed_cells: List[Dict]
