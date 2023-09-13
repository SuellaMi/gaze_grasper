# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tkinter as tk

from dynamixel_sdk import *  # Uses Dynamixel SDK library

# ........................................Port handling................................................
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
# ......................................Control Table..............................................
portHandler = PortHandler("/dev/ttyUSB0")
packetHandler = PacketHandler(2.0)
BAUD_RATE = 57600
ADDR_TORQUE_ENABLE = 64
TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
ADDR_OPERATING_MODE = 11
CHANGE_TO_VELOCITY = 1
CHANGE_TO_POSITION = 3
ADDR_GOAL_VELOCITY = 104
ADDR_GOAL_POSITION = 116
DXL_ID = 1

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


# ..........................................Helper Functions..........................................

def set_degree():
    degree = get_degree()
    position_val = int((degree * 4095.0) / 360.0)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position_val)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def enable_torque():
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def disable_torque():
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


def set_operating_mode(mode):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


# ...........................................Code...................................................


def start_moving(event):
    set_operating_mode(CHANGE_TO_VELOCITY)
    enable_torque()
    set_speed()
    disable_torque()
    set_operating_mode(CHANGE_TO_POSITION)
    enable_torque()
    set_degree()
    disable_torque()


disable_torque()
# ..........................................GUI...................................................
root = tk.Tk()

l1 = tk.Label(root, text="DXL1:")
l2 = tk.Label(root, text="Velocity:")

l1.grid(row=1, column=0)
l2.grid(row=2, column=0)

entry1 = tk.StringVar()
field1 = tk.Entry(root, textvariable=entry1)

entry2 = tk.StringVar()
field2 = tk.Entry(root, textvariable=entry2)

field1.grid(row=1, column=1)
field2.grid(row=2, column=1)


def get_velocity():
    velocity = int(field2.get())
    return velocity


def get_degree():
    degree = float(field1.get())
    return degree


def set_speed():
    velocity = get_velocity()
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))


MovingBtn = tk.Button(root, text="OK")
MovingBtn.grid(row=1, column=2)
MovingBtn.bind('<ButtonPress-1>', start_moving)

tk.Button(root, text="Quit", command=root.destroy).grid(row=5, column=1)
root.mainloop()

# Close port
portHandler.closePort()

print("closed")
