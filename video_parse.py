#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import time

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