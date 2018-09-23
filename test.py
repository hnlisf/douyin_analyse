import json
import datetime
import time

# print("123"<"6")
#
# a = {'a':1}
# print(json.dumps(a),type(json.dumps(a)))
#
# create_time = 1530086364
# tm=datetime.datetime.fromtimestamp(float(create_time))
# print(tm)
#
# print(time.time())


#
# li = ["123.0$$hnhksfd123","456.7$$hnhksfd456","23.4$$hnhksfd23","321.8$$hnhksfd321",]
#
#
# def rating_change(video_str):
#     tmp_list = video_str.split("$$", maxsplit=1)
#     rating = float(tmp_list[0])
#     return rating
#
# li.sort(key=rating_change)
# print(li)
tmp_file = open("../douyin_data/douyin_video_2000.json",mode="a+",encoding="utf-8")

with open("../douyin_data/douyin_video88.json", "r") as f:
    for index, line in enumerate(f):
        if index < 2001:
            tmp_file.write(line)
        else:
            break

tmp_file.close()
