


#  Autonomous 3D Quadrotor Simulation in ROS 2 Jazzy
![ROS 2 Jazzy](https://img.shields.io/badge/ROS_2-Jazzy-blue?logo=ros&logoColor=white)
![Gazebo Harmonic](https://img.shields.io/badge/Gazebo-Harmonic-orange?logo=gazebo&logoColor=white)
![Status](https://img.shields.io/badge/Status-Docker_Verified-success)

| Course | Robot Programming (Fall 2025) |
| :--- | :--- |
| **Author** | Mohammed Almaswary (517097) ,Zyad Al-Shuja (478896)
 **Supervisor** |Dr. Kirilll Artemov
| **Deadline** | January 23, 2026 |
| **Status** | Final Submission |
| **Simulator** | Gazebo Harmonic |
| **Middleware** | ROS 2 Jazzy Jalisco |

---

##  1. Project Overview
This project is a high-fidelity 3D simulation of a Quadrotor UAV. Unlike standard mobile robots, this project handles **aerodynamic physics**, **gravity compensation**, and **6-DOF navigation**.

**Key Features:**
*   **Physics-Based:** Simulates motor thrust and drag using \`MulticopterMotorModel\`.
*   **Hybrid Control:** Supports both **Manual Pilot** mode and **Autonomous PID** mode.
*   **Real-Time Telemetry:** Live data visualization of flight performance.
*   **Dockerized:** 100% portable development environment.

---

##  2. Modular Architecture
To satisfy the course requirement for **Logical Code Separation**, the source code is organized into distinct modules:

```text
Robot_programming_project/
├── 📄 Dockerfile              # Containerization (Requirement)
├── 📄 requirements.txt        # Python Dependencies
├── 📄 .gitignore              # Cleanliness
├── 📄 README.md               # Documentation
├── 📂 src/                    # SOURCE CODE
│   ├── 📂 controllers/        # MODULE 1: PID Navigation Logic
│   ├── 📂 models/             # MODULE 2: Xacro & Physics Plugins
│   ├── 📂 plotters/           # MODULE 3: Matplotlib Visualization
│   ├── 📂 launch/             # System Launch Files
│   ├── 📂 parameters/         # Bridge Configuration
│   ├── 📄 package.xml         # Dependencies
│   └── 📄 setup.py            # Build Config
```

---

##  3. Installation & Build

### Prerequisites
```bash
sudo apt update
sudo apt install python3-matplotlib ros-jazzy-ros-gz ros-jazzy-teleop-twist-keyboard
```

### Build Workspace
```bash
cd ~/ws_drone
colcon build --symlink-install
source install/setup.bash
```

---

##  4. How to Run (4-Terminal Setup)

### Terminal 1: Launch Simulation
Starts Gazebo, spawns the drone, and loads the ROS bridge.
```bash
source install/setup.bash
ros2 launch quadrotor_sim gazebo_model.launch.py
```

### Terminal 2: Arm Motors ( Critical Step)
The drone starts in "Safety Mode". You must enable the motors to fly.
```bash
gz topic -t "/quadrotor/enable" -m gz.msgs.Boolean -p "data: true"
```

### Terminal 3: Choose Your Control Mode

#### **Option A: Manual Pilot (Keyboard)** 
Fly the drone manually using velocity commands.
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

** Flight Key Map:**
| Key | Action | Physics Note |
| :--- | :--- | :--- |
| **`T`** (Shift+t) | **Takeoff / Up** | Increases Thrust (+Z). Press this first! |
| **`B`** | **Land / Down** | Decreases Thrust (-Z). |
| **`I`** | Forward | Pitch Down. |
| **`,`** | Backward | Pitch Up. |
| **`J`** | Left | Roll Left. |
| **`L`** | Right | Roll Right. |
| **`K`** | **Hover / Stop** | Resets horizontal velocity to 0. |

> **Note:** Gravity is always pulling down. You must maintain upward throttle (`T`) to stay in the air.

#### **Option B: Autonomous Pilot (PID)** 
The drone will automatically takeoff and hover at 1.0m.
```bash
source install/setup.bash
ros2 run quadrotor_sim position_controller
```
*   **Usage:** Type coordinates in the terminal (e.g., `2 0 2`) and press **Enter**. The drone will navigate to that location using closed-loop control.

### Terminal 4: Telemetry Plotter
Visualize the Target vs. Actual position in real-time.
```bash
source install/setup.bash
ros2 run quadrotor_sim data_plotter
```

---

##  5. Docker Portability
To ensure this project runs on any machine , a `Dockerfile` is included.

**Build & Run:**
```bash
# Build Image
docker build -t quadrotor_sim .

# Run Container (GUI Enabled)
xhost +local:root
docker run -it --rm --net=host --ipc=host -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix quadrotor_sim
```

---

##  6. Technical Implementation
*   **Coordinate Rotation:** The PID controller rotates World-frame error vectors into Body-frame velocity commands using the current Yaw angle. This prevents spiral instability during rotation.
*   **Thread Safety:** The `data_plotter` uses background threading and snapshotting to prevent race conditions between the ROS callback and the Matplotlib animation loop.

*Built for the Fall 2025 Robot Programming Course.*
EOF
