from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Control table address for X_SERIES
ADDR_GOAL_POSITION = 116  # Address for changing the position
ADDR_GOAL_VELOCITY = 104  # Address for changing the velocity
ADDR_OPERATING_MODE = 11  # Address for changing the operating mode


# Helper function, to map the dynamixel data to degrees
# Return degrees as floats, rounded down to two digits
def change_to_degrees(data):
    degrees = round(float((data * 360.0) / 4095.0), 2)
    return degrees


# Helper function, to set a new position for the robotic arm
def set_position(packetHandler, portHandler, motor, data):
    # Converts degrees back to the data that is readable by the dynamixel
    position_val = int((data * 4095.0) / 360.0)
    result, error = packetHandler.write4ByteTxRx(portHandler, motor, ADDR_GOAL_POSITION, position_val)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))


def set_operating_mode(packetHandler, portHandler, DXL_ID, mode):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
