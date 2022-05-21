from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ExecutionStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"


class RunResult(BaseModel):
    status: ExecutionStatus
    cells: Optional[List] = None
