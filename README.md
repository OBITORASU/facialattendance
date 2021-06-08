# Facial Attendance
This is a model which uses facial data to recognize, authenticate and validate attendance of people. It uses `face_recognition` a pretained neural network capable of highly accurate face detection based on features extracted from existing pictures of users.


## Dependencies 
All project dependencies are listed in `requirements.txt` file.

To install just use:
```
pip3 install -r requirements.txt
```

## Instructions
First use the command:
```
git clone https://github.com/OBITORASU/facialattendance.git
```
After git cloning the project, to use it first you need to create a folder named images inside the clone folder. The images folder will 
contain images of your employees with their names as the file name for identification. When the model is run on the webcam, any employee 
from the images folder will be recognized on the web cam feed and their attendence entry will be stored in an auto generated csv file. The 
csv file is regenerated every time the program is run so it is recommended that you take backup of each csv when running this consecutively.


