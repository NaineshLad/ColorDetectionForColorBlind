# Real Time Color Detector for Color Blind User (Python Code):

from ast import IsNot
import time
import cv2
import pandas as pd
import argparse
import numpy as np
from playsound import playsound
print("WELCOME TO OUR PROGRAM")
time.sleep(3)  #sleep for 3 sec

a=int(input('\n\n***What would you like to do!***\n\n1)PLEASE TYPE 1 IF YOU WANT TO DETECT COLOR FROM IMAGE\n2)PLEASE TYPE 2 IF YOU WANT TO USE WEBCAM TO DETECT COLORS: '))

if a==1:
    #Creating argument parser to take image path from command line
    #ap = argparse.ArgumentParser()
    #ap.add_argument('-i', '--image', required=True, help="Image Path")
    #args = vars(ap.parse_args())
    #img_path = args['image']

    #Reading the image with opencv
    path = r'Colorsample.jpg'
    img = cv2.imread(path)

    #declaring global variables (are used later on)
    clicked = False
    r = g = b = xpos = ypos = 0

    #Reading csv file with pandas and giving names to each column
    index=["color","color_name","hex","R","G","B"]
    csv = pd.read_csv('colors.csv', names=index, header=None)

    #function to calculate minimum distance from all colors and get the most matching color
    def getColorName(R,G,B):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                cname = csv.loc[i,"color_name"]
        return cname

    #function to get x,y coordinates of mouse double click
    def draw_function(event, x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            global b,g,r,xpos,ypos, clicked
            clicked = True
            xpos = x
            ypos = y
            b,g,r = img[y,x]
            b = int(b)
            g = int(g)
            r = int(r)
        
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_function)

    while(1):

        cv2.imshow("image",img)
        if (clicked):
    
            #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
            cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

            #Creating text string to display( Color name and RGB values )
            text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
            
            #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

            #For very light colours we will display text in black colour
            if(r+g+b>=600):
                cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
                
            clicked=False

        #Break the loop when user hits 'esc' key    
        if cv2.waitKey(20) & 0xFF ==27:
            break
        
    cv2.destroyAllWindows()
elif a==2:
    print('Webcam is activating')
    time.sleep(1)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(height / 2)

        #Pick pixel value
        pixel_center = hsv_frame[cy, cx] 
        hue_value = pixel_center[0]
        hue_value2 = pixel_center[1]
        hue_value3 = pixel_center[2]

        color="Undefined"
        if hue_value < 7:
            color = "RED"    
        elif hue_value < 30:
            color = "ORANGE"
        elif hue_value < 66:
            color = "YELLOW"
        elif hue_value < 170:
            color = "GREEN"
        elif hue_value < 256:
            color = "BLUE"
        elif hue_value < 293:
            color = "VIOLET"
        elif hue_value < 335:
            color = "PINK"
        else:
            color = "RED"


        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        cv2.putText(frame, color, (10,70), 0, 1.5, (b, g, r), 2)
        cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        
        if key == 27:
            break

        if color == "RED":
            playsound('RedFinal.mp3')
        if color == "ORANGE":
            playsound('OrangeFinal.mp3')
        if color == "YELLOW":
            playsound('YellowFinal.mp3')
        if color == "GREEN":
            playsound('GreenFinal.mp3')
        if color == "BLUE":
            playsound('BlueFinal.mp3')
        if color == "VIOLET":
            playsound('VioletFinal.mp3')
        if color == "PINK":
            playsound('PinkFinal.mp3')
        
        

    cap.release()
    cv2.destroyAllWindows()
     
elif a>2:
    print('Range is exceeding')   
else:
    print("Please enter a number")
