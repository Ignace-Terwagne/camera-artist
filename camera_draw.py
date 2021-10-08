from tkinter import *
from turtle import *
from PIL import ImageTk,Image, ImageGrab
from datetime import datetime
import tweepy
import json
import numpy as np
import cv2
import os



def take_picture():
    counter = 100
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    img = np.zeros((round(cap_width),round(cap_height),3),np.uint8)
    while True:
        return_value, frame = cap.read()
        counter-=1
        if counter <100:
            if counter<80:
                if counter<60:
                    if counter<40:
                        if counter<20:
                            if counter == 5:
                                cv2.imshow(None,frame)
                                img_height, img_width = frame.shape[:2]
                                if img_width > 400 or img_height > 200:
                                    resized_frame = cv2.resize(frame,(img_width//2,img_height//2))
                                    
                                else:
                                    resized_frame = frame
                                cv2.waitKey(2)
                                saved = cv2.imwrite(f"opencv.png", resized_frame)
                                cap.release()
                                cv2.destroyAllWindows()
                                if saved:     
                                    print('[PROGRAM] succesfully saved')
                                    return resized_frame
                                else:
                                    print('[PROGRAM] saving was unsuccesful')
                                    exit()
                            else:
                                show_text(1,frame)
                        else:
                            show_text(2,frame)
                    else:
                        show_text(3,frame)
                else:
                    show_text(4,frame)
            else:
                show_text(5,frame)
        cv2.imshow('photo',frame)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

def show_text(number,img1):
    number = str(number)
    textsize = cv2.getTextSize(number, cv2.FONT_HERSHEY_DUPLEX,10, 10)[0]
    textX = (img1.shape[1] - textsize[0])/ 2
    textY = (img1.shape[0] + textsize[1])/ 2
    cv2.putText(img1,number,(round(textX),round(textY)),cv2.FONT_HERSHEY_DUPLEX,10,(255,255,255),10)

def edge_detector(image):
    imgCanny = cv2.Canny(image,255,255/3)
    with open("BinImg.txt", 'w') as f:
        for i in range (imgCanny.shape[0]):
            for j in range (imgCanny.shape[1]):
                if imgCanny[i][j] == 255:
                    f.write('1')
                elif imgCanny[i][j] == 0:
                    f.write('0')
            f.write('\n')
    f.close()
    img_inv = cv2.bitwise_not(imgCanny)
    cv2.imwrite("tempimg.png",img_inv)
    print("[PROGRAM] succesfully converted")

def draw_it():
    global canvas
    screen = TurtleScreen(canvas)
    t = RawTurtle(screen)
    screen.tracer(1,0)
    t.clear()
    t.penup()
    filename = 'BinImg.txt'
    t.speed(1)
    with open(filename,'r') as f:
        lines = f.readlines()
        x = 0 - len(str(lines[0]))/2
        y = 0 + (len(lines)/2)
        t.goto(x-1,y+1)
        t.pendown()
        for x in range(2):
            t.forward(len(str(lines[0]))+2)
            t.right(90)
            t.forward(len(lines)+2)
            t.right(90)
        t.penup()
        t.goto(x,y)
        t.speed(0)
        for line in lines:
            screen.tracer(1,0)
            freq=0
            for char in line:
                if char == '1':
                    freq +=1
            freq_1 = freq/len(line)
            print(f"[FREQCOUNT] 1: {freq_1} %")
            if freq_1 > 0.07:
                screen.tracer(0,0)
            for character in line:
                if character == '1':
                    t.penup()
                    t.goto(x,y)
                    t.pendown()
                    t.forward(1)
                x+=1
            t.penup()
            y-=1
            x = 0 - len(str(lines[0]))/2
            t.goto(x,y)
            t.pendown()
    f.close()
    t.penup()
    t.goto(200,-140)
    t.pendown()

def camera_command():
    global act_image
    act_image = take_picture()
    edge_detector(act_image)
    draw_it()

def save_command():
    global photo_counter
    photo_counter +=1
    img = cv2.imread('tempimg.png')
    name = f'opendeurdag_{photo_counter}.png'
    print(name)
    cv2.imwrite(name, img)

def twitter_command():
    global twitter
    twitter.update_status_with_media('test','tempimg.png')

#
#
#
with open('twitter_auth.json') as file:
    secrets = json.load(file)
auth =  tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'],secrets['access_token_secret'])
twitter = tweepy.API(auth)

act_image = None
photo_counter = 0
root = Tk()
root.title('camera artist')
root.iconbitmap('icons\\logo.ico')

camera_img = ImageTk.PhotoImage(Image.open('icons\\camera_button.png'))
save_img = ImageTk.PhotoImage(Image.open("icons\\save_button.png"))
twitter_img = ImageTk.PhotoImage(Image.open("icons\\twitter_button.png"))
cam_btn = Button(root,width=60,height=60,image=camera_img,borderwidth=1,command=lambda : camera_command())
save_btn = Button(root,width=60,height=60,image=save_img,borderwidth=1,command=lambda : save_command())
twitter_btn = Button(root,width=60,height=60,image=twitter_img,borderwidth=1,command=lambda : twitter_command())

title_bar = Label(root,text="Camera artist",foreground="black",font=('Cooper Black',20,'bold'),justify="center" )

canvas = Canvas(root,width=600,height=500,background="white",highlightbackground="blue",highlightthickness=1)
canvas_x0 = canvas.winfo_rootx()
canvas_y0 = canvas.winfo_rooty()
canvas_x1 = canvas_x0 + canvas.winfo_width()
canvas_y1 = canvas_y0 + canvas.winfo_height()
canvas.grid(row=1,column=1,rowspan=3, padx=30, pady=10, sticky=E)

title_bar.grid(row=0,column=0,columnspan=2,pady=10,sticky=N)
cam_btn.grid(row=1,column=0,padx=20,sticky=W)
save_btn.grid(row=2,column=0,padx=20, sticky=W)
twitter_btn.grid(row=3,column=0,padx=20, sticky=W)
root.mainloop()