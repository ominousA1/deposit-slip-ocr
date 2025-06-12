import cv2
import os
from colorama import Fore
import pytesseract 
from pytesseract import Output

CAPTURE_URL = os.getenv("CAPTURE_URL", "0") 

class VideoCapture:

    def __init__(self):
        self.capture_url = int(CAPTURE_URL) if CAPTURE_URL.isdigit() else CAPTURE_URL

    def start_capture(self):
        try:
            cap = cap = cv2.VideoCapture(self.capture_url)
            if not cap.isOpened():
                raise ValueError(f"Failed to open video source: {self.capture_url}")
        except Exception as e:
            print(f"Error initializing video capture: {e}")
            return

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to grab frame")
                break

            

            d = pytesseract.image_to_data(frame, output_type=Output.DICT)
            n_boxes = len(d['text'])
        
            for i in range(n_boxes):
                if int(d['conf'][i]) > 60:
                    (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    # don't show empty text
                    if text and text.strip() != "":
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

            cv2.imshow("Video Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(Fore.GREEN + "Gracefully shutting down")
                print(Fore.BLACK)
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    vid_cap = VideoCapture()
    vid_cap.start_capture()
