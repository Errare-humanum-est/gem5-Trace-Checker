from Machine import Machine
from typing import Set, Dict


class MachineCluster:

    def __init__(self, mach_type: str, stable_state_set: Set[str], time_out: int):
        self.time_out = time_out
        self.mach_type = mach_type
        self.stable_state_set = stable_state_set
        self.machine_dict: Dict[int, Machine] = {}

    def __str__(self):
        return self.mach_type + ': ' + str(len(self.machine_dict))

    def register_cache_block(self, mach_type: str, mach_id: int, line_address: str, time_stamp: int,
                             start_state: str, final_state: str):
        if mach_type == self.mach_type:
            if mach_id not in self.machine_dict:
                self.machine_dict[mach_id] = Machine(mach_type, mach_id, self.stable_state_set, self.time_out)
            self.machine_dict[mach_id].register_cache_block(line_address, time_stamp, start_state, final_state)

    def check_deadlock(self, cur_time_stamp: int):
        for machine in self.machine_dict.values():
            machine.check_deadlock(cur_time_stamp)
