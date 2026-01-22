import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point 
from nav_msgs.msg import Odometry
import math
import threading

class PID:
    def __init__(self, kp, ki, kd, max_val):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_val = max_val
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        # Clamp integral to prevent windup
        self.integral = max(min(self.integral, 1.0), -1.0)
        
        d_term = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * d_term)
        return max(min(output, self.max_val), -self.max_val)

def quaternion_to_yaw(q):
    # Convert quaternion (x,y,z,w) to Euler Yaw angle
    t3 = +2.0 * (q.w * q.z + q.x * q.y)
    t4 = +1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(t3, t4)

class QuadrotorPIDController(Node):
    def __init__(self):
        super().__init__('position_controller')
        # ... existing publishers ...
        self.target_pub = self.create_publisher(Point, '/quadrotor/target', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        
        # Initial Target: Hover at 1 meter
        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = 1.0 
        
        # Tuning: P, I, D, MaxVel
        self.pid_x = PID(1.0, 0.0, 0.5, 2.0)
        self.pid_y = PID(1.0, 0.0, 0.5, 2.0)
        self.pid_z = PID(3.0, 0.5, 1.0, 2.0) # Stronger Z to fight gravity

        self.last_time = self.get_clock().now()
        self.get_logger().info("Automatic Controller Active. Type coordinates to fly!")

    def odom_callback(self, msg):
        # 1. Get current state
        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y
        curr_z = msg.pose.pose.position.z
        
        # Get Yaw (Rotation)
        orientation = msg.pose.pose.orientation
        current_yaw = quaternion_to_yaw(orientation)

        # 2. Time Delta
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        if dt == 0: return
        self.last_time = now

        # 3. Calculate World Frame Velocities needed
        vx_world = self.pid_x.compute(self.target_x, curr_x, dt)
        vy_world = self.pid_y.compute(self.target_y, curr_y, dt)
        vz_world = self.pid_z.compute(self.target_z, curr_z, dt)

        # 4. Rotate World Velocity to Body Velocity
        # (This is crucial: "Forward" changes based on where drone points)
        vx_body = vx_world * math.cos(current_yaw) + vy_world * math.sin(current_yaw)
        vy_body = -vx_world * math.sin(current_yaw) + vy_world * math.cos(current_yaw)

        # 5. Publish
        twist = Twist()
        twist.linear.x = vx_body
        twist.linear.y = vy_body
        twist.linear.z = vz_world
        self.cmd_vel_pub.publish(twist)

       

        # NEW: Publish the Target Position for the Plotter
        target_msg = Point()
        target_msg.x = self.target_x
        target_msg.y = self.target_y
        target_msg.z = self.target_z
        self.target_pub.publish(target_msg)

    def set_target(self, x, y, z):
        self.target_x = float(x)
        self.target_y = float(y)
        self.target_z = float(z)
        print(f">>> Flying to: {x}, {y}, {z}")

def input_loop(controller):
    while True:
        try:
            line = input("Enter X Y Z: ")
            parts = line.split()
            if len(parts) == 3:
                controller.set_target(parts[0], parts[1], parts[2])
            else:
                print("Invalid format. Try: 1 1 2")
        except:
            pass

def main(args=None):
    rclpy.init(args=args)
    controller = QuadrotorPIDController()
    
    # Run input in separate thread
    t = threading.Thread(target=input_loop, args=(controller,), daemon=True)
    t.start()

    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()