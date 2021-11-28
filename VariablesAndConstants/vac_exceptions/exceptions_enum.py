from enum import Enum


class VACErrId(Enum):
    DOUBLE_ASSIGN_SAME_VAR = "got an variable/const that were assigned twice in a single block"
    UPDATING_CONSTANT_VAR = "got an const that we trying to update"
    UNMATCHED_TYPES = "got an variable/constant that we trying to update to a different type"