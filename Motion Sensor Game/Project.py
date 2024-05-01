from genericpath import exists
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pygame
import random

#Camera on (WEBCAM NEEDED)
camera = cv2.VideoCapture(0)
count = 1

#play music
pygame.mixer.init()
pygame.mixer.music.load('mp3.mp3')
pygame.mixer.music.play()

#RedLight/GreenLight = boolean
#Green = True, Red = False
mode = True
gameOver = False
onePicture = True
fileFound = False

#Motion detection 

#Initialize frames that will be compared
_, frame1 = camera.read()
_, frame2 = camera.read()

#creating a loop as long as the camera is up
while camera.isOpened():
  #this will be used for database creation
  #Absolute difference
  abDifference = cv2.absdiff(frame1, frame2)
  #Greyscale
  greyscale = cv2.cvtColor(abDifference, cv2.COLOR_BGR2GRAY)
  #Gaussian blur
  GB = cv2.GaussianBlur(greyscale, (5, 5), 0)

  #Get threshold of frame
  _, threshold = cv2.threshold(GB, 20, 255, cv2.THRESH_BINARY)
  #Dilate to fill holes
  dilate = cv2.dilate(threshold, None, iterations=2)
  #find contour (boundary of image) of dilated 'image'
  contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
  if mode == True:
    cv2.putText(frame1, 'Green Light', (200, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0),  2,  cv2.LINE_4) 
    #Using random gen number to serve as a delay to switch modes
    randomVal = random.randint(1,100)
    if randomVal == 50:
      mode = False

    #Search contours for movement (ONLY IN RED LIGHT MODE)
  if mode == False:
    cv2.putText(frame1, 'Red Light', (200, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255),  2,  cv2.LINE_4) 
    for contour in contours:
        #Testing was done
        if cv2.contourArea(contour) < 400: 
          continue
        #form a rectangle around movement contour
        (x,y,width,height) = cv2.boundingRect(contour)
        cv2.rectangle(frame1,(x,y),(x+width,y+height),(135,206,250),1)
        #If movement is found
        cv2.putText(frame1, '[Detected]: GAME OVER', (100, 250), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0),  2,  cv2.LINE_4) 
        gameOver=True

    if gameOver == False:
      randomVal = random.randint(1,200)
      if randomVal == 50:
       mode = True

    if gameOver == True:
       cv2.putText(frame1, '[Detected]: GAME OVER', (100, 250), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0),  2,  cv2.LINE_4) 
       cv2.putText(frame1, 'Press [SPACEBAR] to quit', (100, 400), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0),  2,  cv2.LINE_4) 
       #Code below is to avoid overriding images
       while onePicture == True:
        file = 'Database/Failure'+str(count)+'.png'
        while exists(file):
            count = (count+1)
            file = 'Database/Failure'+str(count)+'.png'
        cv2.imwrite('Database/Failure'+str(count)+'.png', frame1)
        onePicture = False


  cv2.imshow("Red Light, Green Light", frame1)
  frame1 = frame2
  _, frame2 = camera.read()

  #cv2.putText(textFrame, 'Press [SPACEBAR] to quit', (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255),  2,  cv2.LINE_4) 

  #Press SPACEBAR to close
  if cv2.waitKey(1) == ord(' '):
      camera.release()
      cv2.destroyAllWindows()
      break
              
