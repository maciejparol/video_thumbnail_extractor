import uuid
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

from exceptions import ExtractThumbnailFromVideoException


class ExtractThumbnailFromVideo:
    def __init__(self, tolerance_threshold: Optional[int] = None,
                 destination_thumbnail_path: Optional[str] = None) -> None:
        self.destination_thumbnail_path = self._destination_path_creator(destination_thumbnail_path)
        self.tolerance_threshold = tolerance_threshold
        if isinstance(tolerance_threshold, int) and not 0 < tolerance_threshold < 128:
            raise ExtractThumbnailFromVideoException(f"Tolerance threshold out of range: 0-127")

    def extract(self, video_path: str) -> str:
        video_cap = cv2.VideoCapture(video_path)
        if not video_cap.isOpened():
            raise ExtractThumbnailFromVideoException(f"Video {video_path} does not exist or file is broken")

        non_blank_frame = self._extract_last_non_blank(video_cap)
        if isinstance(non_blank_frame, np.ndarray):
            non_blank_frame_name = str(uuid.uuid4())
            self._save_image(non_blank_frame, non_blank_frame_name, self.destination_thumbnail_path)
            return f"{self.destination_thumbnail_path}/{non_blank_frame_name}.jpg"
        raise ExtractThumbnailFromVideoException(f"Not found non-blank frame in video")

    @staticmethod
    def _check_if_frame_is_blank(frame, tolerance_threshold: Optional[float]) -> bool:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if tolerance_threshold:
            return np.std(gray_frame) > tolerance_threshold
        return cv2.countNonZero(gray_frame) != 0

    @staticmethod
    def _destination_path_creator(path: Optional[str]) -> str:
        if path:
            path = path[-1] if path.endswith("/") else path
            Path(path).mkdir(parents=True, exist_ok=True)
            return path
        return "."

    def _extract_last_non_blank(self, video_cap: cv2.VideoCapture) -> Optional[np.ndarray]:
        frame_count = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        blank = True
        frame_count -= 1
        while blank and not frame_count < 0:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
            success, frame = video_cap.read()
            if not success:
                raise ExtractThumbnailFromVideoException(f"Error while extracting frame {frame_count}")
            if self._check_if_frame_is_blank(frame, self.tolerance_threshold):
                return frame
            frame_count -= 1

    @staticmethod
    def _save_image(image: np.ndarray, name: str, path: Optional[str] = None) -> None:
        if path:
            if path.endswith("/"):
                path = path[:-1]
        else:
            path = '.'
        cv2.imwrite(f"{path}/{name}.jpg", image)
