# Use the official ROS 2 Jazzy image
FROM osrf/ros:jazzy-desktop

# Set environment variables
ENV ROS_DISTRO=jazzy
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    ros-jazzy-ros-gz \
    ros-jazzy-xacro \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-teleop-twist-keyboard \
    python3-colcon-common-extensions \
    python3-matplotlib \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup Workspace
WORKDIR /ws_drone

# 3. Copy Source Code
# (This assumes your Dockerfile is next to the 'src' folder)
COPY src/ /ws_drone/src/

# 4. Build the Project
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --symlink-install

# 5. Setup Entrypoint
# Automatically source the workspace when the container starts
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source /ws_drone/install/setup.bash" >> ~/.bashrc

# Default command
CMD ["bash"]