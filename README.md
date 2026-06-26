# Fitness-App-One-Device
A fitness app, fully developed in python, to guide user on doing fitness with the use of it. 

## What is it, and why?
This is a fitness app, with the purpose of reducing reliant on external devices (e.g. controllers, body-tracking devices). This is achieved with using Pose Estimation, using pre-trained model to predict human pose through in-built webcams.
All you need for this app is a single computer with webcam, which is simple and low cost.

## How does it work?
After authentication page, you can look through different courses and pick them. To participate a course, permission to webcam is **required**. Then you will get scored from your performance during the course. 

By accessing the /codes/Sprite/worksetMoveContent.json, you will be able to easily modify different workout courses by adding movesets or adding your custom courses. 

## Why is the app not working when you download it?
There are dependent libraries such as OpenCV and firebase admin. Another reason is I have intentionally not uploaded the privateKey.json file for database access (I do not want the key to be public). I have also not uploaded the pre-trained model file, which you can find [here](https://github.com/foss-for-synopsys-dwc-arc-processors/synopsys-caffe-models/raw/master/caffe_models/openpose/caffe_model/pose_iter_440000.caffemodel).

## Gallery (App Snapshot)
This will be included in added in the future.
