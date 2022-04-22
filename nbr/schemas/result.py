from enum import Enum

from pydantic import BaseModel


class ExecutionStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"


class RunResult(BaseModel):
    status: ExecutionStatus
    executed_cells: list[dict]
