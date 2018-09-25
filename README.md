# python操作Hadoop实战（mrjob模块分析抖音数据）



### 1.数据：

文件：video_data_2w.json 包含2W条抖音视频数据，其中关键有用的字段有：

用户id  ----------uid

视频id -----------aweme_id

点赞数 -------digg_count

转发数（or推荐数）--------forward_count

视频播放url列表---------play_url_list

视频标题--------title

视频封面url列表---------cover_url_list

视频创建时间-----------create_time

### 2.分析目标：

<1. 对点赞数和转发数进行综合权重评分rating，按照rating进行倒序排列，找出最受欢迎的视频。

<2.对同一用户的视频数据进行聚合分析，分析出用户视频总点赞数，总转发数，方差和期望值（点赞数和转发数）



### 3.代码说明：

video_analyse.py  :对点赞数和转发数进行综合权重评分rating

user_analyse.py  :对同一用户的视频数据进行聚合分析