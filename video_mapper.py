#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
sys.path.append("./")
from video_parse import VideoParser
# from traceback import format_exc
# from loggers import MyLogger

for line in sys.stdin:
    video_parser = VideoParser()
    video_parser.parse(line)
    rating = video_parser.rating
    video_info = json.dumps(video_parser.to_dict())
    print("m",str(rating)+"$$"+video_info)

