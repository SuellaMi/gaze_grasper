# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

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

from tkinter import *
from tkinter import ttk

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
dxl1_goal_velocity = GOAL_VELOCITY1
dxl2_goal_velocity = GOAL_VELOCITY2
dxl3_goal_velocity = GOAL_VELOCITY3

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
        print("Dynamixel motor:" + str(motor_id) + "has been successfully connected")

# Why index = 0 ?
# index = 0


# Control moving by button GUI
# Close by Quit button
# Different functions for GUI interaction
def up(motor):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, motor, ADDR_GOAL_POSITION, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def down(motor):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, motor, ADDR_GOAL_POSITION, -1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def rotate_left():
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, DXL_ID[0], ADDR_GOAL_POSITION, -1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def rotate_right():
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, DXL_ID[0], ADDR_GOAL_POSITION, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def start_up(event, motor):
    up(motor_id)


def start_down(event, motor):
    down(motor_id)


def start_rotate_left(event):
    rotate_left()


def start_rotate_right(event):
    rotate_right()


def stop_moving(event, motor):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, motor_id, ADDR_GOAL_POSITION, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel motor:" + str(motor) + "stopped moving.")


root = Tk()

frm = ttk.Frame(root, padding=150)
frm.grid()

ttk.Label(frm, text="control robotic arm").grid(row=1, column=0)

# this will create a label widget
l1 = Label(root, text="DXL1:")
l2 = Label(root, text="DXL2:")
l3 = Label(root, text="DXL3:")

# grid method to arrange labels in respective
# rows and columns as specified
l1.grid(row=0, column=0, sticky=W, pady=2)
l2.grid(row=1, column=0, sticky=W, pady=2)
l3.grid(row=2, column=0, sticky=W, pady=2)

RotateLeftBtn = ttk.Button(frm, text="Left")
RotateLeftBtn.grid(row=0, column=1, pady=2)
RotateRightBtn = ttk.Button(frm, text="Right")
RotateRightBtn.grid(row=0, column=1, pady=2)

UpDYN1Btn = ttk.Button(frm, text="Up")
UpDYN1Btn.grid(row=1, column=1, pady=2)
DownDYN1Btn = ttk.Button(frm, text="Down")
DownDYN1Btn.grid(row=1, column=2, pady=2)

UpDYN2Btn = ttk.Button(frm, text="Up")
UpDYN2Btn.grid(row=2, column=1, pady=2)
DownDYN2Btn = ttk.Button(frm, text="Down")
DownDYN2Btn.grid(row=2, column=2, pady=2)

ttk.Label(frm, text="\n").grid(column=1, row=3)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=4)

# Enable button pressing for Dynamixel motor 1
# Rotate left
RotateLeftBtn.bind('<ButtonPress-1>', start_rotate_left)
RotateLeftBtn.bind('<ButtonRelease-1>', stop_moving(event=None, motor=DXL_ID[0]))
# Rotate right
RotateRightBtn.bind('<ButtonPress-1>', start_rotate_right)
RotateRightBtn.bind('<ButtonRelease-1>', stop_moving(event=None, motor=DXL_ID[0]))

# Enable button pressing for Dynamixel motor 2
# Moving up
UpDYN1Btn.bind('<ButtonPress-1>', start_up(event=None, motor=DXL_ID[1]))
UpDYN1Btn.bind('<ButtonRelease-1>', stop_moving(event=None, motor=DXL_ID[1]))

# Enable button pressing for Dynamixel motor 2
# Moving down
DownDYN1Btn.bind('<ButtonPress-1>', start_down(event=None, motor=DXL_ID[1]))
DownDYN1Btn.bind('<ButtonRelease-1>', stop_moving(event=None, motor=DXL_ID[1]))

# Enable button pressing for Dynamixel motor 3
# Moving up
UpDYN2Btn.bind('<ButtonPress-1>', start_up(event=None, motor=DXL_ID[2]))
UpDYN2Btn.bind('<ButtonRelease-1>', stop_moving(event=None, motor=DXL_ID[2]))

# Enable button pressing for Dynamixel motor 3
# Moving down
DownDYN2Btn.bind('<ButtonPress-1>', start_down(event=None, motor=DXL_ID[2]))
DownDYN2Btn.bind('<ButtonRelease-1>', stop_moving(event=None, motor=DXL_ID[2]))

# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()

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
