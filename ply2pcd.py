import open3d as o3d
import os
import glob
import sys

path = './staircase_data/' + sys.argv[1] + '/'
for ply in [os.path.basename(p) for p in glob.glob(path + "*.ply", recursive=True) if os.path.isfile(p)]:
    pcd = o3d.io.read_point_cloud(path + ply)
    pcd.transform([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]])
    o3d.io.write_point_cloud(f"{path}/{ply[:-4]}.pcd", pcd, write_ascii=True)