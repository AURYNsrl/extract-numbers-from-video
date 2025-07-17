# roi_selector.py
import cv2

def select_rois(resized_image):
    """
    Seleziona manualmente più ROI su un'immagine, adattando la visualizzazione alla dimensione del monitor.
    Restituisce le ROI con coordinate rispetto all'immagine originale.
    """
    # screen_res = 1280, 720  # dimensioni massime target; puoi prendere dinamicamente se vuoi
    # scale_width = screen_res[0] / image.shape[1]
    # scale_height = screen_res[1] / image.shape[0]
    # scale = min(scale_width, scale_height, 1)  # non ingrandiamo se è più piccolo del monitor

    # window_width = int(image.shape[1] * scale)
    # window_height = int(image.shape[0] * scale)
    # resized_image = cv2.resize(image, (window_width, window_height))

    rois = []
    drawing = False
    start_point = None
    current_rect = None

    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, start_point, current_rect, rois
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                current_rect = (start_point[0], start_point[1], x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x0, y0 = start_point
            x1, y1 = x, y
            x_start = min(x0, x1)
            y_start = min(y0, y1)
            width = abs(x1 - x0)
            height = abs(y1 - y0)
            if width > 0 and height > 0:
                rois.append((x_start, y_start, width, height))

    cv2.namedWindow("Selezione ROI")
    cv2.setMouseCallback("Selezione ROI", mouse_callback)

    while True:
        temp = resized_image.copy()
        for (x, y, w, h) in rois:
            cv2.rectangle(temp, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if drawing and current_rect:
            x0, y0, x1, y1 = current_rect
            cv2.rectangle(temp, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2.putText(temp, f"ROI count: {len(rois)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(temp, "Premi 's' per avviare, 'r' per resettare, 'q' per uscire",
                    (10, temp.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.imshow("Selezione ROI", temp)
        key = cv2.waitKey(20) & 0xFF
        if key == ord('s'):
            if len(rois) > 0:
                break
        elif key == ord('r'):
            rois = []
        elif key == ord('q'):
            rois = []
            break
    cv2.destroyWindow("Selezione ROI")
    return rois
