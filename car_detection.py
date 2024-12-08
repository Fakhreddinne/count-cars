#import libraries of python opencv
import cv2

# capture video/ video path
cap = cv2.VideoCapture('cars.mp4')

# Get the frame width, height, and frames per second (fps) from the original video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Initialize the VideoWriter to save the video as an mp4 file
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

#use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('haarcascade_cars.xml')

#read until video is completed
while True:
    #capture frame by frame
    ret, frame = cap.read()
    
    if not ret:  # If the video ends, break the loop
        break
    
    #convert video into gray scale of each frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect cars in the video
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)

    #to draw a rectangle on each detected car 
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame (optional)
    cv2.imshow('video', frame)

    # Press 'q' on the keyboard to exit early
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

#release the video capture and writer objects
cap.release()
out.release()

#close all the frames
cv2.destroyAllWindows()
