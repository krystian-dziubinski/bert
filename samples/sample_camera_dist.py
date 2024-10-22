import numpy as np

# Function to calculate rotation matrix from roll, pitch, and yaw angles
def euler_to_rotation_matrix(roll, pitch, yaw):
    # Convert angles to radians
    roll_rad = np.radians(roll)
    pitch_rad = np.radians(pitch)
    yaw_rad = np.radians(yaw)

    # Calculate rotation matrix
    R_roll = np.array([[1, 0, 0],
                       [0, np.cos(roll_rad), -np.sin(roll_rad)],
                       [0, np.sin(roll_rad), np.cos(roll_rad)]])
    
    R_pitch = np.array([[np.cos(pitch_rad), 0, np.sin(pitch_rad)],
                        [0, 1, 0],
                        [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]])
    
    R_yaw = np.array([[np.cos(yaw_rad), -np.sin(yaw_rad), 0],
                      [np.sin(yaw_rad), np.cos(yaw_rad), 0],
                      [0, 0, 1]])

    # Combine the rotation matrices
    rotation_matrix = np.dot(R_yaw, np.dot(R_pitch, R_roll))
    
    return rotation_matrix

# Function to calculate Cartesian parameters for gripper destination
def calculate_gripper_destination(x_distance, y_distance, depth, camera_intrinsics, arm_position, arm_orientation):
    # Assuming camera is attached to the head of the robotic arm
    # Extract camera parameters
    fx, fy = camera_intrinsics  # focal lengths along x and y axes

    # Assuming arm_position is a vector [x, y, z] representing the position of the arm's base
    # Assuming arm_orientation is a vector [roll, pitch, yaw] representing the orientation of the arm
    
    # Assuming transformation from arm coordinates to camera coordinates is known,
    # for simplicity, we assume it's just a translation and rotation
    # You would need to replace this transformation with the actual transformation for your setup
    
    # Example transformation: 
    # Translate the camera position by the arm_position
    camera_position = np.array([x_distance, y_distance, depth]) + np.array(arm_position)
    
    # Calculate rotation matrix based on arm_orientation (roll, pitch, yaw)
    rotation_matrix = euler_to_rotation_matrix(*arm_orientation)
    
    # Apply rotation to camera position
    rotated_camera_position = np.dot(rotation_matrix, camera_position)
    
    # Calculate X and Y coordinates based on rotated camera position and camera intrinsics
    x_coordinate = rotated_camera_position[0] * depth / fx
    y_coordinate = rotated_camera_position[1] * depth / fy
    
    return x_coordinate, y_coordinate, depth

# Example values
x_distance = 20  # Horizontal distance from the middle reference point of the camera
y_distance =  2  # Vertical distance from the middle reference point of the camera
depth = 200      # Depth information (distance from the camera to the object)
camera_intrinsics = (4, 4)  # Example focal lengths along x and y axes
arm_position = [0, 0, 0]        # Position of the robotic arm's base
arm_orientation = [0, 90, 0]  # Roll, pitch, and yaw angles of the robotic arm

# Calculate gripper destination
x, y, z = calculate_gripper_destination(x_distance, y_distance, depth, camera_intrinsics, arm_position, arm_orientation)

# Print the result
print("Gripper Destination (X, Y, Z):", (x, y, z))
