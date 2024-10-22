# -*- coding: utf-8 -*-
from sympy import *
from math import *
import numpy as np

#from braccio_control_python import get_previous_teta

# Define arm lengths
l0 = 71.5       #distance from base to ground
l1 = 125        #shoulder to elbow
l2 = 125        #elbow to wrist  
l3 = 60 + 132   #wrist to gripper

r_compensation = 1.02  # add 2 percent for the arm angle compensation
z_compensation = 15   # add 15 mm for height backlash compensation 

 
def calculate_base_angle(x, y):
    """Calculate the base angle based on x and y coordinates. Vertical position of the destination point."""
    if y == 0:
        return 180 if x <= 0 else 0
    else:
        return 90 - degrees(atan(x / y))
    
def calculate_alpha1_radaians(r):
    """Calculate alpha1 based on r to radians. It is the angle between the base and the horizontal line."""
    sin_r=r-l2 #
    cos_r=l1+l3
    return acos((sin_r/ cos_r))

def calculate_horizontal_radious_of_circle_of_destination(x,y,z):
    """ This is calculate from pythagoras theorem. It is the distance from the base TIP (not bottom) to the destination point"""
    return sqrt((sqrt(x**2 + y**2))**2 + (z - l0)**2)

# def calculate_shoulder_angle(r,theta_wrist, alpha1):
#     """Calculate the shoulder angle based on r and alpha1."""
#     return degrees(alpha1 + asin((l3 - l1) / r)) if theta_wrist > 0 else degrees(alpha1)

# def calculate_elbow_and_wrist_angles(theta_wrist, alpha1, alpha3):
#     """Calculate the elbow and wrist angles based on alpha1 and alpha3."""
#     elbow_angle = (90 - degrees(alpha1)) + degrees(alpha3) 
#     wrist_angle = (90 - degrees(alpha1)) - degrees(alpha3)
#     return elbow_angle, wrist_angle

def move_to_position_cart(x, y, z):
    """Calculate the angles needed to move the arm to the given position."""


    theta_base = calculate_base_angle(x, y) #TODO: check if base compansation is needed

    z += z_compensation  # compensation for backlash TODO: check if this is needed
    r_hor = calculate_horizontal_radious_of_circle_of_destination(x,y,z)
    r = r_hor * r_compensation  # compensation for arm angle TODO: check if this is needed
    # Calculate angles for level operation
    alpha1=calculate_alpha1_radaians(r)
    theta_shoulder=degrees(alpha1)
    alpha3=asin((sin(alpha1)*l3-sin(alpha1)*l1)/l2)  #compensate for the difference in arm length
    theta_elbow=(90-degrees(alpha1))+degrees(alpha3)
    theta_wrist=(90+degrees(alpha1))+degrees(alpha3)
    
    if theta_wrist <=0: #when arm length compensation results in negative values
        alpha1=acos(((r-l2)/(l1+l3)))
        print("alpha1: ",alpha1)
        print("l3-l1: ",l3-l1)
        print("r: ",r)
        theta_shoulder=degrees(alpha1+asin((l3-l1)/r))
        theta_elbow=(90-degrees(alpha1))
        print("theta_elbow: ",theta_elbow)
        theta_wrist=(90+degrees(alpha1))
        print("theta_wrist: ",theta_wrist)
        print("alpha1: ",alpha1)
        print("alpha3: ",alpha3)
    # Adjust shoulder angle to increase height
    if z != l0:
        theta_shoulder += degrees(atan((z - l0) / r))

    # Add compensation for bad line-up of servo with mount
    theta_elbow += 5
    theta_wrist -= 5

    theta_array = [round(theta_base), round(theta_shoulder), round(theta_elbow), round(theta_wrist)]
    print("theta_array: ",theta_array)
    return theta_array

def get_previous_teta2():
    text_file = open("prev_teta.txt", "r")
    prev_teta_string=text_file.read()
    text_file.close()
    
    prev_teta= list(prev_teta_string.split(";"))
    prev_teta.pop(6)
    prev_teta=[int(i) for i in prev_teta]
    return prev_teta


def backlash_compensation_base(theta_base):
    theta_base=round(theta_base)
    theta_base_comp=theta_base
    
    compensation_value_CW=8  #degrees (CW roation)
    compensation_value_CCW=np.linspace(0, 14,135)
    prev_angles=get_previous_teta2()  #get previous theta's from txt file
    theta_base_prev=prev_angles[0]
    
    delta_theta_base=theta_base-theta_base_prev
    # print(delta_theta_base)
    if delta_theta_base>1:
        if theta_base<=45:
            theta_base_comp=theta_base
        else:
            index=int(round(theta_base-46))
            theta_base_comp=theta_base+compensation_value_CCW[index]
            theta_base_comp=round(theta_base_comp)
            # print("base theta compensated CCW, val: "+str(round(compensation_value_CCW[theta_base-46])))
    if delta_theta_base<-1:
        theta_base_comp=theta_base-compensation_value_CW
        # print("base theta compensated CW, val: "+str(compensation_value_CW))

        
    return theta_base_comp
    
    
    