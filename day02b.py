#!/usr/bin/env python3

from aocd import data, submit

reports = []
for line in data.splitlines():
    reports.append([int(x) for x in line.split()])

c = 0
for report_big in reports:

    for i in range(-1, len(report_big)):

        report = list(report_big)
        if i >= 0:
            report.pop(i)


        not_decreasing = False
        not_increasing = False
        very_unsafe = False
        for i in range(1, len(report)):
            

            if report[i] >= report[i-1]:
                not_decreasing = True
            if report[i] <= report[i-1]:
                not_increasing = True
            d = abs(report[i] - report[i-1]) 
            if d < 1 or d > 3:
                very_unsafe = True

            if not_decreasing and not_increasing:
                very_unsafe = True

        if not very_unsafe:
            c += 1        
            break


print(c)

# print(ans)
# submit(ans)
