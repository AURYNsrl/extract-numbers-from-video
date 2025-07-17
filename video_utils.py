import cv2
import csv
import os
from datetime import datetime
from ocr_utils import extract_numbers_from_roi

def process_video(video_path, rois, frame_step=10):
    """
    Processa il video per estrarre numeri dalle ROI e salvarli in un CSV in formato tabellare.
    """
    cap = cv2.VideoCapture(video_path)
    base_name = os.path.basename(video_path)
    name_without_ext = os.path.splitext(base_name)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{timestamp}_{name_without_ext}.csv"

    # Crea la cartella 'csvoutput' se non esiste
    output_dir = "output_csv"
    os.makedirs(output_dir, exist_ok=True)

    # Costruisci il path completo del CSV
    csv_path = os.path.join(output_dir, csv_filename)

    # Prepara l'intestazione del CSV
    header = ["Frame"] + [f"number ROI={idx}" for idx in range(len(rois))]

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)

        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_index += 1

            if frame_index % frame_step != 0:
                continue

            row = [frame_index]
            for idx, (x, y, w, h) in enumerate(rois):
                roi = frame[y:y+h, x:x+w]
                numbers = extract_numbers_from_roi(roi)
                if numbers:
                    row.append(numbers[0])  # Prendi solo il primo numero trovato
                    print(f"Frame {frame_index} - ROI {idx}: {numbers[0]}")
                else:
                    row.append("")  # Nessun numero trovato

            writer.writerow(row)

    cap.release()
    print(f"Elaborazione completata. Risultati salvati in '{csv_path}'")
