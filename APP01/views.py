from django.shortcuts import render
# Create your views here.
from rest_framework.generics import GenericAPIView
from APP01.models import Item, Collection, Like
from APP01.serializers import Item_serializer, Collection_serializer, Like_serializer
from rest_framework.response import Response
from rest_framework import status

from random import sample
import csv

# 定时任务
# 定时将log表内的数据读取到log.csv供catboost使用
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from APP01 import schedu

try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    @register_job(scheduler, "interval", seconds=60 * 60 * 12)
    def test_job():
        # 定时每12小时执行一次
        schedu.prepare()


    register_events(scheduler)
    # 启动定时器
    scheduler.start()
except Exception as e:
    print('定时任务异常：%s' % str(e))


# 推荐
class recommend(GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = Item_serializer

    def recom(self, pk):
        # 先查所有文章
        item_list = self.get_queryset()
        itemserializer = self.get_serializer(item_list, many=True)
        items = itemserializer.data

        # 查询此用户收藏的文章
        collection_list = Collection.objects.filter(id=pk)
        collectionserializer = Collection_serializer(instance=collection_list, many=True)
        collections = collectionserializer.data
        coll_id_list = []  # 将用户收藏的文章的序号放进队列
        for collection in collections:
            coll_id_list.append(collection['collection'])

        # 查询此用户喜欢的文章
        like_list = Like.objects.filter(id=pk)
        likeserializer = Like_serializer(instance=like_list, many=True)
        likes = likeserializer.data
        like_id_list = []  # 将用户喜欢的文章id放进列表
        for like in likes:
            like_id_list.append(like['like'])
        # 从items中随机抽取100个
        items = sample(items, 100)

        # 从所有文章中删除已被本用户收藏的文章
        for item in items:
            del item['auto_id_0']
            if item['id'] in coll_id_list:
                items.remove(item)

        logs = []
        for item in items:
            log = dict()
            log['user'] = pk
            log['itemid'] = int(item['id'])
            # -------------------------------------------
            log['tagid'] = int(len(item['tag']))  # 后期需将其换成真正的tagid
            # ---------------------------------------------
            log['time'] = 0
            if item['id'] in like_id_list:
                log['love'] = 1
            else:
                log['love'] = 0
            log['col'] = 0
            logs.append(log)

        # 将筛选后待推荐的文章存入文件
        header = list(logs[0].keys())
        with open("APP01/data/test.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(logs)

        # 调用模型进行预测
        from APP01 import cat
        return cat.boost(), items

    def get(self, request, pk):
        schedu.prepare()
        # 最终的推荐列表
        end_list = []
        i = 0
        while i < 5:
            i += 1
            # 先进行模型的预测
            recom_list, items = self.recom(pk=pk)

            for i in range(len(recom_list)):
                if recom_list[i] > 0.5:
                    end_list.append(items[i])

            if len(end_list) >= 10:
                return Response(end_list[:10])
            else:
                continue

        item_list = self.get_queryset()
        itemserializer = self.get_serializer(item_list, many=True)
        items = itemserializer.data
        items = sample(items, 10)
        return Response(items)
