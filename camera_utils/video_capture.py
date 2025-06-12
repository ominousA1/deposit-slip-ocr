import cv2
import os
import easyocr
import threading

CAPTURE_URL = os.getenv("CAPTURE_URL", "0")

ocr_results = []
ocr_lock = threading.Lock()

class VideoCapture:

    def __init__(self):
        self.capture_url = int(CAPTURE_URL) if CAPTURE_URL.isdigit() else CAPTURE_URL
        self.reader = easyocr.Reader(['en'], gpu=True)

    def process_ocr(self, frame):
        results = self.reader.readtext(frame)
        with ocr_lock:
            ocr_results.clear()
            ocr_results.extend(results)

    def start_capture(self):
        try:
            cap = cv2.VideoCapture(self.capture_url)
            if not cap.isOpened():
                raise ValueError(f"Failed to open video source: {self.capture_url}")
        except Exception as e:
            print(f"Error initializing video capture: {e}")
            return

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame_count += 1

            if frame_count % 20 == 0:
                threading.Thread(target=self.process_ocr, args=(frame.copy(),)).start()

            with ocr_lock:
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
