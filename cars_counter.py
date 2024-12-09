import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

# capturing or reading video
cap = cv2.VideoCapture('cars.mp4')

# adjusting frame rate
fps = cap.set(cv2.CAP_PROP_FPS,1)

# minimum contour width
min_contour_width = 40  #40

# minimum contour height
min_contour_height = 40  #40
offset = 10  #10
line_height = 650  #550
matches = []
cars_up = 0
cars_down = 0

excel_file = "traffic_data.xlsx"

# defining a function
def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

cap.set(3, 1920)
cap.set(4, 1080)

if cap.isOpened():
    ret, frame1 = cap.read()
else:
    ret = False

ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Lists to track cars
cars_up_list = []
cars_down_list = []

while ret:
    d = cv2.absdiff(frame1, frame2)
    grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(th, np.ones((3, 3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

    # Fill any small holes
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    contours, h = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for (i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (h >= min_contour_height)

        if not contour_valid:
            continue

        # Draw a rectangle around the detected contour
        cv2.rectangle(frame1, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)

        # Draw a line representing the road
        cv2.line(frame1, (0, line_height), (1200, line_height), (0, 255, 0), 2)
        
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)
        cv2.circle(frame1, centroid, 5, (0, 255, 0), -1)
        cx, cy = get_centroid(x, y, w, h)
        
        # Determine the direction based on the centroid's position
        for (x, y) in matches:
            if (line_height + offset) > y > (line_height - offset):
                if y < line_height:  # Going up
                    cars_up += 1
                    cars_up_list.append((x, y))
                    matches.remove((x, y))
                    print(f"Cars going up: {cars_up}")
                elif y > line_height:  # Going down
                    cars_down += 1
                    cars_down_list.append((x, y))
                    matches.remove((x, y))
                    print(f"Cars going down: {cars_down}")

    # Display the total count for cars going up and down
    cv2.putText(frame1, f"Cars Going Up: {cars_up}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 170, 0), 2)
    cv2.putText(frame1, f"Cars Going Down: {cars_down}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("OUTPUT", frame1)

    if cv2.waitKey(1) == 27:  # Press 'ESC' to exit
        break

    frame1 = frame2
    ret, frame2 = cap.read()

# Save data to Excel
new_data = {
    "Location": "Location 1",
    "Date": datetime.now().strftime("%Y-%m-%d"),
    'NumberOfCarsGoingUpTheRoad': cars_up,
    'NumberOfCarsGoingDownTheRoad': cars_down
}

if os.path.exists(excel_file):
    # If the file exists, load it into a DataFrame
    df = pd.read_excel(excel_file)
    # Append the new row to the DataFrame
    df = df._append(new_data, ignore_index=True)
else:
    # If the file doesn't exist, create a new DataFrame with headers
    df = pd.DataFrame([new_data])

# Write the DataFrame back to Excel
df.to_excel(excel_file, index=False)

print(f"Data appended successfully to {excel_file}")

cv2.destroyAllWindows()
cap.release()
