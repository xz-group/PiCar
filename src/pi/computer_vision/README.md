Computer Vision

William Luer - 4/30/2018

## Dependencies:
   - OpenCV 3.x
   - Numpy
   - Scikit-learn


## Description:
Computer vision techniques implemented for Raspberry Pi 3 and webcams

### File Structure:

|── Optical Flow/<br>
|&emsp;&emsp;&ensp;|── videos_papers_plots/<br>
|&emsp;&emsp;&ensp;|── demo_follow.py<br>
|&emsp;&emsp;&ensp;|── lk_ttc_constantFOE.py<br>
|&emsp;&emsp;&ensp;|── lk_ttc_constantFOEcloselooptest.py<br>
|&emsp;&emsp;&ensp;|── PID.py<br>
|<br>
|── TrackingAndDetection/<br>
|&emsp;&emsp;&ensp;|── model/<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;|── MobileNetSSD_deploy.caffemodel<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;|── MobileNetSSD_deploy.prototxt.txt<br>

|&emsp;&emsp;&ensp;|── src/<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;|── classification/<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── alternateSearchRescue.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── deep_learning_object_detection.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── searchRescue.py<br>

|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;|── trackingPlatform/<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── clickTrueData.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── featureMatchings.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── keypointFinders.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── MedianFlowTracker.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── recordVideo.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── ReportGenerator.py<br>
|&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;&emsp;&emsp;&ensp;|── TrackingManager.py<br>

## Results
Results of Optical Flow and obstacle avoidance can be seen here:
https://www.youtube.com/watch?v=2QJigzSVVe4&t=4s
https://www.youtube.com/watch?v=4JIqfRzICwc
