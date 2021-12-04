from MachineClusters import MachineCluster
from typing import Dict, Set
import re


class TraceAnalyser:

    time_out = 10000000

    def __init__(self, trace_file_path: str):
        self.trace_file_path: str = trace_file_path

        self.mach_cluster: Dict[str, MachineCluster] = {}
        self.mach_cluster['L1Cache'] = MachineCluster('L1Cache', {'I', 'S', 'E', 'M', 'L'}, self.time_out)
        self.mach_cluster['DeNovo'] = MachineCluster('DeNovo', {'I', 'V', 'M', 'L'}, self.time_out)
        self.mach_cluster['L2Cache'] = MachineCluster('L2Cache',
                                                      {'I_x_I', 'S_c_V', 'I_x_M', 'M_c_I', 'I_c_O'},
                                                      self.time_out)
        self.iterate_trace()

    def iterate_trace(self):
        cur_epoch_time_stamp = -1
        with open(self.trace_file_path) as file:
            for line in file:
                time_stamp = self.regex_line(line)

                if cur_epoch_time_stamp == -1:
                    cur_epoch_time_stamp = time_stamp

                if time_stamp > cur_epoch_time_stamp + self.time_out:
                    print("EPOCH TIMESTAMP: " + str(time_stamp))
                    cur_epoch_time_stamp = time_stamp
                    self.check_deadlocks(time_stamp)

    def regex_line(self, line: str):
        param_list = re.findall(r'(\d+)\s+(\d+)\s+(\w+)\s+\w+\s+(\w*)>(\w*)\s+\[[\d\w]+,\s*line\s+([\d\w]+)\]', line)[0]
        # Check if the machine is in the mach_cluster dict
        if param_list[2] in self.mach_cluster:
            self.mach_cluster[param_list[2]].register_cache_block(param_list[2],
                                                                  int(param_list[1]),
                                                                  param_list[5],
                                                                  int(param_list[0]),
                                                                  param_list[3],
                                                                  param_list[4])
        return int(param_list[0])

    def check_deadlocks(self, cur_time_stamp: int):
        for mach_cluster in self.mach_cluster.values():
            for mach in mach_cluster.machine_dict.values():
                mach.check_deadlock(cur_time_stamp)


TraceAnalyser('trace.out')