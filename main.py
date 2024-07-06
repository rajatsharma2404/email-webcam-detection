import os
from threading import Thread
from emailing import send_email
import glob
import cv2


#Declaring Variables
first_frame = None
status_list = [0]
count = 1
video = cv2.VideoCapture(0)

def clean_folder():
    print("Clean folder function started")
    total_images = glob.glob("images/*.png")
    for image in total_images:
        os.remove(image)
    print("Clean folder function ended")


print("Main Process starting")
while True:
    status = 0
    check, frame = video.read()

    #convert image to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21),0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(gray_frame_gau, first_frame)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    #remove small contour with changes for better results
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

        #Capturing changes in the video
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 255, 0), 3)

        if rectangle.any():
            status=1
            #Saving image
            cv2.imwrite(f"images/{count}.png", frame)
            count = count+1
            all_images = glob.glob("images/*.png")
            index = int(count/2)

            image_path = all_images[index-1]


    #Send Email and Clean Folder
    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_path,))
        email_thread.daemon = True
        email_thread.start()

        count=1


    cv2.imshow("Video", frame)
    clean_thread = Thread(target=clean_folder)
    clean_thread.daemon = True


    key = cv2.waitKey(1)
    if key == ord("q"):
        break



video.release()
clean_thread.start()
clean_thread.join()
print("Main Process ending")



