from django.shortcuts import get_object_or_404
import re

from ..models import VideoProcessor


def get_rtsp_url_by_processor_id(processor_id: int) -> str:
    """
    Gets Video processor's camera RTSP url by Video processor ID.

    Args:
        processor_id: Video processor ID by which to get Parking lots map.
    """
    processor = get_object_or_404(VideoProcessor, pk=processor_id)

    return processor.stream_url
