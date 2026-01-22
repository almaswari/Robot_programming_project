Here is the updated **README.md**. It includes the new instructions for **Automatic PID Control**, **Real-time Plotting**, and the required Python dependencies.

Overwrite your existing file at `~/ws_drone/src/quadrotor_sim/README.md` with this content:

```markdown
# ROS 2 Jazzy Quadrotor Simulation 🚁

A complete, physics-based quadrotor simulation package built from scratch for **ROS 2 Jazzy Jalisco** and **Gazebo Harmonic**.

This project demonstrates aerodynamic physics, sensor integration (LiDAR & Odometry), and multiple control modes (Manual Teleop & Automatic PID Position Control) with real-time data visualization.

## ✨ Features

*   **Aerodynamic Physics:** Uses `MulticopterMotorModel` for 4 rotors to simulate lift and drag.
*   **Dual Control Modes:**
    *   **Manual:** Keyboard teleoperation.
    *   **Automatic:** PID Position Controller (Go to X, Y, Z coordinates).
*   **Live Data Plotting:** Real-time Matplotlib graphs comparing Target vs. Actual position and velocity.
*   **Sensors:** GPU LiDAR (LaserScan) and Odometry (Position/Velocity).
*   **Bridge:** Fully configured `ros_gz_bridge` for `cmd_vel`, `scan`, `odom`, `tf`, and `clock`.

## 🛠️ Prerequisites

*   **OS:** Ubuntu 24.04 (Noble Numbat)
*   **ROS 2:** Jazzy Jalisco
*   **Simulator:** Gazebo Harmonic

### Install Dependencies
Run this command to install ROS packages and Python plotting libraries:

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz \
                 ros-jazzy-xacro \
                 ros-jazzy-robot-state-publisher \
                 ros-jazzy-teleop-twist-keyboard \
                 python3-colcon-common-extensions \
                 python3-matplotlib
```

## 🚀 Installation & Build

1.  **Create Workspace** (if needed):
    ```bash
    mkdir -p ~/ws_drone/src
    cd ~/ws_drone/src
    ```

2.  **Clone/Copy Package** into the `src` folder.

3.  **Build**:
    ```bash
    cd ~/ws_drone
    source /opt/ros/jazzy/setup.bash
    colcon build --symlink-install
    ```

4.  **Source**:
    ```bash
    source install/setup.bash
    ```

## 🎮 How to Run

Running the full simulation requires **up to 4 terminals**.

### Terminal 1: Launch Simulation
Loads the drone, physics, bridge, and Gazebo.
```bash
source ~/ws_drone/install/setup.bash
ros2 launch quadrotor_sim gazebo_model.launch.py
```

### Terminal 2: Arm Motors ⚠️ (Mandatory)
The flight controller starts disabled. Run this **once** to enable motors:
```bash
gz topic -t "/quadrotor/enable" -m gz.msgs.Boolean -p "data: true"
```

---

### Terminal 3: Choose Your Pilot Mode

#### Option A: Manual Flight (Keyboard)
Use this to fly manually.
```bash
source /opt/ros/jazzy/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
*   **Controls:** `T` (Takeoff), `B` (Land), `I/J/K/L` (Move).

#### Option B: Automatic Flight (PID Controller)
Use this to enter coordinates (e.g., "Fly to 2, 2, 3").
```bash
source ~/ws_drone/install/setup.bash
ros2 run quadrotor_sim position_controller
```
*   **Usage:** The drone will hover at `0,0,1`. Type `x y z` (e.g., `2 0 2`) in the terminal to move.

---

### Terminal 4: Real-Time Plotter
Visualize Position (Target vs Actual) and Velocity graphs.
```bash
source ~/ws_drone/install/setup.bash
ros2 run quadrotor_sim data_plotter
```

## 📡 ROS 2 Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/cmd_vel` | `geometry_msgs/Twist` | Velocity commands sent to the controller. |
| `/odom` | `nav_msgs/Odometry` | Current position and velocity of the drone. |
| `/scan` | `sensor_msgs/LaserScan` | 2D LiDAR data. |
| `/quadrotor/target` | `geometry_msgs/Point` | The desired target position (published by PID controller). |

## 📂 Project Structure

```text
quadrotor_sim/
├── launch/
│   └── gazebo_model.launch.py      # Main launch file
├── model/
│   ├── robot.xacro                 # Visuals, Inertia, Collision geometry
│   └── robot.gazebo                # Physics, Motor Plugins, Sensors
├── parameters/
│   └── bridge_parameters.yaml      # ROS-Gazebo Topic mappings
├── quadrotor_sim/                  # Python Nodes
│   ├── position_controller.py      # PID Logic
│   └── data_plotter.py             # Matplotlib Visualization
├── package.xml
└── setup.py
```

## 🐛 Troubleshooting

**1. The drone spawns but won't move.**
*   Did you run **Terminal 2**? The motors need the enable signal.
*   If using PID, did you enter a target? It starts by hovering at (0,0,1).

**2. Plotter crashes with "Shape Mismatch"**
*   Ensure you are using the latest version of `data_plotter.py` which includes the data snapshot logic to prevent race conditions between ROS callbacks and the Plotter animation loop.

**3. Drone wobbles around target**
*   The PID gains in `position_controller.py` might be too aggressive. Reduce the **P** (Proportional) gain in the script: `self.pid_x = PID(0.8, ...)`

---
*Built with ROS 2 Jazzy and Gazebo Harmonic.*
```