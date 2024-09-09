from rest_framework import serializers
from api.models import Video, Subtitle, SubtitleEntry


class SubtitleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtitleEntry
        fields = ['id', 'start_time', 'end_time', 'text']


class SubtitleSerializer(serializers.ModelSerializer):
    entries = SubtitleEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Subtitle
        fields = ['id', 'language', 'content', 'entries']


class VideoSerializer(serializers.ModelSerializer):
    subtitles = SubtitleSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'file', 'uploaded_at', 'subtitles']


class SubtitleSearchResultSerializer(serializers.Serializer):
    start_time = serializers.FloatField()
    end_time = serializers.FloatField()
    text = serializers.CharField()
