# Single Robot Perception Pipeline — ROS2

> **Object Detection · 3D Tracking · RViz Visualization**  
> Built on ROS2 Humble | YOLOv8 | Gazebo | tf2

## Demo

[![Watch the demo](https://img.shields.io/badge/▶%20Watch-Demo%20Video-blue?style=for-the-badge&logo=googledrive)](https://drive.google.com/file/d/1o-fTgSENNxsisA5spfHNmja8TW3CjbuB/view?usp=sharing)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Package Structure](#package-structure)
- [Workspace Tree](#workspace-tree)
- [System Architecture](#system-architecture)
- [Key Components](#key-components)
  - [Custom Messages](#1-custom-messages-single_robo_custom_interface)
  - [Camera Feed Node](#2-camera-feed-node-camera_feedpy)
  - [Transformer Node](#3-transformer-node-cameratoworldtransformer)
  - [Grid-Based Clustering](#4-grid-based-clustering-gridclustercom)
  - [RViz Visualizer](#5-rviz-visualizer-rviz_point_visualiserpy)
- [Data Flow](#data-flow)
- [Dependencies](#dependencies)
- [Build Instructions](#build-instructions)
- [Usage](#usage)
- [Configuration](#configuration)
- [Notes & Limitations](#notes--limitations)
- [Future Improvements](#future-improvements)

---

## Overview

A complete ROS2 perception pipeline for a mobile robot equipped with a camera, operating in a simulated warehouse environment (Gazebo). The system performs:

- Real-time object detection via **YOLOv8** (CPU, with frame skipping)
- **3D localization** from 2D bounding boxes using camera intrinsics and a depth-from-area heuristic
- **Persistent object tracking** using a custom grid-based clustering algorithm (`GridClusterCOM`) with stable IDs
- **Coordinate transformation** from camera frame → world frame using `tf2`
- **RViz visualization** of raw detections, cluster centroids, ID labels, and centroid trajectories

---

## Features

- ✅ YOLOv8 nano inference on CPU with configurable frame skipping
- ✅ Depth estimation from bounding box area — no depth camera required
- ✅ 3D grid-based clustering with persistent object IDs across frames
- ✅ `tf2`-based camera-to-world coordinate transformation
- ✅ RViz `MarkerArray` publishing (spheres, labels, trajectory line strips)
- ✅ Multi-threaded design — inference runs in a separate thread, ROS spinner never blocked
- ✅ Custom ROS2 message types for cluster data
- ✅ Fully configurable via ROS parameters

---

## Package Structure

| Package | Description |
|---|---|
| `single_robo_bringup` | Launch files and Nav2/AMCL configuration for robot bringup and navigation |
| `single_robo_custom_interface` | Custom message definitions (`ClusterPoints`, `ComWithID`) |
| `single_robo_discription` | Robot URDF/xacro, Gazebo worlds, sensor configs, and maps |
| `single_robo_odometry` | Odometry calculation, TF publishing, EKF integration, and error simulation |
| `single_robo_perception` | **Core pipeline** — YOLO detection, 3D estimation, clustering, RViz visualization |

---

## Workspace Tree

```
sakar_asignment/src/
├── single_robo_bringup/
│   ├── config/                  # Nav2 params: AMCL, costmap, BT trees, controller, planner
│   └── launch/                  # Bringup, navigation, spawn, and Kalman filter launch files
│
├── single_robo_custom_interface/
│   └── msg/
│       ├── ClusterPoints.msg    # Array of 3 floats (3D point)
│       └── ComWithID.msg        # 3D centroid + integer cluster ID
│
├── single_robo_discription/
│   ├── config/                  # EKF, Gazebo bridge, RViz, PS4 configs
│   ├── maps/                    # small_warehouse and small_warehouse2 map files
│   ├── urdf/                    # Robot xacro: base, camera, lidar, IMU
│   └── world/                   # ware_house_edit.sdf Gazebo world
│
├── single_robo_odometry/
│   └── single_robo_odometry/    # Odometry nodes, TF publishers, error simulation
│
├── single_robo_perception/
│   ├── dataset/                 # Training images + YOLO labels
│   ├── single_robo_perception/
│   │   ├── camera_feed.py       # Main perception node
│   │   └── rviz_point_visualiser.py
│   └── setup.py
│
└── yolov8n.pt                   # YOLOv8 nano weights
```

---

## System Architecture

```
Camera Stream (/camera/image_raw)
        │
        ▼
┌──────────────────────┐
│   CameraFeed Node    │  ← Frame queue + frame skipping
│   (camera_feed.py)   │
└──────────────────────┘
        │
        ▼ (inference thread)
┌──────────────────────┐
│    YOLOv8 Inference  │  ← Bounding boxes, class labels, confidence
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  Depth Estimation    │  ← depth = k / sqrt(bbox_area)
│  + Ray Direction     │  ← pixel → 3D ray using camera FOV
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  CameraToWorld       │  ← tf2: camera_link → map frame
│  Transformer         │
└──────────────────────┘
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
/world_points (raw)                        GridClusterCOM
                                           (3D clustering)
                                                  │
                                                  ▼
                                     /cluster_centroids (ID + position)
                                                  │
                                                  ▼
                                    ┌─────────────────────────┐
                                    │   RViz Visualizer        │
                                    │ /visualization_markers   │
                                    └─────────────────────────┘
```

---

## Key Components

### 1. Custom Messages (`single_robo_custom_interface`)

**`ClusterPoints.msg`** — a 3D point as an array of 3 floats.

**`ComWithID.msg`** — a centroid point array paired with an integer cluster ID. Used to publish tracked object positions with stable identifiers.

---

### 2. Camera Feed Node (`camera_feed.py`)

The core perception node. Responsibilities:

- Subscribes to `/camera/image_raw` and converts to OpenCV format
- Applies **frame skipping** (every Nth frame) to reduce CPU load
- Pushes frames into a queue consumed by the **inference thread**
- For each YOLO bounding box detection:
  - Computes centroid `(cx, cy)` and bounding box area
  - Estimates depth using `depth = k / sqrt(area)`
  - Computes 3D ray direction from pixel coordinates using camera FOV (90° H / 60° V)
  - Multiplies ray by depth → 3D point in camera frame
  - Calls `CameraToWorldTransformer` to get world coordinates
  - Publishes raw world point on `/world_points`
  - Passes world point to `GridClusterCOM` → receives (centroid, stable ID)
  - Publishes centroid + ID on `/cluster_centroids`
- Draws annotated bounding boxes, class labels, and cluster IDs on frame
- Displays both raw and annotated feeds in OpenCV windows

---

### 3. Transformer Node (`CameraToWorldTransformer`)

A dedicated ROS2 node that wraps `tf2` functionality:

- Looks up the transform from `camera_link` → `map` frame
- Exposes a `transform_point(x, y, z)` method returning the world-frame coordinates
- Runs inside the same `MultiThreadedExecutor` as the camera feed node — no separate launch needed

---

### 4. Grid-Based Clustering (`GridClusterCOM`)

A lightweight, deterministic online clustering algorithm operating in 3D space:

- Divides 3D space into a grid with `cell_size` derived from `com_radius`
- Each incoming point maps to a grid cell; if a cluster already exists in that cell, its centroid is updated via weighted average
- If the cell is empty, a new cluster is created with a unique, auto-incrementing ID
- Each cluster maintains a bounded deque of raw points (`reduction_threshold`) for optional trajectory rendering
- Same physical object retains the same ID as long as it stays within `com_radius` of its cluster centroid

---

### 5. RViz Visualizer (`rviz_point_visualiser.py`)

Subscribes to `/world_points` and `/cluster_centroids`, publishes `MarkerArray` on `/visualization_markers`:

| Marker | Description |
|---|---|
| Small yellow spheres | Raw world points from each detection |
| Large green spheres | Cluster centroids with persistent IDs |
| Text labels | Cluster ID displayed above each centroid sphere |
| Line strips | Centroid movement trajectory (optional) |

All visual properties (colors, sizes, frame, lifetime) are configurable via ROS parameters.

---

## Data Flow

```
1. /camera/image_raw
        ↓
2. Frame pushed to inference queue (with frame skipping)
        ↓
3. YOLO → bounding boxes
        ↓
4. For each box:
   a. Compute centre + area
   b. depth = k / sqrt(area)
   c. pixel → 3D ray (FOV-based)
   d. ray × depth → camera-frame 3D point
   e. tf2 transform → world-frame point
   f. Publish → /world_points
   g. GridClusterCOM → (centroid, ID)
   h. Publish → /cluster_centroids
        ↓
5. RViz Visualizer → /visualization_markers
6. Annotated image displayed in OpenCV window
```

---

## Dependencies

**ROS2 packages:**
- `cv_bridge`, `image_transport`
- `tf2_ros`, `tf2_geometry_msgs`
- `visualization_msgs`
- `rclpy`

**Python packages:**
```bash
pip install ultralytics opencv-python numpy
```

**System:**
- ROS2 Humble (or newer)
- Gazebo (for simulation)
- RViz2

---

## Build Instructions

**1. Clone into your ROS2 workspace:**
```bash
cd ~/ros2_ws/src
git clone <repository_url>
```

**2. Install ROS dependencies:**
```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

**3. Install Python dependencies:**
```bash
pip install ultralytics opencv-python
```

**4. Build:**
```bash
colcon build --packages-up-to single_robo_perception
source install/setup.bash
```

---

## Usage

### Step 1 — Launch the simulation (Gazebo + robot)

```bash
ros2 launch single_robo_bringup single_robo_spawn.launch.py
```

This starts the robot model, sensors, and begins publishing `/camera/image_raw`.

### Step 2 — Run the perception pipeline

```bash
ros2 run single_robo_perception camera_feed.py
```

Two OpenCV windows will open: `"Raw Feed"` and `"YOLO Feed"` (annotated with detections and cluster IDs).

### Step 3 — Run the RViz visualizer

```bash
ros2 run single_robo_perception rviz_point_visualiser.py
```

Then open RViz2 and add a **MarkerArray** display subscribed to `/visualization_markers`.  
Alternatively, load the provided RViz config:

```bash
rviz2 -d src/single_robo_discription/config/rviz_config.rviz
```

> The `CameraToWorldTransformer` node is instantiated internally within `camera_feed.py` via a `MultiThreadedExecutor` — no additional terminal is needed.

---

## Configuration

### Camera Feed (`camera_feed.py`)

| Parameter | Default | Description |
|---|---|---|
| `imgsz` | `320` | YOLO inference resolution |
| `frame_skip` | `2` | Process every Nth frame |
| `com_radius` | `1.0` m | Clustering proximity threshold |
| `reduction_threshold` | `10` | Max raw points stored per cluster |
| Camera FOV | `90° H / 60° V` | Hardcoded — adjust to match your camera |

### RViz Visualizer (ROS parameters)

| Parameter | Default | Description |
|---|---|---|
| `world_frame` | `map` | TF reference frame for all markers |
| `marker_lifetime` | — | Seconds before markers auto-expire |
| `point_color_r/g/b/a` | Yellow | Color for raw world point spheres |
| `centroid_color_r/g/b/a` | Green | Color for centroid spheres |
| `point_size` | — | Radius of raw point markers |
| `centroid_size` | — | Radius of centroid markers |
| `text_size` | — | Size of ID label text |

Parameters can be set via command line or a YAML file passed at launch.

---

## Notes & Limitations

- **Depth calibration** — `calibration_area_for_1m` is a placeholder constant. For accurate depth, measure the bounding box pixel area of a reference object at exactly 1 m from your camera and set this value accordingly.
- **Single object class assumption** — the same depth scale is applied to all detected classes. Objects of different physical sizes will have incorrect absolute depth, though relative ordering remains meaningful.
- **No motion model** — `GridClusterCOM` uses only spatial proximity, not velocity prediction. Fast-moving objects may lose their ID or create duplicate clusters. Increase `com_radius` if this occurs.
- **CPU inference** — the pipeline is designed for CPU. To use a GPU, remove `device='cpu'` from the YOLO initialization call.
- **Log verbosity** — all nodes log at `INFO` level by default. Change severity in node constructors to reduce output.

---

## Future Improvements

- Integrate a depth camera (e.g., Intel RealSense) for metric-accurate range measurements
- Replace area-based depth heuristic with a monocular depth estimation network (e.g., MiDaS, Depth Anything)
- Add a proper multi-object tracker (SORT or DeepSORT) for robust ID association under occlusion and crossing
- Externalize all hardcoded values (FOV, calibration constant) into a YAML parameter file
- Package perception nodes as **composable nodes** for lower inter-node communication overhead
- Add structured output (JSON/CSV per frame) for offline analysis and benchmarking
