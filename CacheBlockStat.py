from typing import Set


class CacheBlock:

    def __init__(self, line_address: str, time_stamp: int, start_state: str, final_state: str):
        # Python dict optimized for string
        self.line_address = line_address
        self.time_stamp = time_stamp
        self.start_state: str = start_state
        self.final_state: str = final_state
        self.stable_state: bool = False

    def __str__(self):
        return self.line_address

    def check_deadlock(self, cur_time_stamp: int, time_out: int, stable_state_set: Set[str]):
        if self.stable_state:
            return False
        # It is assumed that stable_states are not the source of a transaction deadlocking
        elif self.final_state in stable_state_set:
            self.stable_state = True
            return False
        else:
            # Check for timeout
            if cur_time_stamp - self.time_stamp > time_out:
                return True
        return False

