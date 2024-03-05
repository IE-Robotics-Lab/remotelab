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

    # Find contours for black objects
    contours, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:  # Adjust this value according to your requirement
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Find contours for green objects
    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10:  # Adjust this value according to your requirement
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (int(x + w / 2), int(y + h / 2)), 3, (0, 255, 0), -1)

    # Display the resulting frame
    cv2.imshow('Object Tracking', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()