from APP01.models import Item, Collection, Love, Tag
from APP01.serializers import Item_serializer, Collection_serializer, Love_serializer, Tag_serializer
import csv
from random import sample


def recom1(pk):
    # 先查所有文章
    item_list = Item.objects.all()
    itemserializer = Item_serializer(instance=item_list, many=True)
    items = itemserializer.data

    # 查询此用户收藏的文章
    collection_list = Collection.objects.filter(user=pk, category=1)
    collectionserializer = Collection_serializer(instance=collection_list, many=True)
    collections = collectionserializer.data
    coll_id_list = []  # 将用户收藏的文章的序号放进队列
    for collection in collections:
        coll_id_list.append(collection['collection'])

    # 查询此用户喜欢的文章
    like_list = Love.objects.filter(user=pk, category=1)
    likeserializer = Love_serializer(instance=like_list, many=True)
    likes = likeserializer.data
    like_id_list = []  # 将用户喜欢的文章id放进列表
    for like in likes:
        like_id_list.append(like['love'])
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

        # 查询文章的tag
        tag_one = Tag.objects.filter(tag=item['tag'])
        tag_serializer = Tag_serializer(instance=tag_one, many=True)
        tag_data = tag_serializer.data
        tagid = tag_data[0]['id']  # 查询为tagid
        log['tagid'] = int(tagid)

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
    return cat.boost1(), items
