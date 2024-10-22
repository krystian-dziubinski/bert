import cv2
import numpy as np
import threading
import time
from ardurino_control_python import Arm
from stero_vision.stereo_vision import FaceDetector
from stero_vision.triangulation import find_depth

class DistanceCalculator:
    def __init__(self, arm):
        self.center_face = None
        self.center_frame = None
        self.stop_thread = False
        self.arm = arm
        self.current_coodinate = [0, 0, 200]

    def calculate_distance(self):
        while not self.stop_thread:
            if self.center_face is not None and self.center_frame is not None:
                distance_x = self.center_frame[0] - self.center_face[0]
                distance_y = self.center_frame[1] - self.center_face[1]
                print("Cartesian distance in x: ", distance_x)
                print("Cartesian distance in y: ", distance_y)
                try:
                    self.current_coodinate = arm.go_to_coordinate(self.current_coodinate[0] + distance_x, 100, self.current_coodinate[2]+distance_y)
                except Exception as e:
                    print("Error moving the arm: ", e)
            time.sleep(0.5)  # Wait for 2 seconds

def detect_faces_in_stream(arm):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)

    distance_calculator = DistanceCalculator(arm)
    thread = threading.Thread(target=distance_calculator.calculate_distance)
    thread.start()

    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around each face and a point in the middle
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            distance_calculator.center_face = (x + w//2, y + h//2)
            cv2.circle(img, distance_calculator.center_face, radius=5, color=(255, 0, 0), thickness=-1)  # Blue point

        # Draw a red point in the middle of the frame
        height, width, _ = img.shape
        distance_calculator.center_frame = (width//2, height//2)
        cv2.circle(img, distance_calculator.center_frame, radius=5, color=(0, 0, 255), thickness=-1)  # Red point

        # Display
        cv2.imshow('img', img)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
            
    # Release the VideoCapture object
    cap.release()
    distance_calculator.stop_thread = True
    thread.join()
    arm.close()

def track_face_distance():
    cap_right = cv2.VideoCapture(1)
    cap_left = cv2.VideoCapture(0)

    face_detector_right = FaceDetector(cap_right, "right")
    face_detector_left  = FaceDetector(cap_left, "left")

    while cap_left.isOpened() and cap_right.isOpened():
        successL, frame_left = cap_left.read()
        successR, frame_right = cap_right.read()
        frame_right = cv2.flip(frame_right, 0)  # Flip the right frame vertically
                
        if not successL or not successR:   
            raise ValueError("Cannot read the frame")
            
        try:
            center_point_right = next(face_detector_right.detect_faces(frame_right))
        except StopIteration:
            center_point_right = None

        try:
            center_point_left = next(face_detector_left.detect_faces(frame_left))
        except StopIteration:
            center_point_left = None

        if center_point_right is not None and center_point_left is not None:
            depth = find_depth(center_point_right, center_point_left, frame_right, frame_left)

            cv2.putText(frame_right, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)
            cv2.putText(frame_left, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0),3)

            print("Depth: ", str(round(depth,1)))
            
            arm.adjust_based_on_depth(depth)  # Adjust the arm based on depth
        
        cv2.imshow("left frame", frame_left)
        cv2.imshow("right frame", frame_right)
    

        # Release and destroy all windows before termination
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_right.release()
    cap_left.release()
    cv2.destroyAllWindows()

def main():
    arm = Arm('/dev/tty.usbmodem141101')
    # detect_faces_in_stream(arm)
    while True:
        command = input("Enter command (go_to <x> <y> <z>, exit, detect_faces): ")
        parts = command.split()
        if parts[0] == 'go_to':
            if len(parts) == 4:
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                arm.go_to(x, y, z)
            else:
                print("Invalid number of arguments. Usage: add <x> <y>")
        elif command == 'detect_faces':
            track_face_distance()
        elif command == 'exit':
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    # main()
    arm = Arm('/dev/tty.usbmodem1101')
    arm.go_to(0, 100, 200)
    track_face_distance()