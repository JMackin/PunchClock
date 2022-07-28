#!/usr/bin/python

import os
import sys
import re
from datetime import datetime

os.chdir("/media/melanos/StorageAlpha/TTF/PunchClock/")
right_now = datetime.now()
hr = right_now.hour
mn = right_now.minute
sc = right_now.second
time_total = 0
time_buffA = 0
time_buffB = 0
quitting = False
in_clock = False

date = f"{right_now.month}-{right_now.day}-{right_now.year}"
punch_card = date + ".txt"

# sys.argv contains a list of arguments passed from the cmd line
op = sys.argv[1]

if op == "in":
    out = open(punch_card, "a")
    out.write(f"\nClocked In:\n>[ {hr}:{mn}:{sc} ]\n")
    out.close()
    print(f"\nClocked In:\n>[ {hr}:{mn}:{sc} ]\n")
elif op == "break":
    out = open(punch_card, "a")
    out.write(f"\nBreak Started:\n<[ {hr}:{mn}:{sc} ]\n")
    out.close()
    print(f"\nBreak Started:\n<[ {hr}:{mn}:{sc} ]\n")
elif op == "end":
    out = open(punch_card, "a")
    out.write(f"\nBreak Ended:\n>[ {hr}:{mn}:{sc} ]\n")
    out.close()
    print(f"\nBreak Ended:\n>[ {hr}:{mn}:{sc} ]\n")
elif op == "out":
    out = open(punch_card, "a")
    out.write(f"\nClocked Out:\n<[ {hr}:{mn}:{sc} ]\n")
    out.close()
    print(f"\nClocked Out:\n<[ {hr}:{mn}:{sc} ]\n")
elif op == "show":
    out = open(punch_card, "r")
    [print(x) for x in out.readlines()]
    out.close()
elif op == "done":
    out = open(punch_card, "r")
    for x in out.readlines():
        if re.match('>', x):
            if in_clock:
                print("Inconsistent times. Quitting.")
                quitting = True
                break
            else:
                time_arr = x.split(':')
                time_buffA = (int(time_arr[0].strip('<[>[ ')) * 3600) + (int(time_arr[1]) * 60) + int(time_arr[2].strip(' ]\n'))
                in_clock = True

        elif re.match('<', x):
            if not in_clock:
                print("Inconsistent times. Quitting.")
                quitting = True
                break
            else:
                time_arr = x.split(':')
                time_buffB = (int(time_arr[0].strip('<[>[ ')) * 3600) + (int(time_arr[1]) * 60) + int(time_arr[2].strip(' ]\n'))

                time_total += time_buffB - time_buffA
                in_clock = False
        else:
            pass

    if quitting:
        print("Exited with error. No total made")
        out.close()
    else:
        out.close()

        tot_hr = time_total // 3600
        tot_min = (time_total % 3600) // 60
        tot_sc = (time_total % 60)

        tot_time_out = f"{tot_hr}:{tot_min}:{tot_sc}"

        out = open(punch_card, 'a')
        out.write(f"\nTotal time worked:\n"
                  f"----------\n"
                  f"[ {tot_time_out} ]\n"
                  f"----------\n")
        out.close()
        print(f"\nDone:\nTotal Time Worked: {tot_time_out}")
else:
    print(f"\nCurrent time:{hr}:{mn}:{sc}\n")
    print(f"Args passed: {sys.argv}/{op}\n")
    print("Options:\n"
          "'in': Clock in\n'out': Clock out\n"
          "'break': Start break\n'end': End break\n"
          "'show': Print day's clock record\n'done': finish and compute total hours\n")
    print(f"{right_now.month}/{right_now.day}")









