# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from APP01.models import Item, Video
from APP01.serializers import Item_serializer, Video_serializer
from rest_framework.response import Response
from rest_framework import status
from APP01.recom_pre import recom1
from APP01.recom_pre2 import recom2

from random import sample

# 定时任务
# 定时将log表内的数据读取到log.csv供catboost使用
from apscheduler.schedulers.background import BackgroundScheduler
from APP01 import schedu

try:
    scheduler = BackgroundScheduler()


    def test_job():
        # 定时每12小时执行一次
        schedu.prepare()


    scheduler.add_job(test_job, 'interval', hours=12, jitter=120)
    # 启动定时器
    scheduler.start()
except Exception as e:
    print('定时任务异常：%s' % str(e))


# 推荐文章
class recommend1(GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = Item_serializer

    def get(self, request, pk):
        # 最终的推荐列表
        end_list = []
        try:
            i = 0
            while i < 5:
                i += 1
                # 先进行模型的预测
                recom_list, items = recom1(pk=pk)

                for i in range(len(recom_list)):
                    if recom_list[i] > 0.5:
                        end_list.append(items[i])

                if len(end_list) >= 10:
                    print("推荐结果")
                    return Response(end_list[:10])
                else:
                    continue

        except Exception as e:
            print(str(e))
            item_list = self.get_queryset()
            itemserializer = self.get_serializer(item_list, many=True)
            items = itemserializer.data
            items = sample(items, 10)
            print("随机结果")
            return Response(items)

        # 如果预测结果为空返回随机结果
        item_list = self.get_queryset()
        itemserializer = self.get_serializer(item_list, many=True)
        items = itemserializer.data
        items = sample(items, 10)
        print("随机结果")
        return Response(items)



# 推荐视频
class recommend2(APIView):

    def get(self, request, pk):
        # 最终的推荐列表
        end_list = []
        try:
            i = 0
            while i < 5:
                i += 1
                # 先进行模型的预测
                recom_list, items = recom2(pk=pk)

                for i in range(len(recom_list)):
                    if recom_list[i] > 0.5:
                        end_list.append(items[i])

                if len(end_list) >= 8:
                    print("推荐结果")
                    return Response(end_list[:8])
                else:
                    continue
        except Exception as e:
            print(str(e))
            item_list = Video.objects.all()
            itemserializer = Video_serializer(instance=item_list, many=True)
            items = itemserializer.data
            items = sample(items, 8)
            print("随机结果")
            return Response(items)

        # 如果预测结果为空返回随机结果
        item_list = self.get_queryset()
        itemserializer = self.get_serializer(item_list, many=True)
        items = itemserializer.data
        items = sample(items, 10)
        print("随机结果")
        return Response(items)


class recom_prepare(APIView):
    def get(self, request):
        schedu.prepare()
        data = {"error": "ok"}
        return Response(data, status=status.HTTP_200_OK)
