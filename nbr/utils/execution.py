from doctest import OutputChecker
from typing import Dict


class KernelState:
    def __init__(self, state: str):
        self._state = state

    def next_state(self, message: Dict):
        pass

    @staticmethod
    def idle(self):
        pass

    @staticmethod
    def busy(self):
        pass

    @staticmethod
    def status(self):
        pass

    @staticmethod
    def output(self):
        pass

#    ____________________________________
#   /                                    \
# idle <-> busy -> code -> output -> status 
#  /\  
#  \/