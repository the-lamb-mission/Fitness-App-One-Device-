# Fitness-App-One-Device
A fitness app, fully developed in python, for guiding users on fitness training. 

## What is it, and why?
This is a fitness app, with the purpose of reducing reliant on external devices (e.g. controllers, body-tracking devices). This is achieved with the use of Pose Estimation, by using a pre-trained model to predict human poses via in-built webcams.
This app only need a single computer with webcam, which is simpler and cheaper than most fitness apps you have seen.

## How does it work?
### Basic User Interaction
After the authentication page, you can look through different courses and pick them. To participate a course, permission to access webcam is **required**. You will then get scored from your performance during the course.

### Advanced Interaction - Editing Courses
By accessing the /codes/Sprite/worksetMoveContent.json, you will be able to easily modify different workout courses by adding movesets or adding your custom courses. 

## Why is the app not working when you download it?
There are dependent libraries such as OpenCV and firebase admin for this app, which you may be missing. Also, I have intentionally not uploaded the privateKey.json file (a required file for this app to work) for database access (I do not want the key to be public). I have also not uploaded the pre-trained model file, which you can find [here](https://github.com/foss-for-synopsys-dwc-arc-processors/synopsys-caffe-models/raw/master/caffe_models/openpose/caffe_model/pose_iter_440000.caffemodel).

## Gallery (App Snapshot)

Authentication Page: 
![alt text][logo1]

[logo1]: https://github.com/the-lamb-mission/Fitness-App-One-Device-/blob/main/Gallery/AuthenticationPage.png "Authentication"

Main Menu Page: 
![alt text][logo2]

[logo2]: https://github.com/the-lamb-mission/Fitness-App-One-Device-/blob/main/Gallery/MainMenuPage.png "Main Menu"

Course Selection Page: 
![alt text][logo3]

[logo3]: https://github.com/the-lamb-mission/Fitness-App-One-Device-/blob/main/Gallery/CourseSelectionPage.png "Course Selection"

Within A Course: 
![alt text][logo4]

[logo4]:  https://github.com/the-lamb-mission/Fitness-App-One-Device-/blob/main/Gallery/InsideACourse.png "Course"
 
Account Info Page: 
![alt text][logo5]

[logo5]: https://github.com/the-lamb-mission/Fitness-App-One-Device-/blob/main/Gallery/AccountInfoPage.png "Account Info"

Escape Menu: 
![alt text][logo6]

[logo6]: https://github.com/the-lamb-mission/Fitness-App-One-Device-/blob/main/Gallery/EscMenu.png "Escape Menu"
