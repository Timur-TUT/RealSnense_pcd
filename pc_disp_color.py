from open3d import io, visualization
import sys

def visualize_pcd(path):
    pcd = io.read_point_cloud(path)
    pcd.transform([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]])
    visualization.draw_geometries([pcd], left=0, top=35, window_name=path)

if __name__ == "__main__":
    visualize_pcd('./staircase_data/' + sys.argv[1])
    