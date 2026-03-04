'''

def get_world_point(x_2d, y_2d, area): # point from yolo 2d
    frame height
    frame width

    get X_c,Y_c,Z_c  # 3d points in camera frame
    x,y,z =camera_to_world(X_c,Y_c,Z_c)

    return x,y,z  # 3d points in world frame

def publish_point(x,y,z):
    make arr of [x,y,z] and publish it to world_points topic

def get_id(x,y,z):
    get x,y,z then compaire it to awailable points clusters COM's and get the nearest one

    return [nearest_cluster_centroid_point , id]

def show_frame_with_id(nearest_cluster_centroid_point, id):
    # Implementation for displaying frame with ID
    pass
    
def publish_COM(nearest_cluster_centroid_point, id):
    make arr of [[x,y,z],id] and publish it to COM_with_Id topic
    
ROS2 listener for COM_with_Id topic gets array apend it and publishes on marker
ROS2 listener for world_points topic gets array apend it and publishes on marker


'''



import numpy as np
from rtree import index

class OnlineClusterer:
    def __init__(self, cluster_size):
        self.cluster_size = cluster_size
        self.points = []                     # all points (as tuples)
        self.clusters = []                    # list of {'leader': point, 'points': [indices]}
        # R‑tree for leaders (3D)
        prop = index.Property()
        prop.dimension = 3
        self.leader_idx = index.Index(properties=prop)
        # No need for separate IDs; we use cluster index as the R‑tree identifier

    def add_point(self, point):
        """
        Add a point, assign to a cluster, and return the centroid of its cluster.
        point: tuple (x, y, z) or list/array of length 3.
        """
        point = tuple(point)                  # ensure hashable
        point_index = len(self.points)
        self.points.append(point)

        # Find the nearest leader
        nearest = list(self.leader_idx.nearest(point, num_results=1))
        if nearest:
            cluster_idx = nearest[0]           # R‑tree ID = cluster index
            leader = self.clusters[cluster_idx]['leader']
            # Compute exact Euclidean distance
            dist = np.linalg.norm(np.array(point) - np.array(leader))
            if dist <= self.cluster_size:
                # Assign to existing cluster
                self.clusters[cluster_idx]['points'].append(point_index)
                return leader

        # No suitable cluster found – create a new one
        cluster_idx = len(self.clusters)
        self.clusters.append({'leader': point, 'points': [point_index]})
        # Insert leader into R‑tree (bounding box = point itself)
        self.leader_idx.insert(cluster_idx, point + point)  # (minx, miny, minz, maxx, maxy, maxz)
        return point