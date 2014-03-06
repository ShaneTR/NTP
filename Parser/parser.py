__author__ = 'Shane Ryan 10340427'

"""
Parse the ntpq output into one of the following formats
    - xml
    - json
    - python object list
    - python dictionary
"""

# class Entry:
#
#     """
#     Information @ http://tech.kulish.com/2007/10/30/ntp-ntpq-output-explained/
#
#     Columns Defined:
#         remote: peers specified in the ntp.conf file
#         * = current time source
#         # = source selected, distance exceeds maximum value
#         o = source selected, Pulse Per Second (PPS) used
#         + = source selected, included in final set
#         x = source false ticker
#         . = source selected from end of candidate list
#         - = source discarded by cluster algorithm
#         blank = source discarded high stratum, failed sanity
#
#     Entry has the following fields
#     - remote
#     - refid: remote source's synchronization source
#     - st (stratum level of the source)
#     - t (types available)
#         - l = local (such as a GPS, WWVB)
#         - u = unicast (most common)
#         - m = multicast
#         - b = broadcast
#         - = netaddr
#     - when: number of seconds passed since last response
#     - poll: polling interval, in seconds, for source
#     - reach: indicates success/failure to reach source, 377 all attempts successful
#     - delay: indicates the roundtrip time, in milliseconds, to receive a reply
#     - offset: indicates the time difference, in milliseconds, between the client server and source
#     - disp/jitter: indicates the difference, in milliseconds, between two samples
#     """
#
#     def __init__(self, *args, **kwargs):
#         if args is None and kwargs:
#             for key in ('remote', 'refid', 'stratum', 'type', 'when', 'poll', 'reach', 'delay',
#                         'offset', 'jitter'):
#                 if key in kwargs:
#                     setattr(self, key, kwargs[key])
#         else:
#             self.remote = args.pop("remote", None)
#             self.refid = args.pop("refid", None)
#             self.stratum = args.pop("stratum", None)
#             self.type = args.pop("type", None)
#             self.when = args.pop("when", None)
#             self.poll = args.pop("poll", None)
#             self.reach = args.pop("reach", None)
#             self.delay = args.pop("delay", None)
#             self.offset = args.pop("offset", None)
#             self.jitter = args.pop("jitter", None)

import re
import json


def parse_entry(line, headers):
    # split the line into a list
    result = {}
    entry = line.split()
    if len(entry) == len(headers):
        for index, header in enumerate(headers):
            result[header] = entry[index]
        return result
    else:
        print "Header length and entry length are not the same"
    return None

def main():

    with open("../data/ntpq.txt") as ntp_file:
        entries = {}
        entry_count = 0
        runs = {}
        run_count = 0
        data = ntp_file.readlines()
        header_line = re.findall("\w+", data[0])
        for line in data:
            if line == "\n":
                continue
            if line.split()[0] == header_line[0]:
                if len(entries) > 0:
                    run_count += 1
                    runs["%s" % run_count] = entries
                    entries = {}
                    entry_count = 0
            elif line.startswith("="):
                continue
            else:
                entry_count += 1
                entries[entry_count] = parse_entry(line=line, headers=header_line)
        print entries
        print runs
        data = json.dumps(runs, sort_keys=True)
        output = open("../data/data.json", "w")
        output.write(data)
        output.close()


if __name__ == "__main__":
    main()




