from APP01.models import Log
from APP01.serializers import Log_serializer
import csv
from APP01 import cat

def prepare():
    queryset = Log.objects.all()
    log_data = Log_serializer(instance=queryset, many=True).data
    for log in log_data:
        del log['id']
    header = list(log_data[0].keys())
    with open("APP01/data/log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(log_data)
    cat.cat_prepare()