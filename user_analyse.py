#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析视频文件，根据用户id进行聚合，分析总点赞数，总转发数，点赞数和转发数（方差，期望）
"""
import json
import sys
sys.path.append("./")
from mrjob.job import MRJob
from mrjob.job import MRStep

class MRUserAnalyser(MRJob):
    FILES = ['video_parse.py', "tool.py"]
    def mapper(self,_,line):
            from video_parse import VideoParser
            self.video_parser = VideoParser()
            line = line.strip("\n")
            self.video_parser.parse(line)
            uid = self.video_parser.uid
            digg_count = self.video_parser.digg_count
            forward_count = self.video_parser.forward_count
            video_info = json.dumps(self.video_parser.to_dict())
            yield uid,str(digg_count)+"$$"+str(forward_count)+"$$"+video_info

    def reducer_calculation(self,uid,values):
            from tool import analyse
            calcu_info = dict()
            total_digg, total_forward, digg_variance, forward_variance, digg_exp, forward_exp = analyse(values)
            calcu_info["total_digg"] = total_digg
            calcu_info["total_forward"] = total_forward
            calcu_info["digg_variance"] = digg_variance
            calcu_info["forward_variance"] = forward_variance
            calcu_info["digg_exp"] = digg_exp
            calcu_info["forward_exp"] = forward_exp
            calcu_str = json.dumps(calcu_info)
            yield uid,calcu_str

    def steps(self):
        return [
            MRStep(mapper = self.mapper,reducer=self.reducer_calculation),
        ]

if __name__ == '__main__':
    MRUserAnalyser.run()

