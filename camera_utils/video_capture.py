import cv2
import os

CAPTURE_URL = os.getenv("CAPTURE_URL", "0") 

class VideoCapture:

    def __init__(self):
        self.capture_url = int(CAPTURE_URL) if CAPTURE_URL.isdigit() else CAPTURE_URL

    def start_capture(self):
        try:
            cap = cap = cv2.VideoCapture(f"ffmpeg -i {self.capture_url} -f rawvideo -pix_fmt bgr24 -", cv2.CAP_FFMPEG)
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
            cv2.imshow("Video Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    vid_cap = VideoCapture()
    vid_cap.start_capture()
