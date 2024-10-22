import cv2
import numpy as np




# The focal length is the first element of the diagonal of the camera matrix
focal_length = 1500  # in pixels

# Calculate the field of view
sensor_width = 4.8  # width of the sensor in mm, adjust to your camera's sensor
field_of_view = 2 * np.arctan(sensor_width / (2 * focal_length))

print("Focal length: ", focal_length)
print("Field of view: ", np.degrees(field_of_view), "degrees")