#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# import json
sys.path.append("./")

info_list = list()

def rating_change(video_str):
    tmp_list = video_str.split("$$", maxsplit=1)
    rating = float(tmp_list[0])
    return rating

for line in sys.stdin:
    line = line.split("\t")
    info_list.append(line[1])

info_list.sort(key=rating_change,reverse=True)

for values in info_list:
    tmp = values.split("$$", maxsplit=1)
    rating = tmp[0]
    video = tmp[1]
    print("{0}\t{1}".format(rating, video))