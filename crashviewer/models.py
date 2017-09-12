from django.db import models
from django.utils import timezone
import django_tables2 as tables


# Has: CrashData's
class Project(models.Model):
    name = models.TextField()
    comment = models.TextField()


# Has: NetworkMessage's
class CrashData(models.Model):
    seed = models.CharField(max_length = 64)
    offset = models.IntegerField()
    module = models.CharField(max_length = 1024)
    signal = models.IntegerField()
    asanoutput = models.TextField()
    time = models.DateTimeField()
    stdout = models.TextField()
    filename = models.CharField(max_length = 1024)

    project = models.ForeignKey('Project', related_name='crashDataList', on_delete=models.CASCADE, null=True)

    class Meta:
         ordering = ('time',)


class NetworkMessage(models.Model):
    crashData = models.ForeignKey('CrashData', related_name="messageList", on_delete=models.CASCADE, null = True)
    index = models.IntegerField()
    sentBy = models.CharField(max_length = 16)
    msg = models.BinaryField()
    fuzzed = models.IntegerField()


class CrashDataTable(tables.Table):
    class Meta:
        model = CrashData
        fields = ('id', 'seed', 'offset', 'signal', 'time')
        attrs = {'class': 'paleblue','width':'100%'}
