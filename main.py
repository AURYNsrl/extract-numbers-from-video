import tkinter as tk
from tkinter import filedialog
from roi_selector import select_rois
from video_utils import process_video
import cv2

def main():
    root = tk.Tk()
    root.withdraw()
    video_path = filedialog.askopenfilename(
        title="Seleziona il video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if not video_path:
        print("Nessun file selezionato.")
        return

    cap = cv2.VideoCapture(video_path)
    ret, first_frame = cap.read()
    cap.release()
    if not ret:
        print("Impossibile leggere il video.")
        return

    print("Seleziona le aree di interesse (ROI).")
    rois = select_rois(first_frame)
    if not rois:
        print("Nessuna ROI selezionata. Uscita.")
        return

    process_video(video_path, rois)

if __name__ == "__main__":
    main()
