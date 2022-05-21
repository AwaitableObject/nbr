class KernelState:
    def __init__(self, state: str):
        self._state = state


#    ____________________________________
#   /                                    \
# idle <-> busy -> code -> output -> status
#  /\
#  \/
