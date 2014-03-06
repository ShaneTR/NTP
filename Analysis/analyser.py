import math

__author__ = 'Shane Ryan 10340427'

import os
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pprint import pprint

FILE_HOME = os.path.realpath(os.path.dirname(__file__))

json_data = open(os.path.join(FILE_HOME, "../data/data.json"), "r")

data = json.load(json_data)

data_headers = {'jitter', 'reach', 'delay', 'offset', 'poll'}

stats = {}

ntp_stats = {}

for run in data:
    run_data = data[run]
    for server in run_data:
        if not ntp_stats.get(server, None):
            ntp_stats[server] = []
        element = run_data[server]
        ntp_stats[server].append(element)

del data


def get_stats(data_headers, data, server):
    results = {}
    plots = []

    for plot_number, header in enumerate(data_headers):
        field_entries = []
        for entry in data:
            field_entries.append(entry[header])
        print header
        plot = plt.plot([x for x in xrange(0, len(field_entries))], field_entries, )
        plots.append(plot)
        mean = np.mean(np.array(field_entries, dtype=np.float64), axis=0)
        std = np.std(np.array(field_entries, dtype=np.float64), axis=0)
        results[header] = {'mean': mean,
                           'min': min(field_entries),
                           'max': max(field_entries),
                           'std_dev': std}
    return results

output_stats = {}

for server in ntp_stats:
    data = ntp_stats[server]
    output_stats[server] = get_stats(data_headers, data, server)
    plt.show()


json = json.dumps(output_stats, sort_keys=True)
output = open("../data/stats.json", "w")
output.write(json)
output.close()





