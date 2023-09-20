from __future__ import print_function
from ctypes import *
from pixycamev3 import *
from pixycamev3.pixy2 import Pixy2

# Pixy2 Python SWIG get blocks example #

print("Get Blocks")

pixy = Pixy2(port=1, i2c_address=0x54)


class Blocks(Structure):
    _fields_ = [("m_signature", c_uint),
                ("m_x", c_uint),
                ("m_y", c_uint),
                ("m_width", c_uint),
                ("m_height", c_uint),
                ("m_angle", c_uint),
                ("m_index", c_uint),
                ("m_age", c_uint)]


blocks = Blocks[100]
frame = 0

while 1:
    count = pixy.get_blocks(1, 100)

    if count > 0:
        print('frame %3d:' % frame)
        frame = frame + 1
        for index in range(0, count):
            print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (
                blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width,
                blocks[index].m_height))
