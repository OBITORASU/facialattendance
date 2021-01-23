import os
import cv2
import numpy as np
import face_recognition 
import csv
import datetime
#Function definition to encode images
def encode(images):
    #List of Encoded Images
    encoded_list = []
    missing = []
    #Function to encode each image in the image list
    for image, name in zip(images, employee_names):
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(image)[0]
            encoded_list.append(encode)
        except:
            print("[-] No face found in image {0}!".format(name))
            missing.append(name)
    #Return encoded image list
    return encoded_list, missing
#Function to make the attendance log file
def createcsv():
    with open('logs.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'Time of Entry', 'Date'])
#Function to mark each employee's entry time and not repeat it once the are marked to prevent errors
def attendance(name):
    with open('logs.csv', 'r+') as csvfile:
        data = csvfile.readlines()
        name_list = []
        for line in data:
            entry = line.split(",")
            name_list.append(entry[0])
        if name not in name_list:
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            date = now.strftime(r"%d:%m:%Y")
            csvfile.writelines("\n{0},{1},{2}".format(name,time,date))


path = os.path.dirname(__file__)+"/images/"
images = []
employee_names = []
lst = os.listdir(path)
#Looping through each employee name in list
for name in lst:
    #Removes the extension from the names and updates Employee Name List
    employee_names.append(os.path.splitext(name)[0])
    #Images loaded 
    current_image = face_recognition.load_image_file("{0}{1}".format(path, name))
    #Adds each image to the image list for the AI to work with
    images.append(current_image)

print("[+] Please wait initializing.......")

#List of encoded image of employees created
encoded_employee_list, missing = encode(images)
#Sanitize the final list
for name in missing:
    employee_names.remove(name)

print("[+] Finished Initialization!")

#Create the log file
createcsv()

#Video capture through webcam initiated
capture = cv2.VideoCapture(0)
#Loop to capture images of employees frame by frame via a webcam which is of the device id 0 here
print("\n[+] If you want to terminate the live feed, just press ctrl+c as the keyboard interrupt")
while True:
    ret, image = capture.read()
    try:
        #Resize image for faster processing
        small_image = cv2.resize(image, (0,0), None, 0.20, 0.20)
        #Find face locations in webcam feed
        current_face = face_recognition.face_locations(small_image)
        #Encode found faces
        current_encoding = face_recognition.face_encodings(small_image, current_face)
        #Loop to iterate through all the found faces and their encoding in current frame
        for encoded_face, face_location in zip(current_encoding, current_face):
            #Compare and match encoded faces from feed frame by frame to known encoded list of employee images
            match = face_recognition.compare_faces(encoded_employee_list, encoded_face)
            #Compare face distance values from live feed with values from encoded employee list
            face_distance = face_recognition.face_distance(encoded_employee_list, encoded_face)
            #Select the employee index for the employee with the highest similarity with face in current frame
            match_index = np.argmin(face_distance)
            #Condition to draw a rectangle and display the name of the found face in feed 
            if match[match_index]:
                name = employee_names[match_index].title()
                top, right, bottom, left = face_location 
                top*=5
                bottom*=5
                right*=5
                left*=5
                #Draw Rectangle on face 
                cv2.rectangle(image, (left, top), (right, bottom), (0,0,255), 1)
                cv2.rectangle(image, (left, bottom-15), (right, bottom), (0,0,255), cv2.FILLED)
                #Put name on text
                cv2.putText(image, name, (left+3, bottom-3), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
                #Mark the attendance of identified employee
                attendance(name)
        #Display live feed
        cv2.imshow("Webcam Feed", image)
        key=cv2.waitKey(1) & 0xFF
        if key == ord('q'): 
            break      
    except:
        #Error exception 
        print("\n[-] Webcam not detected or the feed has been interrupted.")
        print("[-] Terminating!")
        break

capture.release()
cv2.destroyAllWindows()
