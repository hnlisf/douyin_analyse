#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析视频文件，根据用户id进行聚合，分析总点赞数，总转发数，点赞数和转发数（方差，期望）
"""
import json
import math
import time
from collections import Counter
from mrjob.job import MRJob
from mrjob.job import MRStep

# 求方差的函数
def var(lst,avg):
    var1 = 0
    for i in lst:
        var1 += float((i-avg)**2*1.0)
    # 样本个数为1时，方差为0
    if len(lst) ==1:
        var2 = 0
    else:
        var2 = (math.sqrt(var1/(len(lst)-1)*1.0))
    var2 = round(var2,2)
    return var2
# 求期望的函数
def exp(lst):
    ex = 0
    count = len(lst)
    values_counts = Counter(lst)
    se = set(lst)
    for i in se:
        # print(i,values_counts[i])
        ex += i*(float(values_counts[i]/count))
    ex = round(ex,2)
    return ex
# 综合分析函数
def analyse(values):
    total_digg = 0
    total_forward = 0
    digg_list = list()
    forward_list = list()
    lines = list(values)
    count = len(lines)
    for line in lines:
        tmp = line.split("$$", maxsplit=2)
        digg_count = int(float(tmp[0]))
        forward_count = int(float(tmp[1]))
        digg_list.append(digg_count)
        forward_list.append(forward_count)
    total_digg = sum(digg_list)
    total_forward = sum(forward_list)
    digg_avg = total_digg/float(count*1.0)
    forward_avg = total_forward/float(count*1.0)
    digg_avg = round(digg_avg,2)
    forward_avg = round(forward_avg,2)
    digg_variance = var(digg_list,digg_avg)
    forward_variance = var(forward_list,forward_avg)
    digg_exp = exp(digg_list)
    forward_exp = exp(forward_list)
    return total_digg,total_forward,digg_variance,forward_variance,digg_exp,forward_exp

class VideoParser:
    # 点赞数和转发数评分权重
    digg_weight = 0.6
    forward_weight = 0.4
    def  __init__(self):
        # 用户id
        self._uid = ''
        # 视频id
        self._aweme_id = ''
        # 视频点赞数
        self._digg_count = 0
        # 老视频无此参数，怀疑是视频提升次数，抖音推荐算法中，根据用户视频点赞数和评论数的百分比，不断提升到更大的用户池
        self._forward_count = 0
        # 播放url地址列表，抖音视频有两个播放地址
        self._play_url_list = list()
        # 视频标题,新视频数据无该字段
        self._title = ''
        # 视频封面url列表
        self._cover_url_list = list()
        # 视频评分
        self._rating = 0.0
        # 视频创建时间
        self._create_time = ''

    def parse(self,line):
        """
        传入一行数据进行解析
        :param line:
        :return:
        """
        video_info = json.loads(line,encoding="utf-8")

        self.uid = video_info.get("uid")
        self.aweme_id = video_info.get("aweme_id")
        self.play_url_list = video_info["video"]["play_addr"]["url_list"]
        self.cover_url_list = video_info["video"]["cover"]["url_list"]
        statistics = video_info["statistics"]
        self.digg_count = statistics["digg_count"]
        forward_count = statistics.get("forward_count")
        if forward_count is not None:
            self.forward_count = forward_count
        else:
            # print(statistics.get("share_count"))
            self.forward_count = statistics.get("share_count")

        self.title = video_info.get("desc")
        self.create_time = video_info.get("create_time")
        self.rating = self.analyse_rating()

    def to_dict(self):
        """
        将属性（@property）转化为dict输出
        :return:
        """
        propertys = {}
        propertys["uid"] = self.uid
        propertys["aweme_id"] = self.aweme_id
        propertys["digg_count"] = self.digg_count
        propertys["forward_count"] = self.forward_count
        propertys["play_url_list"] = self.play_url_list
        propertys["title"] = self.title
        propertys["cover_url_list"] = self.cover_url_list
        propertys["rating"] = self.rating
        propertys["create_time"] = self.create_time
        return propertys

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self,uid):
        self._uid = uid

    @property
    def aweme_id(self):
        return self._aweme_id

    @aweme_id.setter
    def aweme_id(self,aweme_id):
        self._aweme_id = aweme_id

    @property
    def digg_count(self):
        return self._digg_count

    @digg_count.setter
    def digg_count(self,digg_count):
        if str(digg_count).endswith("w"):
            digg_count = float(str(digg_count)[:-1])*10000
        elif str(digg_count).endswith("k"):
            digg_count = float(str(digg_count)[:-1]) * 1000
        self._digg_count = digg_count

    @property
    def forward_count(self):
        return self._forward_count

    @forward_count.setter
    def forward_count(self,forward_count):
        self._forward_count = forward_count

    @property
    def play_url_list(self):
        return self._play_url_list

    @play_url_list.setter
    def play_url_list(self,play_url_list):
        self._play_url_list = play_url_list

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,title):
        if title:
            self._title = title
        else:
            self._title = "抖音-原创音乐短视频社区"

    @property
    def cover_url_list(self):
        return self._cover_url_list

    @cover_url_list.setter
    def cover_url_list(self,cover_url_list):
        self._cover_url_list = cover_url_list

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self,rating):
        self._rating = rating

    @property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self,create_time):
        if create_time:
            self._create_time = create_time
        else:
            self._create_time = str(time.time()).split(".")[0]

    # 计算评分的方法
    def analyse_rating(self):
        socore = self.digg_count * self.digg_weight + self.forward_count*self.forward_weight
        socore = round(socore,3)
        return socore

class MRUserAnalyser(MRJob):
    video_parser = VideoParser()
    def mapper(self,_,line):
            line = line.strip("\n")
            self.video_parser.parse(line)
            uid = self.video_parser.uid
            digg_count = self.video_parser.digg_count
            forward_count = self.video_parser.forward_count
            video_info = json.dumps(self.video_parser.to_dict())
            yield uid,str(digg_count)+"$$"+str(forward_count)+"$$"+video_info
            # print("error:%s" % (format_exc()))

    def reducer_calculation(self,uid,values):
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

