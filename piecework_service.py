# Author: GouHaoliang
# Date: 2025/5/14
# Time: 16:30

import pandas as pd
import time


def piecework_service(data, idx):

    act_timestamp = int(time.time())
    act_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(act_timestamp))

    data[idx][''] = act_time

