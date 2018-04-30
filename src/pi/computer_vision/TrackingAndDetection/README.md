Computer Vision

William Luer - 4/30/2018

## Dependencies:
   - OpenCV 3.x
   - Numpy
   - Scikit-learn


## Description:
Tracking and testing platform developed to allow for automated comparison of tracking techniques.
Customizable tracking techniques via command line. Supports 5 different keypoint finding methods and three feature matching techniques. Supports reading videos from local files or from source (webcam). Ability to generate performance report for local files once true data has been gathered.

### Keypoint Finding methods
1. surf *
2. sift *
3. random
4. shi-tomasi
5. orb *
6. fast

 NOTE: * - incompatible with opticalflow feature matching


### Feature matching techniques
1. opticalflow
2. flann
3. bruteforce


### Usage:
python3 TrackingManager.py [-h] [-e] -s SOURCE -k KEYPOINT -m MATCHER

ex. To use shi-tomasi keypoint detection and optical feature matching on a local file called bottle.mp4: <br>
python3 TrackingManager.py -s bottle.mp4 -k shi-tomasi -m opticalflow

To generate a performace report, follow the following steps:
1. Record video using recordVideo.py <br>
&emsp;&ensp;- Edit file to include correct video path name<br>
2. Manually gather true data with clickTrueData.py<br>
&emsp;&ensp;- Edit file to include correct csv path name to store<br>
3. Run TrackingManager via command line with -e flag<br>
&emsp;&ensp;- Edit ReportGenerator to include correct pathways to csv files.<br>
&emsp;&ensp;- Delete the files test.csv and timingData.csv from the data folder before every run because data will be appended to file.

ex. To generate a performance report use the -e flag:<br>
python3 TrackingManager.py -e -s bottle.mp4 -k shi-tomasi -m opticalflow


## Results
Tracking visual will be displayed on pop-up window.
Performance report will be generated and stored in an appropriately named folder under the reports/ folder.
