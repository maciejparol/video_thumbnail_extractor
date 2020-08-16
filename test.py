import uuid
from os import path

import cv2
import pytest

from exceptions import ExtractThumbnailFromVideoException
from extractor import ExtractThumbnailFromVideo

DESTINATION_PATH = "/tmp/thumbnail"


def test_file_not_exist():
    with pytest.raises(ExtractThumbnailFromVideoException) as excinfo:
        ExtractThumbnailFromVideo(tolerance_threshold=1, destination_thumbnail_path=DESTINATION_PATH).extract(
            "fake_video.mp4")
        assert excinfo == "Video fake_video.mp4 does not exist or file is broken"


def test_video_with_non_blank_frames(mocker):
    mocker.patch('extractor.ExtractThumbnailFromVideo._extract_last_non_blank', return_value=None)
    with pytest.raises(ExtractThumbnailFromVideoException) as excinfo:
        ExtractThumbnailFromVideo(tolerance_threshold=1, destination_thumbnail_path=DESTINATION_PATH).extract(
            "tests_data/test_video.mp4")
        assert excinfo == "Not found non-blank frame in video"


def test_tolerance_threshold_out_of_range():
    with pytest.raises(ExtractThumbnailFromVideoException) as excinfo:
        ExtractThumbnailFromVideo(tolerance_threshold=1300).extract("tests_data/test_video.mp4")
        assert excinfo == "Tolerance threshold out of range: 0-127"


def test_thumbnail_destination_path():
    destination_path = f"/tmp/{uuid.uuid4()}"
    assert not path.exists(destination_path)
    ExtractThumbnailFromVideo(destination_thumbnail_path=destination_path)
    assert path.exists(destination_path)


def test_with_tolerance_tolerance_threshold():
    frame_path = ExtractThumbnailFromVideo(tolerance_threshold=1, destination_thumbnail_path=DESTINATION_PATH).extract(
        "tests_data/test_video.mp4")
    frame_from_extractor = cv2.imread(frame_path)
    original_frame = cv2.imread("tests_data/output_frame_with_threshold.jpg")
    assert frame_from_extractor.all() == original_frame.all()


def test_without_tolerance_tolerance_threshold():
    frame_path = ExtractThumbnailFromVideo(tolerance_threshold=1, destination_thumbnail_path=DESTINATION_PATH).extract(
        "tests_data/test_video.mp4")
    frame_from_extractor = cv2.imread(frame_path)
    original_frame = cv2.imread("tests_data/output_frame_without_threshold.jpg")
    assert frame_from_extractor.all() == original_frame.all()
