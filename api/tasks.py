import os
import subprocess
import logging

from django.conf import settings
from celery import shared_task
from .models import Video, Subtitle, SubtitleEntry

logger = logging.getLogger(__name__)


@shared_task
def process_video(video_id):
    try:
        video = Video.objects.get(id=video_id)
        video_path = os.path.join(settings.MEDIA_ROOT, str(video.file))
        output_srt = os.path.join(settings.MEDIA_ROOT, f"{video.id}_subtitles.srt")

        logger.info(f"Processing video: {video_path}")
        logger.info(f"Output SRT file: {output_srt}")

        # Check if input video file exists
        if not os.path.exists(video_path):
            logger.error(f"Input video file not found: {video_path}")
            return f"Error: Input video file not found for video {video.id}"

        command = [
            'docker', 'run', '--rm',
            '-v', f"{os.getenv('HOST_MEDIA_PATH')}:/app/media",
            '-w', '/app/media',
            'ccextractor:latest', video_path, '-o', output_srt
        ]
        logger.info(f"Trying CCExtractor with options: {' '.join(command)}")

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(f"CCExtractor output: {result.stdout}")
            logger.info(f"CCExtractor return code: {result.returncode}")

            # If subtitles were extracted, break the loop
            if os.path.exists(output_srt) and os.path.getsize(output_srt) > 0:
                logger.info("Subtitles successfully extracted.")
            else:
                logger.warning("No subtitles extracted with these options. Trying next option set.")

        except subprocess.TimeoutExpired:
            logger.warning("CCExtractor process timed out. Trying next option set.")
        except subprocess.CalledProcessError as e:
            logger.error(f"CCExtractor command failed: {e}")
            logger.error(f"Error output: {e.stderr}")

            # Remove empty output file if it was created
            if os.path.exists(output_srt) and os.path.getsize(output_srt) == 0:
                os.remove(output_srt)

        # Final check if subtitles were extracted
        if os.path.exists(output_srt) and os.path.getsize(output_srt) > 0:
            with open(output_srt, 'r', encoding='utf-8') as srt_file:
                subtitle_content = srt_file.read()

            subtitle = Subtitle.objects.create(video=video, language='en', content=subtitle_content)
            parse_srt(subtitle, subtitle_content)

            os.remove(output_srt)
            return f"Processed video {video.id}: {video.title}"
        else:
            logger.warning(f"No subtitles extracted for video {video.id}: {video.title}")
            return f"No subtitles found for video {video.id}: {video.title}"

    except Exception as e:
        logger.error(f"Error processing video {video_id}: {str(e)}")
        logger.exception("Full traceback:")
        return f"Error: Unexpected exception for video {video_id}"


def parse_srt(subtitle, content):
    entries = content.strip().split('\n\n')
    for entry in entries:
        lines = entry.split('\n')
        if len(lines) >= 3:
            times = lines[1].split(' --> ')
            start_time = time_to_seconds(times[0])
            end_time = time_to_seconds(times[1])
            text = ' '.join(lines[2:])
            SubtitleEntry.objects.create(
                subtitle=subtitle,
                start_time=start_time,
                end_time=end_time,
                text=text
            )


def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s.replace(',', '.'))
