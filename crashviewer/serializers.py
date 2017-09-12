from rest_framework import serializers
from crashviewer.models import Project, CrashData, NetworkMessage



class NetworkMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMessage
        fields = ('index', 'sentBy', 'msg', 'fuzzed', 'crashData')


class CrashDataSerializer(serializers.ModelSerializer):
    messageList = NetworkMessageSerializer(many=True)

    class Meta:
        model = CrashData
        fields = ('seed', 'offset', 'module', 'signal', 'asanoutput', 'time', 'stdout', 'filename', 'project', 'messageList')


    def create(self, validated_data):
        messageList_data = validated_data.pop('messageList')

        crashData = CrashData.objects.create(**validated_data)
        for message in messageList_data:
            NetworkMessage.objects.create(crashData=crashData, **message)
        return crashData



class ProjectSerializer(serializers.ModelSerializer):
    crashDataList = CrashDataSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'comment', 'crashDataList')
