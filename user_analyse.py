#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析视频文件，根据用户id进行聚合，分析总点赞数，总转发数，点赞数和转发数（方差，期望）
"""
import json
import sys
from mrjob.job import MRJob
from mrjob.job import MRStep
sys.path.append("./")
from video_parse import VideoParser
from traceback import format_exc
from loggers import MyLogger
from tool import analyse

class MRUserAnalyser(MRJob):
    video_parser = VideoParser()
    logger = MyLogger("user_analyse","./useranalyse.log")
    def mapper(self,_,line):
        try:
            line = line.strip("\n")
            self.video_parser.parse(line)
            uid = self.video_parser.uid
            digg_count = self.video_parser.digg_count
            forward_count = self.video_parser.forward_count
            video_info = json.dumps(self.video_parser.to_dict())
            yield uid,str(digg_count)+"$$"+str(forward_count)+"$$"+video_info
        except Exception as e:
            self.logger.write("error","e:%s"%str(e))
            self.logger.write("error","error:%s" % (format_exc()))
            # print("error:%s" % (format_exc()))

    def reducer_calculation(self,uid,values):
        try:
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

        except Exception as e:
            self.logger.write("error", "e:%s" % str(e))
            self.logger.write("error", "error:%s" % (format_exc()))

    def steps(self):
        return [
            MRStep(mapper = self.mapper,reducer=self.reducer_calculation),
        ]

if __name__ == '__main__':
    MRUserAnalyser.run()

