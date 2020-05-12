# **Finding Lane Lines on the Road** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

<img src="examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

Overview
---

When we drive, we use our eyes to decide where to go.  The lines on the road that show us where the lanes are act as our constant reference for where to steer the vehicle.  
Naturally, one of the first things we would like to do in developing a self-driving car is to automatically detect lane lines using an algorithm.

This repository contains solution for the *Project 1: Finding Lane Lines*.

Repository contains the following code:

* `src` directory contains library code with the image processing pipeline
* `identify_lanes_images.ipynb` - Jupiter Notebook file with the research for lane detection.
* `identify_lanes_videos.ipynb` - Jupiter Notebook that contains demonstration of the pipeline on test videos.
* `writepup.md` - Contains report about the pipeline and reflection on the areas for pipeline improvement.
 
Lane lines in images are identified using Python and OpenCV.  

OpenCV means "Open-Source Computer Vision", which is a package that has many useful tools for analyzing images.  


Testing
---

To test the pipeline run unittest command in shell from the root of the project:

```shell script
python -m unittest discover src
```

Image Pipeline
___

See writeup.md file for details on image processing steps.
