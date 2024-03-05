import cv2
import numpy as np

def detect_black_box(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Increase the threshold value to include darker shades, not just black
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)  # Adjusted threshold to 50
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        if len(approx) == 4 and cv2.isContourConvex(approx):
            area = cv2.contourArea(cnt)
            if area > 1000:  # Adjust this threshold based on your requirement
                cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 3)

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Can't receive frame. Exiting...")
            break

        detect_black_box(frame)

        cv2.imshow('Live Camera Feed with Black Box Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
