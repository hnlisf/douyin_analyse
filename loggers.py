#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

class MyLogger:
    def __init__(self,logname,logpath):
        self.logname = logname
        self.logpath = logpath
        self.logger = self._get_log()

    def _get_log(self):
        logger = logging.getLogger(self.logname)
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler(self.logpath,encoding='utf-8')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def write(self,level,msg):
        try:
            if level =='info':
                self.logger.info(msg)
            elif level == 'debug':
                self.logger.debug(msg)
            elif level == 'error':
                self.logger.error(msg)
            elif level == 'warning':
                self.logger.warning(msg)
        except UnicodeEncodeError as e:
            print('日志写入%s发生编码错误%e'%(msg,e))

if __name__ == '__main__':
    logger = MyLogger('test','test_log.txt')
    # msg = '视频下载地址https://aweme.snssdk.com/aweme/v1/play/?video_id=4c168148226243abb6bb869cd545ffc0&line=0,视频文件谭松韵v_点赞数(13798)_2017-08-18-12-03-55.mp4已下载完成'
    # msg = '视频Miss.Lu児💃🏻_点赞数(72188)_2018-05-29-23-14-19.mp4 [文件大小]:1.13 MB'
    msg = '视频조이_点赞数（129938)_2017-12-25-11-33-43.mp4 [文件大小]:2.72 MB'
    logger.write('info',msg)