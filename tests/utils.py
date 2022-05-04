import json
import os
from typing import Dict

CWD = os.getcwd()


def read_json(name: str) -> Dict:
    path = f"{CWD}/tests/data/{name}"
    with open(file=path, encoding="utf-8") as file:
        return json.load(file)
