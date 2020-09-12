# facialattendance
This is a prototype of a model which uses facial data to recognize, authenticate and validate attendance data of people.

Dependencies include:
1) OpenCV
2) dlib
3) cmake
4) face_recognition
5) Visual Studio C++
6) Python 3

This code is entirely written in python.

Things to do:

Make a folder where you can store images of faces along with the python file before running it. 
Note: It won't identify any faces if you don't give it images to identify faces with.

Instructions:

Upon downloading the webcam.py file, make sure all the dependencies are met. Before running please add the path to the folder which contains all the images of the faces you want to recognize in a video feed. Once that has been taken care of, the code should run normally and should easily detect faces.

The attendance feature will mark the current date and time when each face is encountered for the first time in a feed and store it in a csv file named 'logs'. This file will act as a temporary database which will be storing all the attendance data. 

Note: The program creates a csv file named 'logs' everytime its run so it is recommend that you save your previous logs in some personal database before re running the code as it will start over from scratch upon doing so.
