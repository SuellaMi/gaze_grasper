# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tkinter as tk  # Used for the GUI

from Pixy_Controller import *
from kinematics import *
from dynamixel_sdk import *  # Uses Dynamixel SDK library

if os.name == 'nt':
    import msvcrt


    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)


    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# **************************************** DYNAMIXEL Model definition ***********************************************

# DYNAMIXEL Model definition for XL430-W250-T
MY_DXL = 'X_SERIES'
# DYNAMIXEL Protocol Version
PROTOCOL_VERSION = 2.0

# Control table addresses for X_SERIES
ADDR_TORQUE = 64  # Enable and disable the torque

ADDR_PRESENT_POSITION = 132  # Address for reading the current position
ADDR_GOAL_POSITION = 116  # Address for changing the position

ADDR_PROFILE_VELOCITY = 112  # Address for changing the velocity in positional mode

# Refer to the Minimum Position Limit of product eManual
DXL_MINIMUM_POSITION_VALUE = 0
# Refer to the Maximum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE = 4095
BAUD_RATE = 57600

# Factory default ID of all DYNAMIXEL is 1
# For the robotic arm:
# ID: 1 is the base servo that controls the rotation of the robotic arm
# ID: 2, 3 are the servos that determine the height and horizontal distance of the gripper end
# ID: 4 controls the gripper
DXL_ID = [1, 2, 3, 4]
# Gripper codes
OPEN = 100
CLOSE = 220

# Use the actual port assigned to the U2D2
# Linux: "/dev/ttyUSB*"
DEVICE_NAME = "/dev/ttyUSB0"

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque

ADDR_OPERATING_MODE = 11  # Address for changing the operating mode
CHANGE_TO_VELOCITY = 1  # Velocity Control Mode
CHANGE_TO_POSITION = 3  # Position Control Mode

# Define goal positions [0, 4095]
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,
                     DXL_MAXIMUM_POSITION_VALUE]  # Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux
portHandler = PortHandler(DEVICE_NAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baud rate
if portHandler.setBaudRate(BAUD_RATE):
    print("Succeeded to change the baud rate")
else:
    print("Failed to change the baud rate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque for each motor
# DXL_ID is an array which includes the different Dynamixel motor ID's
for motor_id in DXL_ID:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        # Read in initial position of motors
        present_position = get_position(packetHandler, portHandler, motor_id)
        # Read in initial speed of motors
        present_velocity = get_speed(packetHandler, portHandler, motor_id)
        # Change the data into degrees
        present_position = change_to_degrees(present_position)
        print("Dynamixel motor:" + str(motor_id) + " has been successfully connected.")
        print("The current position is:" + str(present_position))
        print("The current velocity is:" + str(present_velocity))

    # Set the initial velocity
    for x in DXL_ID:
        if x == 1:
            set_speed(packetHandler, portHandler, x, 90)
        set_speed(packetHandler, portHandler, x, 200)

# Set initial positions for motor: 2,3,4
initial_position = inverse_kinematics([27.7, 6.6, 0])
set_position(packetHandler, portHandler, DXL_ID[1], initial_position[1])
set_position(packetHandler, portHandler, DXL_ID[2], initial_position[2])
set_position(packetHandler, portHandler, DXL_ID[3], OPEN)
# Searching for an object in our environment
while True:
    # Get the offset of the block we locked on
    x_offset = offset_width()
    # If object can be directly tracked
    if (check_view() > 0) and (x_offset == 0.0):
        break
    else:
        # Move to look for the object between 90 and 270 degrees
        for x in range(90, 270):
            set_position(packetHandler, portHandler, DXL_ID[0], x)
            # Get the offset of the block we locked on
            x_offset = offset_width()
            print("The offset of x is: " + str(x_offset))
            # Move motor until we are centered
            if (check_view() > 0) and (x_offset == 0.0):
                break
    break
# Get the offset of the block we locked on
# x_offset = offset_width()
# Move motor until we are centered
# print("The offset of x is: " + str(x_offset))


# The event that triggers the arm to move
# Takes the input (degrees) from the users input and the corresponding id of the motor we want to move
# Checks if input is outside expected boundaries (0-180 degrees)
def start_moving(event):
    # Get the velocity input from GUI
    velocity = get_velocity()
    # Get the input values for x,y,z
    input_values = get_input_values()
    # Get the command to open or close the gripper
    gripper_code = get_gripper()
    # Set the speed for each motor
    for motor in DXL_ID:
        # Set velocity
        set_speed(packetHandler, portHandler, motor, velocity)
    # Do the inverse kinematics for each input value to get the motor values
    motor_values = inverse_kinematics(input_values)
    for motor in DXL_ID:
        if motor == 4:
            set_position(packetHandler, portHandler, motor, gripper_code)
        else:
            # Get the motor value for each motor
            motor_value = motor_values[motor - 1]
            # Set new positions for each motor
            set_position(packetHandler, portHandler, motor, motor_value)
    # Sleep for 1 msec, so that the motors can be brought in a new position before reading in again
    time.sleep(1)
    # Test the forward kinematics
    forward_kinematics(packetHandler, portHandler)


# ******************************************** Here starts the GUI**************************************************
# Initialize window
root = tk.Tk()

# Create text output
l1 = tk.Label(root, text="Robotic Arm Controller")
l2 = tk.Label(root, text="X:")
l3 = tk.Label(root, text="Y:")
l4 = tk.Label(root, text="Z:")
l5 = tk.Label(root, text="Gripper:")
l6 = tk.Label(root, text="Velocity:")

# Display text in GUI
l1.grid(row=0, column=0)
l2.grid(row=1, column=0)
l3.grid(row=2, column=0)
l4.grid(row=3, column=0)
l5.grid(row=4, column=0)
l6.grid(row=5, column=0)

# Create first entry field for DXL1
entry1 = tk.StringVar()
field1 = tk.Entry(root, textvariable=entry1)

# Create second entry field for DXL2
entry2 = tk.StringVar()
field2 = tk.Entry(root, textvariable=entry2)

# Create third entry field for DXL3
entry3 = tk.StringVar()
field3 = tk.Entry(root, textvariable=entry3)

# Create fourth entry field for gripper
entry4 = tk.StringVar()
field4 = tk.Entry(root, textvariable=entry4)

# Create fifth entry for velocity
entry5 = tk.StringVar()
field5 = tk.Entry(root, textvariable=entry5)

# Display entry fields
field1.grid(row=1, column=1)
field2.grid(row=2, column=1)
field3.grid(row=3, column=1)
field4.grid(row=4, column=1)
field5.grid(row=5, column=1)


# Function to get the input for the motors from the GUI
def get_input_values():
    input_values = [float(field1.get()), float(field2.get()), float(field3.get())]
    return input_values


# Function to get the velocity entry from GUI
def get_velocity():
    velocity = int(field5.get())
    return velocity


# Function to get the command to open or close the gripper
def get_gripper():
    gripper_code = float(field4.get())
    return gripper_code


# Create OK button to start movement
MovingBtn = tk.Button(root, text="OK")
MovingBtn.grid(row=1, column=2)
# Call moving function
MovingBtn.bind('<ButtonPress-1>', start_moving)

tk.Button(root, text="Quit", command=root.destroy).grid(row=6, column=1)

# Infinite loop which can be terminated by keyboard or mouse interrupt
root.mainloop()

# Disable Dynamixel Torque for each motor
# DXL_ID is an array which includes the different Dynamixel motor ID's
for motor_id in DXL_ID:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()

print("closed")
