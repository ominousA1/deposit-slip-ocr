import cv2
import os 

CAPTURE_URL = os.getenv("CAPTURE_URL", None)


class VideoCapture: 

    def __init__(self):
        pass

    def start_capture(self): 
        cap = cv2.VideoCapture(CAPTURE_URL)

        while True: 
            ret, frame = cap.read()
            if not ret: 
                break
            cv2.imshow("")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()    


vid_cap  = VideoCapture()

vid_cap.start_capture()