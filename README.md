# RealSnense PCD
**Generate .pcd file via Python program using RealSense RGB-D camera.**

**RealSenseのRGB-Dカメラを使用して，「.pcd」形式で点群データを保存・表示が可能**

* The "staircase_data" point cloud takes up a huge amount of space (7.6 GB), so it is recommended to partially pull the data.

## Contents

### [staircase_data:](https://github.com/Timur-TUT/RealSnense_pcd/tree/master/staircase_data)

Point cloud data obtained indoors and outdoors

### [pc_capt_color.py:](https://github.com/Timur-TUT/RealSnense_pcd/blob/master/pc_capt_color.py)

Program to save point clouds in ".pcd" format with RealSense RGB-D camera connected

```python pc_capt_color.py *path_to_folder_in_staircase_data*/*file_name*.pcd```

To apply RealSense post-processing filters, run with the "--filter" option

### [pc_disp_color.py:](https://github.com/Timur-TUT/RealSnense_pcd/blob/master/pc_disp_color.py)

Program to display point clouds in ".pcd" format

```python pc_disp_color.py *path_to_folder_in_staircase_data*/*file_name*.pcd```

### [ply2pcd.py](https://github.com/Timur-TUT/RealSnense_pcd/blob/master/ply2pcd.py)

Program to convert all point clouds in ".ply" format in the folder to ".pcd" format

```python ply2pcd.py *path_to_folder_in_staircase_data*```

### [階段認識実験.xlsx](https://github.com/Timur-TUT/RealSnense_pcd/blob/master/%E9%9A%8E%E6%AE%B5%E8%AA%8D%E8%AD%98%E5%AE%9F%E9%A8%93.xlsx)

Results of staircase recognition based on the "staircase_data" from the reference paper[^1].

[^1]: Alejandro Perez-Yus, Daniel Guti´errez-G´omez, Gonzalo Lopez-Nicolas, and JJ Guerrero. Stairsdetection with odometry-aided traversal from awearable rgb-d camera. Computer Vision and Image Understanding, Vol. 154, pp. 192–205, 2017.
