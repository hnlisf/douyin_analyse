#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析视频文件，按照评分进行排序
"""
import json
import sys
from mrjob.job import MRJob
from mrjob.job import MRStep
sys.path.append("./")
from video_parse import VideoParser
from traceback import format_exc
from loggers import MyLogger

class MRVideoAnalyser(MRJob):
    video_parser = VideoParser()
    logger = MyLogger("video_analyse", "./videoanalyse.log")
    def mapper(self,_,line):
        try:
            line = line.strip("\n")
            self.video_parser.parse(line)
            rating = self.video_parser.rating
            video_info = json.dumps(self.video_parser.to_dict())
        except Exception as e:
            self.logger.write("error","e:%s"%str(e))
            self.logger.write("error","error:%s"%(format_exc()))
        yield "m",str(rating)+"$$"+video_info

    def reducer_sort(self,_,values):
        lines = list(values)
        lines.sort(key=self.rating_change,reverse=True)
        for values in lines:
            tmp = values.split("$$",maxsplit=1)
            rating = tmp[0]
            video = tmp[1]
            yield rating,video

    def rating_change(self,video_str):
        tmp_list = video_str.split("$$",maxsplit=1)
        rating = float(tmp_list[0])
        return rating

    def steps(self):
        return [
            MRStep(mapper=self.mapper,reducer=self.reducer_sort),
            # MRStep(reducer=self.reducer_top)
        ]

if __name__ == '__main__':
    MRVideoAnalyser.run()