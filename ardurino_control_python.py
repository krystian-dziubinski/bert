import serial
import time
import inverse_kinematics
import numpy as np


class Arm:
    def __init__(self, port='/dev/tty.usbmodem1101'):
        self.ser = serial.Serial(port, 115201, timeout=5)
        time.sleep(2)
        print("Initializing arm") 
        time.sleep(2)
        self.ser.write(b'H0,90,20,90,90,73,20\n')  #home the arm at low speeds
        time.sleep(2)  # Wait for the Arduino to initialize
        self.base =[0,0,180,0]  #default value for base, min value and max value, write location
        self.shoulder=[150,15,165,1]
        self.elbow=[0,0,180,2]
        self.wrist=[0,0,180,3]
        self.wristRot=[90,0,180,4]
        self.gripper=[73,73,0,5]

    def close(self):
        self.ser.close()

    def write_arduino(self, angles):
        
        angles[0]=180-angles[0]  #invert degrees for base
        angles[3]=180-angles[3]  #invert degrees for base
        angle_string=','.join([str(elem) for elem in angles])  # join the list values togheter
        angle_string="P"+angle_string+",200\n"    
        self.ser.write(angle_string.encode())          #.encode encodes the string to bytes
                
        

    def rotate_joint(self, joint):  #rotate a specifi joint to the outer limits of the joint angles

        def calculate_joint(self, joint,number):
            angle_string_def_angles=[self.base[0],self.shoulder[0],self.elbow[0],self.wrist[0],self.wristRot[0],self.gripper[0]]  #load in default values
            angle_string_def_angles[joint[3]]=joint[number]  #write minimum angle to the string
            self.write_arduino(angle_string_def_angles)
            
        calculate_joint(joint,1)
        time.sleep(2)
        calculate_joint(joint,2)
        time.sleep(2)
        calculate_joint(joint,1)
        time.sleep(2)
        
        
        
    def home(self,speed=20):
        print("Homing the arm.")
        angle_string_def_angles=[self.base[0],self.shoulder[0],self.elbow[0],self.wrist[0],self.wristRot[0],self.gripper[0]]
        self.write_arduino(angle_string_def_angles)

    def rotate_all_joints(self):
        print("The base.")
        self.rotate_joint(self.base)
        print("The shoulder.")
        self.rotate_joint(self.shoulder)
        print("The elbow.")
        self.rotate_joint(self.elbow)
        print("The vertical axis of the wrist.")
        self.rotate_joint(self.wrist)
        print("The rotational axis of the wrist.")
        self.rotate_joint(self.wristRot)
        print("The gripper.")
        self.rotate_joint(self.gripper)
    
    def write_position(self, *args, **kwargs):


        theta_base = args[0] if len(args) > 0 else self.base[0]
        theta_shoulder = args[1] if len(args) > 1 else self.shoulder[0]
        theta_elbow = args[2] if len(args) > 2 else self.elbow[0]
        theta_wrist = args[3] if len(args) > 3 else self.wrist[0]
        theta_wristRot = args[4] if len(args) > 4 else self.wristRot[0]
        grip = kwargs.get('grip', 'open')
        
        if grip=="closed":
            theta_gripper=self.gripper[1]
        if grip=="open":
            theta_gripper=self.gripper[2]

        theta_base_comp= inverse_kinematics.backlash_compensation_base(theta_base)  #check if compensation is neededbacklash_compensation_base(theta_base)  #check if compensation is needed    
            
        angle_string_def_angles=[theta_base_comp,theta_shoulder,theta_elbow,theta_wrist,theta_wristRot,theta_gripper]
        self.write_arduino(angle_string_def_angles)
        
        #write angle values in txt file without the compensation
        angles=[theta_base,theta_shoulder,theta_elbow,theta_wrist,theta_wristRot,theta_gripper]

        text_file = open("prev_teta.txt", "w")
        iteration=[0,1,2,3,4,5]
        for elem in iteration:
            text_file.write(str(angles[elem]))
            text_file.write(";")
        text_file.close()
        
        
    def go_to(self,x,y,z,grip_position="open"):
        print("Moving to coordinate: ",x,y,z)
        theta_list=inverse_kinematics.move_to_position_cart(x,y,z)
        self.write_position(theta_list[0],theta_list[1],theta_list[2],theta_list[3],grip=grip_position)
        return (x,y,z)
        
        
    def move_vertical(self, x,y):
        loop_iteration=np.linspace(0, 350, 2)
        for z in loop_iteration:
            print(z)
            self.go_to(x,y,round(z))
            time.sleep(2)
            
    def move_horizontal(self,z):
        loop_iteration=np.linspace(100, 350,2)
        for x in loop_iteration:
            print(x)
            self.go_to(round(x),0,z)
            time.sleep(2)
            
            
    def get_previous_teta():
        text_file = open("prev_teta.txt", "r")
        prev_teta_string=text_file.read()
        text_file.close()
        
        prev_teta= list(prev_teta_string.split(";"))
        prev_teta.pop(6)
        prev_teta=[int(i) for i in prev_teta]
        return prev_teta

    def open_gripper(self):
        print('opening gripper')
        prev_angles=self.get_previous_teta()
        self.write_position(prev_angles[0],prev_angles[1],prev_angles[2],prev_angles[3],prev_angles[4],grip="open")
        
    def close_gripper(self):
        print('closing gripper')
        prev_angles=self.get_previous_teta()
        self.write_position(prev_angles[0],prev_angles[1],prev_angles[2],prev_angles[3],prev_angles[4],grip="closed")  
        
        
        
    def pick_up(self,x,y):
        glass_pos=[310,95] #x,y pos of glass
        delay=1  #delay between steps
        pick_up_heigth=10  #heigth of the object
        self.home()
        time.sleep(delay)
        self.go_to(x,y,100,"closed")
        time.sleep(delay)
        self.open_gripper()
        time.sleep(delay)
        print('pick-up foam')
        self.go_to(x,y,pick_up_heigth-20,"open")
        time.sleep(delay)
        self.close_gripper()
        time.sleep(delay)
        self.go_to(x,y,200,"closed")
        time.sleep(delay)
        self.go_to(glass_pos[0],glass_pos[1],200,"closed")
        time.sleep(delay)
        self.go_to(glass_pos[0],glass_pos[1],120,"closed")
        time.sleep(delay)
        self.open_gripper()
        self.home()
        
    def backlash(self):
        print("Performing backlash compensation")
        time.sleep(5)
        self.write_position(90,0,90,90)
        time.sleep(2)
        self.write_position(45,0,90,90)
        time.sleep(2)
        self.write_position(90,0,90,90)

    # %%
    def camera_compensation(x_coordinate,y_coordinate):
        h_foam=80  #fam heigth of 80mm
        camera_position=[480,150,880]  #x,y,z coordinate from origin in mm
        #add 300 to move orgin to under the camera
        offset=300
        x_coordinate=(offset-x_coordinate)+(camera_position[0]-offset)
        
        #perform compensation
        x_compensated=x_coordinate-(h_foam/(camera_position[2]/x_coordinate))
        if y_coordinate<camera_position[1]:
            y_compensated=y_coordinate-(h_foam/(camera_position[2]/y_coordinate))
        else:
            y_compensated=y_coordinate+(h_foam/(camera_position[2]/y_coordinate))
        #substract the offset
        x_compensated=offset-(x_compensated-(camera_position[0]-offset))
        
        return int(x_compensated),int(y_compensated)
        
