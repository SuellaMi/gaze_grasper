from dynamixel_sdk import *  # Uses Dynamixel SDK library
from numpy import *  # Used for inverse kinematics

# Control table address for X_SERIES
ADDR_GOAL_POSITION = 116  # Address for changing the position
ADDR_GOAL_VELOCITY = 104  # Address for changing the velocity
ADDR_OPERATING_MODE = 11  # Address for changing the operating mode

# The link lengths of our robotic arm in cm
link1 = 17.5
link2 = 14
link3 = 1


# Helper function, to map the dynamixel data to degrees
# Returns degrees as floats, rounded down to two digits
def change_to_degrees(data):
    degrees = round(float((data * 360.0) / 4095.0), 2)
    return degrees


# Function that does the inverse kinematics
def inverse_kinematics(motor_values):
    # Desired position of end effector (3D)
    x = motor_values[0]
    y = motor_values[1]
    z = motor_values[2]
    # Equations for inverse kinematics with 3-DOF
    r1 = sqrt(x ** 2 + y ** 2)  # Equation 1

    # Calculate angles for the first two joints (theta1 and theta2) as before
    phi1 = arccos((link2 ** 2 - link1 ** 2 - r1 ** 2) / (-2 * link1 * r1))  # Equation 2
    phi2 = arctan2(-y + 8, x)  # Equation 3
    phi3 = arccos((r1 ** 2 - link1 ** 2 - link2 ** 2) / (-2 * link1 * link2))

    theta1 = 180 + rad2deg(phi2 - phi1) + 12.2  # Equation 4 converted to degrees + buffer
    theta2 = 270 - rad2deg(phi3) - 23.57

    # Calculate the angle for the new joint (theta3) for z-axis movement
    theta3 = rad2deg(arctan2(z, r1))

    # Return the new array with calculated values in correct motor order
    # Theta1 belongs to Motor2
    motor_values[1] = theta1
    # Theta2 belongs to Motor3
    motor_values[2] = theta2
    # Theta3 belongs to Motor1
    motor_values[0] = theta3
    return motor_values


# Helper function, to set a new position for the robotic arm
def set_position(packetHandler, portHandler, motor, new_position):
    # Converts degrees back to the data that is readable by the dynamixel
    # position_val = int((data * 4095.0) / 360.0)
    result, error = packetHandler.write4ByteTxRx(portHandler, motor, ADDR_GOAL_POSITION, new_position)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))


# Changes the operating mode
def set_operating_mode(packetHandler, portHandler, DXL_ID, mode):
    result, error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
