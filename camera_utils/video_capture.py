import cv2
import os
import easyocr

CAPTURE_URL = os.getenv("CAPTURE_URL", "0")  # Default to webcam

class VideoCapture:

    def __init__(self):
        self.capture_url = int(CAPTURE_URL) if CAPTURE_URL.isdigit() else CAPTURE_URL
        self.reader = easyocr.Reader(['en'], gpu=False)

    def start_capture(self):
        try:
            cap = cv2.VideoCapture(self.capture_url)
            if not cap.isOpened():
                raise ValueError(f"Failed to open video source: {self.capture_url}")
        except Exception as e:
            print(f"Error initializing video capture: {e}")
            return

        frame_count = 0
        ocr_results = []

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame_count += 1

            if frame_count % 5 == 0:
                ocr_results = self.reader.readtext(frame)

            for (bbox, text, prob) in ocr_results:
                if prob > 0.6:
                    (tl, tr, br, bl) = bbox
                    tl = tuple(map(int, tl))
                    br = tuple(map(int, br))
                    frame = cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
                    frame = cv2.putText(frame, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow("Live OCR Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting...")
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    vid_cap = VideoCapture()
    vid_cap.start_capture()
