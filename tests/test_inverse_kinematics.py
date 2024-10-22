# test_solverNNA.py
import pytest
from math import * 
from inverse_kinematics import *


l0 = 71.5       #distance from base to ground
l1 = 125        #shoulder to elbow
l2 = 125        #elbow to wrist  
l3 = 60 + 132   #wrist to gripper

def forward_kinemetics(l1,l2,l3,theta1,theta2,theta3):
    # Calculate the position of the end effector
    x = l1 * cos(theta1) + l2 * cos(theta1 + theta2) + l3 * cos(theta1 + theta2 + theta3)
    z = l1 * sin(theta1) + l2 * sin(theta1 + theta2) + l3 * sin(theta1 + theta2 + theta3)
    return x,z

def test_calculate_base_angle():
    # Test when y is 0 and x is negative
    assert calculate_base_angle(-1, 0) == 180

    # Test when y is 0 and x is positive
    assert calculate_base_angle(1, 0) == 0
    assert calculate_base_angle(2, 2) == 45.0
    assert calculate_base_angle(2, 1) == 26.565051177077983
    assert calculate_base_angle(-2, -2) == 45.0
    assert calculate_base_angle(100, 0) == 0
    assert calculate_base_angle(0, 100) == 90
    assert calculate_base_angle(0, -100) == 90
    assert calculate_base_angle(20, 100) == 78.69006752597979
    assert calculate_base_angle(10, 400) == 88.56790381583535         

    # Test when y is not 0
    x, y = 1, 1
    expected_angle = 90 - degrees(atan(x / y))
    assert calculate_base_angle(x, y) == expected_angle



# def test_calculate_shoulder_angle():
#     # Define arm lengths
#     l1 = 125
#     l3 = 60 + 132
#     # Test when (l3 - l1) / r is within the range -1 to 1
#     r, alpha1 = 100, 0.5
#     expected_angle = degrees(alpha1 + asin((l3 - l1) / r))
#     assert calculate_shoulder_angle(r, alpha1) == expected_angle

#     # Test when (l3 - l1) / r is outside the range -1 to 1
#     r, alpha1 = 10, 0.5
#     expected_angle = degrees(alpha1)
#     assert calculate_shoulder_angle(r, alpha1) == expected_angle

# def test_calculate_elbow_and_wrist_angles():
#     # Test with alpha1 = 0.5 and alpha3 = 0.3
#     alpha1, alpha3 = 0.5, 0.3
#     elbow_angle, wrist_angle = calculate_elbow_and_wrist_angles(alpha1, alpha3)
#     assert 78.54084409738354 == elbow_angle
#     assert 44.16337638953414 == wrist_angle

#     # Test with alpha1 = 0.7 and alpha3 = 0.2
#     alpha1, alpha3 = 0.7, 0.2
#     expected_elbow_angle = (90 - degrees(alpha1)) + degrees(alpha3)
#     expected_wrist_angle = (90 - degrees(alpha1)) - degrees(alpha3)
#     elbow_angle, wrist_angle = calculate_elbow_and_wrist_angles(alpha1, alpha3)
#     assert elbow_angle == expected_elbow_angle
#     assert wrist_angle == expected_wrist_angle


def test_calculate_alpha1():
    assert calculate_alpha1_radaians(1) == 1.9726958249959086

def test_calculate_horizontal_radious_of_circle_of_destination():
    assert calculate_horizontal_radious_of_circle_of_destination(1,1,1) == 70.5141829705202

def test_move_to_position_cart():
    assert move_to_position_cart(0,50,10) == [90, 66, 27, 217]