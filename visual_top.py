#! /usr/bin/env python

import random

f = open("ps_snapshot.txt", 'r')
f1 = open("cpu_times.txt", 'r')

class new_top:
    def __init__(self, user, pid, cpu_per, mem_per, vzs, rss, tty, stat, start_date, time, cmd):
        self.user = user
        self.pid = pid
        self.cpu_per = cpu_per
        self.mem_per = mem_per
        self.vzs = vzs
        self.rss = rss
        self.tty = tty
        self.stat = stat
        self.start_date = start_date
        self.time = time
        self.cmd = cmd

data_list = []



def add_to_list(line):
    data_list.append(new_top(line[0],
                            line[1],
                            line[2],
                            line[3],
                            line[4],
                            line[5],
                            line[6],
                            line[7],
                            line[8],
                            line[9],
                            line[10]))

for line in f:
    line_sep = line.split(" ")
    line_sep = [i for i in line_sep if i]
    add_to_list(line_sep)

cpu_dict = {}

active_times = {}

for line in f1:
    line_sep = line.split(" ")
    user_t = (float(line_sep[1]) / float(line_sep[4])) * 100
    nice_t = (float(line_sep[2]) / float(line_sep[4])) * 100
    system_t = (float(line_sep[3]) / float(line_sep[4])) * 100
    active_t = (1 - (float(line_sep[5]) / float(line_sep[4]))) * 100
    temp_name = line_sep[0]
    active_times[int(temp_name[3:])] = active_t
    cpu_dict[int(temp_name[3:])] = [user_t, nice_t, system_t]


ordered_cpu_times = dict(sorted(cpu_dict.items()))
ordered_total_cpu_times = dict(sorted(active_times.items()))

# print(cpu_dict)
# for obj in data_list:
#     print(obj.user, obj.pid)


data_list.sort(reverse=True, key=lambda x: x.cpu_per)

top_10 = data_list[0:10]

print("newgraph")
print("xaxis min 0 max %d hash 10" % 100)
print("label : Percentage of Usage")
print("yaxis min 0 max 10 nodraw")
print("no_auto_hash_labels")
print("no_draw_hash_marks")
print("newstring x -17 y 5 : Process")
print("    fontsize 12 rotate 90 font Times-Bold")
print("newcurve marktype ybar cfill .5 1 1 color .5 1 1  marksize 1 .3")
print("label : CPU Usage")
print("pts")
num = 10
for i in top_10:
    print("%f %f" % (float(i.cpu_per), num - .5))
    num -= 1
print("newcurve marktype ybar cfill 1 .5 1 color 1 .5 1  marksize 1 .3")
print("label : Memory Usage")
print("pts")
num = 10
for i in top_10:
    print("%f %f" % (float(i.mem_per), num - .8))
    num -= 1

num = 10
for i in top_10:
    if float(i.mem_per) < 10:
        print("newstring x %f y %f" % (-8, num - .9))
        print("    fontsize 6 : Mem %: " + i.mem_per)
    if float(i.cpu_per) < 10:
        print("newstring x %f y %f" % (-8, num - .6))
        print("    fontsize 6 : CPU %: " + i.cpu_per)
    num -= 1

print("newgraph")
print("xaxis min 0 max 100.9 nodraw")
print("yaxis min 0 max 10 nodraw")
num = 1
for i in top_10:
    print("newstring hjl vjc x 0 y %f : %s" % (num - .5, i.cmd))
    num += 1


# cpu time graph
print("newgraph")
print("x_translate -4")
print("xaxis min 0.4 max %f hash 1 mhash 0 shash 0" % ((len(cpu_dict) + 1) - .4))
print("label : CPU Number")
print("no_auto_hash_labels")
num = 1
for key,val in ordered_cpu_times.items():
    print(("hash_label at %f : cpu" % num) + str(key))
    num += 1
print("hash_labels hjl vjc rotate -60")
print("yaxis min 0 max 100")
print("label : Percentage Totals")


colors = ["0 1 0", "0 0 1", "1 0 0"]
num = 1
num_colors = 0
accum_y = .35
for key,val in ordered_cpu_times.items():
    for x in val:
        print("newline poly linethickness .2 pcfill " + colors[num_colors])
        print("pts")
        temp_below = num - .4
        temp_above = num + .4
        print("%f %f %f %f %f %f %f %f" % (temp_below, accum_y, temp_above, accum_y, temp_above, x + accum_y, temp_below, x + accum_y))
        accum_y += x
        num_colors += 1

    if accum_y < 100:
        print("newline poly linethickness .2 pcfill .85 .85 .85")
        print("pts")
        print("%f %f %f %f %f %f %f %f" % (temp_below, accum_y, temp_above, accum_y, temp_above, 100, temp_below, 100))
    num += 1
    num_colors = 0
    accum_y = .35

num = 5
for i in colors:
    if i == colors[0]:
        print("newline poly linethickness .2 pcfill " + i)
        print("pts")
        print("-9 %f -7 %f -7 %f -9 %f" % (num, num, num+5, num+5))
        print("newstring vjc x %f y %f" % (-5.5, num + 2.5))
        print("    fontsize 10 : " + "User Time")
    if i == colors[1]:
        print("newline poly linethickness .2 pcfill " + i)
        print("pts")
        print("-9 %f -7 %f -7 %f -9 %f" % (num, num, num+5, num+5))
        print("newstring vjc x %f y %f" % (-5.5, num + 2.5))
        print("    fontsize 10 : " + "Nice Time")
    if i == colors[2]:
        print("newline poly linethickness .2 pcfill " + i)
        print("pts")
        print("-9 %f -7 %f -7 %f -9 %f" % (num, num, num+5, num+5))
        print("newstring vjc x %f y %f" % (-5.5, num + 2.5))
        print("    fontsize 10 : " + "    System Time")

    num += 15

print("newline poly linethickness .2 pcfill .85 .85 .85")
print("pts")
print("-9 %f -7 %f -7 %f -9 %f" % (num, num, num+5, num+5))
print("newstring vjc x %f y %f" % (-5.5, num + 2.5))
print("    fontsize 10 : " + "Idle Time")


print("newgraph")
print("y_translate -4")
print("x_translate -4")
print("xaxis min 0.4 max %f hash 1 mhash 0 shash 0" % ((len(cpu_dict) + 1) - .4))
print("label : CPU Number")
print("no_auto_hash_labels")
num = 1
for key,val in ordered_total_cpu_times.items():
    print(("hash_label at %f : cpu" % num) + str(key))
    num += 1
print("hash_labels hjl vjc rotate -60")
print("yaxis min 0 max 100")
print("label : Percentage Totals")

print("newcurve marktype xbar cfill 1 0 1 marksize .8 5")
print("label : Total CPU usage per core")
print("pts")

for key,val in ordered_total_cpu_times.items():
    print("%f %f" % (key + 1, val))


#do legend and axis title and change colors
#also write a script to run
