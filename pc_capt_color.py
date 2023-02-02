import pyrealsense2 as rs
import numpy as np
import argparse
from open3d import *
from pc_disp_color import visualize_pcd

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')
    parser.add_argument('--filter', action='store_true', help="Apply post processing filters")

    return parser.parse_args()

class Filters:
    ### Change each filter option for your own use
    def __init__(self):
        #Decimation
        self.decimation = rs.decimation_filter()
        self.decimation.set_option(rs.option.filter_magnitude, 1)

        #Spatial
        self.spatial = rs.spatial_filter()
        self.spatial.set_option(rs.option.filter_magnitude, 5)
        self.spatial.set_option(rs.option.filter_smooth_alpha, 0.3)
        self.spatial.set_option(rs.option.filter_smooth_delta, 50)
        self.spatial.set_option(rs.option.holes_fill, 4)

        #Temporal
        self.temporal = rs.temporal_filter()
        self.temporal.set_option(rs.option.filter_smooth_alpha, 0.1)
        self.temporal.set_option(rs.option.filter_smooth_delta, 100)
        
        #Hole Filling
        self.hole_filling = rs.hole_filling_filter()

        #Threshold
        self.threshold = rs.threshold_filter()
        self.threshold.set_option(rs.option.min_distance, 0)
        self.threshold.set_option(rs.option.max_distance, 16)

        #Depth to disparity
        self.depth_to_disparity = rs.disparity_transform(True)
        self.disparity_to_depth = rs.disparity_transform(False)    

if __name__=="__main__":
    args = parse_arguments()
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

    profile = pipeline.start(config)
    device = profile.get_device()

    # 0: Custom　　1: Default　　2: Hand　　3: High Accuracy　　4: High Density
    depth_sensor = device.first_depth_sensor()
    depth_sensor.set_option(rs.option.visual_preset, 4)
    
    ### The current value of each option and the possible ranges can be obtained and changed:
    # laser_pwr = depth_sensor.get_option(rs.option.laser_power)
    # laser_range = depth_sensor.get_option_range(rs.option.laser_power)
    depth_sensor.set_option(rs.option.laser_power, 360)

    ### Advanced mode can be turned on for more detailed parameter settings
    # advnc_mode = rs.rs400_advanced_mode(profile.get_device())
    # advnc_mode.toggle_advanced_mode(True)
    
    #Define filters
    fl = Filters()

    align = rs.align(rs.stream.color)    

    #Get camera intrinsics
    intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
    pinhole_camera_intrinsic = camera.PinholeCameraIntrinsic(intr.width, intr.height, intr.fx, intr.fy, intr.ppx, intr.ppy)

    #将来的にはExposureの値を取得して、変化しなくなったら次に進む処理にしたい
    print("Waiting for Auto-Exposure")
    for _ in range(25):
        pipeline.wait_for_frames()

    print("Capturing frames")
    frames = []
    while True:
            frameset = pipeline.wait_for_frames()
            if not frameset: continue

            frames.append(frameset)
            if len(frames) > 9:
                break

    pipeline.stop()

    if args.filter:
        #Post-processing filters are applied if the option is used
        print("Applying filters")
        for x in range(len(frames)):
            frame = frames[x]
            frame = fl.decimation.process(frame)
            frame = fl.depth_to_disparity.process(frame)
            frame = fl.threshold.process(frame)
            frame = fl.spatial.process(frame)
            frame = fl.temporal.process(frame)
            frame = fl.disparity_to_depth.process(frame)
            frame = fl.hole_filling.process(frame)
            frame = frame.as_frameset()

        aligned_frame = align.process(frame)
        depth = geometry.Image(np.asanyarray(aligned_frame.get_depth_frame().get_data()))
        color = geometry.Image(np.asanyarray(aligned_frame.get_color_frame().get_data()))
    else:
        aligned_frame = align.process(frames[0])
        depth = geometry.Image(np.asanyarray(aligned_frame.get_depth_frame().get_data()))
        color = geometry.Image(np.asanyarray(aligned_frame.get_color_frame().get_data()))

    rgbd = geometry.RGBDImage.create_from_color_and_depth(color, depth, convert_rgb_to_intensity = False)
    pcd = geometry.PointCloud.create_from_rgbd_image(rgbd, pinhole_camera_intrinsic)
    print("Done")

    io.write_point_cloud('./staircase_data/' + args.filename, pcd, write_ascii=True)
    visualize_pcd('./staircase_data/' + args.filename)
    