import rclpy
from rclpy.node import Node
from open_manipulator_msgs.srv import SetKinematicsPose
import sys
from std_msgs.msg import Float32MultiArray, String
import chess 
import time

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
        self.recv_board = self.create_subscription(String, 'chess_board', self.recv_board, 10)

        self.chess_states = {"a1": [.603, -.235, .738, 1.080], "a2": [.449, -.054, .601, 1.032], "a3":[.397, .086, .368, 1.127], "a4":[.290, .304, .074, 1.204], "a5":[.279, .359, -.041, 1.223], 
                             "b1":  [.314, -.356, .881, 1.015], "b2": [.249, -.198, .723, 1.017] , "b3": [.193, -.009, .492, 1.057], "b4": [.160, .193, .239, 1.109], "b5": [.161, .347, -.014, 1.204], 
                             "c1": [0.000, -.397, .894, 1.048], "c2": [0.000, -.198, .729, 1.015], "c3":[0.000, -.048, .531, 1.065], "c4": [0.000, .153, .201, 1.193], "c5": [0.000, .364, -.058, 1.247], 
                             "d1":  [-.241, -.288, .836, 1.034], "d2":  [-.152, -.124, .664, 1.043], "d3":[-.152, .051, .394, 1.131], "d4":[-.120, .098, .341, 1.029], "d5":[-.120, .379, -.091, 1.259], 
                             "e1": [-.535, -.235, .796, 1.023], "e2": [-.411, -.092, .653, 1.025], "e3": [-.316, .066, .431, .992], "e4":[-.298, .196, .276, 1.014], "e5":[-.265, .385, -.087, 1.243], 
                             "f1":[-.739, -.198, .755, .989] , "f2": [-.621, -.067, .588, 1.023], "f3":[-.509, .086, .402, 1.057], "f4": [-.417, .256, .140, 1.150], "f5":[-.368, .405, -.100, 1.239], 
                             "g1": [-.905, -.003, .541, 1.011], "g2": [-.738, .135, .333, 1.080], "g3": [-.620, .253, .118, 1.173], "g4": [-.526, .408, -.143, 1.292], "g5":[-.483, .561, -.394, 1.387], 
                             "h1": [-1.014, .112, .296, 1.175], "h2": [-.870, .288, .109, 1.186], "h3":[-.733, .425, -.212, 1.376], "h4": [-.650, .588, -.448, 1.440], "h5":[-.595, .793, -.861, 1.649]}
        self.chess_point = {"a1": [.621, -.383, .190, 1.772], "a2":  [.469, -.212, .155, 1.635], "a3":[.390, -.008, -.084, 1.671], "a4":[.291, .144, -.235, 1.666], "a5":[.282, .291, -.299, 1.540], 
                             "b1":[.314, -.495, .565, 1.471], "b2":[.249, -.336, .390, 1.493], "b3":[.193, -.133, .164, 1.506], "b4": [.160, .087, -.005, 1.450], "b5":[.160, .278, -.373, 1.637], 
                             "c1": [0.000, -.528, .503, 1.572], "c2": [0.000, -.337, .368, 1.520], "c3":[0.000, -.156, .291, 1.414], "c4":[0.000, .083, -.075, 1.545], "c5":[0.000, .301, -.430, 1.667], 
                             "d1": [-.241, -.419, .322, 1.681] , "d2": [-.152, -.255, .279, 1.563], "d3":[-.152, -.040, .061, 1.557], "d4": [-.120, .126, -.256, 1.717], "d5":[-.120, .327, -.368, 1.592], 
                             "e1": [-.535, -.376, .382, 1.582] , "e2":[-.411, -.230, .192, 1.624], "e3": [-.314, -.058, .244, 1.305], "e4": [-.298, .055, .038, 1.387], "e5":[-.265, .325, -.365, 1.582], 
                             "f1":[-.739, -.353, .307, 1.598] , "f2":[-.621, -.175, .399, 1.319] , "f3":[-.508, -.009, .242, 1.308], "f4":[-.417, .164, -.247, 1.629], "f5":[-.368, .347, -.387, 1.588], 
                             "g1": [-.905, -.141, .265, 1.425], "g2":  [-.738, .023, .031, 1.496], "g3":[-.620, 1.81, -.262, 1.638], "g4": [-.526, .396, -.629, 1.793], "g5":[-.483, .560, -.776, 1.758], 
                             "h1":[-1.014, .032, -.100, 1.652] , "h2":  [-.870, .206, -.249, 1.615], "h3": [-.733, .459, -.818, 1.928], "h4":[-.649, .669, -1.035, 1.947], "h5":[-.575, .772, -1.141, 1.948]}

        #self.a1 = [0.075,0.06,0.07,0.00099947,0.68064208, -0.00099947,0.73261475, -1.0]
        self.home = [1.600, .445, -.543, 1.618, 0.0]
        self.valid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.valid_numbers = ['1', '2', '3', '4', '5']
        self.board = None
        #print("Did a data: ", data)
    def publish(self, data):
        msg = Float32MultiArray()
        #data = self.chess_mappings[command_name]
        print("Data: ", data)
        msg.data = data
        self.command_joints.publish(msg)
    
    def pose_for_square(self, chess_string):
        if chess_string[0] in self.valid_letters and chess_string[1] in self.valid_numbers:
            pick_up_pose = self.chess_states[chess_string]
            point_pose = self.chess_point[chess_string]
            if(len(pick_up_pose) < 5):
                pick_up_pose.append(-1.0)
                point_pose.append(-1.0)
            else:
                pick_up_pose[4] = -1.0
                point_pose[4] = -1.0
            return pick_up_pose, point_pose
        else:
            print("Move incorrect for robot workspace (limited movement!)")

    def captured(self, chess_move):
        print("Capturing...")
        chess_string = chess_move[2:4]
        pick_up_pose, point_pose = self.pose_for_square(chess_string)
        #open
        
        #self.publish(point_pose)
        #manuevering down and closing over chess piece.
        self.pickup(pick_up_pose, point_pose)
        #Manuevering to deposit piece in captured area...
        self.publish(self.home)

    def pickup(self, pick_up_pose, point_pose):

        print("Picking up.")
        assert len(point_pose) == 5
        point_pose[4] = 0.0
        pick_up_pose[4] = 1.0

        self.publish(point_pose)
        self.publish(pick_up_pose)
        point_pose[4] = -1.0
        self.publish(point_pose)

    def dropoff(self, pick_up_pose, point_pose):
        print("picking down..")
        point_pose[4] = -1.0
        pick_up_pose[4] = 0.0
        #Move above spot
        self.publish(point_pose)
        #Move down and drop
        self.publish(pick_up_pose)
        #Move up.
        self.publish(point_pose)


    def make_move(self, chess_move):
        print("Making move")
        pick_up_pose, point_pose = self.pose_for_square(chess_move[0:2])
        print("pick_up_pose: ", pick_up_pose)
        #print("picking up..")
        self.pickup(pick_up_pose, point_pose)
        pick_up_pose, point_pose = self.pose_for_square(chess_move[2:4])
        self.dropoff(pick_up_pose, point_pose)
        print("Moving home.")
        self.publish(self.home)
        

    def recv_board(self, msg):
        if(self.board == None):
            self.board = chess.Board(msg.data)
            print("Updating board state for first time!")
        else:
            print("HELLO???")
            prevBoard = self.board
            self.board = chess.Board(msg.data)
            print("new fen: ", self.board.fen()[0:-9])
            move_str = 0
            captured = False
            states = [i+k for i in self.valid_letters for k in self.valid_numbers]
        
            for move in prevBoard.generate_pseudo_legal_moves():
                print("Move: ", move)
                try:
                    print("This occurred.")
                    print("Old FEN: ", prevBoard.fen()[0:-9])
                    prevBoard.push(move)
                    print("New FEN: ", prevBoard.fen()[0:-9])
                except:
                    print("This is happening")
                    continue
                print("Comparing...: {}, {},".format(prevBoard.fen()[0:-9], self.board.fen()[0:-9]))
                b1 = prevBoard.fen()[0:-9]
                b2 = prevBoard.fen()[0:-9]
                if b1 == b2:
                    move_str = move.uci()
                    if prevBoard.is_capture(move):
                        captured = True
                    break
                else:
                    print("{}, {}".format(b1, b2))
                prevBoard.pop()
            if(move_str == 0):
                print("Error in chess board. Valid move between two boards not found.")
            else:
                if(captured):
                    self.captured(move_str)
                self.make_move(move_str)
                    
            
                
            
    
    


def main(args=None):
    rclpy.init(args=args)
    interface = Interface()
    '''
    valid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    valid_numbers = ['1', '2', '3', '4', '5']
    interface = Interface()

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
            data[0] = data[0] + x_offset
            data[1] = data[1] - y_offset
            interface.publish(data)
            data[3] = data[3] -.3
            data[7] = 1
        else:
            print("Wrong input, try again.")


    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    '''
    #interface.make_move("a1h1")
    #time.sleep(5.0)
    #print("Doing r2")
    #interface.make_move("h1h5")
    #time.sleep(5.0)
    #interface.make_move("h5a5")
    #time.sleep(5.0)
    #interface.make_move("a5a1")
    #interface.make_move("a1c2")
    #interface.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
