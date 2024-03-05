import cv2
import numpy as np

# Function to handle mouse events
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_MOUSEMOVE:
        # Get RGB values of the pixel
        b, g, r = frame[y, x]
        # Display RGB values and coordinates
        text = f"RGB: ({r}, {g}, {b})  Coordinates: ({x}, {y})"
        print(text)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Define the lower and upper bounds for the black box and green dot
lower_black = np.array([0, 0, 0])
upper_black = np.array([120, 120, 120])
lower_green = np.array([40, 100, 40])
upper_green = np.array([100, 255, 180])

# Set up mouse callback function
cv2.namedWindow('Object Tracking')
cv2.setMouseCallback('Object Tracking', mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the image to get only black objects
    mask_black = cv2.inRange(frame, lower_black, upper_black)

    # Threshold the image to get only green objects
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours for green objects
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find contours for black objects
    contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw green squares and check if they are inside black rectangles
    for contour_green in contours_green:
        area_green = cv2.contourArea(contour_green)
        if area_green > 10:  # Adjust this value according to your requirement
            x_green, y_green, w_green, h_green = cv2.boundingRect(contour_green)
            cv2.rectangle(frame, (x_green, y_green), (x_green + w_green, y_green + h_green), (0, 255, 0), 2)
            for contour_black in contours_black:
                area_black = cv2.contourArea(contour_black)
                if area_black > 5000:  # Adjust this value according to your requirement
                    x_black, y_black, w_black, h_black = cv2.boundingRect(contour_black)
                    if x_black < x_green < x_black + w_black and y_black < y_green < y_black + h_black:
                        cv2.rectangle(frame, (x_black, y_black), (x_black + w_black, y_black + h_black), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Object Tracking', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
