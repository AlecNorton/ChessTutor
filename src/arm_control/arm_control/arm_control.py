import rclpy
from rclpy.node import Node
from open_manipulator_msgs.srv import SetJointPosition
import sys
from std_msgs.msg import Float32MultiArray, String
import math
import array
'''

class BasicRobotControl(Node):
    def __init__(self):
        super().__init__('basic_robot_control')
        #self.client = self.create_client(SetJointPosition, 'goal_joint_space_path')

        self.joint_command = self.create_subscription(Float32MultiArray, 'chess_joints', self.recv_command, 10)
        
        #while not self.client.wait_for_service(timeout_sec=1.0):
        #    if not rclpy.ok():
        #        self.get_logger().error('Interrupted while waiting for the service. Exiting.')
        #        sys.exit(0)
        #    self.get_logger().info('Service not available, waiting again...')

    def recv_command(self, msg):
        joints = msg.data
        self.send_request(joints)
        rclpy.spin_until_future_complete(self, self.future)
        response = self.future.result


    def send_request(self, joints):
        request = SetJointPosition.Request()
        request.planning_group = ''
        request.joint_position.joint_name = ['joint1', 'joint2', 'joint3', 'joint4', 'gripper']
        request.joint_position.position = joints
        #request.joint_position.position = [0.0, 0.0, 0.0, 0.0, 0.0]
        request.path_time = 5.0

        self.future = self.client.call_async(request)
'''

class RobotControl(Node):

    def __init__(self):
        super().__init__('Robot_Control')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'chess_joints',
            self.recv_command,
            10)
        self.client = self.create_client(SetJointPosition, 'goal_joint_space_path')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        #Prevent unused variable warnings
        self.subscription  # prevent unused variable warning
        self.future = None

    def recv_command(self, msg):
        if self.future is None:
            data = msg.data
            #print("Data")
            request = SetJointPosition.Request()
            request.planning_group = ''
            request.joint_position.joint_name= ['joint1', 'joint2', 'joint3', 'joint4', 'gripper']

            request.joint_position.position = array.array('d', data)
            request.path_time = 5.0
            print("Request: ", request)
            self.future = self.client.call_async(request)
        #print("Did a data: ", data)

    
    def spin(self):
        while rclpy.ok():
            rclpy.spin_once(self)
            if self.future is None:
                print("Waiting for chess commands...")
            else:
                #print("Request is not none.")
                if self.future.done():
                    res = self.future.result()
                    print("received service result : {}".format(res))
                    self.future = None


def main(args=None):
    rclpy.init(args=args)

    robot_control = RobotControl()

    robot_control.spin()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    robot_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
