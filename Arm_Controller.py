# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tkinter as tk

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

# ********* DYNAMIXEL Model definition *********

# DYNAMIXEL Model definition for XL430-W250-T
MY_DXL = 'X_SERIES'
# DYNAMIXEL Protocol Version
PROTOCOL_VERSION = 2.0

# Control table address for X_SERIES
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_PRESENT_VELOCITY = 128
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
GOAL_VELOCITY1 = 80  # max: 265
GOAL_VELOCITY2 = 80  # max: 265
GOAL_VELOCITY3 = 80  # max: 265
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
DXL_ID = [1, 2, 3]

# Use the actual port assigned to the U2D2
# Linux: "/dev/ttyUSB*"
DEVICE_NAME = "/dev/ttyUSB0"

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold
CHANGE_TO_VELOCITY = 1

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
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel motor:" + str(motor_id) + " has been successfully connected")


# Helper function, to map the input value to the real world position
def set_goal_position(motor, degree):
    position_val = int((degree * 4095) / 360)
    result, error = packetHandler.write4ByteTxRx(portHandler, motor, ADDR_GOAL_POSITION, position_val)
    return result, error


# Moving function
def moving(motor_id, degree):
    dxl_comm_result, dxl_error = set_goal_position(motor_id, degree)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


# The event that triggers the arm to move
# Takes the input (degrees) from the users input and the corresponding id of the motor we want to move
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Checks still have to bet done
# Checks input number
def start_moving(event):
    for motor in DXL_ID:
        moving(motor, get_degrees()[motor - 1])


# Initialize window
root = tk.Tk()

# Create text output
l1 = tk.Label(root, text="Robotic Arm Controller")
l2 = tk.Label(root, text="DXL1:")
l3 = tk.Label(root, text="DXL2:")
l4 = tk.Label(root, text="DXL3:")

# Display text in GUI
l1.grid(row=0, column=0)
l2.grid(row=1, column=0)
l3.grid(row=2, column=0)
l4.grid(row=3, column=0)

# Create first entry field
# Call variablenname.get() to get the degrees
entry1 = tk.StringVar()
field1 = tk.Entry(root, textvariable=entry1)

# Create second entry field
entry2 = tk.StringVar()
field2 = tk.Entry(root, textvariable=entry2)

# Create third entry field
entry3 = tk.StringVar()
field3 = tk.Entry(root, textvariable=entry3)

# Display entry fields
field1.grid(row=1, column=1)
field2.grid(row=2, column=1)
field3.grid(row=3, column=1)


# Function to get the entries
def get_degrees():
    degrees = [int(field1.get()), int(field2.get()), int(field3.get())]
    return degrees


# Create OK button to start movement
MovingBtn = tk.Button(root, text="OK")
MovingBtn.grid(row=1, column=2)
# Call moving function
MovingBtn.bind('<ButtonPress-1>', start_moving)

tk.Button(root, text="Quit", command=root.destroy).grid(column=1, row=4)

# Infinite loop which can be terminated by keyboard or mouse interrupt
root.mainloop()

# Disable Dynamixel Torque for each motor
# DXL_ID is an array which includes the different Dynamixel motor ID's
for motor_id in DXL_ID:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, motor_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()

print("closed")
