from dynamixel_sdk import *  # Uses Dynamixel SDK library

import os
from pynput import keyboard
from tkinter import *
from tkinter import ttk

# import sys
# import tty
# import termios

# fd = sys.stdin.fileno()
# old_settings = termios.tcgetattr(fd)


#def getch():
#    try:
#        tty.setraw(sys.stdin.fileno())
#        ch = sys.stdin.read(1)
#    finally:
#        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#    return ch


# ********* DYNAMIXEL Model definition *********
MY_DXL = 'X_SERIES'
PROTOCOL_VERSION = 2.0

# Control table address
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_PRESENT_VELOCITY = 128
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
GOAL_VELOCITY0 = 80  # max: 265
GOAL_VELOCITY1 = 80  # max: 265
GOAL_VELOCITY2 = 80  # max: 265
# Refer to the Minimum Position Limit of product eManual
DXL_MINIMUM_POSITION_VALUE = 0
# Refer to the Maximum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE = 4095
BAUD_RATE = 57600

# Factory default ID of all DYNAMIXEL is 1
# For the robotic arm:
# ID: 0 is the base servo that controls the rotation of the robotic arm
# ID: 1, 2 are the servos that determine the height and horizontal distance of the gripper end
# ID: 3 controls the gripper
DXL0_ID = 0
DXL1_ID = 1
DXL2_ID = 2

# Use the actual port assigned to the U2D2
# Linux: "/dev/ttyUSB*"
DEVICE_NAME = '/dev/ttyUSB0'

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold
CHANGE_TO_VELOCITY = 1

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,
                     DXL_MAXIMUM_POSITION_VALUE]  # Goal position
dxl0_goal_velocity = GOAL_VELOCITY0
dxl1_goal_velocity = GOAL_VELOCITY1
dxl2_goal_velocity = GOAL_VELOCITY2

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
    # getch()
    quit()

# Set port baud rate
if portHandler.setBaudRate(BAUD_RATE):
    print("Succeeded to change the baud rate")
else:
    print("Failed to change the baud rate")
    print("Press any key to terminate...")
    # getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
    portHandler, DXL0_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("[0]Dynamixel has been successfully connected")


# Control moving by button GUI.
# Close by Quit button
# GUI interaction
def Up(motor_id):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, motor_id, ADDR_GOAL_VELOCITY, dxl1_goal_velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def Down(motor_id):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, motor_id, ADDR_GOAL_VELOCITY, -dxl2_goal_velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def RotateLeft():
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, DXL0_ID, ADDR_GOAL_VELOCITY, -dxl0_goal_velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def RotateRight():
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, DXL0_ID, ADDR_GOAL_VELOCITY, dxl0_goal_velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def start_up(event, motor_id):
    Up(motor_id)


def start_down(event, motor_id):
    Down(motor_id)


def start_rotate_left(event):
    RotateLeft()


def start_rotate_right(event):
    RotateRight()


def stop_moving(event, motor_id):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, motor_id, ADDR_GOAL_VELOCITY, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("motor" + motor_id + "stop")


root = Tk()

frm = ttk.Frame(root, padding=100)
frm.grid()

ttk.Label(frm, text="control robotic arm").grid(row=1, column=0)

# this will create a label widget
l1 = Label(root, text="DYN0:")
l2 = Label(root, text="DYN1:")
l3 = Label(root, text="DYN2:")

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

UpDYN1Btn.bind('<ButtonPress-1>', start_up(motor_id=DXL1_ID))
UpDYN1Btn.bind('<ButtonRelease-1>', stop_moving(motor_id=DXL1_ID))
UpDYN2Btn.bind('<ButtonPress-1>', start_up(motor_id=DXL2_ID))
UpDYN2Btn.bind('<ButtonRelease-1>', stop_moving(motor_id=DXL2_ID))

DownDYN1Btn.bind('<ButtonPress-1>', start_down(motor_id=DXL1_ID))
DownDYN1Btn.bind('<ButtonRelease-1>', stop_moving(motor_id=DXL1_ID))
DownDYN2Btn.bind('<ButtonPress-1>', start_down(motor_id=DXL2_ID))
DownDYN2Btn.bind('<ButtonRelease-1>', stop_moving(motor_id=DXL2_ID))

RotateLeftBtn.bind('<ButtonPress-1>', start_rotate_left)
RotateLeftBtn.bind('<ButtonRelease-1>', stop_moving(motor_id=DXL0_ID))
RotateRightBtn.bind('<ButtonPress-1>', start_rotate_right)
RotateRightBtn.bind('<ButtonRelease-1>', stop_moving(motor_id=DXL0_ID))

# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
    portHandler, DXL0_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()

print("closed")
