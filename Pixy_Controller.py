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


MINIMUM_BLOCK_AGE_TO_LOCK = 30


# mylib = ctypes.CDLL()


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
def check_view():
    blocks = pixy2.BlockArray(100)
    count = pixy2.ccc_get_blocks(100, blocks)
    return count


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


# Pixy Cam checks if an object is centered in the frame width (x)
def offset_width():
    frame = 0
    locked_on_block = False
    locked_block_index = 0
    blocks = pixy2.BlockArray(1)

    while True:
        count = pixy2.ccc_get_blocks(1, blocks)

        frame = frame + 1

        # Block acquisition logic #
        if locked_on_block:
            # Find the block that we are locked to
            for Index in range(0, count):
                if Blocks[Index].m_index == locked_block_index:
                    print('Frame %3d: Locked' % frame)
                    display_block(Index, Blocks[Index])

                    x_offset = (pixy2.get_frame_width() / 2) - Blocks[Index].m_x
                    return x_offset
        else:
            print('Frame %3d:' % frame)

            # Display all the blocks in the frame
            for index in range(0, count):
                display_block(index, blocks[index])

            # Find an acceptable block to lock on to #
            if Blocks[0].m_age > MINIMUM_BLOCK_AGE_TO_LOCK:
                locked_block_index = Blocks[0].m_index
                locked_on_block = True
