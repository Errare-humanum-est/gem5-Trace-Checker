from CacheBlockStat import CacheBlock

from typing import Set, Dict


class Machine:

    def __init__(self, mach_type: str, mach_id: int, stable_state_set: Set[str], time_out: int):
        self.time_out = time_out
        self.mach_type = mach_type
        self.mach_id = mach_id
        self.stable_state_set = stable_state_set
        self.line_address_dict: Dict[str, CacheBlock] = {}

    def __str__(self):
        return self.mach_type + ': ' + str(self.mach_id)

    def register_cache_block(self, line_address: str, time_stamp: int, start_state: str, final_state: str):
        self.line_address_dict[line_address] = CacheBlock(line_address, time_stamp, start_state, final_state)

    def check_deadlock(self, cur_time_stamp: int):
        for cache_block in self.line_address_dict.values():
            if cache_block.check_deadlock(cur_time_stamp, self.time_out, self.stable_state_set):
                print(f'DEADLOCK   '
                      f'TimeStamp: {cache_block.time_stamp},   '
                      f'ID: {self.mach_id},   '
                      f'Machine: {self.mach_type},   '
                      f'TimeStamp: {cache_block.time_stamp},   '
                      f'LineAddress: {cache_block.line_address},   '
                      f'State: {cache_block.final_state}')
