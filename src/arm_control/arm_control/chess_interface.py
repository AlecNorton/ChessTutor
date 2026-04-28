import rclpy
from rclpy.node import Node
from open_manipulator_msgs.srv import SetKinematicsPose
import sys
from std_msgs.msg import Float32MultiArray, String


'''s
class BasicRobotControl(Node):
    def __init__(self):
        super().__init__('basic_robot_control')
        #self.client = self.create_client(SetJointPosition, 'goal_joint_space_path')

        self.joint_command = self.create_subscription(Float32MultiArray, '/chess_joints', self.recv_command, 10)
        
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

class Interface(Node):

    def __init__(self):
        super().__init__('Robot_Control')
        self.command_joints = self.create_publisher(Float32MultiArray, 'chess_pos', 10)

        
        #print("Did a data: ", data)
    def publish(self, data):
        msg = Float32MultiArray()
        #data = self.chess_mappings[command_name]
        msg.data = data
        print("Data: ", data)
        self.command_joints.publish(msg)
    
    


def main(args=None):
    rclpy.init(args=args)
    valid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    valid_numbers = ['1', '2', '3', '4', '5']
    interface = Interface()
    a1 = [0.1,0.06,0.05,-0.20429387342668381,0.6661030581833234,0.21033662531077235,0.6858055360027521]

    flag = True
    while(flag):
        chess_command = input("Enter chess notation (a-h)(1-8): ")
        if chess_command == 'q':
            flag = False
        elif chess_command[0] in valid_letters and chess_command[1] in valid_numbers:
            y_offset = valid_letters.index(chess_command[0])
            x_offset = valid_numbers.index(chess_command[1])
            print(x_offset)
            print(y_offset)
            data = a1.copy()
            print("Data: ", data)
            data[0] = data[0] + (0.027 * x_offset)
            data[1] = data[1] - (0.027 * y_offset)
            interface.publish(data)
        else:
            print("Wrong input, try again.")


    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    interface.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
