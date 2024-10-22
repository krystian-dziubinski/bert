import cv2
import time
import stero_vision.calibration as calibration
import mediapipe as mp


class FaceDetector:

    def __init__(self, cap, camera_side):
        self.mp_facedetector = mp.solutions.face_detection
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cap
        self.camera_side = camera_side

    def detect_faces(self, frame):
        with self.mp_facedetector.FaceDetection(min_detection_confidence=0.7) as face_detection:
            if self.camera_side == "right":
                frame = cv2.flip(frame, -1)

            frame = calibration.undistortRectify(frame, self.camera_side)
            start = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            for center_point in self._handle_detection(frame, results):
                yield center_point

            end = time.time()
            totalTime = end - start
            fps = 1 / totalTime
            cv2.putText(frame, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    def _handle_detection(self, frame, results):
        if results.detections is not None:
            for id, detection in enumerate(results.detections):
                self.mp_draw.draw_detection(frame, detection)
                bBox = detection.location_data.relative_bounding_box
                h, w, c = frame.shape
                boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)
                center_point = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)
                cv2.putText(frame, f'{int(detection.score[0] * 100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                yield center_point