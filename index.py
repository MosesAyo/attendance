from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
import attendance
import cv2
import os
import numpy as np
from PIL import Image
import csv
from datetime import datetime
from PyQt5.uic import loadUiType

welcomeUi, onboarding = loadUiType('Welcome.ui')
ui,_ = loadUiType('UserInterface.ui')
attendanceUi, base = loadUiType('attendance.ui')
con = sqlite3.connect("attendance.db")
cur = con.cursor()




class MainApp(QMainWindow, welcomeUi):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Welcome")
        self.pushButton.clicked.connect(self.Start_Button)
        self.pushButton_2.clicked.connect(self.Exit_Button)
        self.show()

    def Start_Button(self):
        self.display = Home()
        self.display.show()
        self.close()

    def Exit_Button(self):
        self.close()
class Home(_, ui,):
    def __init__(self):
        _.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.setWindowTitle("Nigerian Defence Academy Attendance System")
        self.show()
        self.getCourses()
        self.handle_UI_Changes()
       


    def Handle_Buttons(self):
        self.StartAClass.clicked.connect(self.Start_A_Class_Tab)
        self.CreateAClass.clicked.connect(self.Create_A_Class_Tab)
        # self.MyClasses.clicked.connect(self.My_Classes_Tab)
        self.EnrollAStudent.clicked.connect(self.Enroll_A_Student_Class)
        self.AddStudent.clicked.connect(self.Add_Student)
        self.CreateClass.clicked.connect(self.Add_class)
        self.EnrollFaceId.clicked.connect(self.Enroll_face_recognition)
        self.pushButton_7.clicked.connect(self.Attendance_Window)
        self.listWidget.doubleClicked.connect(self.SelectedCourse)

    # Opening Tabs

    def handle_UI_Changes(self):
        self.tabWidget_2.tabBar().setVisible(False)

    def getCourses(self):
        # total_courses = cur.execute("SELECT * FROM courses ORDER BY id DESC LIMIT 1").fetchone()
        # print("Total Courses"+str(total_courses[0]))
        self.listWidget.clear()
        # if (self.listWidget.count()>=)
        query ='SELECT course_code, course_title FROM courses'
        courses = cur.execute(query).fetchall()

        for course in courses :
            self.listWidget.addItem(str(course[0])+"   -------------------------------   "+str(course[1]))


    def SelectedCourse(self):
        global courseId
        listItemSelected = self.listWidget.currentItem().text()
        courseId = self.listWidget.currentRow()+1
        courseSelected = listItemSelected[:7].strip()
        courseSelectedTitle = listItemSelected[43:].strip()
        print("course id =="+str(courseId+1))
        print(listItemSelected )
        print(courseSelected )
        print(courseSelectedTitle )
        self.display = TakeAttendance()
        self.display.show()
        self.close()

    def Start_A_Class_Tab(self):
        self.tabWidget_2.setCurrentIndex(0)
        self.getCourses()
        # print(self.listWidget.count ())     
        pass

    def Create_A_Class_Tab(self):
        self.tabWidget_2.setCurrentIndex(1)
        pass

    # def My_Classes_Tab(self):
    #     self.tabWidget_2.setCurrentIndex(2)
    #     pass

    def Enroll_A_Student_Class(self):
        self.tabWidget_2.setCurrentIndex(3)
        pass
    
    def Attendance_Window(self):
        self.newAttendance = TakeAttendance()
        self.close()

    

    def Add_Student(self):
        studentId=self.StudentIdTextField.toPlainText()
        fullName=self.StudentNameTextField.toPlainText()

        if (studentId and fullName !=""):
            try:
                query ="INSERT INTO students (student_id, full_name) VALUES(?,?)"
                cur.execute(query,(studentId,fullName))
                con.commit()
                QMessageBox.information(self,"Success","Student has been added")
                self.StudentIdTextField.setText("")
                self.StudentNameTextField.setText("")
            except:
                QMessageBox.information(self,"Warning","Student has not been added")
        else:
            QMessageBox.information(self,"Warning","Fields cannot be empty")

    def Add_class(self):
        courseCode = self.CourseCodeTextField.toPlainText()
        courseTitle = self.CourseTitleTextField.toPlainText()

        if (courseCode and courseTitle !=""):
            try:
                query = "INSERT INTO courses (course_code, course_title) VALUES(?,?)"
                cur.execute(query,(courseCode,courseTitle))
                con.commit()
                QMessageBox.information(self,"Success","Class has been created")
                self.CourseCodeTextField.setText("")
                self.CourseTitleTextField.setText("")
            except:
                QMessageBox.information(self,"Warning","Course has not been created")
        else:
            QMessageBox.information(self,"Warning","Fields cannot be empty")
    
    def Start_Class_Button (self):
        self.startClass=attendance.StartClass()

    def Enroll_face_recognition(self):
        cur.execute("SELECT * FROM students ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()
        print(result)
        print(result[0])
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # For each person, enter one numeric face id
        # face_id = input('\n enter user id end press <return> ==>  ')
        face_id = result[0]

        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0

        while(True):

            ret, img = cam.read()
            # img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            cv2.imshow('camera',img)
            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                
             
                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])


            k = cv2.waitKey(20) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                # Do a bit of cleanup
                print("\n [INFO] Exiting Window and cleanup stuff")
                cam.release()
                cv2.destroyAllWindows()
                ####################################################################################################
                # Path for face image database
                path = 'dataset'

                recognizer = cv2.face.LBPHFaceRecognizer_create()
                detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

                # function to get the images and label data
                def getImagesAndLabels(path):

                    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
                    faceSamples=[]
                    ids = []

                    for imagePath in imagePaths:

                        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                        img_numpy = np.array(PIL_img,'uint8')

                        id = int(os.path.split(imagePath)[-1].split(".")[1])
                        faces = detector.detectMultiScale(img_numpy)

                        for (x,y,w,h) in faces:
                            faceSamples.append(img_numpy[y:y+h,x:x+w])
                            ids.append(id)

                    return faceSamples,ids

                print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
                faces,ids = getImagesAndLabels(path)
                recognizer.train(faces, np.array(ids))

                # Save the model into trainer/trainer.yml
                recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

                # Print the numer of faces trained and end program
                print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
                break

class TakeAttendance(base, attendanceUi):
    def __init__(self):
        super(base,self).__init__()
        self.setupUi(self)
        self.Handle_Buttons()
        self.setWindowTitle("Attendance")
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.UI()
        # self.setGeometry(450,150,350,600)
        self.show()


    def UI(self):
        self.CourseDetails()

    def CourseDetails(self):
        global courseId
        global closeCam
        global studentsList

        studentsList = []
        closeCam = 0
        query=("SELECT * FROM courses WHERE id=?")
        getCourse = cur.execute(query, (courseId,)).fetchone()
        print("Course ID   "+ str(courseId))
        print(getCourse)
        self.attendanceCourseText.setText(getCourse[1])
        self.attendanceCourseTitle.setText(getCourse[2])
        global f 
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S %p")
        newtime = getCourse[1]+" "+now.strftime("%I%p %a-%dth-%b-%y")
        print(newtime)
        # date = now.year+"-"
        print("Current Time =", current_time)
        f= csv.writer(open("classes/"+newtime+".csv", "a"), lineterminator ="\n")
        f.writerow([
            "Number",
            "NDA Number",
            "Fullname"
            ]) 
        print(getCourse)

    def Handle_Buttons(self):
        self.EndClassButton.clicked.connect(self.End_Class_Button)
        self.SignInButton.clicked.connect(self.Sign_In_Button)

    def Sign_In_Button(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        #iniciate id counter
        id = 0

        # names related to ids: example ==> Marcelo: id=1,  etc
        names = ['None', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100] 

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:

            ret, img =cam.read()
            img = cv2.flip(img, 1) # Flip vertically
            cv2.imshow('camera',img) 
          
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                accuracy = confidence
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    validateThreshold = round(100 - accuracy)
                    
                    if(validateThreshold>=40):
                        global studentsList
                        query=("SELECT * FROM students WHERE id=?")
                        student = cur.execute(query, (id,)).fetchone()
                        if (not student[1] in studentsList):
                            print("Student not in the class")
                            studentsList.append(student[1])
                            totalAttendees = self.attendanceListWidget.count()+1
                            self.attendanceListWidget.addItem(str(totalAttendees)+"  "+str(student[1])+"  "+str(student[2]))
                            self.totalStudents.setText("Total: "+str(totalAttendees))
                            print(studentsList)
                            global closeCam
                            closeCam=27
                            # cv2.waitKey(10) = 20
                            global f
                            f.writerow([
                            totalAttendees,
                            student[1],
                            student[2]
                            ]) 
                        
                        print(student)
                        # print(str(id)+"    "+str(confidence))
                else:
                    id = "Unknown Cadet"
                    confidence = "  {0}%".format(round(100 - confidence))
                
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('camera',img) 

            # global closeCam
            if closeCam == 20:
                closeCam=0
                break
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 20:
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()

################################################################################################################################        

    def End_Class_Button(self):
        self.main_window = MainApp()
        self.close()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    # attendance.StartClass().show
    app.exec_()

if __name__ == '__main__':
    main()
