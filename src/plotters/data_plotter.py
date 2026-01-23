import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading

class DataPlotter(Node):
    def __init__(self):
        super().__init__('data_plotter')
        
        # Subscribe to Data
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.create_subscription(Point, '/quadrotor/target', self.target_callback, 10)

        # Buffers for plotting (Store last 200 points)
        self.max_len = 200
        self.time_steps = deque(maxlen=self.max_len)
        
        # Position Data
        self.pos_x = deque(maxlen=self.max_len)
        self.pos_y = deque(maxlen=self.max_len)
        self.pos_z = deque(maxlen=self.max_len)
        
        # Target Data
        self.tar_x = deque(maxlen=self.max_len)
        self.tar_y = deque(maxlen=self.max_len)
        self.tar_z = deque(maxlen=self.max_len)

        # Velocity Data
        self.vel_x = deque(maxlen=self.max_len)
        self.vel_y = deque(maxlen=self.max_len)
        self.vel_z = deque(maxlen=self.max_len)

        self.current_target = [0.0, 0.0, 1.0] # Default target
        self.start_time = self.get_clock().now().nanoseconds / 1e9

    def target_callback(self, msg):
        self.current_target = [msg.x, msg.y, msg.z]

    def odom_callback(self, msg):
        # Time
        now = self.get_clock().now().nanoseconds / 1e9
        t = now - self.start_time
        
        # Position
        px = msg.pose.pose.position.x
        py = msg.pose.pose.position.y
        pz = msg.pose.pose.position.z
        
        # Velocity (Linear)
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        vz = msg.twist.twist.linear.z

        # Append to buffers
        self.time_steps.append(t)
        
        self.pos_x.append(px); self.pos_y.append(py); self.pos_z.append(pz)
        self.tar_x.append(self.current_target[0]); self.tar_y.append(self.current_target[1]); self.tar_z.append(self.current_target[2])
        self.vel_x.append(vx); self.vel_y.append(vy); self.vel_z.append(vz)

# GLOBAL PLOTTING SETUP
node = None
fig, (ax_pos, ax_vel) = plt.subplots(2, 1, figsize=(10, 8))

def animate(i):
    if node is None or len(node.time_steps) < 2: return

    # --- SAFETY SYNC: PREVENT CRASHES ---
    # 1. Copy deques to lists immediately (Snapshot)
    t = list(node.time_steps)
    
    px = list(node.pos_x); py = list(node.pos_y); pz = list(node.pos_z)
    tx = list(node.tar_x); ty = list(node.tar_y); tz = list(node.tar_z)
    vx = list(node.vel_x); vy = list(node.vel_y); vz = list(node.vel_z)

    # 2. Find minimum length (In case ROS updated one list while we were copying another)
    min_len = min(len(t), 
                  len(px), len(py), len(pz),
                  len(tx), len(ty), len(tz),
                  len(vx), len(vy), len(vz))

    # 3. Trim all lists to ensure they are EXACTLY the same size
    t = t[:min_len]
    px = px[:min_len]; py = py[:min_len]; pz = pz[:min_len]
    tx = tx[:min_len]; ty = ty[:min_len]; tz = tz[:min_len]
    vx = vx[:min_len]; vy = vy[:min_len]; vz = vz[:min_len]
    # ------------------------------------

    # Clear axes
    ax_pos.clear()
    ax_vel.clear()

    # --- PLOT 1: POSITIONS ---
    ax_pos.plot(t, px, 'r-', label='X Current')
    ax_pos.plot(t, tx, 'r--', label='X Target', alpha=0.5)
    
    ax_pos.plot(t, py, 'g-', label='Y Current')
    ax_pos.plot(t, ty, 'g--', label='Y Target', alpha=0.5)
    
    ax_pos.plot(t, pz, 'b-', label='Z Current')
    ax_pos.plot(t, tz, 'b--', label='Z Target', alpha=0.5)
    
    ax_pos.legend(loc='upper left', ncol=3, fontsize='small')
    ax_pos.set_title(f"Position vs Target (Current Height: {pz[-1]:.2f}m)")
    ax_pos.grid(True)
    ax_pos.set_ylabel("Position (m)")

    # --- PLOT 2: VELOCITIES ---
    ax_vel.plot(t, vx, 'r-', label='Vx')
    ax_vel.plot(t, vy, 'g-', label='Vy')
    ax_vel.plot(t, vz, 'b-', label='Vz')
    
    ax_vel.legend(loc='upper left')
    ax_vel.set_title("Linear Velocities")
    ax_vel.grid(True)
    ax_vel.set_ylabel("Velocity (m/s)")
    ax_vel.set_xlabel("Time (s)")

def main(args=None):
    global node
    rclpy.init(args=args)
    node = DataPlotter()

    # Run ROS in a separate thread so Plotting doesn't block it
    thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    thread.start()

    # Show Plot
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.tight_layout()
    plt.show()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()