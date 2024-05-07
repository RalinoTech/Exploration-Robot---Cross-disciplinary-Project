import cv2
import numpy as np

# Constantes
SEUIL_TAILLE = 200  # Seuil de taille en pixels pour le carré rouge
RED_LOWER = np.array([0, 120, 70])
RED_UPPER = np.array([10, 255, 255])

def detect_formes(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(hsv, RED_LOWER, RED_UPPER)
    mask_red = cv2.GaussianBlur(mask_red, (7, 7), 0)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours_red:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:  # Carré détecté
            area = cv2.contourArea(cnt)
            if area > SEUIL_TAILLE:
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(approx)
                if max (w, h) > SEUIL_TAILLE:  # Vérifier si la taille du carré dépasse le seuil
                    cv2.putText(img, "DANGER PROCHE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Initialisation de la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur: Impossible de lire la vidéo.")
        break
    detect_formes(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
