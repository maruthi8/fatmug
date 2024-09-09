from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    language = models.CharField(max_length=10)
    content = models.TextField()

    def __str__(self):
        return f"Subtitle for {self.video.title} ({self.language})"


class SubtitleEntry(models.Model):
    """This will Particularly useful for search functionality, as we can query entries based on their text content"""
    subtitle = models.ForeignKey(Subtitle, on_delete=models.CASCADE, related_name='entries')
    start_time = models.FloatField()
    end_time = models.FloatField()
    text = models.TextField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}: {self.text[:30]}..."

    class Meta:
        ordering = ['start_time']
