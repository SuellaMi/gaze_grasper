from __future__ import print_function

import ctypes
import pixy2.build.python_demos.pixy as pixy2
from ctypes import *

import bluetooth

# Pixy2 Python SWIG get blocks example #

print("Pixy2 Python SWIG Example -- Get Blocks")

pixy2.init()
pixy2.change_prog("color_connected_components")


class Blocks(Structure):
    _fields_ = [("m_signature", c_uint),
                ("m_x", c_uint),
                ("m_y", c_uint),
                ("m_width", c_uint),
                ("m_height", c_uint),
                ("m_angle", c_uint),
                ("m_index", c_uint),
                ("m_age", c_uint)]


MINIMUM_BLOCK_AGE_TO_LOCK = 30


# Searches for an object in our frame we can lock on
def set_target(color_code):
    blocks = pixy2.BlockArray(100)
    # Count all detected objects
    count_blocks = pixy2.ccc_get_blocks(100, blocks)
    for obj in range(0, count_blocks):
        # Checks if block has correct color
        if blocks[obj].msignature == color_code:
            # Returns largest block in frame (nearest block to PixyCam) with correct color code
            print(str(blocks[obj]))
            return blocks[obj]


# Checks if there are any objects detected
# !!!!!!!! change give an id for a block that you want to lock on
def check_view():
    blocks = pixy2.BlockArray(100)
    count = pixy2.ccc_get_blocks(100, blocks)
    return count


def check_quarter_frame():
    blocks = pixy2.BlockArray(1)
    count = pixy2.ccc_get_blocks(1, blocks)
    if count > 0:
        frame_y = pixy2.get_frame_height()
        quarter_frame = frame_y - (frame_y / 4)
        obj_y = blocks[0].m_y
        print(quarter_frame, obj_y)
        return [True, quarter_frame, obj_y]
    else:
        return [False]


# Prints all the blocks recognized by the PixyCam
def print_blocks():
    blocks = pixy2.BlockArray(100)
    frame = 0
    count = pixy2.ccc_get_blocks(100, blocks)

    while 1:
        if count > 0:
            print('frame %3d:' % frame)
            frame = frame + 1
            for index in range(0, count):
                print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (
                    blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width,
                    blocks[index].m_height))


# Prints one single block
def display_block(index, block):
    print('Block[%3d]: I: %3d / S:%2d / X:%3d / Y:%3d / W:%3d / H:%3d / A:%3d' % (
        index, block.m_index, block.m_signature, block.m_x, block.m_y, block.m_width, block.m_height, block.m_age))


def find_center():
    blocks = pixy2.BlockArray(10)
    frame = 0
    locked_on_block = False
    locked_block_index = 0

    while True:
        count = pixy2.ccc_get_blocks(1, blocks)

        frame = frame + 1

        if blocks[0].m_age > MINIMUM_BLOCK_AGE_TO_LOCK:
            locked_block_index = blocks[0].m_index
            locked_on_block = True

        if locked_on_block:
            for index in range(0, count):
                if blocks[index].m_index == locked_block_index:
                    print('Frame %3d: Locked' % frame)
                    display_block(index, blocks[index])
                    x_offset = (pixy2.get_frame_width() / 2) - blocks[index].m_x
                    # y_offset = (pixy2.get_frame_height() / 2) - blocks[index].m_y
                    return x_offset


# Get the frame from the Pixy Camera. Returns the frame
def get_Frame():
    clibrary = ctypes.CDLL("File")
    return clibrary.get_raw_frame()


# Creates the Bluetooth loop by creating a BluetoothServe4r, where data were received.
# It gets the integer from the Android Application.
def bluetooth_loop():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    uuid ="00001101-0000-1000-8000-00805f9b34fb"
    bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print("Waiting for connection on RFCOMM channel", port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

