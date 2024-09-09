from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Video, SubtitleEntry
from api.serializers import VideoSerializer
from api.tasks import process_video


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        video_serializer = VideoSerializer(data=data)
        video_serializer.is_valid(raise_exception=True)
        video = video_serializer.save()
        process_video.delay(video.pk)
        return Response("processing")

    @action(detail=True, methods=['get'])
    def search_subtitles(self, request, *args, **kwargs):
        video = self.get_object()
        query = request.query_params.get('q', '')

        subtitle_entries = SubtitleEntry.objects.filter(
            subtitle__video=video,
            text__icontains=query
        )

        if not subtitle_entries.exists():
            return Response({"message": "No matching subtitles found"}, status=status.HTTP_404_NOT_FOUND)

        results = [
            {
                "start_time": entry.start_time,
                "end_time": entry.end_time,
                "text": entry.text
            }
            for entry in subtitle_entries
        ]

        return Response(results, status=status.HTTP_200_OK)
