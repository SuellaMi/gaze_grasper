from dynamixel_sdk import *  # Uses Dynamixel SDK library
from numpy import *  # Used for inverse kinematics

# Control table addresses for X_SERIES
ADDR_PRESENT_POSITION = 132  # Address for reading the current position
ADDR_GOAL_POSITION = 116  # Address for changing the position

ADDR_PROFILE_VELOCITY = 112  # Address for changing the velocity in positional mode

ADDR_OPERATING_MODE = 11  # Address for changing the operating mode


# Helper function, to map the dynamixel data to degrees
# Returns degrees as floats, rounded down to two decimals
def change_to_degrees(data):
    degree = round(float((data * 360.0) / 4095.0), 2)
    return degree


# Function that does the inverse kinematics
# The link lengths of our robotic arm in cm (link1=18cm, link2=27cm)
def inverse_kinematics(input_values, link1, link2):
    print("input:" + str(input_values))
    # Desired position of end effector (3D)
    x = input_values[0]
    y = input_values[1]
    z = input_values[2]
    # Equations for inverse kinematics with 3-DOF
    r1 = sqrt(x ** 2 + y ** 2)  # Equation 1

    # Calculate angles for the first two joints (theta1 and theta2) as before
    phi1 = arccos((link2 ** 2 - link1 ** 2 - r1 ** 2) / (-2 * link1 * r1))  # Equation 2
    phi2 = arctan2(-y, x)  # Equation 3
    phi3 = arccos((r1 ** 2 - link1 ** 2 - link2 ** 2) / (-2 * link1 * link2))

    theta1 = 180 + rad2deg(phi2 - phi1)  # Equation 4 converted to degrees
    theta2 = 90 + rad2deg(phi3)

    # Calculate the angle for the new joint (theta3) for z-axis movement
    theta3 = 180 + rad2deg(arctan2(z, r1))

    # Return a new array with calculated motor values in degrees
    # Map: theta3 -> motor1, theta1 -> motor2, theta2 -> motor3

    # If x is smaller than 0 we have to adjust the theta1 and theta2 values
    if x < 0:
        theta1 = - theta1
        theta2 = 540 - theta2
    # If x is positive no need to adjust the values
    motor_values = [theta3, theta1, theta2]
    # Throw error message if input for DXL_ID 1 is out of boundaries
    if (motor_values[0] < 0.0) or (motor_values[0] > 270.0):
        raise ValueError("Sorry, invalid output:" + str(motor_values[0]))
    # Throw error message if input for DXL_ID 2 is out of boundaries
    if (motor_values[1] < 0.0) or (motor_values[1] > 180.0):
        raise ValueError("Sorry, invalid output:" + str(motor_values[1]))
    # Throw error message if input for DXL_ID 3 is out of boundaries
    if (motor_values[2] < 0.0) or (motor_values[2] > 360.0):
        raise ValueError("Sorry, invalid output:" + str(motor_values[1]))
    # Print the calculated degrees
    print("For IK, Link1:" + str(link1) + "Link2:" + str(link2))
    print("The new motor values in degrees are: " + str(motor_values))
    # Returns an array that includes the calculated theta values for each motor
    return motor_values


# Function that does the forward kinematics
# The link lengths of our robotic arm in cm (link1=18cm, link2=27cm)
def forward_kinematics(packetHandler, portHandler, link1, link2):
    # Get current position for each motor
    position1 = change_to_degrees(get_position(packetHandler, portHandler, 1))
    position2 = change_to_degrees(get_position(packetHandler, portHandler, 2))
    position3 = change_to_degrees(get_position(packetHandler, portHandler, 3))
    # Given joint angles (in degrees for this example)
    theta1 = deg2rad(position2 - 180)  # Convert to radians
    theta2 = deg2rad(270 - position3)  # Convert to radians
    theta3 = deg2rad(position1 - 180)  # Convert to radians, example value for the 3rd DOF

    # Forward kinematics equations
    x = link1 * cos(theta1) + (link2 * cos(theta1 + theta2))
    y = (-(link1 * sin(theta1) + (link2 * sin(theta1 + theta2)))) + 11

    # Compute r, the projection of the end effector on XY plane
    r = sqrt(x ** 2 + y ** 2)

    # Compute the z-coordinate of the end effector using theta3
    z = r * tan(theta3)
    # Add point values to one array
    point_values = [x, y, z]
    # Print the values
    print("For FK, Link1:" + str(link1) + "Link2:" + str(link2))
    print("The points we are getting from the forward kinematics are: " + str(point_values))
    # Return target points
    return point_values


# Get the current position
def get_position(packetHandler, portHandler, motor):
    present_position, result, error = packetHandler.read4ByteTxRx(portHandler, motor, ADDR_PRESENT_POSITION)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    return present_position


# Set a new position for the robotic arm
def set_position(packetHandler, portHandler, motor, degree_position):
    # Converts degrees back to the data that is readable by the dynamixel
    new_position = int((degree_position * 4095.0) / 360.0)
    result, error = packetHandler.write4ByteTxRx(portHandler, motor, ADDR_GOAL_POSITION, new_position)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))


# Get the current velocity
def get_speed(packetHandler, portHandler, motor):
    present_velocity, result, error = packetHandler.read4ByteTxRx(portHandler, motor, ADDR_PROFILE_VELOCITY)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
    return present_velocity


# Set the speed
def set_speed(packetHandler, portHandler, motor, speed):
    speed = int(speed * 0.229)
    result, error = packetHandler.write4ByteTxRx(portHandler, motor, ADDR_PROFILE_VELOCITY, speed)
    if result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(result))
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
