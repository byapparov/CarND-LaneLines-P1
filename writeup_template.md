# **Finding Lane Lines on the Road** 


The goals / steps of this project are the following:

* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---


## 1. Pipeline to detect lanes

Image processing pipeline consists of the following steps:

* Read original image into Greyscale copy with one layer
* Apply Canny filter edge detection 
* Remove edges outside of the area where road is expected
* Lines are detected from the segments using Probabalistic Hough Transform
* Detected lines are added to the original image

We will focus on the processing part starting with the application Canny filter for edge detection. 

### Edge Detection 
Canny filter is an out of the box transformation of the image with just two parameters that can be tunned 
for a given problem. 

I have done tuning using list of lower and uper thersholds to pick best parameters. 

Thresholds | Lower 50 | Lower 100 | Lower 150
:-------|:--------------------------:|:--------------------------:|:--------------------------:
Upper 150 |![Canny 50 150](writeup_images/img_canny_tunning_50_150.jpg) | ![Canny 100 150](writeup_images/img_canny_tunning_100_150.jpg) | ![Canny 150 200](writeup_images/img_canny_tunning_150_150.jpg)
Upper 200 |![Canny 50 200](writeup_images/img_canny_tunning_50_200.jpg) | ![Canny 100 150](writeup_images/img_canny_tunning_100_200.jpg) | ![Canny 150 200](writeup_images/img_canny_tunning_150_200.jpg)
Upper 250 |![Canny 50 250](writeup_images/img_canny_tunning_50_250.jpg) | ![Canny 100 250](writeup_images/img_canny_tunning_100_250.jpg) | ![Canny 150 250](writeup_images/img_canny_tunning_150_250.jpg)


Canny edge detection algorithm is very robust with a picture taken in good light condition.
Thresholds don't impact the outcome for the next steps and we can confortably choose values applying subjective judgment.

This can become a problem with a wider range of images taken in different weather and light conditions, 
where we would potentially need to detect which conditions picture was taken in from and use parameters that are more appropriate.

During this excersise it was important for me to try to do tuning in a way that will allow me to repeate it later at scale
on other images. I have been trying different options of displaying multiple images with annotations in Jupiter Notebook. 
I came up with a way of combining image output with markdown which makes it very simple to build and customise. 


### Limiting the view

Camera mounted on the car has a wide angle and will capture objects outside of the road. 

Knowing where the road and lane segments are likely to be is very helpful to remove irrelevant edges which will
add noise at the line detection step. 

Base on the image and the geometry of image perspective I have chosen to reduce detection to a triangle area as shown 
on the first image:

Road View Filter | Original Image | Filtered View
:-------|:----:|:-------:
![Limiting the view demo](writeup_images/img_view_demo.jpg)|![Limiting the view demo](writeup_images/img_gradient.jpg)|![Limiting the view demo](writeup_images/img_limited_view.jpg)

I have written a function `limit_view()` that sets values outside of the view to 0. 

This function has several parameters, one of which allows to change the position of the top middle point in the view. 

In the future it would be useful to detect that point or even the whole road segment as it might change its position 
based on the road angle. 

Separation of the function is important for pipeline maintainability and future development. 
Right now it is possibly implemented in a suboptimal way which can be improved without any changes to the pipeline itself. 


### Line Detection

The last processing stage of the pipeline finds lines on the image using `HoughLinesP()` function from OpenCV library. 

This stage has required eventually the most amount of manual trial-and-error type of tuning due the number of parameters
that this algorithm has. 

I have used information about the lines from the example image to make sure that whole line if possible is detected,
as opposed to multiple segnments on a single line. 

This step will require further turning using multiple images potentially and tunning report similar to edge dection stage 
will be benefitial.



### 2. Pipeline shortcomings


The first shortcoming of the pipeline is that it is build based on the image that was taken in great weather conditions on 
a flat straight motorway with paint in good condition. Neither the car or other traffic are crossing the lanes. 

This means that pipeline was not really tested for wide range of real cases and was not written in a way that 
would allow to inspect or tag large amount of images. 

Going into more specific issues, the could be:

* Canny edge detection is applied to the whole image rather than to the filtered view. Potentially, bruring out image outside 
of the view area would reduce the noise for line detection stage.

* Line detection falls short for broken lines which can be potentially improved through heuristic approaches. 
  For example if we have high confidence from one solid line, we could use that information to improve our confidence about broken lines.

* View area is filtered out with `for` loop, which can be suboptimal in terms of speed. In general this pipeline was written without
 any non-functional requirements in mind and can fail from memory or CPU issues once code is ported to the real system. 
 
* Line detection has been only tested on the straight road, with sharp turn on the road it might not work, and this is something
that we probably will need to address by allowing for shorter line segments or through additional transformation of the image that 
would allow detect road lines still.


## 3. Suggest possible improvements to your pipeline

Depending on the primary use of the pipeline there are several directions for improvements that can be taken.

### Performance

Pipeline has not been tested for any non-functional requirements and that would be an obvious areay of 
improvement if code is to be ported to process video in real time for example.

### Research Scalability

Pipeline was written to process a single image, but to facilitate it would be great to be able to process 
hundreds of tagged images taken in different conditions and compare pipeline output to existing tags. 

### Edge Detection

Despite the fact that edge detection seems to be very stable on the test images, it would be benefitial to understand
how it changes in Fog, Rain and Night conditions. If there is an impact on the result, we would need to add a step
to detect these conditions and change algorithm parameters dynamically. 

### View Filter

Currentl implementation is based on a specific view of the camera and proportions of the road to above the road area. 
This can change and we would want to have a step in the pipeline that detects the area of the road first and view filter is 
adjusted dynamically. 

### Line Detection

Line detection can be improved in many ways, for example:
- We could apply knowledge about one line to fill the gaps if information is missing for another line as we know the are 
parallel and can be extrapolated based on the perspective geometry. 
- We could use information from previous images to extrapolate the gaps in the segments as the road view changes gradually.

