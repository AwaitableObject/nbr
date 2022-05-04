import json
import os
from typing import Dict


def read_json(name: str) -> Dict:
    path = f"{os.getcwd()}/tests/data/{name}"
    with open(file=path, encoding="utf-8") as file:
        return json.load(file)
