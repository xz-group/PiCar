Executable files:
	1. LKopticalFlow.py - first opt flow, does not clear, crashes if points go off screen
	2. lk_track.py - opt flow on certain points, keeps track of how many are being tracked
	3. opt_flow.py - Produces vector field that overlays video

Source Files:
	1. common.py
	2. video.py
	3. tst_scene_render.py

Code refactored from https://github.com/opencv/opencv to work with Raspberry Pi camera.

Optical flow tracking - First_screenshot_avi
time to contact - ttc_screenshot_avi
clustering - clustering_screenshot.avi
clustering with most significant cluster shown sig_cluster.avi

