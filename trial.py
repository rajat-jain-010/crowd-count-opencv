import numpy as np
import cv2 as cv
import time

def detect_humans(video_path):
    cap = cv.VideoCapture(video_path)

    # Background Subtractor
    fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)

    # Optical Flow Parameters
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

    # Define Region of Interest (ROI)
    roi = [(50, 50), (200, 200)]  # Example: Rectangle defined by top-left and bottom-right corners

    # Variables for counting
    cnt_in = 0
    cnt_out = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply Background Subtraction
        fgmask = fgbg.apply(frame)

        # Compute Optical Flow
        next_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        prev_frame = next_frame.copy() if 'prev_frame' not in locals() else prev_frame
        flow = cv.calcOpticalFlowFarneback(prev_frame, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Filter Optical Flow within ROI
        flow_roi = flow[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
        mag, ang = cv.cartToPolar(flow_roi[..., 0], flow_roi[..., 1])

        # Detect Motion Direction
        # Example: Assuming motion towards the bottom of ROI as 'in' and towards the top as 'out'
        motion_direction = np.mean(ang)  # Calculate mean angle of optical flow vectors

        # Count Humans Going In and Out
        if motion_direction > 0:  # Motion towards bottom
            cnt_in += 1
        else:  # Motion towards top
            cnt_out += 1

        # Visualize Motion Direction
        cv.rectangle(frame, roi[0], roi[1], (0, 255, 0), 2)
        cv.putText(frame, f'In: {cnt_in}, Out: {cnt_out}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv.imshow('Frame', frame)

        if cv.waitKey(30) & 0xFF == ord('q'):
            break

        prev_frame = next_frame

    cap.release()
    cv.destroyAllWindows()

# Example usage
video_path = r"C:\Users\Rajat\Desktop\CrowdSense\Test Files\TestVideo\video.mp4"
detect_humans(video_path)
