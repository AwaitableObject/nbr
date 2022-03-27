from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class Kernel(BaseModel):
    """Kernel model."""

    id: str
    name: str
    last_activity: str
    execution_state: str
    connections: int


class Notebook(BaseModel):
    """Notebook model."""

    path: Optional[str] = None
    name: str


class Session(BaseModel):
    """Session model."""

    id: str
    path: str
    name: str
    type: str
    kernel: Kernel
    notebook: Notebook


class KernelName(BaseModel):
    """Kernel name scheme."""

    name: str = "python3"


class CreateSession(BaseModel):
    """Session scheme."""

    kernel: KernelName = KernelName()
    name: str
    path: str = uuid4().hex
    type: str = "notebook"
