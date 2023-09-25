from __future__ import print_function

import pixy2.build.python_demos.pixy as pixy2
from ctypes import *

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


blocks = pixy2.BlockArray(100)


# mylib = ctypes.CDLL()


# Searches for an object in our frame we can lock on
def set_target(color_code):
    # Count all detected objects
    count_blocks = pixy2.ccc_get_blocks(100, blocks)
    for obj in range(0, count_blocks):
        # Checks if block has correct color
        if blocks[obj].msignature == color_code:
            # Returns largest block in frame (nearest block to PixyCam) with correct color code
            print(str(blocks[obj]))
            return blocks[obj]


# Checks if there are any objects detected
def check_view():
    count = pixy2.ccc_get_blocks()
    return count


# Prints all the blocks recognized by the PixyCam
def print_blocks():
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


# Pixy Cam follows given target
def center_target(block):
    # Get the frame width (x) in pixel
    frame_x = pixy2.get_frame_width()
    # Get the frame height (y) in pixel
    frame_y = pixy2.get_frame_height()
    # Calculate the middle of the frame
    frame_center = (frame_x / 2, frame_y / 2)
    # Get the center of the target object
    obj_center = (block.m_x, block.m_y)

    # if (frame_center[0] != obj_center[0]) or (frame_center[1] != obj_center[1]):
