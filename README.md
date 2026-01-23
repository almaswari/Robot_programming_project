
# 🚁 Autonomous Quadrotor Simulation in ROS 2 Jazzy

![ROS 2 Jazzy](https://img.shields.io/badge/ROS_2-Jazzy-blue?logo=ros&logoColor=white)
![Gazebo Harmonic](https://img.shields.io/badge/Gazebo-Harmonic-orange?logo=gazebo&logoColor=white)
![Status](https://img.shields.io/badge/Status-Docker_Verified-success)



| Course | Robot Programming (Fall 2025) |
| :--- | :--- |
| **Author** | [Mohammed Almaswary (517097) ,Zyad Al-Shuja (478896)] |
| **Deadline** | January 23, 2026 |
| **Status** | Final Submission  |
| **Simulator** | Gazebo Harmonic |
| **Middleware** | ROS 2 Jazzy Jalisco |

---

## 🎯 1. Project Objective & Problem Statement
The goal of this project is to design and implement a fully autonomous 3D Quadrotor simulation. Moving beyond 2D ground vehicles, this simulation addresses the complexities of **non-linear flight dynamics**, **gravity compensation**, and **6-DOF stabilization**.

Key challenges solved in this implementation:
1.  **Dynamic Modeling:** Creating a URDF/Xacro model compatible with Gazebo's aerodynamic `MulticopterMotorModel`.
2.  **Autonomous Navigation:** Development of a custom **Closed-Loop PID Controller** for precise $(x, y, z)$ position hold.
3.  **Frame Transformation:** Implementing rotation matrices to translate World-frame position errors into Body-frame velocity commands using real-time Yaw feedback.

---

## 🏗️ 2. Modular Architecture (Logical Code Separation)
In accordance with the course requirements for modularity and maintainability, the repository follows a strictly decoupled structure. Each module represents a distinct logical component of the robotics stack.

```text
Robot_programming_project/
├── 📂 src/                    # PROJECT CORE SOURCE (quadrotor_sim package)
│   ├── 📂 controllers/        # MODULE 1: PID Autonomous Navigation Logic
│   │   └── position_controller.py
│   ├── 📂 models/             # MODULE 2: Xacro Geometry & Physics Plugins
│   │   ├── robot.xacro        # 3D Visuals, Inertia, and Macros
│   │   └── robot.gazebo       # Aerodynamic and Sensor Plugins
│   ├── 📂 plotters/           # MODULE 3: Real-time Telemetry Visualization
│   │   └── data_plotter.py
│   ├── 📂 launch/             # System Ignition/Launch Scripts
│   ├── 📂 parameters/         # Communication Bridge Configurations
│   ├── 📄 package.xml         # ROS 2 Metadata & Dependencies
│   └── 📄 setup.py            # Package Build & Install Configuration
├── 📂 tests/                  # Automated quality and syntax tests
├── 📄 Dockerfile              # Containerization for Reproducible Deployment
├── 📄 requirements.txt        # Python dependencies (matplotlib, etc.)
├── 📄 .gitignore              # Cleanliness: Excludes build/install artifacts
└── 📄 README.md               # Root Documentation
```

---

## ✨ 3. Technical Implementation Details

### 🤖 Hybrid Control System
*   **Manual Mode:** Direct velocity control via the `teleop_twist_keyboard` interface for flight testing.
*   **Autonomous Mode:** A high-frequency Python node that calculates $(x, y, z)$ errors and outputs velocity commands via a tuned PID algorithm featuring **Integral Clamping** to prevent windup.

### 📐 World-to-Body Transformation
A critical feature of the navigation system is the handling of the drone's orientation. Because velocity commands are relative to the drone's heading, the controller uses the current **Yaw angle** (extracted from Odometry) to rotate the error vectors from the World Frame to the Body Frame, preventing instability during rotation.

### 📊 Real-Time Visualization
The `data_plotter` module provides live feedback of the drone's telemetry. To ensure the high-frequency ROS 2 communication is not interrupted by the GUI rendering, the plotter utilizes **background threading** and **synchronized data snapshots** to maintain thread safety.

---

## 🚀 4. Launch and Operation Guide

### 🔨 Building the Workspace
Ensure you have installed the requirements (`python3-matplotlib`, `ros-jazzy-ros-gz`).
```bash
cd ~/ws_drone
colcon build --symlink-install
source install/setup.bash
```

### 🎮 Running the simulation (4 Terminals)

**Terminal 1: Start Simulation Environment**
```bash
cd ~/ws_drone
source install/setup.bash
ros2 launch quadrotor_sim gazebo_model.launch.py
```

**Terminal 2: Arm the Motors (Enable Physics)**
```bash

gz topic -t "/quadrotor/enable" -m gz.msgs.Boolean -p "data: true"
```

**Terminal 3: Pilot Control (Select One)**
*   **Manual Teleop:**
```bash

ros2 run teleop_twist_keyboard teleop_twist_keyboard
``` 
*   **PID Position Control:** ``
```bash

ros2 run quadrotor_sim position_controller
``` 

**Terminal 4: Real-Time Telemetry Plotter**
```bash
source install/setup.bash
ros2 run quadrotor_sim data_plotter
```

---

## 🐳 5. Portability (Docker Deployment)
The project is fully Dockerized. The image has been tested and verified to build the modular structure successfully.

**Run the simulation via Docker with GUI support:**
```bash
# Enable X11 forwarding
xhost +local:root

# Run the pre-configured container
docker run -it --rm --net=host --ipc=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix quadrotor_sim
```

---




